# Reproducible Machine Learning Pipeline

## Overview

An end-to-end supervised learning workflow on the UCI Wine Quality dataset: data ingestion, preprocessing, leak-free sklearn Pipelines, model comparison, cross-validation, visualisation, testing, and reproducible documentation. The goal is to demonstrate a well-structured, production-minded ML workflow rather than to maximise a performance metric.

---

## What this demonstrates

- Leak-free preprocessing using sklearn Pipelines and ColumnTransformer (all transformers fitted on training data only)
- Structured model comparison across three algorithm families with consistent evaluation
- Cross-validated performance reporting with mean and standard deviation
- Automated test suite covering schema validation, no-leakage property, model fitting, and metric ranges
- Reproducible output: pinned dependencies, fixed random states, serialised models, documented outputs

---

## Data

**UCI Wine Quality Data Set**
Source: https://archive.ics.uci.edu/ml/datasets/wine+quality
Files: winequality-red.csv (1,599 rows) + winequality-white.csv (4,898 rows)
Combined: 6,497 rows × 13 columns (adds `wine_type`: 0 = red, 1 = white)
Features: 11 physicochemical measurements + wine type
Licence: Open; cite Cortez et al. (2009), Decision Support Systems 47(4), 547–553.

Data is downloaded from the UCI ML Repository (publicly accessible, no authentication required). Raw CSV files are excluded from version control; run the download script to fetch them.

**Task:** Binary classification — predict whether a wine is high quality (score ≥ 6) or low quality (score < 6).

| Split | Samples | Class balance |
|-------|---------|---------------|
| Train | 5,197 | 63.3% high |
| Test | 1,300 | 63.3% high |

---

## Methods

| Step | Implementation |
|------|----------------|
| Feature preprocessing | ColumnTransformer: z-score standardisation for numeric features; `wine_type` passed through |
| Pipeline | sklearn Pipeline (preprocessor + estimator); no data leakage across folds |
| Models compared | Logistic Regression, Random Forest, Gradient Boosting |
| Evaluation | 5-fold stratified cross-validation; test-set accuracy, F1, ROC-AUC |
| Testing | pytest (11 smoke tests) |
| Serialisation | Trained pipelines saved as .pkl |

---

## Results

| Model | Accuracy | F1 | ROC-AUC | CV Accuracy |
|---|---|---|---|---|
| Logistic Regression | 0.739 | 0.804 | 0.806 | 0.743 ± 0.010 |
| Random Forest | **0.841** | **0.878** | **0.900** | **0.815 ± 0.008** |
| Gradient Boosting | 0.805 | 0.851 | 0.875 | 0.791 ± 0.010 |

Random Forest achieves the best performance on all metrics.
Top feature importances: alcohol, volatile_acidity, density, sulphates.

---

## Repository structure

ml-pipeline/
├── data/
│   ├── README.md           Data source and licence documentation
│   └── raw/                Downloaded CSVs (excluded from version control)
├── scripts/
│   ├── download_data.py    Data acquisition from UCI repository
│   ├── train.py            Full training and evaluation run
│   └── visualise.py        Figure generation
├── src/
│   ├── data.py             Loading, validation, train/test split
│   ├── features.py         ColumnTransformer preprocessor definition
│   ├── modeling.py         Model definitions and training
│   └── evaluation.py       Metrics and cross-validation
├── tests/
│   └── test_pipeline.py    11 pytest smoke tests
├── outputs/
│   ├── figures/            Six PNG figures
│   └── tables/             model_comparison.csv
├── models/                 Serialised sklearn Pipelines (.pkl)
├── Makefile
├── requirements.txt
└── README.md

---

## Reproducibility

Install dependencies:
pip install -r requirements.txt

Download data:
python3 scripts/download_data.py

Train all models:
python3 scripts/train.py

Generate figures:
python3 scripts/visualise.py

Run tests:
python3 -m pytest tests/ -v

Or use make:
make all

All outputs are written to outputs/tables/model_comparison.csv and outputs/figures/fig1–fig6.png. Trained pipelines are saved to models/.

---

## Outputs

- `outputs/figures/fig1_target_distribution.png` — Class distribution overview
- `outputs/figures/fig2_correlation_heatmap.png` — Feature correlation matrix
- `outputs/figures/fig3_model_comparison.png` — Cross-validated accuracy comparison
- `outputs/figures/fig4_confusion_matrices.png` — Confusion matrices for all three models
- `outputs/figures/fig5_roc_curves.png` — ROC curves with AUC scores
- `outputs/figures/fig6_feature_importance.png` — Random Forest feature importances
- `outputs/tables/model_comparison.csv` — Full metric table

---

## Limitations

- The binary threshold (≥ 6) is chosen for demonstration; a different threshold changes which samples are positive and affects all metric values.
- Gini-based feature importances overestimate the importance of high-cardinality continuous features; permutation importance would be more reliable.
- The dataset has mild class imbalance (63% high quality); threshold tuning or class weighting could improve recall for low-quality wines.
- Models use sensible defaults without hyperparameter search; Bayesian or grid search could improve performance further.

---

## Website

[jonathan-goedeke.de/project-ml-pipeline.html](https://jonathan-goedeke.de/project-ml-pipeline.html)
