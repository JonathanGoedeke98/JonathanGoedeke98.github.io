# Selected Data Science Projects

This page summarises selected case studies demonstrating reproducible analysis, machine-learning workflows, causal reasoning, text analysis, and public administrative data visualisation.

---

| Project | What it demonstrates | Tools | Website | Code |
|---|---|---|---|---|
| Political Text Analysis of Parliamentary Speeches | End-to-end NLP pipeline: XML parsing, German text preprocessing, TF-IDF feature extraction, NMF topic modelling, classification evaluation, reproducible figure generation | Python, scikit-learn, lxml, TF-IDF, NMF, matplotlib | [Project page](https://jonathan-goedeke.de/project-parliamentary-text.html) | [projects/parliamentary-text-analysis](projects/parliamentary-text-analysis/) |
| Reproducible Machine Learning Pipeline | Supervised-learning workflow with leak-free sklearn Pipelines, model comparison (LR · RF · GBM), cross-validation, pytest test suite, serialised models, and documented outputs | Python, scikit-learn, pandas, pytest, Makefile | [Project page](https://jonathan-goedeke.de/project-ml-pipeline.html) | [projects/ml-pipeline](projects/ml-pipeline/) |
| Causal Policy Analysis | Quasi-experimental methods: difference-in-differences, regression discontinuity design, robustness checks (placebo, donut-hole, bandwidth sensitivity), uncertainty communication | Stata, R, DiD, RDD, PSM | [Project page](https://jonathan-goedeke.de/project-causal-policy.html) | [projects/causal-policy-analysis](projects/causal-policy-analysis/) |
| Public PMK Data Dashboard | Descriptive analysis of official aggregated PMK statistics: dataset construction from BMI/BKA publications, checksum validation, sober visualisation, transparent limitations, ethical handling of sensitive public data | Python, pandas, matplotlib, public administrative data | [Project page](https://jonathan-goedeke.de/project-crime-trends.html) | [projects/crime-trends-dashboard](projects/crime-trends-dashboard/) |

---

The website provides polished summaries; the project folders provide methods, code, data-source notes, and reproducibility details.
