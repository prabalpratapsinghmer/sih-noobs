"""Training script for Spatio-Temporal Transformer."""

import os
import sys
from pathlib import Path
import argparse
import yaml
from typing import Dict, Tuple

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import numpy as np
from tqdm import tqdm
from loguru import logger
import mlflow

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from models.spatio_temporal.model import SpatioTemporalTransformer
from models.utils.mlflow_utils import setup_mlflow_for_training, end_mlflow_run, create_input_example, MLflowTracker
from models.utils.tensorboard_utils import TensorBoardLogger, LiveTrainingMonitor, create_live_monitor


class EarlyStopping:
    """Early stopping to stop training when validation loss doesn't improve."""

    def __init__(self, patience: int = 20, min_delta: float = 0.001, mode: str = 'min'):
        self.patience = patience
        self.min_delta = min_delta
        self.mode = mode
        self.counter = 0
        self.best_score = None
        self.early_stop = False

    def __call__(self, score: float) -> bool:
        if self.best_score is None:
            self.best_score = score
            return False

        if self.mode == 'min':
            improved = score < (self.best_score - self.min_delta)
        else:
            improved = score > (self.best_score + self.min_delta)

        if improved:
            self.best_score = score
            self.counter = 0
        else:
            self.counter += 1
            if self.counter >= self.patience:
                self.early_stop = True
                return True

        return False


def create_dummy_data(num_samples: int = 1000) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    """Create dummy data for training (until real data synthesis is ready)."""

    # Spatial features: lat, lon, dist_metro, dist_police (normalized)
    spatial = torch.randn(num_samples, 4)

    # Temporal features: hour_sin, hour_cos, day, weekend, time_since_complaint, fraud_spike_hour
    temporal = torch.randn(num_samples, 6)

    # Labels: ATM indices (0-499)
    labels = torch.randint(0, 500, (num_samples,))

    return spatial, temporal, labels


def train_epoch(model, dataloader, criterion, optimizer, device, gradient_clip: float = 1.0):
    """Train for one epoch."""
    model.train()
    total_loss = 0
    correct = 0
    total = 0

    pbar = tqdm(dataloader, desc='Training')
    for spatial, temporal, labels in pbar:
        spatial = spatial.to(device)
        temporal = temporal.to(device)
        labels = labels.to(device)

        # Forward pass
        optimizer.zero_grad()
        logits = model(spatial, temporal)
        loss = criterion(logits, labels)

        # Backward pass
        loss.backward()

        # Gradient clipping
        torch.nn.utils.clip_grad_norm_(model.parameters(), gradient_clip)

        optimizer.step()

        # Metrics
        total_loss += loss.item()
        _, predicted = torch.max(logits, 1)
        correct += (predicted == labels).sum().item()
        total += labels.size(0)

        pbar.set_postfix({'loss': loss.item(), 'acc': 100 * correct / total})

    avg_loss = total_loss / len(dataloader)
    accuracy = 100 * correct / total
    return avg_loss, accuracy


def validate(model, dataloader, criterion, device):
    """Validate the model."""
    model.eval()
    total_loss = 0
    correct = 0
    top3_correct = 0
    top5_correct = 0
    total = 0

    with torch.no_grad():
        for spatial, temporal, labels in tqdm(dataloader, desc='Validating'):
            spatial = spatial.to(device)
            temporal = temporal.to(device)
            labels = labels.to(device)

            # Forward pass
            logits = model(spatial, temporal)
            loss = criterion(logits, labels)

            # Metrics
            total_loss += loss.item()

            # Top-1 accuracy
            _, predicted = torch.max(logits, 1)
            correct += (predicted == labels).sum().item()

            # Top-3 accuracy
            _, top3 = torch.topk(logits, 3, dim=1)
            top3_correct += sum([labels[i] in top3[i] for i in range(len(labels))])

            # Top-5 accuracy
            _, top5 = torch.topk(logits, 5, dim=1)
            top5_correct += sum([labels[i] in top5[i] for i in range(len(labels))])

            total += labels.size(0)

    avg_loss = total_loss / len(dataloader)
    accuracy = 100 * correct / total
    top3_accuracy = 100 * top3_correct / total
    top5_accuracy = 100 * top5_correct / total

    return avg_loss, accuracy, top3_accuracy, top5_accuracy


