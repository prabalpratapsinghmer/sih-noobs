"""Automated Retraining Pipeline for Cybercrime Prediction Models."""

import os
import sys
import json
import time
import shutil
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, Tuple
from dataclasses import dataclass, asdict
import subprocess

import yaml
import torch
import numpy as np
import joblib
from loguru import logger

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from models.utils.feature_engineering import FeatureEngineer
from models.spatio_temporal.train import train as train_stm
from models.mule_detection.train import train as train_gnn
from models.utils.mlflow_utils import MLflowTracker


@dataclass
class RetrainingMetrics:
    """Metrics for model comparison."""
    stm_val_accuracy: float
    stm_val_top3: float
    stm_val_top5: float
    stm_val_loss: float
    gnn_val_f1: float
    gnn_val_precision: float
    gnn_val_recall: float
    gnn_val_accuracy: float
    gnn_val_loss: float
    timestamp: str


@dataclass
class RetrainingResult:
    """Result of a retraining run."""
    success: bool
    metrics: Optional[RetrainingMetrics]
    previous_metrics: Optional[RetrainingMetrics]
    meets_criteria: bool
    message: str
    model_paths: Dict[str, str]


class RetrainingPipeline:
    """
    Automated retraining pipeline for cybercrime prediction models.

    Pipeline stages:
    1. Data refresh - fetch new data from banking API
    2. Feature recomputation - re-run feature engineering
    3. Model retraining - retrain both STM and GNN models
    4. Model validation - evaluate on test set
    5. Deployment criteria check - compare with production models
    6. Model promotion - if criteria met, promote to production
    7. Notification - send alerts
    """

    def __init__(self, config_path: str = "config/config.yaml"):
        """Initialize retraining pipeline."""
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        self.retraining_config = self.config['retraining']
        self.data_config = self.config['data']
        self.training_config = self.config['training']
        self.mlflow_config = self.config['mlflow']

        # Paths
        self.processed_dir = Path(self.data_config['processed_dir'])
        self.raw_dir = Path(self.data_config['raw_dir'])
        self.validation_dir = Path(self.data_config['validation_dir'])
        self.backup_dir = Path("models/backups")
        self.backup_dir.mkdir(parents=True, exist_ok=True)

        # MLflow tracker
        self.mlflow_tracker = MLflowTracker(self.mlflow_config)

        # Criteria
        self.criteria = self.retraining_config['criteria']

        logger.info("Retraining pipeline initialized")

    def run_data_refresh(self) -> bool:
        """Fetch new data from banking API and update raw data."""
        logger.info("Stage 1: Data refresh")

        try:
            # In production, this would call the banking API
            # For now, we'll regenerate synthetic data with updated timestamps
            logger.info("Generating updated synthetic data...")

            # Run data synthesis script
            result = subprocess.run([
                sys.executable, "scripts/generate_data.py",
                "--config", "config/config.yaml"
            ], capture_output=True, text=True, cwd=project_root)

            if result.returncode != 0:
                logger.error(f"Data generation failed: {result.stderr}")
                return False

            logger.info("✓ Data refresh complete")
            return True

        except Exception as e:
            logger.error(f"Data refresh failed: {e}")
            return False

    def run_feature_engineering(self) -> bool:
        """Re-run feature engineering on updated data."""
        logger.info("Stage 2: Feature engineering")

        try:
            # Load feature engineer
            feature_engineer = FeatureEngineer(self.config)

            # Process training data
            train_complaints = self.raw_dir / 'complaints.csv'
            train_transactions = self.raw_dir / 'transactions.csv'
            train_atms = self.raw_dir / 'atms.csv'

            if not all(p.exists() for p in [train_complaints, train_transactions, train_atms]):
                logger.error("Raw data files not found")
                return False

            # Process and save
            feature_engineer.process_and_save(
                complaints_path=train_complaints,
                transactions_path=train_transactions,
                atms_path=train_atms,
                output_dir=self.processed_dir
            )

            # Also process validation data
            val_complaints = self.validation_dir / 'complaints.csv'
            val_transactions = self.validation_dir / 'transactions.csv'
            val_atms = self.validation_dir / 'atms.csv'

            if all(p.exists() for p in [val_complaints, val_transactions, val_atms]):
                feature_engineer.process_and_save(
                    complaints_path=val_complaints,
                    transactions_path=val_transactions,
                    atms_path=val_atms,
                    output_dir=self.validation_dir,
                    is_validation=True
                )

            logger.info("✓ Feature engineering complete")
            return True

        except Exception as e:
            logger.error(f"Feature engineering failed: {e}")
            return False

    def backup_current_models(self) -> Dict[str, str]:
        """Backup current production models."""
        logger.info("Backing up current models...")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_paths = {}

        # Backup STM model
        stm_checkpoint = Path(self.training_config['spatio_temporal']['checkpoint']['save_dir']) / 'best_model.pth'
        if stm_checkpoint.exists():
            backup_path = self.backup_dir / f"stm_best_model_{timestamp}.pth"
            shutil.copy2(stm_checkpoint, backup_path)
            backup_paths['stm'] = str(backup_path)
            logger.info(f"Backed up STM model to {backup_path}")

        # Backup GNN model
        gnn_checkpoint = Path(self.training_config['mule_detection']['checkpoint']['save_dir']) / 'best_model.pth'
        if gnn_checkpoint.exists():
            backup_path = self.backup_dir / f"gnn_best_model_{timestamp}.pth"
            shutil.copy2(gnn_checkpoint, backup_path)
            backup_paths['gnn'] = str(backup_path)
            logger.info(f"Backed up GNN model to {backup_path}")

        # Backup scalers and encoders
        for artifact in ['spatial_scaler.joblib', 'temporal_scaler.joblib', 'label_encoders.joblib']:
            src = self.processed_dir / artifact
            if src.exists():
                backup_path = self.backup_dir / f"{artifact}_{timestamp}"
                shutil.copy2(src, backup_path)

        return backup_paths

    def get_current_metrics(self) -> Optional[RetrainingMetrics]:
        """Get metrics from current production models."""
        try:
            # Load from MLflow or checkpoint
            stm_checkpoint = Path(self.training_config['spatio_temporal']['checkpoint']['save_dir']) / 'best_model.pth'
            gnn_checkpoint = Path(self.training_config['mule_detection']['checkpoint']['save_dir']) / 'best_model.pth'

            if not (stm_checkpoint.exists() and gnn_checkpoint.exists()):
                return None

            stm_ckpt = torch.load(stm_checkpoint, map_location='cpu', weights_only=False)
            gnn_ckpt = torch.load(gnn_checkpoint, map_location='cpu', weights_only=False)

            return RetrainingMetrics(
                stm_val_accuracy=stm_ckpt.get('val_acc', 0),
                stm_val_top3=stm_ckpt.get('val_top3', 0),
                stm_val_top5=stm_ckpt.get('val_top5', 0),
                stm_val_loss=stm_ckpt.get('val_loss', float('inf')),
                gnn_val_f1=gnn_ckpt.get('val_f1', 0),
                gnn_val_precision=gnn_ckpt.get('val_precision', 0),
                gnn_val_recall=gnn_ckpt.get('val_recall', 0),
                gnn_val_accuracy=gnn_ckpt.get('val_acc', 0),
                gnn_val_loss=gnn_ckpt.get('val_loss', float('inf')),
                timestamp=datetime.now().isoformat()
            )
        except Exception as e:
            logger.warning(f"Could not load current metrics: {e}")
            return None

    def run_model_training(self) -> Tuple[bool, Dict[str, str]]:
        """Retrain both models."""
        logger.info("Stage 3: Model retraining")

        model_paths = {}

        try:
            # Train STM
            logger.info("Training Spatio-Temporal Transformer...")
            # Import and run training
            # We'll call the training function directly
            from models.spatio_temporal.train import train as stm_train
            stm_train(self.config)

            stm_checkpoint = Path(self.training_config['spatio_temporal']['checkpoint']['save_dir']) / 'best_model.pth'
            if stm_checkpoint.exists():
                model_paths['stm'] = str(stm_checkpoint)

            # Train GNN
            logger.info("Training Mule Detection GNN...")
            from models.mule_detection.train import train as gnn_train
            gnn_train(self.config)

            gnn_checkpoint = Path(self.training_config['mule_detection']['checkpoint']['save_dir']) / 'best_model.pth'
            if gnn_checkpoint.exists():
                model_paths['gnn'] = str(gnn_checkpoint)

            logger.info("✓ Model retraining complete")
            return True, model_paths

        except Exception as e:
            logger.error(f"Model retraining failed: {e}")
            return False, {}

    def evaluate_models(self) -> Optional[RetrainingMetrics]:
        """Evaluate newly trained models on test set."""
        logger.info("Stage 4: Model evaluation")

        try:
            # Load test data
            X_test = np.load(self.processed_dir / 'st_X_test.npy')
            y_test = np.load(self.processed_dir / 'st_y_test.npy')

            spatial_dim = X_test.shape[1] // 2
            spatial_test = X_test[:, :spatial_dim]
            temporal_test = X_test[:, spatial_dim:]

            device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

            # Evaluate STM
            from models.spatio_temporal.model import SpatioTemporalTransformer
            stm_checkpoint = Path(self.training_config['spatio_temporal']['checkpoint']['save_dir']) / 'best_model.pth'
            stm_model = SpatioTemporalTransformer(self.config['models']['spatio_temporal'])
            stm_ckpt = torch.load(stm_checkpoint, map_location=device, weights_only=False)
            stm_model.load_state_dict(stm_ckpt['model_state_dict'])
            stm_model = stm_model.to(device)
            stm_model.eval()

            from torch.utils.data import DataLoader, TensorDataset
            test_dataset = TensorDataset(
                torch.FloatTensor(spatial_test),
                torch.FloatTensor(temporal_test),
                torch.LongTensor(y_test)
            )
            test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)

            criterion = torch.nn.CrossEntropyLoss()
            stm_model.eval()
            test_loss = 0
            correct = 0
            top3_correct = 0
            top5_correct = 0
            total = 0

            with torch.no_grad():
                for spatial, temporal, labels in test_loader:
                    spatial, temporal, labels = spatial.to(device), temporal.to(device), labels.to(device)
                    logits = stm_model(spatial, temporal)
                    loss = criterion(logits, labels)

                    test_loss += loss.item()
                    _, predicted = torch.max(logits, 1)
                    correct += (predicted == labels).sum().item()

                    _, top3 = torch.topk(logits, 3, dim=1)
                    top3_correct += sum([labels[i] in top3[i] for i in range(len(labels))])

                    _, top5 = torch.topk(logits, 5, dim=1)
                    top5_correct += sum([labels[i] in top5[i] for i in range(len(labels))])

                    total += labels.size(0)

            stm_val_accuracy = 100 * correct / total
            stm_val_top3 = 100 * top3_correct / total
            stm_val_top5 = 100 * top5_correct / total
            stm_val_loss = test_loss / len(test_loader)

            # Evaluate GNN
            from models.mule_detection.model import MuleDetectionGNN
            gnn_checkpoint = Path(self.training_config['mule_detection']['checkpoint']['save_dir']) / 'best_model.pth'
            gnn_data = torch.load(self.processed_dir / 'gnn_data.pt', map_location=device, weights_only=False)
            gnn_model = MuleDetectionGNN(self.config['models']['mule_detection'])
            gnn_ckpt = torch.load(gnn_checkpoint, map_location=device, weights_only=False)
            gnn_model.load_state_dict(gnn_ckpt['model_state_dict'])
            gnn_model = gnn_model.to(device)
            gnn_model.eval()

            from torch_geometric.loader import NeighborLoader
            test_loader = NeighborLoader(
                gnn_data,
                num_neighbors=[15, 10, 5],
                batch_size=64,
                input_nodes=gnn_data.test_mask,
                shuffle=False,
                num_workers=0
            )

            pos_weight = torch.tensor([self.training_config['mule_detection'].get('pos_weight', 5.0)]).to(device)
            criterion = torch.nn.BCEWithLogitsLoss(pos_weight=pos_weight)

            gnn_model.eval()
            test_loss = 0
            all_preds = []
            all_labels = []

            with torch.no_grad():
                for batch in test_loader:
                    batch = batch.to(device)
                    logits = gnn_model(batch.x, batch.edge_index).squeeze()
                    loss = criterion(logits[batch.test_mask], batch.y[batch.test_mask].float())
                    test_loss += loss.item()

                    probs = torch.sigmoid(logits)
                    preds = (probs > 0.5).float()
                    all_preds.append(preds[batch.test_mask].cpu())
                    all_labels.append(batch.y[batch.test_mask].cpu())

            if all_preds:
                all_preds = torch.cat(all_preds)
                all_labels = torch.cat(all_labels)

                tp = ((all_preds == 1) & (all_labels == 1)).sum().item()
                fp = ((all_preds == 1) & (all_labels == 0)).sum().item()
                fn = ((all_preds == 0) & (all_labels == 1)).sum().item()
                tn = ((all_preds == 0) & (all_labels == 0)).sum().item()

                precision = tp / (tp + fp) if (tp + fp) > 0 else 0
                recall = tp / (tp + fn) if (tp + fn) > 0 else 0
                f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
                accuracy = (tp + tn) / (tp + tn + fp + fn) if (tp + tn + fp + fn) > 0 else 0
            else:
                precision = recall = f1 = accuracy = 0

            gnn_val_loss = test_loss / len(test_loader)

            metrics = RetrainingMetrics(
                stm_val_accuracy=stm_val_accuracy,
                stm_val_top3=stm_val_top3,
                stm_val_top5=stm_val_top5,
                stm_val_loss=stm_val_loss,
                gnn_val_f1=f1,
                gnn_val_precision=precision,
                gnn_val_recall=recall,
                gnn_val_accuracy=accuracy,
                gnn_val_loss=gnn_val_loss,
                timestamp=datetime.now().isoformat()
            )

            logger.info(f"STM - Acc: {stm_val_accuracy:.2f}%, Top-3: {stm_val_top3:.2f}%, Top-5: {stm_val_top5:.2f}%")
            logger.info(f"GNN - F1: {f1:.4f}, Prec: {precision:.4f}, Rec: {recall:.4f}, Acc: {accuracy:.4f}")

            return metrics

        except Exception as e:
            logger.error(f"Model evaluation failed: {e}")
            return None

    def check_deployment_criteria(self, new_metrics: RetrainingMetrics, old_metrics: Optional[RetrainingMetrics]) -> Tuple[bool, str]:
        """Check if new models meet deployment criteria."""
        logger.info("Stage 5: Checking deployment criteria")

        if old_metrics is None:
            logger.info("No previous models to compare - deploying new models")
            return True, "First deployment - no comparison baseline"

        # Check STM accuracy improvement
        stm_acc_improvement = new_metrics.stm_val_accuracy - old_metrics.stm_val_accuracy
        if stm_acc_improvement < self.criteria['min_accuracy_improvement']:
            return False, f"STM accuracy improvement ({stm_acc_improvement:.4f}) below threshold ({self.criteria['min_accuracy_improvement']})"

        # Check STM accuracy degradation
        stm_acc_degradation = old_metrics.stm_val_accuracy - new_metrics.stm_val_accuracy
        if stm_acc_degradation > self.criteria['max_accuracy_degradation']:
            return False, f"STM accuracy degraded by {stm_acc_degradation:.4f} (max allowed: {self.criteria['max_accuracy_degradation']})"

        # Check GNN F1 improvement
        gnn_f1_improvement = new_metrics.gnn_val_f1 - old_metrics.gnn_val_f1
        if gnn_f1_improvement < self.criteria['min_f1_improvement']:
            return False, f"GNN F1 improvement ({gnn_f1_improvement:.4f}) below threshold ({self.criteria['min_f1_improvement']})"

        logger.info("✓ All deployment criteria met")
        return True, "All deployment criteria satisfied"

    def promote_models(self, model_paths: Dict[str, str]) -> bool:
        """Promote new models to production."""
        logger.info("Stage 6: Promoting models to production")

        try:
            # Models are already saved to checkpoint directories by training scripts
            # In production, this might involve copying to a model registry or serving directory

            # Log to MLflow
            self.mlflow_tracker.log_retraining_run(model_paths)

            logger.info("✓ Models promoted to production")
            return True

        except Exception as e:
            logger.error(f"Model promotion failed: {e}")
            return False

    def send_notification(self, result: RetrainingResult) -> bool:
        """Send notification about retraining result."""
        logger.info("Stage 7: Sending notifications")

        if not self.retraining_config['notification']['enabled']:
            logger.info("Notifications disabled")
            return True

        try:
            # In production, send to email/slack
            message = f"""
Retraining Pipeline {'SUCCESS' if result.success else 'FAILED'}
Time: {datetime.now().isoformat()}
Criteria Met: {result.meets_criteria}
Message: {result.message}

STM Metrics:
  - Accuracy: {result.metrics.stm_val_accuracy:.2f}% (prev: {result.previous_metrics.stm_val_accuracy:.2f}% if result.previous_metrics else 'N/A')
  - Top-3: {result.metrics.stm_val_top3:.2f}%
  - Top-5: {result.metrics.stm_val_top5:.2f}%

GNN Metrics:
  - F1: {result.metrics.gnn_val_f1:.4f} (prev: {result.previous_metrics.gnn_val_f1:.4f} if result.previous_metrics else 'N/A')
  - Precision: {result.metrics.gnn_val_precision:.4f}
  - Recall: {result.metrics.gnn_val_recall:.4f}
            """

            logger.info(message)
            # TODO: Implement actual email/slack sending
            return True

        except Exception as e:
            logger.error(f"Notification failed: {e}")
            return False

    def run(self) -> RetrainingResult:
        """Run the complete retraining pipeline."""
        logger.info("=" * 60)
        logger.info("STARTING RETRAINING PIPELINE")
        logger.info("=" * 60)

        start_time = time.time()

        # Get current metrics before retraining
        previous_metrics = self.get_current_metrics()

        # Backup current models
        self.backup_current_models()

        # Stage 1: Data refresh
        if not self.run_data_refresh():
            return RetrainingResult(
                success=False,
                metrics=None,
                previous_metrics=previous_metrics,
                meets_criteria=False,
                message="Data refresh failed",
                model_paths={}
            )

        # Stage 2: Feature engineering
        if not self.run_feature_engineering():
            return RetrainingResult(
                success=False,
                metrics=None,
                previous_metrics=previous_metrics,
                meets_criteria=False,
                message="Feature engineering failed",
                model_paths={}
            )

        # Stage 3: Model training
        training_success, model_paths = self.run_model_training()
        if not training_success:
            return RetrainingResult(
                success=False,
                metrics=None,
                previous_metrics=previous_metrics,
                meets_criteria=False,
                message="Model training failed",
                model_paths={}
            )

        # Stage 4: Model evaluation
        new_metrics = self.evaluate_models()
        if new_metrics is None:
            return RetrainingResult(
                success=False,
                metrics=None,
                previous_metrics=previous_metrics,
                meets_criteria=False,
                message="Model evaluation failed",
                model_paths=model_paths
            )

        # Stage 5: Check deployment criteria
        meets_criteria, criteria_message = self.check_deployment_criteria(new_metrics, previous_metrics)

        # Stage 6: Promote models if criteria met
        if meets_criteria:
            promotion_success = self.promote_models(model_paths)
            if not promotion_success:
                return RetrainingResult(
                    success=False,
                    metrics=new_metrics,
                    previous_metrics=previous_metrics,
                    meets_criteria=False,
                    message="Model promotion failed",
                    model_paths=model_paths
                )

        # Stage 7: Notification
        result = RetrainingResult(
            success=True,
            metrics=new_metrics,
            previous_metrics=previous_metrics,
            meets_criteria=meets_criteria,
            message=criteria_message,
            model_paths=model_paths
        )

        self.send_notification(result)

        elapsed = time.time() - start_time
        logger.info(f"Pipeline completed in {elapsed:.1f}s")
        logger.info(f"Result: {'SUCCESS' if result.success else 'FAILED'} - {result.message}")

        return result


def main():
    """CLI entry point for retraining pipeline."""
    import argparse

    parser = argparse.ArgumentParser(description='Run retraining pipeline')
    parser.add_argument('--config', type=str, default='config/config.yaml',
                       help='Path to configuration file')
    parser.add_argument('--skip-data-refresh', action='store_true',
                       help='Skip data refresh stage')
    parser.add_argument('--force-deploy', action='store_true',
                       help='Force deployment even if criteria not met')

    args = parser.parse_args()

    pipeline = RetrainingPipeline(args.config)

    if args.skip_data_refresh:
        # Override data refresh to skip
        original_refresh = pipeline.run_data_refresh
        pipeline.run_data_refresh = lambda: True

    result = pipeline.run()

    # Exit with appropriate code
    sys.exit(0 if result.success and result.meets_criteria else 1)


if __name__ == '__main__':
    main()