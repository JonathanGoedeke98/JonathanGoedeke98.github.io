# Trends in Politically Motivated Crime: Public Data Dashboard

A reproducible descriptive analysis of Germany's official PMK (Politisch motivierte
Kriminalität) aggregate statistics, published annually by BMI and BKA.

**Status:** Initial public-data dashboard complete — dataset built, validated,
and four figures generated from official 2023–2024 data.

---

## Project purpose

Demonstrate careful analysis of public administrative data:

- sourcing and documenting official aggregate statistics,
- transparent data extraction with full source attribution,
- checksum validation against published totals,
- clean, sober visualisation of descriptive findings,
- clear communication of what the data does and does not show.

This is a **descriptive analysis only**. No causal claims, no forecasting,
no individual-level inference, no operational intelligence framing.

---

## Data sources

All data comes from official BMI and BKA publications:

| Source | Year(s) | URL |
|--------|---------|-----|
| BMI/BKA PMK-Jahresbericht 2024 | 2024 | https://www.bmi.bund.de/SharedDocs/pressemitteilungen/DE/2025/05/pmk2024.html |
| BMI/BKA PMK-Jahresbericht 2023 | 2023 | https://www.bmi.bund.de/SharedDocs/pressemitteilungen/DE/2024/05/pmk2023.html |
| BKA PMK-Jahresbericht 2022 | 2022 | https://www.bka.de/DE/UnsereAufgaben/Deliktsbereiche/PMK/PMKZahlen2022/PMKZahlen2022_node.html |

Data was manually transcribed from official publications because the BKA/BMI web
servers block automated access. All figures were cross-verified across at least
two independent sources. Checksums confirm that category totals match published
overall totals exactly.

---

## Headlines (2024, official BMI/BKA figures)

- **84,172** politically motivated offenses recorded in 2024 (+40.2% vs. 2023)
- **4,107** violent offenses (+15.3% vs. 2023)
- **20,074** offenses via internet (≈24% of total)
- Largest single category: PMK -rechts- with 42,788 offenses (50.8% of total)

---

## Dataset structure

| File | Description |
|------|-------------|
| `data/raw/pmk_totals_2023_2024.csv` | Annual headline totals (2023–2024) |
| `data/raw/pmk_categories_2023_2024.csv` | Breakdown by Phänomenbereich (2023–2024) |
| `data/raw/pmk_subcategories.csv` | Antisemitic offenses 2022–2024; hate crime; islamophobic offenses |
| `data/processed/pmk_categories.csv` | Cleaned with computed shares and YoY changes |
| `data/processed/pmk_totals.csv` | Cleaned totals with YoY change columns |

See `data/README.md` for full variable documentation and comparability warnings.

---

## Figures produced

| File | Description |
|------|-------------|
| `outputs/figures/fig1_pmk_2024_composition.png` | 2024 total offenses by Phänomenbereich |
| `outputs/figures/fig2_pmk_2023_vs_2024.png` | 2023 vs. 2024 comparison by category |
| `outputs/figures/fig3_pmk_2024_violent.png` | 2024 violent offenses by category |
| `outputs/figures/fig4_pmk_antisemitic_trend.png` | Antisemitic offenses 2022–2024 |

---

## Reproduction

```bash
pip install -r requirements.txt
make all          # build dataset → generate figures
# or step by step:
python3 scripts/build_dataset.py
python3 scripts/make_figures.py
```

---

## Ethical note

This project uses only publicly available, aggregated official statistics. It does
not involve personal data, operational intelligence, scraping of extremist content,
or identification of individuals or groups. The aim is to demonstrate careful
statistical analysis and transparent visualisation of public administrative data.

---

## Limitations

1. PMK statistics measure police-recorded offenses, not underlying crime prevalence.
   Changes may reflect reporting behaviour, enforcement priorities, or classification
   changes — these cannot be disentangled from aggregate totals alone.
2. Category definitions: the Phänomenbereich classification has evolved; cross-year
   comparisons require checking for definitional continuity.
3. PMK -sonstige Zuordnung- (26% of 2024 total) is a residual category that limits
   interpretation of the breakdown.
4. The dataset covers 2023–2024 at category level (2022–2024 for antisemitic offenses).
   It is not a long-run time series.
5. The analysis is purely descriptive. No causal interpretation is made or implied.

---

## Next steps

- Add prior years (2020–2022) from historical BKA annual reports to extend the time series
- Add Bundesland-level breakdown if consistent state data is publicly available
- Add a data freshness check that warns when the dataset is older than one year
