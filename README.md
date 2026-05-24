# Jonathan Goedeke — Personal Website & Data Science Portfolio

This repository hosts my personal website and selected applied data science case studies. The site presents work in reproducible data analysis, statistical modelling, machine learning, causal inference, NLP, and public-policy data visualisation.

- Live website: [jonathan-goedeke.de](https://jonathan-goedeke.de)
- Projects: [jonathan-goedeke.de/projects.html](https://jonathan-goedeke.de/projects.html)
- CV: [files/CV\_Jonathan\_Goedeke.pdf](files/CV_Jonathan_Goedeke.pdf)

---

## Repository structure

.
├── index.html                          Homepage
├── projects.html                       Projects overview
├── project-parliamentary-text.html     NLP / text analysis case study
├── project-ml-pipeline.html            Reproducible ML pipeline case study
├── project-causal-policy.html          Causal inference case study
├── project-crime-trends.html           Public PMK data dashboard case study
├── theses.html                         Academic work overview
├── contact.html                        Contact page
├── education-experience.html           Background page
├── essay-cash-transfers.html           Cash transfers & political support essay
├── essay-msc-thesis.html               MSc dissertation summary
├── essay-wellbys.html                  WELLBY / life satisfaction essay
├── essay-dual-process.html             Dual-process model essay
├── essay-philosophy.html               Philosophy of wellbeing essay
├── CNAME                               Custom domain configuration
├── css/
│   ├── styles.css
│   ├── responsive.css
│   ├── accessibility.css
│   └── profile-image-styles.css
├── js/
│   └── main.js
├── images/
│   ├── Profil.png
│   ├── figures/                        Academic essay figures
│   └── projects/                       Project image assets
├── files/
│   ├── CV_Jonathan_Goedeke.pdf
│   ├── MSC_Thesis_Endogeneity_Distribution_Regression.pdf
│   └── [academic papers]
├── projects/
│   ├── parliamentary-text-analysis/    NLP pipeline with scripts, data, outputs
│   ├── ml-pipeline/                    ML workflow with scripts, src, tests, outputs
│   ├── causal-policy-analysis/         Causal inference documentation and figures
│   └── crime-trends-dashboard/         PMK data pipeline with scripts and outputs
├── PROJECTS.md                         Project index for GitHub visitors
├── GITHUB_SETUP_CHECKLIST.md           Manual GitHub configuration steps
└── README.md

---

## Selected case studies

### 1. Political Text Analysis of Parliamentary Speeches

End-to-end NLP pipeline on real Bundestag Plenarprotokoll XML: parsing, German-language preprocessing, TF-IDF feature extraction, NMF topic modelling, and classification evaluation.

- [Website](https://jonathan-goedeke.de/project-parliamentary-text.html)
- [Project folder](projects/parliamentary-text-analysis/)

### 2. Reproducible Machine Learning Pipeline

Supervised-learning workflow on the UCI Wine Quality dataset: data ingestion, preprocessing, leak-free sklearn Pipelines, model comparison, cross-validation, testing, and documentation.

- [Website](https://jonathan-goedeke.de/project-ml-pipeline.html)
- [Project folder](projects/ml-pipeline/)

### 3. Causal Policy Analysis

Research-based case study documenting quasi-experimental analysis using difference-in-differences, regression discontinuity, robustness checks, and careful communication of uncertainty and limitations.

- [Website](https://jonathan-goedeke.de/project-causal-policy.html)
- [Project folder](projects/causal-policy-analysis/)

### 4. Public PMK Data Dashboard

Descriptive analysis of official aggregated PMK statistics (BMI/BKA): dataset construction, checksum validation, and sober visualisation of public administrative data with transparent limitations.

- [Website](https://jonathan-goedeke.de/project-crime-trends.html)
- [Project folder](projects/crime-trends-dashboard/)

---

## Reproducibility

- Each project folder contains a README with an overview, methods, and reproduction instructions.
- Scripts and outputs are documented where applicable.
- Figures and tables are saved in `outputs/figures/` and `outputs/tables/` within each project folder.
- Data source notes are in `data/README.md` within each project folder.
- All projects use only publicly available data; see individual data notes for access instructions.

---

## Data-use notes

The Bundestag and PMK projects use public data sources only. The PMK case study uses official, aggregated statistics and does not involve personal data, scraping of extremist content, operational analysis, or individual profiling.

---

## Local preview

Run:
python3 -m http.server 8000

Then open:
http://localhost:8000
