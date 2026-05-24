# Trends in Politically Motivated Crime: Public Data Dashboard

## Overview

A reproducible descriptive analysis of Germany's official PMK (Politisch motivierte Kriminalität) aggregate statistics, published annually by BMI and BKA. The case study covers dataset construction from official publications, checksum validation against published totals, and clean, sober visualisation of publicly available administrative data.

This is a descriptive analysis only. No causal claims, no forecasting, no individual-level inference.

---

## What this demonstrates

- Careful sourcing and documentation of official aggregate statistics from government publications
- Manual data extraction with full source attribution and cross-verification
- Checksum validation: category totals confirmed to match published overall totals exactly
- Clean, honest visualisation of public administrative data with explicit caveats
- Ethical handling of sensitive public data: aggregated, anonymised, official figures only

---

## Data

All data comes from official BMI and BKA publications:

| Source | Year(s) | URL |
|--------|---------|-----|
| BMI/BKA PMK-Jahresbericht 2024 | 2024 | https://www.bmi.bund.de/SharedDocs/pressemitteilungen/DE/2025/05/pmk2024.html |
| BMI/BKA PMK-Jahresbericht 2023 | 2023 | https://www.bmi.bund.de/SharedDocs/pressemitteilungen/DE/2024/05/pmk2023.html |
| BKA PMK-Jahresbericht 2022 | 2022 | https://www.bka.de/DE/UnsereAufgaben/Deliktsbereiche/PMK/PMKZahlen2022/PMKZahlen2022_node.html |

Data was manually transcribed from official publications; automated access is blocked by server-side restrictions. All figures were cross-verified across at least two independent sources. Checksums confirm that category totals match published overall totals exactly.

**2024 headline figures (official BMI/BKA):**
- 84,172 politically motivated offenses recorded
- 4,107 violent offenses
- 20,074 offenses via internet

---

## Methods

- Manual extraction from official publications with source citation for every data point
- Cross-verification across independent official sources
- Checksum validation against published headline totals
- Year-over-year comparisons at category level
- Descriptive visualisation with honest labelling and explicit limitation notes

---

## Repository structure

crime-trends-dashboard/
├── data/
│   ├── README.md                         Variable documentation and comparability notes
│   ├── raw/
│   │   ├── pmk_totals_2023_2024.csv      Annual headline totals (2023–2024)
│   │   ├── pmk_categories_2023_2024.csv  Breakdown by Phänomenbereich (2023–2024)
│   │   └── pmk_subcategories.csv         Antisemitic offenses 2022–2024 and subcategories
│   └── processed/
│       ├── pmk_totals.csv                Cleaned totals with YoY change columns
│       ├── pmk_categories.csv            Cleaned categories with shares and YoY changes
│       ├── pmk_subcategories.csv         Cleaned subcategory data
│       └── data_dictionary.md            Full variable descriptions
├── scripts/
│   ├── build_dataset.py                  Dataset construction and validation
│   └── make_figures.py                   Figure generation
├── outputs/
│   └── figures/                          Four PNG figures
├── Makefile
├── requirements.txt
└── README.md

---

## Reproducibility

Install dependencies:
pip install -r requirements.txt

Build dataset and validate checksums:
python3 scripts/build_dataset.py

Generate figures:
python3 scripts/make_figures.py

Or use make:
make all

Note: the raw data files in data/raw/ are included in the repository (manually transcribed from official publications). No external download is required.

---

## Outputs

- `outputs/figures/fig1_pmk_2024_composition.png` — 2024 total offenses by Phänomenbereich
- `outputs/figures/fig2_pmk_2023_vs_2024.png` — Year-over-year comparison by category
- `outputs/figures/fig3_pmk_2024_violent.png` — 2024 violent offenses by category
- `outputs/figures/fig4_pmk_antisemitic_trend.png` — Antisemitic offenses 2022–2024

---

## Limitations

1. PMK statistics measure police-recorded offenses, not underlying crime prevalence. Changes may reflect reporting behaviour, enforcement priorities, or classification changes that cannot be disentangled from aggregate totals alone.
2. The Phänomenbereich classification has evolved; cross-year comparisons require checking for definitional continuity.
3. PMK -sonstige Zuordnung- (approximately 26% of 2024 total) is a residual category that limits interpretation of the breakdown.
4. The dataset covers 2023–2024 at category level and 2022–2024 for antisemitic offenses. It is not a long-run time series.
5. The analysis is purely descriptive. No causal interpretation is made or implied.

---

## Ethical note

This case study uses only publicly available, aggregated official statistics published by German federal authorities. It does not involve personal data, operational intelligence, scraping of extremist content, or identification of individuals or groups. The aim is to demonstrate careful statistical analysis and transparent visualisation of public administrative data.

---

## Website

[jonathan-goedeke.de/project-crime-trends.html](https://jonathan-goedeke.de/project-crime-trends.html)
