"""TensorBoard Integration Utilities for Live Training Visualization."""

import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime
import torch
import torch.nn as nn
try:
    from torch.utils.tensorboard import SummaryWriter
    TENSORBOARD_AVAILABLE = True
except (ImportError, ModuleNotFoundError):
    TENSORBOARD_AVAILABLE = False
    class SummaryWriter:
        def __init__(self, *args, **kwargs): pass
        def add_scalar(self, *args, **kwargs): pass
        def add_scalars(self, *args, **kwargs): pass
        def add_histogram(self, *args, **kwargs): pass
        def add_graph(self, *args, **kwargs): pass
        def add_embedding(self, *args, **kwargs): pass
        def add_figure(self, *args, **kwargs): pass
        def add_text(self, *args, **kwargs): pass
        def flush(self): pass
        def close(self): pass

from loguru import logger


class TensorBoardLogger:
    """TensorBoard logger for training visualization."""

    def __init__(self, log_dir: str = "logs/tensorboard", model_name: str = "model"):
        """Initialize TensorBoard logger."""
        self.log_dir = Path(log_dir) / model_name / datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.writer = SummaryWriter(log_dir=str(self.log_dir))
        self.model_name = model_name
        if TENSORBOARD_AVAILABLE:
            logger.info(f"TensorBoard logging to: {self.log_dir}")
        else:
            logger.warning("TensorBoard not available, logging in no-op mode.")

    def log_scalar(self, tag: str, value: float, step: int):
        """Log a scalar value."""
        self.writer.add_scalar(tag, value, step)

    def log_scalars(self, main_tag: str, tag_scalar_dict: Dict[str, float], step: int):
        """Log multiple scalars at once."""
        self.writer.add_scalars(main_tag, tag_scalar_dict, step)

    def log_histogram(self, tag: str, values: torch.Tensor, step: int):
        """Log histogram of values (e.g., weights, gradients)."""
        self.writer.add_histogram(tag, values, step)

    def log_model_graph(self, model: nn.Module, input_example: Tuple[torch.Tensor, ...]):
        """Log model architecture graph."""
        try:
            self.writer.add_graph(model, input_example)
            logger.info(f"Logged model graph for {self.model_name}")
        except Exception as e:
            logger.warning(f"Could not log model graph: {e}")

    def log_embeddings(self, embeddings: torch.Tensor, metadata: List[str],
                       label_img: Optional[torch.Tensor] = None, step: int = 0):
        """Log embeddings for visualization."""
        self.writer.add_embedding(embeddings, metadata=metadata, label_img=label_img, global_step=step)

    def log_figure(self, tag: str, figure, step: int):
        """Log matplotlib figure."""
        self.writer.add_figure(tag, figure, step)

    def log_text(self, tag: str, text: str, step: int):
        """Log text (e.g., config, notes)."""
        self.writer.add_text(tag, text, step)

    def log_hyperparams(self, hparams: Dict[str, Any], metrics: Dict[str, float]):
        """Log hyperparameters and final metrics."""
        self.writer.add_hparams(hparams, metrics)

    def log_training_curves(self, train_losses: List[float], val_losses: List[float],
                            train_accs: List[float], val_accs: List[float],
                            step: int):
        """Log training curves."""
        epochs = list(range(1, len(train_losses) + 1))

        # Loss curves
        self.log_scalars(f"{self.model_name}/Loss", {
            'train': train_losses[-1] if train_losses else 0,
            'val': val_losses[-1] if val_losses else 0
        }, step)

        # Accuracy curves
        self.log_scalars(f"{self.model_name}/Accuracy", {
            'train': train_accs[-1] if train_accs else 0,
            'val': val_accs[-1] if val_accs else 0
        }, step)

    def log_gradients(self, model: nn.Module, step: int):
        """Log gradient histograms for all parameters."""
        for name, param in model.named_parameters():
            if param.grad is not None:
                self.writer.add_histogram(f"gradients/{name}", param.grad, step)

    def log_weights(self, model: nn.Module, step: int):
        """Log weight histograms for all parameters."""
        for name, param in model.named_parameters():
            self.writer.add_histogram(f"weights/{name}", param, step)

    def log_learning_rate(self, lr: float, step: int):
        """Log learning rate."""
        self.writer.add_scalar(f"{self.model_name}/Learning_Rate", lr, step)

    def log_confusion_matrix(self, cm: torch.Tensor, class_names: List[str], step: int):
        """Log confusion matrix as image."""
        import matplotlib.pyplot as plt
        import numpy as np

        fig, ax = plt.subplots(figsize=(8, 6))
        im = ax.imshow(cm.numpy(), interpolation='nearest', cmap=plt.cm.Blues)
        ax.figure.colorbar(im, ax=ax)

        ax.set(xticks=np.arange(cm.shape[1]),
               yticks=np.arange(cm.shape[0]),
               xticklabels=class_names, yticklabels=class_names,
               title=f'Confusion Matrix (Epoch {step})',
               ylabel='True label',
               xlabel='Predicted label')

        plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

        # Add text annotations
        thresh = cm.max() / 2.
        for i in range(cm.shape[0]):
            for j in range(cm.shape[1]):
                ax.text(j, i, format(cm[i, j], 'd'),
                       ha="center", va="center",
                       color="white" if cm[i, j] > thresh else "black")

        fig.tight_layout()
        self.writer.add_figure(f"{self.model_name}/Confusion_Matrix", fig, step)
        plt.close(fig)

    def log_roc_curve(self, fpr: torch.Tensor, tpr: torch.Tensor, auc: float, step: int):
        """Log ROC curve."""
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(8, 6))
        ax.plot(fpr.numpy(), tpr.numpy(), label=f'ROC curve (AUC = {auc:.4f})')
        ax.plot([0, 1], [0, 1], 'k--', label='Random')
        ax.set_xlabel('False Positive Rate')
        ax.set_ylabel('True Positive Rate')
        ax.set_title(f'ROC Curve (Epoch {step})')
        ax.legend()
        self.writer.add_figure(f"{self.model_name}/ROC_Curve", fig, step)
        plt.close(fig)

    def log_pr_curve(self, precision: torch.Tensor, recall: torch.Tensor, auc: float, step: int):
        """Log Precision-Recall curve."""
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(8, 6))
        ax.plot(recall.numpy(), precision.numpy(), label=f'PR curve (AUC = {auc:.4f})')
        ax.set_xlabel('Recall')
        ax.set_ylabel('Precision')
        ax.set_title(f'Precision-Recall Curve (Epoch {step})')
        ax.legend()
        self.writer.add_figure(f"{self.model_name}/PR_Curve", fig, step)
        plt.close(fig)

    def flush(self):
        """Flush writer buffer."""
        self.writer.flush()

    def close(self):
        """Close writer."""
        self.writer.close()


