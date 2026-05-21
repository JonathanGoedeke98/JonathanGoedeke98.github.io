# Reproducible Machine Learning Pipeline

An end-to-end supervised learning workflow on the UCI Wine Quality dataset:
data ingestion, preprocessing, leak-free sklearn Pipelines, model comparison,
validation, visualisation, and reproducible documentation.

**Status:** Initial prototype complete — pipeline runs end-to-end with real results.

---

## Task

**Binary classification:** predict whether a wine is high quality (score ≥ 6)
or low quality (score < 6) from 12 physicochemical measurements.

| Split | Samples | Class balance |
|-------|---------|---------------|
| Train | 5 197   | 63.3% high    |
| Test  | 1 300   | 63.3% high    |

---

## Dataset

**UCI Wine Quality Data Set**  
Source: <https://archive.ics.uci.edu/ml/datasets/wine+quality>  
Files: `winequality-red.csv` (1 599 rows) + `winequality-white.csv` (4 898 rows)  
Combined: 6 497 rows × 13 columns (adds `wine_type`: 0 = red, 1 = white)  
Features: 11 physicochemical measurements + wine type  
Licence: Open; cite Cortez et al. (2009), Decision Support Systems 47(4), 547–553.

---

## Results

| Model | Accuracy | F1 | ROC-AUC | CV Accuracy |
|---|---|---|---|---|
| Logistic Regression | 0.739 | 0.804 | 0.806 | 0.743 ± 0.010 |
| Random Forest | **0.841** | **0.878** | **0.900** | **0.815 ± 0.008** |
| Gradient Boosting | 0.805 | 0.851 | 0.875 | 0.791 ± 0.010 |

Random Forest achieves the best performance on all metrics.  
Top feature importances: `alcohol`, `volatile_acidity`, `density`, `sulphates`.

---

## How to reproduce

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Download data
python3 scripts/download_data.py

# 3. Train all models
python3 scripts/train.py

# 4. Generate figures
python3 scripts/visualise.py

# 5. Run tests
python3 -m pytest tests/ -v
```

Or use make:

```bash
make all   # download → train → figures → tests
```

All outputs:
- `outputs/tables/model_comparison.csv` — metric table for all models
- `outputs/figures/fig1–fig6.png`       — six analysis figures
- `models/*.pkl`                         — serialised trained Pipelines

---

## Project structure

```
ml-pipeline/
├── data/
│   ├── README.md           Data source and licence documentation
│   └── raw/                Downloaded CSVs (gitignored)
├── scripts/
│   ├── download_data.py    Data acquisition
│   ├── train.py            Full training + evaluation run
│   └── visualise.py        Figure generation
├── src/
│   ├── data.py             Loading, validation, train/test split
│   ├── features.py         ColumnTransformer preprocessor
│   ├── modeling.py         Model definitions and training
│   └── evaluation.py       Metrics and cross-validation
├── tests/
│   └── test_pipeline.py    11 smoke tests (pytest)
├── outputs/
│   ├── figures/            Six PNG charts
│   └── tables/             model_comparison.csv
├── models/                 Serialised Pipelines (.pkl)
├── Makefile
├── requirements.txt
└── README.md
```

---

## Design notes

- **No data leakage:** all transformers are wrapped in a `Pipeline` with the
  estimator and are fitted only on training data. Cross-validation folds see
  only their training split.
- **ColumnTransformer:** numeric features are z-score standardised; `wine_type`
  (binary 0/1) is passed through unchanged.
- **Reproducibility:** random states are fixed; the download script records the
  access date; models are serialised to disk after training.
- **Tests:** 11 pytest smoke tests cover schema validation, preprocessor shape,
  no-leakage property, model fitting/prediction, and metric ranges.

---

## Limitations

- Binary threshold (≥ 6) is chosen for demonstration; the exact threshold
  changes which samples are positive and affects all metric values.
- Gini-based feature importances overestimate the importance of high-cardinality
  continuous features; permutation importance would be more reliable.
- The dataset contains mild class imbalance (63% high quality); a threshold-
  tuning step or class weighting could improve recall for low-quality wines.
- Models are not hyperparameter-tuned beyond sensible defaults; a grid or
  Bayesian search could improve performance further.

---

## Data note

Data is downloaded from the UCI ML Repository (publicly accessible, no
authentication required). The raw CSV files are excluded from version control
(see `.gitignore`); run `python3 scripts/download_data.py` to fetch them.
