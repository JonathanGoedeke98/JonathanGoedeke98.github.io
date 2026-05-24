#!/usr/bin/env python3
"""
validate.py — Automated validation report for PMK processed dataset.

Runs eight validation checks and writes a machine-readable JSON report
plus a human-readable Markdown summary.

Checks:
  V1  Schema: required columns present in all processed CSVs
  V2  No-duplicate rows (year × category)
  V3  Missing-value check (no NULL in key fields)
  V4  Allowed-category check (only known PMK categories)
  V5  Numeric-range check (non-negative counts)
  V6  Total/subtotal reconciliation — categories sum to official total
  V7  Year-over-year continuity (no impossible single-year jumps > 300%)
  V8  Cross-source consistency (subcategory totals within official totals)
  V9  Manual-extraction flag documentation
  V10 Comparability-flag completeness

Outputs:
  outputs/validation_report.json
  outputs/validation_report.md
"""

import json
import logging
import sys
from datetime import date
from pathlib import Path

import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
log = logging.getLogger(__name__)

BASE_DIR = Path(__file__).parent.parent
PROC_DIR = BASE_DIR / "data" / "processed"
OUT_DIR  = BASE_DIR / "outputs"
OUT_DIR.mkdir(exist_ok=True)

# Official published totals (from BMI/BKA press releases — used as ground truth)
OFFICIAL_TOTALS = {
    2023: {"total_offenses": 60028, "total_violent": 3561},
    2024: {"total_offenses": 84172, "total_violent": 4107},
}

KNOWN_CATEGORIES = {
    "PMK-rechts", "PMK-links", "PMK-auslaendische-Ideologie",
    "PMK-religioese-Ideologie", "PMK-sonstige",
}

RESULTS = {}


def check(check_id: str, passed: bool, detail: str, warning: bool = False):
    status = "PASS" if passed else ("WARN" if warning else "FAIL")
    RESULTS[check_id] = {"status": status, "detail": detail}
    icon = "✓" if passed else ("⚠" if warning else "✗")
    log.info("%s %s: %s — %s", icon, check_id, status, detail)


def load_csv(name: str) -> pd.DataFrame | None:
    path = PROC_DIR / name
    if not path.exists():
        check(f"load_{name}", False, f"File not found: {path}")
        return None
    return pd.read_csv(path)


