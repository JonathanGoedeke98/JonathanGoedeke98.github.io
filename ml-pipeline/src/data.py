"""
data.py — Data loading, validation, and train/test splitting.

All data work happens here: nothing leaks into feature or modelling code.
"""

import logging
from pathlib import Path

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

log = logging.getLogger(__name__)

RAW_FILE = Path(__file__).parent.parent / "data" / "raw" / "winequality-combined.csv"

# Binary target: quality >= 6 → high (1), quality < 6 → low (0)
QUALITY_THRESHOLD = 6

FEATURE_COLS = [
    "fixed_acidity", "volatile_acidity", "citric_acid", "residual_sugar",
    "chlorides", "free_sulfur_dioxide", "total_sulfur_dioxide", "density",
    "ph", "sulphates", "alcohol", "wine_type",
]
TARGET_COL = "quality_binary"


def load_raw(path: Path = RAW_FILE) -> pd.DataFrame:
    """Load the combined wine quality CSV."""
    if not path.exists():
        raise FileNotFoundError(
            f"Raw data not found at {path}. Run: python scripts/download_data.py"
        )
    df = pd.read_csv(path)
    log.info("Loaded %d rows × %d columns from %s", *df.shape, path.name)
    return df


def validate(df: pd.DataFrame) -> None:
    """Basic data quality checks. Raises ValueError on failure."""
    missing = df.isnull().sum()
    if missing.any():
        log.warning("Missing values detected:\n%s", missing[missing > 0])

    for col in FEATURE_COLS[:-1]:   # exclude wine_type which we added
        if col not in df.columns:
            raise ValueError(f"Expected column '{col}' not found. Check the raw file.")

    if "quality" not in df.columns:
        raise ValueError("Column 'quality' not found.")

    q_range = (df["quality"].min(), df["quality"].max())
    log.info("Quality range: %d – %d", *q_range)
    log.info("Data validation passed.")


def make_target(df: pd.DataFrame, threshold: int = QUALITY_THRESHOLD) -> pd.Series:
    """Binary classification target: 1 if quality >= threshold, else 0."""
    return (df["quality"] >= threshold).astype(int)


def prepare(
    df: pd.DataFrame,
    test_size: float = 0.20,
    random_state: int = 42,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """Add binary target, split into train and test sets. No leakage."""
    df = df.copy()
    df[TARGET_COL] = make_target(df)

    X = df[FEATURE_COLS]
    y = df[TARGET_COL]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )

    log.info(
        "Split: %d train / %d test (%.0f%% / %.0f%%) | class balance train: %.1f%% high",
        len(X_train), len(X_test),
        100 * (1 - test_size), 100 * test_size,
        100 * y_train.mean(),
    )
    return X_train, X_test, y_train, y_test
