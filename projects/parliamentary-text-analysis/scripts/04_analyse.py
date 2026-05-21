#!/usr/bin/env python3
"""
04_analyse.py — TF-IDF feature extraction, NMF topic modelling, and
                optional party-affiliation classification.

Steps:
  A. TF-IDF vectorisation of cleaned speech texts
  B. NMF topic modelling (k topics, configurable)
  C. Top-terms extraction per topic
  D. Document–topic assignment
  E. Optional: logistic regression classifier (party from speech text)

Input:  outputs/tables/corpus_clean.csv
Output:
  outputs/tables/tfidf_top_terms.csv   — top TF-IDF terms per document
  outputs/tables/topic_terms.csv       — top terms per NMF topic
  outputs/tables/doc_topics.csv        — document–topic assignments
  outputs/tables/classification_report.txt (if classification is run)

Usage:
  python scripts/04_analyse.py [--n-topics 5] [--top-n 15] [--classify]
"""

import sys
import logging
import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
log = logging.getLogger(__name__)

BASE_DIR = Path(__file__).parent.parent
INPUT_PATH = BASE_DIR / "outputs" / "tables" / "corpus_clean.csv"
OUTPUT_DIR = BASE_DIR / "outputs" / "tables"


def build_tfidf(texts: pd.Series, max_features: int = 500, min_df: int = 2):
    """Fit a TF-IDF vectoriser and return (matrix, vectoriser, feature_names)."""
    vectoriser = TfidfVectorizer(
        max_features=max_features,
        min_df=min_df,
        max_df=0.95,
        ngram_range=(1, 2),  # unigrams + bigrams
        sublinear_tf=True,   # log-scale TF to compress high-frequency terms
    )
    X = vectoriser.fit_transform(texts)
    feature_names = vectoriser.get_feature_names_out()
    log.info("TF-IDF matrix: %d documents × %d features", X.shape[0], X.shape[1])
    return X, vectoriser, feature_names


def top_tfidf_terms(X, feature_names: np.ndarray, top_n: int = 15) -> pd.DataFrame:
    """Return the top-N TF-IDF terms averaged across all documents."""
    mean_tfidf = np.asarray(X.mean(axis=0)).flatten()
    top_idx = mean_tfidf.argsort()[::-1][:top_n]
    return pd.DataFrame({
        "term": feature_names[top_idx],
        "mean_tfidf": mean_tfidf[top_idx],
    })


def run_nmf(X, feature_names: np.ndarray, n_topics: int = 5, top_n: int = 10):
    """Fit NMF and return (model, doc_topics_df, topic_terms_df)."""
    log.info("Fitting NMF with %d topics...", n_topics)
    nmf = NMF(
        n_components=n_topics,
        init="nndsvda",
        random_state=42,
        max_iter=500,
    )
    W = nmf.fit_transform(X)  # document–topic matrix
    H = nmf.components_        # topic–term matrix

    # Topic–term table
    topic_rows = []
    for t_idx in range(n_topics):
        top_term_idx = H[t_idx].argsort()[::-1][:top_n]
        for rank, term_idx in enumerate(top_term_idx):
            topic_rows.append({
                "topic": f"Topic {t_idx + 1}",
                "rank": rank + 1,
                "term": feature_names[term_idx],
                "weight": H[t_idx, term_idx],
            })
    topic_terms_df = pd.DataFrame(topic_rows)

    # Document–topic table (dominant topic assignment)
    dominant = W.argmax(axis=1)
    doc_topics_df = pd.DataFrame({
        "dominant_topic": [f"Topic {d + 1}" for d in dominant],
        **{f"Topic {t + 1}": W[:, t] for t in range(n_topics)},
    })

    log.info("NMF reconstruction error: %.4f", nmf.reconstruction_err_)
    return nmf, doc_topics_df, topic_terms_df


