#!/usr/bin/env python3
"""
build_dataset.py

Loads the raw manually-extracted PMK data CSVs, validates checksums,
standardises variable names, computes derived columns (share, YoY change),
and writes processed CSVs to data/processed/.

Run from the project root:
  python3 scripts/build_dataset.py
"""

import sys
import logging
from pathlib import Path

import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
log = logging.getLogger(__name__)

BASE_DIR   = Path(__file__).parent.parent
RAW_DIR    = BASE_DIR / "data" / "raw"
PROC_DIR   = BASE_DIR / "data" / "processed"
PROC_DIR.mkdir(parents=True, exist_ok=True)

KNOWN_TOTALS = {
    2023: {"offenses": 60028, "violent": 3561},
    2024: {"offenses": 84172, "violent": 4107},
}


def validate_totals(df: pd.DataFrame, year: int, col: str, known: int):
    actual = df.loc[df["year"] == year, col].sum()
    if actual != known:
        log.error("CHECKSUM FAIL year=%d col=%s: expected %d, got %d", year, col, known, actual)
        sys.exit(1)
    log.info("  Checksum OK year=%d %s=%d", year, col, known)


def build_totals():
    log.info("Loading pmk_totals_2023_2024.csv ...")
    df = pd.read_csv(RAW_DIR / "pmk_totals_2023_2024.csv")
    df["yoy_change_pct"] = df["total_offenses"].pct_change() * 100
    df["yoy_violent_change_pct"] = df["violent_offenses"].pct_change() * 100
    out = PROC_DIR / "pmk_totals.csv"
    df.to_csv(out, index=False)
    log.info("  Saved %s", out.name)
    return df


def build_categories():
    log.info("Loading pmk_categories_2023_2024.csv ...")
    df = pd.read_csv(RAW_DIR / "pmk_categories_2023_2024.csv")

    # Validate checksums
    for year, vals in KNOWN_TOTALS.items():
        validate_totals(df, year, "offenses",         vals["offenses"])
        validate_totals(df, year, "violent_offenses", vals["violent"])

    # Compute percentage share within each year
    year_totals = df.groupby("year")["offenses"].transform("sum")
    df["share_pct"] = (df["offenses"] / year_totals * 100).round(2)

    year_totals_v = df.groupby("year")["violent_offenses"].transform("sum")
    df["violent_share_pct"] = (df["violent_offenses"] / year_totals_v * 100).round(2)

    # YoY change per category
    df_sorted = df.sort_values(["category", "year"])
    df_sorted["yoy_offenses_change_pct"] = (
        df_sorted.groupby("category")["offenses"].pct_change() * 100
    ).round(2)
    df_sorted["yoy_violent_change_pct"] = (
        df_sorted.groupby("category")["violent_offenses"].pct_change() * 100
    ).round(2)

    out = PROC_DIR / "pmk_categories.csv"
    df_sorted.to_csv(out, index=False)
    log.info("  Saved %s", out.name)
    return df_sorted


def build_subcategories():
    log.info("Loading pmk_subcategories.csv ...")
    df = pd.read_csv(RAW_DIR / "pmk_subcategories.csv")
    out = PROC_DIR / "pmk_subcategories.csv"
    df.to_csv(out, index=False)
    log.info("  Saved %s", out.name)
    return df


def write_data_dictionary(cats: pd.DataFrame):
    lines = [
        "# Processed Data Dictionary\n",
        "## pmk_categories.csv\n",
        "| Variable | Description |",
        "|----------|-------------|",
    ]
    for col in cats.columns:
        lines.append(f"| `{col}` | {col.replace('_', ' ')} |")
    out = PROC_DIR / "data_dictionary.md"
    out.write_text("\n".join(lines))
    log.info("  Saved %s", out.name)


def main():
    log.info("=== PMK Dashboard: Building processed dataset ===")
    totals = build_totals()
    cats   = build_categories()
    _      = build_subcategories()
    write_data_dictionary(cats)
    log.info("=== Done. Run scripts/make_figures.py next. ===")


if __name__ == "__main__":
    main()
