# Data Documentation

## Overview

All data in this project is manually transcribed from official, publicly available
aggregate publications by the German Federal Ministry of the Interior (BMI) and
the Federal Criminal Police Office (BKA). No personal data is used or collected.

## Data sources

| Source | Period | URL | Accessed |
|--------|--------|-----|----------|
| BMI/BKA PMK-Jahresbericht 2024 (press release) | 2024 | https://www.bmi.bund.de/SharedDocs/pressemitteilungen/DE/2025/05/pmk2024.html | 2025-05-20 |
| BMI/BKA PMK-Jahresbericht 2024 (BKA factsheet) | 2024 | https://www.bka.de/DE/UnsereAufgaben/Deliktsbereiche/PMK/PMKZahlen2024/PMKZahlen2024_node.html | 2025-05-20 |
| BMI/BKA PMK-Jahresbericht 2023 (press release) | 2023 | https://www.bmi.bund.de/SharedDocs/pressemitteilungen/DE/2024/05/pmk2023.html | 2025-05-20 |
| BKA PMK-Jahresbericht 2022 | 2022 | https://www.bka.de/DE/UnsereAufgaben/Deliktsbereiche/PMK/PMKZahlen2022/PMKZahlen2022_node.html | 2025-05-20 |
| bpb.de synthesis article (secondary, cites BMI/BKA) | 2024 | https://www.bpb.de/themen/innere-sicherheit/dossier-innere-sicherheit/577004/politisch-motivierte-kriminalitaet-2024/ | 2025-05-20 |

**Note:** BKA and BMI web servers blocked automated access. Figures were extracted from
the bpb.de synthesis article and web search snippets that quote official BMI/BKA press releases
verbatim. All figures were cross-verified across at least two independent sources.
The checksum verification script confirms that category totals match the published overall totals.

## Files

### `raw/pmk_totals_2023_2024.csv`
Annual headline figures.

| Variable | Type | Description |
|----------|------|-------------|
| `year` | int | Reporting year |
| `total_offenses` | int | Total PMK offenses recorded (Straftaten gesamt) |
| `violent_offenses` | int | Total PMK violent offenses (Gewalttaten gesamt) |
| `internet_offenses` | int | PMK offenses using the internet as means (Tatmittel Internet) |
| `clearance_rate_pct` | int | Police clearance rate in percent (Aufklärungsquote) |
| `source` | str | Full citation of the primary source |
| `source_url` | str | URL to official publication |
| `access_date` | date | Date data was extracted |
| `notes` | str | Derivation notes and caveats |

### `raw/pmk_categories_2023_2024.csv`
Breakdown by Phänomenbereich (phenomenon area) for 2023 and 2024.

| Variable | Type | Description |
|----------|------|-------------|
| `year` | int | Reporting year |
| `category` | str | Machine-readable category identifier |
| `category_label_de` | str | Official German category label |
| `offenses` | int | Total recorded offenses in this category |
| `violent_offenses` | int | Violent offenses (Gewalttaten) in this category |
| `source` | str | Source citation |
| `source_url` | str | URL to source |
| `access_date` | date | Extraction date |
| `notes` | str | Derivation and caveat notes |

### `raw/pmk_subcategories.csv`
Selected subcategory figures (antisemitic offenses trend; hate crime total; islamophobic offenses 2024).

### `processed/pmk_totals.csv`
Cleaned version of totals file (standardised column names, validated checksums).

### `processed/pmk_categories.csv`
Cleaned categories file with computed percentage shares.

## Extraction method

Data was **manually transcribed** from official BMI/BKA publications and their
verbatim citations in authoritative secondary sources. This approach was necessary
because the official government websites (bmi.bund.de, bka.de) block automated access.

Each figure was verified by cross-referencing at least two independent sources and
by checksum: the five Phänomenbereich totals for 2024 sum to exactly 84,172
(total offenses) and 4,107 (violent offenses) as published.

## Limitations and comparability warnings

1. **PMK statistics measure police-recorded offenses, not underlying prevalence.**
   Changes over time may reflect reporting behaviour, enforcement priorities,
   classification practice changes, and actual incident patterns — these effects
   cannot be separated from aggregate totals alone.

2. **Category definitions.** The PMK Phänomenbereich classification has evolved over time.
   Comparisons across periods longer than those covered here require careful checking
   of whether category boundaries changed.

3. **"Sonstige Zuordnung" (other assignment).** A substantial share of offenses —
   22,193 in 2024, 26% of the total — fall in this residual category, limiting
   interpretation of the breakdown.

4. **Internet offenses for 2023** are derived from the 2024 figure and the stated
   29.6% year-on-year increase and are marked accordingly.

5. **PMK-rechts 2023 violent offenses** (1,270) are derived arithmetically: they equal
   the 2023 violent offense total (3,561) minus the sum of the other four confirmed
   sub-categories (916 + 491 + 90 + 794 = 2,291). This is internally consistent
   and also consistent with the stated 17.17% increase to 1,488 in 2024.

6. **This dataset covers only 2023 and 2024 at the category level, and 2022–2024
   for antisemitic offenses.** It does not constitute a long-run time series.
   Longer series require manual compilation from prior BMI/BKA annual reports.
