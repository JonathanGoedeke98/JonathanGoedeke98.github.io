# Data

## Source

**UCI Machine Learning Repository — Wine Quality Data Set**

- URL: <https://archive.ics.uci.edu/ml/datasets/wine+quality>
- Files: `winequality-red.csv` (1,599 rows) + `winequality-white.csv` (4,898 rows)
- Combined: 6,497 rows × 13 columns (adds `wine_type`: 0 = red, 1 = white)
- Features: 11 physicochemical measurements + `wine_type`
- Target: `quality` (integer 3–9, sensory score from ≥3 expert tasters)

## Licence

Open access. Please cite:

> P. Cortez, A. Cerdeira, F. Almeida, T. Matos, J. Reis.
> Modeling wine preferences by data mining from physicochemical properties.
> *Decision Support Systems* 47(4), 547–553, 2009.

## Download

Run the download script from the project root:

```bash
python3 scripts/download_data.py
```

This fetches both CSVs from the UCI repository, combines them, adds
`wine_type`, and writes `data/raw/winequality-combined.csv`.
The script records the access date in the file's metadata.

## Version control

`data/raw/` is excluded from version control (see `.gitignore`).
The download script is the authoritative source of the raw data.
