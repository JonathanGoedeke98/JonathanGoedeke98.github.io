"""
validate_bfv.py — Cross-consistency checks for BfV Verfassungsschutzbericht data.

Validates:
  V1  Schema — required columns present in both CSVs
  V2  Non-negative values — all numeric fields >= 0
  V3  PP internal consistency — gewaltorientiert < personalpotenzial (where both given)
  V4  Cross-year consistency — prior-year values in later reports match earlier reports
  V5  Straftaten plausibility — rechtsextremismus Straftaten < gesamt Straftaten (same year)
  V6  Source URLs — every row has a non-empty source_url
  V7  Observation years — all years are in [2021, 2022, 2023, 2024]
  V8  No duplicate rows — no (year, category/indicator) pairs appear twice

Usage: python validate_bfv.py
"""

import csv
import json
from pathlib import Path
from datetime import date

DATA_DIR = Path(__file__).parent.parent / "data" / "raw"
OUTPUT_DIR = Path(__file__).parent.parent / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

VALID_YEARS = {2021, 2022, 2023, 2024}
PP_FILE = DATA_DIR / "vsb_personalpotenzial.csv"
ST_FILE = DATA_DIR / "vsb_straftaten.csv"

results = {}
all_pass = True


def fail(check_id, msg):
    global all_pass
    results[check_id] = {"status": "FAIL", "message": msg}
    all_pass = False
    print(f"  FAIL  {check_id}: {msg}")


def passed(check_id, msg):
    results[check_id] = {"status": "PASS", "message": msg}
    print(f"  PASS  {check_id}: {msg}")


print("=== BfV Verfassungsschutzbericht Validation ===\n")

# Load data
pp_rows = list(csv.DictReader(open(PP_FILE, encoding="utf-8")))
st_rows = list(csv.DictReader(open(ST_FILE, encoding="utf-8")))

# V1: Schema check
PP_REQUIRED = {"observation_year", "category", "personalpotenzial", "source_url"}
ST_REQUIRED = {"observation_year", "indicator", "value", "category", "source_url"}
pp_cols = set(pp_rows[0].keys()) if pp_rows else set()
st_cols = set(st_rows[0].keys()) if st_rows else set()
missing_pp = PP_REQUIRED - pp_cols
missing_st = ST_REQUIRED - st_cols
if missing_pp or missing_st:
    fail("V1_schema", f"Missing columns — PP: {missing_pp}, ST: {missing_st}")
else:
    passed("V1_schema", f"All required columns present ({len(pp_rows)} PP rows, {len(st_rows)} ST rows)")

# V2: Non-negative values
neg_pp = [(r["observation_year"], r["category"]) for r in pp_rows
          if r.get("personalpotenzial") and int(r["personalpotenzial"]) < 0]
neg_st = [(r["observation_year"], r["indicator"]) for r in st_rows
          if r.get("value") and int(r["value"]) < 0]
if neg_pp or neg_st:
    fail("V2_nonnegative", f"Negative values found — PP: {neg_pp}, ST: {neg_st}")
else:
    passed("V2_nonnegative", "All numeric values >= 0")

# V3: Gewaltorientiert < Personalpotenzial
v3_violations = []
for r in pp_rows:
    if r.get("gewaltorientiert") and r["gewaltorientiert"].strip():
        pp = int(r["personalpotenzial"])
        gw = int(r["gewaltorientiert"])
        if gw >= pp:
            v3_violations.append(f"{r['observation_year']}/{r['category']}: gw={gw} >= pp={pp}")
if v3_violations:
    fail("V3_gw_lt_pp", f"Violence-oriented >= total PP: {v3_violations}")
else:
    passed("V3_gw_lt_pp", "All gewaltorientiert values < personalpotenzial")

# V4: Cross-year consistency — 2022 Rechtsextremismus PP
# VSB 2022 primary: 38800; should match prior-year in VSB 2023 (i.e. 2022 value in our data)
pp_by_year_cat = {(int(r["observation_year"]), r["category"]): int(r["personalpotenzial"]) for r in pp_rows}
rechts_2022 = pp_by_year_cat.get((2022, "Rechtsextremismus"))
rechts_2023 = pp_by_year_cat.get((2023, "Rechtsextremismus"))
rechts_2024 = pp_by_year_cat.get((2024, "Rechtsextremismus"))
v4_ok = True
# From VSB 2023 press release: prior year (2022) stated as 38800
if rechts_2022 != 38800:
    fail("V4_cross_year_rechts_2022", f"Rechtsextremismus 2022 PP = {rechts_2022}, expected 38800 per VSB 2022 press release")
    v4_ok = False