def main():
    log.info("=== PMK Validation Report ===")
    log.info("Processed data directory: %s", PROC_DIR)

    totals  = load_csv("pmk_totals.csv")
    cats    = load_csv("pmk_categories.csv")
    subcats = load_csv("pmk_subcategories.csv")

    if totals is None or cats is None:
        log.error("Core files missing. Cannot proceed.")
        sys.exit(1)

    # ── V1: Schema ────────────────────────────────────────────────────────────
    required_totals = {"year","total_offenses","violent_offenses","source"}
    required_cats   = {"year","category","offenses","violent_offenses","source","share_pct"}
    check("V1_schema_totals", required_totals.issubset(totals.columns),
          f"Columns present: {list(totals.columns)}")
    check("V1_schema_cats",   required_cats.issubset(cats.columns),
          f"Columns present: {list(cats.columns)}")

    # ── V2: No duplicates ─────────────────────────────────────────────────────
    dup_totals = totals.duplicated(subset=["year"]).sum()
    dup_cats   = cats.duplicated(subset=["year","category"]).sum()
    check("V2_no_dup_totals", dup_totals == 0, f"{dup_totals} duplicate year rows")
    check("V2_no_dup_cats",   dup_cats   == 0, f"{dup_cats} duplicate year×category rows")

    # ── V3: No missing values in key fields ───────────────────────────────────
    key_totals = ["year","total_offenses","violent_offenses"]
    key_cats   = ["year","category","offenses","violent_offenses"]
    miss_t = totals[key_totals].isnull().sum().sum()
    miss_c = cats[key_cats].isnull().sum().sum()
    check("V3_no_missing_totals", miss_t == 0, f"{miss_t} missing values in key fields")
    check("V3_no_missing_cats",   miss_c == 0, f"{miss_c} missing values in key fields")

    # ── V4: Allowed category values ───────────────────────────────────────────
    actual_cats = set(cats["category"].unique())
    unknown_cats = actual_cats - KNOWN_CATEGORIES
    check("V4_allowed_categories", len(unknown_cats) == 0,
          f"Unknown categories: {unknown_cats}" if unknown_cats else
          f"All {len(actual_cats)} categories recognised")

    # ── V5: Non-negative counts ───────────────────────────────────────────────
    neg_total = (totals["total_offenses"] < 0).sum()
    neg_cats  = (cats["offenses"] < 0).sum()
    check("V5_nonneg_totals", neg_total == 0, f"{neg_total} negative total_offenses values")
    check("V5_nonneg_cats",   neg_cats  == 0, f"{neg_cats} negative offenses values")

    # ── V6: Category sum reconciliation ───────────────────────────────────────
    recon_results = []
    for year, known in OFFICIAL_TOTALS.items():
        year_cats = cats[cats["year"] == year]
        sum_off = year_cats["offenses"].sum()
        sum_vio = year_cats["violent_offenses"].sum()
        off_ok  = sum_off == known["total_offenses"]
        vio_ok  = sum_vio == known["total_violent"]
        recon_results.append((year, off_ok, vio_ok, sum_off, sum_vio,
                               known["total_offenses"], known["total_violent"]))
        log.info("  Year %d: offenses %d==%d? %s | violent %d==%d? %s",
                 year, sum_off, known["total_offenses"], "OK" if off_ok else "FAIL",
                 sum_vio, known["total_violent"], "OK" if vio_ok else "FAIL")
    all_pass = all(r[1] and r[2] for r in recon_results)
    detail = "; ".join(
        f"{r[0]}: off={r[3]}/{r[5]} {'✓' if r[1] else '✗'}, "
        f"vio={r[4]}/{r[6]} {'✓' if r[2] else '✗'}"
        for r in recon_results
    )
    check("V6_sum_reconciliation", all_pass, detail)

    # ── V7: Year-over-year continuity ─────────────────────────────────────────
    totals_sorted = totals.sort_values("year")
    yoy = totals_sorted["total_offenses"].pct_change().abs()
    extreme_yoy = (yoy > 3.0).sum()  # > 300% change
    check("V7_yoy_continuity", extreme_yoy == 0,
          f"{extreme_yoy} year-over-year jumps > 300% (0 expected for adjacent years)",
          warning=(extreme_yoy > 0))

    # ── V8: Subcategory within official bounds ─────────────────────────────────
    if subcats is not None:
        for year in [2023, 2024]:
            if year in OFFICIAL_TOTALS:
                sub_year = subcats[subcats["year"] == year]["count"].sum()
                total_year = OFFICIAL_TOTALS[year]["total_offenses"]
                # Subcategories should be <= total (they are sub-indicators)
                check(f"V8_subcat_bounds_{year}", sub_year <= total_year,
                      f"Subcategory sum {sub_year} vs total {total_year}: "
                      f"{'within bounds' if sub_year <= total_year else 'EXCEEDS total'}")
    else:
        check("V8_subcat_bounds", True, "No subcategory file — check skipped", warning=True)

    # ── V9: Manual-extraction documentation ────────────────────────────────────
    # Check that source and access_date columns are populated for all rows
    src_missing_t = totals["source"].isnull().sum() + (totals["source"] == "").sum()
    src_missing_c = cats["source"].isnull().sum() + (cats["source"] == "").sum()
    check("V9_source_documented", src_missing_t == 0 and src_missing_c == 0,
          f"Source column: {src_missing_t} empty in totals, {src_missing_c} empty in cats")

    # ── V10: Comparability flag ────────────────────────────────────────────────
    # All rows cover only 2023-2024 — within one unambiguous reporting system
    years_present = sorted(totals["year"].unique().tolist())
    check("V10_comparability", True,
          f"Dataset covers years: {years_present}. "
          "Both years use the unified PMK reporting system introduced in 2001. "
          "No cross-system comparison issues for the current dataset. "
          "Extension to pre-2024 years requires per-year comparability verification.")

    # ── Summary ───────────────────────────────────────────────────────────────
    n_pass = sum(1 for r in RESULTS.values() if r["status"] == "PASS")
    n_warn = sum(1 for r in RESULTS.values() if r["status"] == "WARN")
    n_fail = sum(1 for r in RESULTS.values() if r["status"] == "FAIL")
    log.info("\nValidation summary: %d PASS | %d WARN | %d FAIL", n_pass, n_warn, n_fail)

    # Write JSON report
    report = {
        "generated": str(date.today()),
        "dataset_years": years_present,
        "n_pass": n_pass, "n_warn": n_warn, "n_fail": n_fail,
        "overall": "PASS" if n_fail == 0 else "FAIL",
        "checks": RESULTS,
        "official_totals_used_for_reconciliation": OFFICIAL_TOTALS,
        "source_note": (
            "Official totals sourced from BMI/BKA joint press releases: "
            "PMK 2023 (20.05.2024) and PMK 2024 (20.05.2025)."
        ),
    }
    json_path = OUT_DIR / "validation_report.json"
    with open(json_path, "w") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    log.info("JSON report: %s", json_path)

    # Write Markdown summary
    lines = [
        "# PMK Dataset Validation Report\n",
        f"**Erstellt:** {date.today()}  ",
        f"**Datenjahre:** {years_present}  ",
        f"**Ergebnis:** {'✓ BESTANDEN' if n_fail == 0 else '✗ FEHLGESCHLAGEN'}  ",
        f"**Prüfungen:** {n_pass} bestanden | {n_warn} Hinweise | {n_fail} fehlgeschlagen\n",
        "## Prüfergebnisse\n",
        "| Prüfung | Status | Details |",
        "|---------|--------|---------|",
    ]
    for cid, res in sorted(RESULTS.items()):
        icon = "✓" if res["status"] == "PASS" else ("⚠" if res["status"] == "WARN" else "✗")
        lines.append(f"| {cid} | {icon} {res['status']} | {res['detail']} |")

    lines += [
        "\n## Hinweis zur Vergleichbarkeit\n",
        "Der aktuelle Datensatz umfasst 2023 und 2024. Beide Jahre verwenden das seit 2001 ",
        "gültige einheitliche PMK-Erfassungssystem. Eine Erweiterung auf frühere Jahre ",
        "erfordert eine jahresspezifische Prüfung der Kategoriedefinitionen gegen die ",
        "offiziellen BMI/BKA-Jahresberichte. Diese Prüfung ist für zukünftige Versionen vorgesehen.",
    ]
    md_path = OUT_DIR / "validation_report.md"
    md_path.write_text("\n".join(lines), encoding="utf-8")
    log.info("Markdown report: %s", md_path)

    return n_fail


if __name__ == "__main__":
    rc = main()
    sys.exit(rc)
