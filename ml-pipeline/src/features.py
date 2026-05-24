"""
features.py — Feature preprocessing using sklearn Pipeline / ColumnTransformer.

All transformers are fit only on training data to prevent leakage.
"""

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer

from src.data import FEATURE_COLS

# wine_type is binary (0/1) — we pass it through without scaling
NUMERIC_COLS  = [c for c in FEATURE_COLS if c != "wine_type"]
PASSTHROUGH_COLS = ["wine_type"]


def build_preprocessor() -> ColumnTransformer:
    """Return an unfitted ColumnTransformer.

    Numeric features are z-score standardised (zero mean, unit variance).
    wine_type is passed through unchanged (it is already 0/1).
    """
    numeric_transformer = Pipeline(steps=[("scaler", StandardScaler())])

    return ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, NUMERIC_COLS),
            ("passthrough", "passthrough", PASSTHROUGH_COLS),
        ],
        remainder="drop",
        verbose_feature_names_out=False,
    )
