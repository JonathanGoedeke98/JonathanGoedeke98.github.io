#!/usr/bin/env python3
"""
train.py — Full training pipeline.

Loads data, validates, splits, trains all models, runs evaluation,
saves the model comparison table.

Usage:
  python scripts/train.py
"""

import sys
import logging
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

BASE_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(BASE_DIR))

from src.data import load_raw, validate, prepare
from src.modeling import train_all
from src.evaluation import run_all_evaluations


def main():
    log.info("=== ML Pipeline: Training ===")

    # ── 1. Load and validate ──────────────────────────────────────────────────
    df = load_raw()
    validate(df)

    # ── 2. Prepare split ─────────────────────────────────────────────────────
    X_train, X_test, y_train, y_test = prepare(df)

    # ── 3. Train all models ───────────────────────────────────────────────────
    fitted = train_all(X_train, y_train)

    # ── 4. Evaluate ───────────────────────────────────────────────────────────
    comparison = run_all_evaluations(fitted, X_train, y_train, X_test, y_test)
    log.info("\n%s", comparison[["Accuracy", "F1", "ROC-AUC"]].round(3).to_string())

    log.info("=== Training complete. Run scripts/visualise.py to generate figures. ===")
    return fitted, X_test, y_test


if __name__ == "__main__":
    main()