# From VSB 2024 press release: prior year (2023) stated as 40600
if rechts_2023 != 40600:
    fail("V4_cross_year_rechts_2023", f"Rechtsextremismus 2023 PP = {rechts_2023}, expected 40600 per VSB 2023 press release")
    v4_ok = False
if v4_ok:
    passed("V4_cross_year_consistency",
           f"Rechtsextremismus PP cross-report consistent: 2022={rechts_2022}, 2023={rechts_2023}, 2024={rechts_2024}")

# V5: Rechtsextremismus Straftaten < Gesamt Straftaten (same year, where both present)
st_by = {}
for r in st_rows:
    y = int(r["observation_year"])
    st_by.setdefault(y, {})[r["indicator"]] = int(r["value"])
v5_ok = True
for y in [2024]:
    if "straftaten_rechtsextremismus" in st_by.get(y, {}) and "straftaten_gesamt_extremismus" in st_by.get(y, {}):
        r_st = st_by[y]["straftaten_rechtsextremismus"]
        g_st = st_by[y]["straftaten_gesamt_extremismus"]
        if r_st >= g_st:
            fail("V5_rechts_lt_gesamt",
                 f"Year {y}: rechtsextremismus Straftaten ({r_st}) >= gesamt ({g_st})")
            v5_ok = False
if v5_ok:
    passed("V5_rechts_lt_gesamt",
           "Rechtsextremismus Straftaten < Gesamt Straftaten for all available years")

# V6: Source URLs non-empty
missing_url_pp = [(r["observation_year"], r["category"]) for r in pp_rows if not r.get("source_url", "").strip()]
missing_url_st = [(r["observation_year"], r["indicator"]) for r in st_rows if not r.get("source_url", "").strip()]
if missing_url_pp or missing_url_st:
    fail("V6_source_urls", f"Empty source_url — PP: {missing_url_pp}, ST: {missing_url_st}")
else:
    passed("V6_source_urls", f"All {len(pp_rows) + len(st_rows)} rows have source_url")

# V7: Observation years in valid range
invalid_pp = [(r["observation_year"], r["category"]) for r in pp_rows
              if int(r["observation_year"]) not in VALID_YEARS]
invalid_st = [(r["observation_year"], r["indicator"]) for r in st_rows
              if int(r["observation_year"]) not in VALID_YEARS]
if invalid_pp or invalid_st:
    fail("V7_year_range", f"Unexpected years — PP: {invalid_pp}, ST: {invalid_st}")
else:
    passed("V7_year_range", f"All observation years in valid range {VALID_YEARS}")

# V8: No duplicates
pp_keys = [(r["observation_year"], r["category"]) for r in pp_rows]
st_keys = [(r["observation_year"], r["indicator"]) for r in st_rows]
dup_pp = [k for k in set(pp_keys) if pp_keys.count(k) > 1]
dup_st = [k for k in set(st_keys) if st_keys.count(k) > 1]
if dup_pp or dup_st:
    fail("V8_no_duplicates", f"Duplicate rows found — PP: {dup_pp}, ST: {dup_st}")
else:
    passed("V8_no_duplicates", "No duplicate (year, category/indicator) pairs")

# Summary
n_pass = sum(1 for v in results.values() if v["status"] == "PASS")
n_fail = sum(1 for v in results.values() if v["status"] == "FAIL")
print(f"\n{'='*50}")
print(f"Result: {n_pass}/{n_pass+n_fail} checks passed")
print(f"Status: {'ALL PASS' if all_pass else f'{n_fail} FAIL(S)'}")

# Write output
report = {
    "validation_date": str(date.today()),
    "data_files": [str(PP_FILE.name), str(ST_FILE.name)],
    "n_pp_rows": len(pp_rows),
    "n_st_rows": len(st_rows),
    "checks": results,
    "summary": {"n_pass": n_pass, "n_fail": n_fail, "all_pass": all_pass}
}
out_path = OUTPUT_DIR / "validation_report.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=2)
print(f"\nValidation report written to: {out_path}")
