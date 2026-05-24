"""
modeling.py — Model definitions and training.

Each model is wrapped in a full sklearn Pipeline (preprocessor + estimator)
so that preprocessing is always applied consistently and cannot leak from
validation folds into training data.
"""

import logging
import pickle
from pathlib import Path

from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier

from src.features import build_preprocessor

log = logging.getLogger(__name__)

MODELS_DIR = Path(__file__).parent.parent / "models"
MODELS_DIR.mkdir(exist_ok=True)

# Model registry: name → (estimator, hyperparameters)
MODEL_CONFIGS = {
    "Logistic Regression": LogisticRegression(
        C=1.0,
        max_iter=1000,
        solver="lbfgs",
        random_state=42,
    ),
    "Random Forest": RandomForestClassifier(
        n_estimators=200,
        max_depth=None,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1,
    ),
    "Gradient Boosting": GradientBoostingClassifier(
        n_estimators=200,
        learning_rate=0.1,
        max_depth=4,
        subsample=0.8,
        random_state=42,
    ),
}


def build_pipeline(estimator) -> Pipeline:
    """Wrap preprocessor + estimator into a single, leak-free Pipeline."""
    return Pipeline(steps=[
        ("preprocessor", build_preprocessor()),
        ("classifier",   estimator),
    ])


def train_all(X_train, y_train) -> dict[str, Pipeline]:
    """Train all models. Returns dict: model_name → fitted Pipeline."""
    fitted = {}
    for name, estimator in MODEL_CONFIGS.items():
        log.info("Training %s ...", name)
        pipe = build_pipeline(estimator)
        pipe.fit(X_train, y_train)
        fitted[name] = pipe

        # Persist to disk
        out_path = MODELS_DIR / f"{name.lower().replace(' ', '_')}.pkl"
        with open(out_path, "wb") as fh:
            pickle.dump(pipe, fh)
        log.info("  Saved to %s", out_path.name)

    return fitted


def load_model(name: str) -> Pipeline:
    """Load a previously saved Pipeline by model name."""
    path = MODELS_DIR / f"{name.lower().replace(' ', '_')}.pkl"
    with open(path, "rb") as fh:
        return pickle.load(fh)
