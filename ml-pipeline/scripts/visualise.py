#!/usr/bin/env python3
"""
visualise.py — Generate publication-quality figures from pipeline outputs.

Produces:
  fig1_target_distribution.png  — class balance and quality-score distribution
  fig2_correlation_heatmap.png  — feature correlation matrix
  fig3_model_comparison.png     — bar chart: Accuracy / F1 / ROC-AUC by model
  fig4_confusion_matrices.png   — confusion matrices for all three models
  fig5_roc_curves.png           — ROC curves for all three models
  fig6_feature_importance.png   — Random Forest feature importances

Usage:
  python scripts/visualise.py
"""

import sys
import logging
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
log = logging.getLogger(__name__)

BASE_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(BASE_DIR))

from src.data import load_raw, validate, prepare, FEATURE_COLS, TARGET_COL
from src.modeling import load_model
from src.evaluation import get_confusion_matrix, get_roc_data

FIG_DIR   = BASE_DIR / "outputs" / "figures"
TABLE_DIR = BASE_DIR / "outputs" / "tables"
FIG_DIR.mkdir(parents=True, exist_ok=True)

# ── Style constants (match website palette) ──────────────────────────────────
PRIMARY   = "#2d3e50"
SECONDARY = "#3498db"
ACCENT    = "#1abc9c"
LIGHT     = "#f8f9fa"
GRID      = "#e0e0e0"
MODEL_COLOURS = {
    "Logistic Regression": "#3498db",
    "Random Forest":       "#2ecc71",
    "Gradient Boosting":   "#e67e22",
}
MODEL_NAMES = list(MODEL_COLOURS.keys())

plt.rcParams.update({
    "font.family":       "sans-serif",
    "axes.facecolor":    LIGHT,
    "figure.facecolor":  "white",
    "axes.spines.top":   False,
    "axes.spines.right": False,
    "axes.grid":         True,
    "grid.color":        GRID,
    "grid.linewidth":    0.6,
    "axes.titlesize":    11,
    "axes.labelsize":    9,
    "xtick.labelsize":   8,
    "ytick.labelsize":   8,
})

DPI = 150


def _savefig(fig, name: str):
    path = FIG_DIR / name
    fig.savefig(path, dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    log.info("Saved %s", path.name)


# ── Fig 1: Target distribution ───────────────────────────────────────────────
def fig1_target_distribution(df: pd.DataFrame):
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))

    # Left: raw quality score histogram
    ax = axes[0]
    counts = df["quality"].value_counts().sort_index()
    bars = ax.bar(counts.index, counts.values, color=SECONDARY, alpha=0.85, width=0.7, zorder=3)
    for b, v in zip(bars, counts.values):
        ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 15,
                str(v), ha="center", va="bottom", fontsize=8, color=PRIMARY)
    ax.set_xlabel("Quality Score (3 – 9)")
    ax.set_ylabel("Count")
    ax.set_title("Quality Score Distribution")
    ax.set_xticks(counts.index)

    # Right: binary target by wine type
    ax2 = axes[1]
    binary = (df["quality"] >= 6).astype(int)
    wine_type = df["wine_type"].map({0: "Red wine", 1: "White wine"})
    cross = pd.crosstab(wine_type, binary)
    cross.columns = ["Low (< 6)", "High (≥ 6)"]
    cross.plot(kind="bar", ax=ax2, color=["#e74c3c", ACCENT], alpha=0.85,
               edgecolor="none", width=0.55, zorder=3)
    ax2.set_xlabel("")
    ax2.set_ylabel("Count")
    ax2.set_title("Binary Target by Wine Type")
    ax2.set_xticklabels(ax2.get_xticklabels(), rotation=0)
    ax2.legend(title="Quality class", fontsize=8, title_fontsize=8)

    fig.suptitle("UCI Wine Quality — Target Variable", fontsize=12,
                 fontweight="bold", color=PRIMARY, y=1.02)
    fig.tight_layout()
    _savefig(fig, "fig1_target_distribution.png")


