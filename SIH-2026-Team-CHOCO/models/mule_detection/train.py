"""Training script for Mule Detection GNN."""

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
from torch_geometric.data import Data
from torch_geometric.loader import NeighborLoader
import numpy as np
from tqdm import tqdm
from loguru import logger
import mlflow

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from models.mule_detection.model import MuleDetectionGNN
from models.utils.mlflow_utils import setup_mlflow_for_training, end_mlflow_run, create_input_example, MLflowTracker
from models.utils.tensorboard_utils import TensorBoardLogger, LiveTrainingMonitor, create_live_monitor


class EarlyStopping:
    """Early stopping to stop training when validation metric doesn't improve."""

    def __init__(self, patience: int = 15, min_delta: float = 0.001, mode: str = 'max'):
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


def load_gnn_data(data_path: str) -> Data:
    """Load preprocessed GNN data."""
    import torch
    data = torch.load(data_path, weights_only=False)
    return data


def train_epoch(model, loader, criterion, optimizer, device, gradient_clip: float = 1.0):
    """Train for one epoch."""
    model.train()
    total_loss = 0
    correct = 0
    total = 0

    pbar = tqdm(loader, desc='Training')
    for batch in pbar:
        batch = batch.to(device)
        optimizer.zero_grad()

        # Forward pass
        logits = model(batch.x, batch.edge_index).squeeze()
        loss = criterion(logits[batch.train_mask], batch.y[batch.train_mask].float())

        # Backward pass
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), gradient_clip)
        optimizer.step()

        # Metrics
        total_loss += loss.item()
        preds = (torch.sigmoid(logits) > 0.5).float()
        correct += (preds[batch.train_mask] == batch.y[batch.train_mask]).sum().item()
        total += batch.train_mask.sum().item()

        pbar.set_postfix({'loss': loss.item(), 'acc': 100 * correct / total if total > 0 else 0})

    avg_loss = total_loss / len(loader)
    accuracy = 100 * correct / total if total > 0 else 0
    return avg_loss, accuracy


def validate(model, loader, criterion, device):
    """Validate the model."""
    model.eval()
    total_loss = 0
    all_preds = []
    all_labels = []

    with torch.no_grad():
        for batch in tqdm(loader, desc='Validating'):
            batch = batch.to(device)
            logits = model(batch.x, batch.edge_index).squeeze()
            loss = criterion(logits[batch.val_mask], batch.y[batch.val_mask].float())

            total_loss += loss.item()

            probs = torch.sigmoid(logits)
            preds = (probs > 0.5).float()
            all_preds.append(preds[batch.val_mask].cpu())
            all_labels.append(batch.y[batch.val_mask].cpu())

    if all_preds:
        all_preds = torch.cat(all_preds)
        all_labels = torch.cat(all_labels)

        # Compute metrics
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

    avg_loss = total_loss / len(loader)
    return avg_loss, accuracy, precision, recall, f1


