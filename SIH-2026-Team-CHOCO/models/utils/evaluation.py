"""Model Evaluation and Visualization Module for SIH26184."""

import os
import sys
from pathlib import Path
from typing import Dict, Any, Tuple
import numpy as np
import torch
import yaml
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_curve, auc, precision_recall_curve, confusion_matrix
)
from loguru import logger

# Project root
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from models.spatio_temporal.model import SpatioTemporalTransformer
from models.mule_detection.model import MuleDetectionGNN


def evaluate_spatio_temporal(model: SpatioTemporalTransformer, X_test: np.ndarray, y_test: np.ndarray,
                             device: torch.device) -> Dict[str, float]:
    """Evaluate ATM prediction model on test dataset."""
    model.eval()
    spatial_dim = X_test.shape[1] // 2
    sp_test = torch.FloatTensor(X_test[:, :spatial_dim]).to(device)
    tm_test = torch.FloatTensor(X_test[:, spatial_dim:]).to(device)

    with torch.no_grad():
        logits = model(sp_test, tm_test)
        probs = torch.softmax(logits, dim=1).cpu().numpy()
        preds = np.argmax(probs, axis=1)

        # Top-3 and Top-5
        top3 = torch.topk(logits, 3, dim=1)[1].cpu().numpy()
        top5 = torch.topk(logits, 5, dim=1)[1].cpu().numpy()

    top1_acc = accuracy_score(y_test, preds) * 100.0
    top3_acc = np.mean([y_test[i] in top3[i] for i in range(len(y_test))]) * 100.0
    top5_acc = np.mean([y_test[i] in top5[i] for i in range(len(y_test))]) * 100.0

    precision = precision_score(y_test, preds, average="weighted", zero_division=0)
    recall = recall_score(y_test, preds, average="weighted", zero_division=0)
    f1 = f1_score(y_test, preds, average="weighted", zero_division=0)

    return {
        "top1_accuracy": round(float(top1_acc), 2),
        "top3_accuracy": round(float(top3_acc), 2),
        "top5_accuracy": round(float(top5_acc), 2),
        "precision": round(float(precision), 4),
        "recall": round(float(recall), 4),
        "f1_score": round(float(f1), 4),
    }


def evaluate_gnn(model: MuleDetectionGNN, data, device: torch.device) -> Dict[str, Any]:
    """Evaluate GNN Mule Detection model on test nodes."""
    model.eval()
    x = data.x.to(device)
    edge_index = data.edge_index.to(device)
    y = data.y.cpu().numpy()
    mask = data.test_mask.cpu().numpy()

    with torch.no_grad():
        logits = model(x, edge_index).squeeze().cpu().numpy()
        probs = 1 / (1 + np.exp(-logits))
        preds = (probs > 0.5).astype(int)

    test_y = y[mask]
    test_probs = probs[mask]
    test_preds = preds[mask]

    acc = accuracy_score(test_y, test_preds) * 100.0
    prec = precision_score(test_y, test_preds, zero_division=0)
    rec = recall_score(test_y, test_preds, zero_division=0)
    f1 = f1_score(test_y, test_preds, zero_division=0)

    # ROC & PR
    fpr, tpr, _ = roc_curve(test_y, test_probs)
    roc_auc = auc(fpr, tpr)
    precision_curve, recall_curve, _ = precision_recall_curve(test_y, test_probs)
    pr_auc = auc(recall_curve, precision_curve)
    cm = confusion_matrix(test_y, test_preds)

    return {
        "accuracy": round(float(acc), 2),
        "precision": round(float(prec), 4),
        "recall": round(float(rec), 4),
        "f1_score": round(float(f1), 4),
        "roc_auc": round(float(roc_auc), 4),
        "pr_auc": round(float(pr_auc), 4),
        "confusion_matrix": cm,
        "fpr": fpr,
        "tpr": tpr,
        "recall_curve": recall_curve,
        "precision_curve": precision_curve,
    }


def generate_evaluation_plots(gnn_metrics: Dict[str, Any], output_dir: Path):
    """Generate ROC, PR, and Confusion Matrix plots in docs/ directory."""
    output_dir.mkdir(parents=True, exist_ok=True)

    # 1. Confusion Matrix
    plt.figure(figsize=(6, 5))
    cm = gnn_metrics["confusion_matrix"]
    plt.imshow(cm, interpolation="nearest", cmap=plt.cm.Blues)
    plt.title("Mule Detection Confusion Matrix")
    plt.colorbar()
    tick_marks = np.arange(2)
    plt.xticks(tick_marks, ["Legitimate", "Mule"])
    plt.yticks(tick_marks, ["Legitimate", "Mule"])
    for i in range(2):
        for j in range(2):
            plt.text(j, i, format(cm[i, j], "d"), horizontalalignment="center",
                     color="white" if cm[i, j] > cm.max() / 2 else "black")
    plt.ylabel("True Label")
    plt.xlabel("Predicted Label")
    plt.tight_layout()
    plt.savefig(output_dir / "confusion_matrix.png", dpi=300)
    plt.close()

    # 2. ROC Curve
    plt.figure(figsize=(6, 5))
    plt.plot(gnn_metrics["fpr"], gnn_metrics["tpr"], color="#e74c3c", lw=2,
             label=f"ROC (AUC = {gnn_metrics['roc_auc']:.3f})")
    plt.plot([0, 1], [0, 1], color="gray", lw=1, linestyle="--")
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("Mule Detection ROC Curve")
    plt.legend(loc="lower right")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_dir / "roc_curve.png", dpi=300)
    plt.close()

    # 3. PR Curve
    plt.figure(figsize=(6, 5))
    plt.plot(gnn_metrics["recall_curve"], gnn_metrics["precision_curve"], color="#2ecc71", lw=2,
             label=f"PR (AUC = {gnn_metrics['pr_auc']:.3f})")
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel("Recall")
    plt.ylabel("Precision")
    plt.title("Mule Detection Precision-Recall Curve")
    plt.legend(loc="lower left")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_dir / "pr_curve.png", dpi=300)
    plt.close()

    logger.info(f"Saved evaluation plots to {output_dir}")


def main():
    with open("config/config.yaml") as f:
        config = yaml.safe_load(f)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    processed_dir = Path(config["data"]["processed_dir"])
    docs_dir = Path("docs")

    # Evaluate GNN
    gnn_path = processed_dir / "gnn_data.pt"
    if gnn_path.exists():
        gnn_data = torch.load(gnn_path, weights_only=False)
        gnn_model = MuleDetectionGNN(config["models"]["mule_detection"]).to(device)
        gnn_chk = Path(config["training"]["mule_detection"]["checkpoint"]["save_dir"]) / "best_model.pth"
        if gnn_chk.exists():
            gnn_model.load_state_dict(torch.load(gnn_chk, map_location=device, weights_only=False)["model_state_dict"])
        metrics = evaluate_gnn(gnn_model, gnn_data, device)
        generate_evaluation_plots(metrics, docs_dir)
        print("GNN Evaluation:", metrics)


if __name__ == "__main__":
    main()