# ── Fig 2: Correlation heatmap ───────────────────────────────────────────────
def fig2_correlation_heatmap(df: pd.DataFrame):
    corr = df[FEATURE_COLS + ["quality"]].corr()

    fig, ax = plt.subplots(figsize=(9, 7))
    cmap = plt.get_cmap("RdBu_r")
    im = ax.imshow(corr.values, cmap=cmap, vmin=-1, vmax=1, aspect="auto")

    labels = [c.replace("_", " ") for c in corr.columns]
    ax.set_xticks(range(len(labels)))
    ax.set_yticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=45, ha="right", fontsize=7.5)
    ax.set_yticklabels(labels, fontsize=7.5)

    # Annotate cells with value
    for i in range(len(corr)):
        for j in range(len(corr.columns)):
            val = corr.values[i, j]
            color = "white" if abs(val) > 0.6 else PRIMARY
            ax.text(j, i, f"{val:.2f}", ha="center", va="center",
                    fontsize=6.5, color=color)

    plt.colorbar(im, ax=ax, fraction=0.03, pad=0.04, label="Pearson r")
    ax.set_title("Feature Correlation Matrix", fontsize=12,
                 fontweight="bold", color=PRIMARY, pad=12)
    ax.spines[:].set_visible(False)
    ax.grid(False)
    fig.tight_layout()
    _savefig(fig, "fig2_correlation_heatmap.png")


# ── Fig 3: Model comparison bar chart ────────────────────────────────────────
def fig3_model_comparison(comparison: pd.DataFrame):
    metrics = ["Accuracy", "F1", "ROC-AUC"]
    x = np.arange(len(metrics))
    width = 0.22
    n = len(MODEL_NAMES)

    fig, ax = plt.subplots(figsize=(8, 4.5))

    for i, (name, colour) in enumerate(MODEL_COLOURS.items()):
        vals = [comparison.loc[name, m] for m in metrics]
        offset = (i - (n - 1) / 2) * width
        bars = ax.bar(x + offset, vals, width, color=colour, alpha=0.88,
                      label=name, zorder=3)
        for b, v in zip(bars, vals):
            ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 0.003,
                    f"{v:.3f}", ha="center", va="bottom", fontsize=7.5, color=PRIMARY)

    ax.set_xticks(x)
    ax.set_xticklabels(metrics, fontsize=9)
    ax.set_ylim(0.5, 1.0)
    ax.set_ylabel("Score")
    ax.set_title("Model Comparison — Test Set Performance",
                 fontsize=11, fontweight="bold", color=PRIMARY)
    ax.legend(fontsize=8.5, framealpha=0.9)
    ax.yaxis.grid(True, color=GRID, linewidth=0.6, zorder=0)
    ax.set_facecolor(LIGHT)

    fig.tight_layout()
    _savefig(fig, "fig3_model_comparison.png")


# ── Fig 4: Confusion matrices ─────────────────────────────────────────────────
def fig4_confusion_matrices(fitted_models: dict, X_test, y_test):
    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    cmaps = ["Blues", "Greens", "Oranges"]

    for ax, (name, pipe), cmap in zip(axes, fitted_models.items(), cmaps):
        cm = get_confusion_matrix(pipe, X_test, y_test)
        total = cm.sum()
        im = ax.imshow(cm, cmap=cmap, aspect="auto")

        for i in range(2):
            for j in range(2):
                pct = cm[i, j] / total * 100
                ax.text(j, i, f"{cm[i, j]}\n({pct:.1f}%)",
                        ha="center", va="center", fontsize=10,
                        color="white" if cm[i, j] > cm.max() / 2 else PRIMARY)

        ax.set_xticks([0, 1])
        ax.set_yticks([0, 1])
        ax.set_xticklabels(["Low", "High"])
        ax.set_yticklabels(["Low", "High"])
        ax.set_xlabel("Predicted")
        ax.set_ylabel("Actual")
        ax.set_title(name, fontsize=10, fontweight="bold", color=PRIMARY)
        ax.grid(False)

    fig.suptitle("Confusion Matrices — Test Set",
                 fontsize=12, fontweight="bold", color=PRIMARY, y=1.03)
    fig.tight_layout()
    _savefig(fig, "fig4_confusion_matrices.png")