def train(config: Dict):
    """Main training function."""

    # Device
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    logger.info(f"Using device: {device}")

    # Set up MLflow
    mlflow_tracker, mlflow_run = setup_mlflow_for_training(config, "gnn_training")
    input_example = create_input_example('mule_detection', config)

    try:
        # Load preprocessed GNN data
        data_path = config['data']['processed_dir'] + '/gnn_data.pt'
        logger.info(f"Loading GNN data from {data_path}...")
        data = load_gnn_data(data_path)
        data = data.to(device)

        logger.info(f"Graph: {data.num_nodes} nodes, {data.num_edges} edges")
        logger.info(f"Features: {data.num_node_features}")

        # Create NeighborLoader for training
        train_cfg = config['training']['mule_detection']

        train_loader = NeighborLoader(
            data,
            num_neighbors=[15, 10, 5],
            batch_size=train_cfg['batch_size'],
            input_nodes=data.train_mask,
            shuffle=True,
            num_workers=0
        )

        val_loader = NeighborLoader(
            data,
            num_neighbors=[15, 10, 5],
            batch_size=train_cfg['batch_size'],
            input_nodes=data.val_mask,
            shuffle=False,
            num_workers=0
        )

        # Model
        logger.info("Initializing model...")
        model = MuleDetectionGNN(config['models']['mule_detection'])
        model = model.to(device)

        logger.info(f"Model parameters: {sum(p.numel() for p in model.parameters()):,}")

        # Set up TensorBoard monitoring
        tb_monitor = create_live_monitor(model, config, "mule_detection_gnn")
        tb_monitor.on_train_start(input_example)

        # Loss and optimizer
        pos_weight = torch.tensor([train_cfg.get('pos_weight', 5.0)]).to(device)
        criterion = nn.BCEWithLogitsLoss(pos_weight=pos_weight)

        optimizer = optim.AdamW(
            model.parameters(),
            lr=train_cfg['learning_rate'],
            weight_decay=train_cfg['weight_decay']
        )

        # Scheduler
        scheduler = optim.lr_scheduler.ReduceLROnPlateau(
            optimizer,
            mode='max' if train_cfg['early_stopping']['monitor'] == 'val_f1' else 'min',
            patience=train_cfg['lr_scheduler']['patience'],
            factor=train_cfg['lr_scheduler']['factor'],
            min_lr=train_cfg['lr_scheduler']['min_lr']
        )

        # Early stopping
        early_stopping = EarlyStopping(
            patience=train_cfg['early_stopping']['patience'],
            min_delta=train_cfg['early_stopping']['min_delta'],
            mode='max' if train_cfg['early_stopping']['monitor'] == 'val_f1' else 'min'
        )

        # Training loop
        best_val_f1 = 0
        best_val_loss = float('inf')

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
            val_loss, val_acc, val_prec, val_rec, val_f1 = validate(
                model, val_loader, criterion, device
            )

            logger.info(
                f"Train Loss: {train_loss:.4f} | Train Acc: {train_acc:.2f}% | "
                f"Val Loss: {val_loss:.4f} | Val Acc: {val_acc:.2f}% | "
                f"Val Prec: {val_prec:.4f} | Val Rec: {val_rec:.4f} | Val F1: {val_f1:.4f}"
            )

            # Log to MLflow
            mlflow_tracker.log_metrics({
                'gnn_train_loss': train_loss,
                'gnn_train_acc': train_acc,
                'gnn_val_loss': val_loss,
                'gnn_val_acc': val_acc,
                'gnn_val_precision': val_prec,
                'gnn_val_recall': val_rec,
                'gnn_val_f1': val_f1,
                'gnn_learning_rate': optimizer.param_groups[0]['lr']
            }, step=epoch)

            # Log to TensorBoard
            current_lr = optimizer.param_groups[0]['lr']
            tb_monitor.on_epoch_end(epoch, train_loss, train_acc, val_loss, val_acc, 0, 0, current_lr)

            # Scheduler step (use F1 for mode='max', loss for mode='min')
            monitor_metric = val_f1 if train_cfg['early_stopping']['monitor'] == 'val_f1' else val_loss
            scheduler.step(monitor_metric)
            logger.info(f"Learning rate: {current_lr:.6f}")

            # Save best model
            if val_f1 > best_val_f1:
                best_val_f1 = val_f1
                best_val_loss = val_loss

                checkpoint_dir = Path(train_cfg['checkpoint']['save_dir'])
                checkpoint_dir.mkdir(parents=True, exist_ok=True)

                torch.save({
                    'epoch': epoch,
                    'model_state_dict': model.state_dict(),
                    'optimizer_state_dict': optimizer.state_dict(),
                    'val_loss': val_loss,
                    'val_f1': val_f1,
                    'val_precision': val_prec,
                    'val_recall': val_rec,
                    'config': config
                }, checkpoint_dir / 'best_model.pth')

                logger.info(f"✓ Saved best model (F1: {val_f1:.4f})")

            # Early stopping
            if early_stopping(monitor_metric):
                logger.info(f"Early stopping triggered at epoch {epoch + 1}")
                break

        logger.info(f"\n✓ Training complete!")
        logger.info(f"Best validation F1: {best_val_f1:.4f}")
        logger.info(f"Best validation loss: {best_val_loss:.4f}")

        # Final TensorBoard logging
        final_metrics = {
            'best_val_f1': best_val_f1,
            'best_val_loss': best_val_loss,
            'total_epochs': epoch + 1
        }
        tb_monitor.on_train_end(final_metrics)

        # Register model
        if mlflow_run:
            model_uri = f"runs:/{mlflow_run.info.run_id}/gnn_epoch_{epoch}"
            registered_name = config['mlflow']['experiments'].get('mule_detection', 'mule_detection_gnn')
            mlflow_tracker.register_model(registered_name, model_uri, stage="Staging")

    finally:
        end_mlflow_run()


def main():
    parser = argparse.ArgumentParser(description='Train Mule Detection GNN')
    parser.add_argument('--config', type=str, default='config/config.yaml',
                       help='Path to configuration file')
    parser.add_argument('--epochs', type=int, default=None,
                       help='Override number of training epochs')
    args = parser.parse_args()

    # Load config
    with open(args.config, 'r') as f:
        config = yaml.safe_load(f)

    if args.epochs is not None:
        config['training']['mule_detection']['epochs'] = args.epochs

    # Train
    train(config)


if __name__ == '__main__':
    main()