class LiveTrainingMonitor:
    """Monitor training progress and log to TensorBoard."""

    def __init__(self, model: nn.Module, config: Dict[str, Any],
                 log_dir: str = "logs/tensorboard", model_name: str = "model"):
        self.logger = TensorBoardLogger(log_dir, model_name)
        self.model = model
        self.config = config
        self.model_name = model_name
        self.step = 0
        self.epoch = 0

        # Store history for plotting
        self.train_losses = []
        self.val_losses = []
        self.train_accs = []
        self.val_accs = []
        self.train_top3s = []
        self.val_top3s = []
        self.train_top5s = []
        self.val_top5s = []
        self.learning_rates = []

    def on_train_start(self, input_example: Tuple[torch.Tensor, ...]):
        """Call at start of training."""
        # Log model graph
        self.logger.log_model_graph(self.model, input_example)

        # Log config as text
        import yaml
        config_text = yaml.dump(self.config, default_flow_style=False)
        self.logger.log_text("config", config_text, 0)

        # Log hyperparameters
        hparams = self._extract_hyperparams()
        self.logger.log_hyperparams(hparams, {})

    def on_epoch_start(self, epoch: int):
        """Call at start of each epoch."""
        self.epoch = epoch
        self.logger.log_scalar(f"{self.model_name}/Epoch", epoch, self.step)

    def on_batch_end(self, epoch: int, batch_idx: int, loss: float,
                     batch_size: int, total_batches: int):
        """Call at end of each batch."""
        global_step = epoch * total_batches + batch_idx

        # Log batch loss
        self.logger.log_scalar(f"{self.model_name}/Batch_Loss", loss, global_step)

        # Log gradient norms periodically
        if batch_idx % 50 == 0:
            total_norm = 0
            for p in self.model.parameters():
                if p.grad is not None:
                    total_norm += p.grad.data.norm(2).item() ** 2
            self.logger.log_scalar(f"{self.model_name}/Grad_Norm", total_norm ** 0.5, global_step)

    def on_epoch_end(self, epoch: int, train_loss: float, train_acc: float,
                     val_loss: float, val_acc: float, val_top3: float = 0,
                     val_top5: float = 0, lr: float = 0):
        """Call at end of each epoch."""
        # Store history
        self.train_losses.append(train_loss)
        self.val_losses.append(val_loss)
        self.train_accs.append(train_acc)
        self.val_accs.append(val_acc)
        self.val_top3s.append(val_top3)
        self.val_top5s.append(val_top5)
        self.learning_rates.append(lr)

        # Log epoch metrics
        self.logger.log_scalars(f"{self.model_name}/Loss", {
            'train': train_loss,
            'val': val_loss
        }, epoch)

        self.logger.log_scalars(f"{self.model_name}/Accuracy", {
            'train': train_acc,
            'val': val_acc
        }, epoch)

        if val_top3 > 0:
            self.logger.log_scalars(f"{self.model_name}/Top_K_Accuracy", {
                'top1': val_acc,
                'top3': val_top3,
                'top5': val_top5
            }, epoch)

        self.logger.log_learning_rate(lr, epoch)

        # Log weight and gradient histograms periodically
        if epoch % 10 == 0:
            self.logger.log_weights(self.model, epoch)
            self.logger.log_gradients(self.model, epoch)

        self.logger.flush()

    def on_train_end(self, final_metrics: Dict[str, float]):
        """Call at end of training."""
        # Log final metrics as hyperparameters
        hparams = self._extract_hyperparams()
        self.logger.log_hyperparams(hparams, final_metrics)

        # Log final model graph
        self.logger.flush()
        self.logger.close()

    def _extract_hyperparams(self) -> Dict[str, Any]:
        """Extract hyperparameters from config."""
        hparams = {}

        # Flatten config
        def flatten_dict(d: Dict, parent_key: str = '', sep: str = '.'):
            for k, v in d.items():
                new_key = f"{parent_key}{sep}{k}" if parent_key else k
                if isinstance(v, dict):
                    flatten_dict(v, new_key, sep)
                elif isinstance(v, (list, tuple)):
                    hparams[new_key] = str(v)
                else:
                    hparams[new_key] = v

        flatten_dict(self.config)
        return hparams


def create_tensorboard_logger(config: Dict[str, Any], model_name: str) -> TensorBoardLogger:
    """Factory function to create TensorBoard logger."""
    log_dir = config.get('logging', {}).get('tensorboard_dir', 'logs/tensorboard')
    return TensorBoardLogger(log_dir, model_name)


def create_live_monitor(model: nn.Module, config: Dict[str, Any], model_name: str) -> LiveTrainingMonitor:
    """Factory function to create live training monitor."""
    return LiveTrainingMonitor(model, config, model_name=model_name)