# ── Fig 5: ROC curves ────────────────────────────────────────────────────────
def fig5_roc_curves(fitted_models: dict, X_test, y_test):
    fig, ax = plt.subplots(figsize=(6, 5))

    ax.plot([0, 1], [0, 1], "k--", linewidth=1, alpha=0.4, label="Random (AUC = 0.50)")

    for name, pipe in fitted_models.items():
        fpr, tpr, auc = get_roc_data(pipe, X_test, y_test)
        colour = MODEL_COLOURS[name]
        ax.plot(fpr, tpr, color=colour, linewidth=2,
                label=f"{name} (AUC = {auc:.3f})")

    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate")
    ax.set_title("ROC Curves — Test Set", fontsize=11, fontweight="bold", color=PRIMARY)
    ax.legend(fontsize=8.5, loc="lower right", framealpha=0.9)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1.02)

    fig.tight_layout()
    _savefig(fig, "fig5_roc_curves.png")


# ── Fig 6: Feature importance (Random Forest) ────────────────────────────────
def fig6_feature_importance(fitted_models: dict):
    rf_pipe = fitted_models["Random Forest"]
    rf = rf_pipe.named_steps["classifier"]

    # Feature names after ColumnTransformer (numeric cols first, then wine_type)
    from src.data import FEATURE_COLS
    from src.features import NUMERIC_COLS, PASSTHROUGH_COLS
    feature_names = NUMERIC_COLS + PASSTHROUGH_COLS

    importances = rf.feature_importances_
    idx = np.argsort(importances)

    fig, ax = plt.subplots(figsize=(7, 5))
    colours = [SECONDARY if imp < np.median(importances) else ACCENT
               for imp in importances[idx]]
    bars = ax.barh(
        [feature_names[i].replace("_", " ") for i in idx],
        importances[idx],
        color=colours, alpha=0.88, zorder=3,
    )

    for b, v in zip(bars, importances[idx]):
        ax.text(v + 0.002, b.get_y() + b.get_height() / 2,
                f"{v:.3f}", va="center", fontsize=7.5, color=PRIMARY)

    ax.set_xlabel("Mean Decrease in Impurity (Gini importance)")
    ax.set_title("Random Forest — Feature Importances",
                 fontsize=11, fontweight="bold", color=PRIMARY)
    ax.xaxis.grid(True, color=GRID, linewidth=0.6, zorder=0)
    ax.yaxis.grid(False)
    ax.set_facecolor(LIGHT)

    fig.tight_layout()
    _savefig(fig, "fig6_feature_importance.png")


def main():
    # Load data
    df = load_raw()
    validate(df)
    X_train, X_test, y_train, y_test = prepare(df)

    # Load trained models
    fitted_models = {}
    for name in MODEL_NAMES:
        try:
            fitted_models[name] = load_model(name)
        except FileNotFoundError:
            log.error("Model '%s' not found — run scripts/train.py first.", name)
            sys.exit(1)

    # Load comparison table
    comp_path = TABLE_DIR / "model_comparison.csv"
    if not comp_path.exists():
        log.error("model_comparison.csv not found — run scripts/train.py first.")
        sys.exit(1)
    comparison = pd.read_csv(comp_path, index_col="Model")

    # Generate all figures
    fig1_target_distribution(df)
    fig2_correlation_heatmap(df)
    fig3_model_comparison(comparison)
    fig4_confusion_matrices(fitted_models, X_test, y_test)
    fig5_roc_curves(fitted_models, X_test, y_test)
    fig6_feature_importance(fitted_models)

    log.info("All figures saved to %s", FIG_DIR)


if __name__ == "__main__":
    main()