def load_processed_data(processed_dir: Path):
    """Load preprocessed data from numpy files."""
    X_train = np.load(processed_dir / 'st_X_train.npy')
    y_train = np.load(processed_dir / 'st_y_train.npy')
    X_val = np.load(processed_dir / 'st_X_val.npy')
    y_val = np.load(processed_dir / 'st_y_val.npy')
    X_test = np.load(processed_dir / 'st_X_test.npy')
    y_test = np.load(processed_dir / 'st_y_test.npy')

    logger.info(f"Loaded data - Train: {X_train.shape[0]}, Val: {X_val.shape[0]}, Test: {X_test.shape[0]}")
    logger.info(f"Features - Spatial: {X_train.shape[1]//2}, Temporal: {X_train.shape[1]//2}")

    return X_train, y_train, X_val, y_val, X_test, y_test


def train(config: Dict):
    """Main training function."""

    # Device
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    logger.info(f"Using device: {device}")

    # Set up MLflow
    mlflow_tracker, mlflow_run = setup_mlflow_for_training(config, "stm_training")
    input_example = create_input_example('spatio_temporal', config)

    try:
        # Load processed data
        processed_dir = Path(config['data']['processed_dir'])
        logger.info("Loading processed training data...")
        X_train, y_train, X_val, y_val, X_test, y_test = load_processed_data(processed_dir)

        # Split features (first half spatial, second half temporal)
        spatial_dim = X_train.shape[1] // 2
        spatial_train = X_train[:, :spatial_dim]
        temporal_train = X_train[:, spatial_dim:]
        spatial_val = X_val[:, :spatial_dim]
        temporal_val = X_val[:, spatial_dim:]
        spatial_test = X_test[:, :spatial_dim]
        temporal_test = X_test[:, spatial_dim:]

        # Dataloaders
        train_dataset = TensorDataset(
            torch.FloatTensor(spatial_train),
            torch.FloatTensor(temporal_train),
            torch.LongTensor(y_train)
        )
        val_dataset = TensorDataset(
            torch.FloatTensor(spatial_val),
            torch.FloatTensor(temporal_val),
            torch.LongTensor(y_val)
        )
        test_dataset = TensorDataset(
            torch.FloatTensor(spatial_test),
            torch.FloatTensor(temporal_test),
            torch.LongTensor(y_test)
        )

        train_cfg = config['training']['spatio_temporal']

        train_loader = DataLoader(
            train_dataset,
            batch_size=train_cfg['batch_size'],
            shuffle=True,
            num_workers=0,
            pin_memory=True if device.type == 'cuda' else False
        )

        val_loader = DataLoader(
            val_dataset,
            batch_size=train_cfg['batch_size'],
            shuffle=False,
            num_workers=0,
            pin_memory=True if device.type == 'cuda' else False
        )

        # Model
        logger.info("Initializing model...")
        model = SpatioTemporalTransformer(config['models']['spatio_temporal'])
        model = model.to(device)

        logger.info(f"Model parameters: {sum(p.numel() for p in model.parameters()):,}")

        # Set up TensorBoard monitoring
        tb_monitor = create_live_monitor(model, config, "spatio_temporal_transformer")
        tb_monitor.on_train_start(input_example)

        # Loss and optimizer
        criterion = nn.CrossEntropyLoss(label_smoothing=train_cfg.get('label_smoothing', 0.1))
        optimizer = optim.AdamW(
            model.parameters(),
            lr=train_cfg['learning_rate'],
            weight_decay=train_cfg['weight_decay']
        )

        # Scheduler
        scheduler = optim.lr_scheduler.ReduceLROnPlateau(
            optimizer,
            mode='min',
            patience=train_cfg['lr_scheduler']['patience'],
            factor=train_cfg['lr_scheduler']['factor'],
            min_lr=train_cfg['lr_scheduler']['min_lr']
        )

        # Early stopping
        early_stopping = EarlyStopping(
            patience=train_cfg['early_stopping']['patience'],
            min_delta=train_cfg['early_stopping']['min_delta'],
            mode='min'
        )

        # Training loop
        best_val_loss = float('inf')
        best_val_acc = 0

        logger.info("Starting training...")
        for epoch in range(train_cfg['epochs']):
            logger.info(f"\nEpoch {epoch + 1}/{train_cfg['epochs']}")
            tb_monitor.on_epoch_start(epoch)

            # Train
            train_loss, train_acc = train_epoch(
                model, train_loader, criterion, optimizer, device,
                gradient_clip=train_cfg['gradient_clip']
            )

            # Validate
            val_loss, val_acc, val_top3, val_top5 = validate(
                model, val_loader, criterion, device
            )

            logger.info(
                f"Train Loss: {train_loss:.4f} | Train Acc: {train_acc:.2f}% | "
                f"Val Loss: {val_loss:.4f} | Val Acc: {val_acc:.2f}% | "
                f"Val Top-3: {val_top3:.2f}% | Val Top-5: {val_top5:.2f}%"
            )

            # Log metrics to MLflow
            mlflow_tracker.log_metrics({
                'stm_train_loss': train_loss,
                'stm_train_acc': train_acc,
                'stm_val_loss': val_loss,
                'stm_val_acc': val_acc,
                'stm_val_top3': val_top3,
                'stm_val_top5': val_top5,
                'stm_learning_rate': optimizer.param_groups[0]['lr']
            }, step=epoch)

            # Log to TensorBoard
            current_lr = optimizer.param_groups[0]['lr']
            tb_monitor.on_epoch_end(epoch, train_loss, train_acc, val_loss, val_acc, val_top3, val_top5, current_lr)

            # Scheduler step
            scheduler.step(val_loss)
            logger.info(f"Learning rate: {current_lr:.6f}")

            # Save best model
            if val_acc > best_val_acc:
                best_val_acc = val_acc
                best_val_loss = val_loss

                checkpoint_dir = Path(train_cfg['checkpoint']['save_dir'])
                checkpoint_dir.mkdir(parents=True, exist_ok=True)

                torch.save({
                    'epoch': epoch,
                    'model_state_dict': model.state_dict(),
                    'optimizer_state_dict': optimizer.state_dict(),
                    'val_loss': val_loss,
                    'val_acc': val_acc,
                    'val_top3': val_top3,
                    'val_top5': val_top5,
                    'config': config
                }, checkpoint_dir / 'best_model.pth')

                logger.info(f"✓ Saved best model (acc: {val_acc:.2f}%)")

            # Early stopping
            if early_stopping(val_loss):
                logger.info(f"Early stopping triggered at epoch {epoch + 1}")
                break

        logger.info(f"\n✓ Training complete!")
        logger.info(f"Best validation accuracy: {best_val_acc:.2f}%")
        logger.info(f"Best validation loss: {best_val_loss:.4f}")

        # Log final model to MLflow
        mlflow_tracker.log_model_artifacts(
            model, f"stm_epoch_{epoch}", config, processed_dir, input_example
        )

        # Final TensorBoard logging
        final_metrics = {
            'best_val_acc': best_val_acc,
            'best_val_loss': best_val_loss,
            'total_epochs': epoch + 1
        }
        tb_monitor.on_train_end(final_metrics)

        # Register model
        if mlflow_run:
            model_uri = f"runs:/{mlflow_run.info.run_id}/stm_epoch_{epoch}"
            registered_name = config['mlflow']['experiments'].get('spatio_temporal', 'spatio_temporal_transformer')
            mlflow_tracker.register_model(registered_name, model_uri, stage="Staging")

    finally:
        end_mlflow_run()


def main():
    parser = argparse.ArgumentParser(description='Train Spatio-Temporal Transformer')
    parser.add_argument('--config', type=str, default='config/config.yaml',
                       help='Path to configuration file')
    parser.add_argument('--epochs', type=int, default=None,
                       help='Override number of training epochs')
    args = parser.parse_args()

    # Load config
    with open(args.config, 'r') as f:
        config = yaml.safe_load(f)

    if args.epochs is not None:
        config['training']['spatio_temporal']['epochs'] = args.epochs

    # Train
    train(config)


if __name__ == '__main__':
    main()
