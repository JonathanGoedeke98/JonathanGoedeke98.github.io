"""
evaluation.py — Model evaluation, metric computation, and cross-validation.

Generates the model comparison table and records metrics that are used
both for reporting and for figure generation.
"""

import logging
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    roc_curve,
)
from sklearn.model_selection import StratifiedKFold, cross_validate

log = logging.getLogger(__name__)

OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / "tables"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

CV_FOLDS = 5


def evaluate_model(name: str, pipe, X_test, y_test) -> dict:
    """Compute held-out test metrics for a single fitted Pipeline."""
    y_pred  = pipe.predict(X_test)
    y_proba = pipe.predict_proba(X_test)[:, 1]

    metrics = {
        "Model":     name,
        "Accuracy":  accuracy_score(y_test, y_pred),
        "Precision": precision_score(y_test, y_pred, zero_division=0),
        "Recall":    recall_score(y_test, y_pred, zero_division=0),
        "F1":        f1_score(y_test, y_pred, zero_division=0),
        "ROC-AUC":   roc_auc_score(y_test, y_proba),
    }
    log.info(
        "%s — Acc: %.3f | F1: %.3f | AUC: %.3f",
        name, metrics["Accuracy"], metrics["F1"], metrics["ROC-AUC"],
    )
    return metrics


def cross_validate_model(name: str, pipe, X_train, y_train) -> dict:
    """Run stratified k-fold CV and return mean ± std for key metrics."""
    cv = StratifiedKFold(n_splits=CV_FOLDS, shuffle=True, random_state=42)
    scoring = ["accuracy", "f1", "roc_auc"]
    results = cross_validate(pipe, X_train, y_train, cv=cv, scoring=scoring, n_jobs=-1)

    summary = {}
    for metric in scoring:
        key = f"test_{metric}"
        summary[f"CV_{metric}_mean"] = results[key].mean()
        summary[f"CV_{metric}_std"]  = results[key].std()

    log.info(
        "%s — CV accuracy: %.3f ± %.3f | CV F1: %.3f ± %.3f | CV AUC: %.3f ± %.3f",
        name,
        summary["CV_accuracy_mean"], summary["CV_accuracy_std"],
        summary["CV_f1_mean"],       summary["CV_f1_std"],
        summary["CV_roc_auc_mean"],  summary["CV_roc_auc_std"],
    )
    return summary


def run_all_evaluations(
    fitted_models: dict,
    X_train, y_train,
    X_test,  y_test,
) -> pd.DataFrame:
    """Evaluate all models and return a combined comparison DataFrame."""
    rows = []
    for name, pipe in fitted_models.items():
        test_metrics = evaluate_model(name, pipe, X_test, y_test)
        cv_metrics   = cross_validate_model(name, pipe, X_train, y_train)
        rows.append({**test_metrics, **cv_metrics})

    comparison = pd.DataFrame(rows).set_index("Model")
    out_path = OUTPUT_DIR / "model_comparison.csv"
    comparison.to_csv(out_path)
    log.info("Model comparison saved to %s", out_path)
    return comparison


def get_confusion_matrix(pipe, X_test, y_test) -> np.ndarray:
    return confusion_matrix(y_test, pipe.predict(X_test))


def get_roc_data(pipe, X_test, y_test) -> tuple:
    proba = pipe.predict_proba(X_test)[:, 1]
    fpr, tpr, _ = roc_curve(y_test, proba)
    auc = roc_auc_score(y_test, proba)
    return fpr, tpr, auc
