#!/usr/bin/env python3
"""
download_data.py — Download UCI Wine Quality dataset and prepare combined file.

Dataset:
  UCI Machine Learning Repository — Wine Quality Data Set
  Source:  https://archive.ics.uci.edu/ml/datasets/wine+quality
  Licence: Open / no restrictions stated; commonly used for research and education.
  Citation: P. Cortez, A. Cerdeira, F. Almeida, T. Matos and J. Reis. (2009).
            Modeling wine preferences by data mining from physicochemical properties.
            Decision Support Systems, 47(4), 547–553.

Files downloaded:
  data/raw/winequality-red.csv   (1 599 records, semicolon-separated)
  data/raw/winequality-white.csv (4 898 records, semicolon-separated)
  data/raw/winequality-combined.csv (6 497 records, comma-separated, adds 'wine_type')

Usage:
  python scripts/download_data.py
"""

import sys
import logging
from pathlib import Path
from datetime import date

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
log = logging.getLogger(__name__)

try:
    import requests
    import pandas as pd
except ImportError as e:
    log.error("Missing dependency: %s  — run: pip install -r requirements.txt", e)
    sys.exit(1)

BASE_DIR = Path(__file__).parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

SOURCES = {
    "winequality-red.csv":   "https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv",
    "winequality-white.csv": "https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-white.csv",
}


def download_file(url: str, dest: Path) -> None:
    if dest.exists():
        log.info("Already downloaded: %s", dest.name)
        return
    log.info("Downloading %s ...", url)
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    dest.write_bytes(resp.content)
    log.info("Saved %s (%.1f KB)", dest.name, len(resp.content) / 1024)


def build_combined() -> pd.DataFrame:
    """Load red and white, add wine_type column, combine."""
    red   = pd.read_csv(RAW_DIR / "winequality-red.csv",   sep=";")
    white = pd.read_csv(RAW_DIR / "winequality-white.csv", sep=";")
    red["wine_type"]   = 0   # 0 = red
    white["wine_type"] = 1   # 1 = white
    combined = pd.concat([red, white], ignore_index=True)
    combined.columns = [c.strip().lower().replace(" ", "_") for c in combined.columns]
    return combined


def main():
    # Download source files
    for filename, url in SOURCES.items():
        download_file(url, RAW_DIR / filename)

    # Build and save combined dataset
    combined = build_combined()
    out_path = RAW_DIR / "winequality-combined.csv"
    combined.to_csv(out_path, index=False)
    log.info("Combined dataset: %d rows × %d columns", *combined.shape)
    log.info("Columns: %s", list(combined.columns))
    log.info("Quality distribution:\n%s", combined["quality"].value_counts().sort_index().to_string())
    log.info("Saved combined file to %s", out_path)
    log.info("Access date: %s", date.today())


if __name__ == "__main__":
    main()