def run_classification(corpus: pd.DataFrame, X):
    """Train a logistic regression to predict Fraktion from TF-IDF features.

    Only meaningful with at least ~30 documents per class. With small samples
    (fewer than 5 per class) cross-validation scores will be very noisy and are
    reported with appropriate caveats.
    """
    # Normalise encoding variants and drop rows without a party label
    corpus = corpus.copy()
    corpus["fraktion"] = corpus["fraktion"].str.replace("\xa0", " ", regex=False)
    corpus = corpus[corpus["fraktion"].notna() & (corpus["fraktion"].str.strip() != "")]
    # Only keep classes with enough samples for CV
    counts = corpus["fraktion"].value_counts()
    valid_classes = counts[counts >= 3].index
    corpus = corpus[corpus["fraktion"].isin(valid_classes)]
    if corpus.empty:
        log.warning("No valid classes for classification.")
        return None, None
    if hasattr(X, "toarray"):
        X = X[corpus.index]

    le = LabelEncoder()
    y = le.fit_transform(corpus["fraktion"])

    min_class_size = np.bincount(y).min()
    cv_folds = min(5, min_class_size)

    if cv_folds < 2:
        log.warning("Too few samples per class for meaningful cross-validation.")
        return None, None

    clf = LogisticRegression(max_iter=500, C=1.0, solver="lbfgs")
    cv = StratifiedKFold(n_splits=cv_folds, shuffle=True, random_state=42)
    scores = cross_val_score(clf, X, y, cv=cv, scoring="accuracy")

    log.info("Cross-validated accuracy (%d folds): %.3f ± %.3f",
             cv_folds, scores.mean(), scores.std())
    log.info("Classes: %s", list(le.classes_))

    # Train on full dataset for classification report
    clf.fit(X, y)
    y_pred = clf.predict(X)
    report = classification_report(y, y_pred, target_names=le.classes_)
    log.info("Classification report (training set — for inspection only):\n%s", report)

    return clf, {
        "cv_accuracy_mean": scores.mean(),
        "cv_accuracy_std": scores.std(),
        "cv_folds": cv_folds,
        "classes": list(le.classes_),
        "note": "Small corpus: CV scores are noisy and should not be over-interpreted.",
    }


def main():
    parser = argparse.ArgumentParser(description="TF-IDF + NMF analysis")
    parser.add_argument("--n-topics", type=int, default=5,
                        help="Number of NMF topics (default: 5)")
    parser.add_argument("--top-n", type=int, default=15,
                        help="Top terms to show per topic (default: 15)")
    parser.add_argument("--classify", action="store_true",
                        help="Run Fraktion classification (logistic regression)")
    args = parser.parse_args()

    if not INPUT_PATH.exists():
        log.error("Clean corpus not found. Run 03_preprocess.py first.")
        sys.exit(1)

    corpus = pd.read_csv(INPUT_PATH, encoding="utf-8")
    log.info("Loaded %d speeches", len(corpus))

    # Drop speeches with empty clean text
    corpus = corpus[corpus["clean_text"].notna() & (corpus["clean_text"].str.len() > 20)]
    log.info("Non-empty speeches: %d", len(corpus))

    # ── A. TF-IDF ────────────────────────────────────────────────────────────
    X, vectoriser, feature_names = build_tfidf(corpus["clean_text"])

    top_terms = top_tfidf_terms(X, feature_names, top_n=args.top_n)
    top_terms_path = OUTPUT_DIR / "tfidf_top_terms.csv"
    top_terms.to_csv(top_terms_path, index=False, encoding="utf-8")
    log.info("Top TF-IDF terms saved to %s", top_terms_path)
    log.info("Top 10 terms:\n%s", top_terms.head(10).to_string(index=False))

    # ── B. NMF Topic Modelling ────────────────────────────────────────────────
    nmf_model, doc_topics, topic_terms = run_nmf(
        X, feature_names, n_topics=args.n_topics, top_n=args.top_n
    )

    # Attach topic assignments to corpus
    corpus = corpus.reset_index(drop=True)
    corpus = pd.concat([corpus, doc_topics], axis=1)

    topic_terms_path = OUTPUT_DIR / "topic_terms.csv"
    topic_terms.to_csv(topic_terms_path, index=False, encoding="utf-8")
    log.info("Topic terms saved to %s", topic_terms_path)

    doc_topics_path = OUTPUT_DIR / "doc_topics.csv"
    corpus.to_csv(doc_topics_path, index=False, encoding="utf-8")
    log.info("Document–topic assignments saved to %s", doc_topics_path)

    # Print topic summaries
    for topic_name, group in topic_terms.groupby("topic"):
        terms = ", ".join(group.sort_values("rank")["term"].head(8).tolist())
        log.info("%s: %s", topic_name, terms)

    # ── C. Classification (optional) ─────────────────────────────────────────
    if args.classify:
        clf, report = run_classification(corpus, X)
        if report:
            import json
            rep_path = OUTPUT_DIR / "classification_report.json"
            with open(rep_path, "w", encoding="utf-8") as fh:
                json.dump(report, fh, ensure_ascii=False, indent=2)
            log.info("Classification report saved to %s", rep_path)

    return corpus, topic_terms, top_terms


if __name__ == "__main__":
    main()
