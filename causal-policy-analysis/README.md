# Causal Policy Analysis with Quasi-Experimental Methods

## Overview

A research-based case study documenting my experience with quasi-experimental methods for causal policy evaluation. The analyses documented here were conducted during MSc studies at the London School of Economics and assessed by academic supervisors and examiners. The page and associated outputs demonstrate a systematic approach to causal identification, assumption testing, robustness analysis, and honest communication of uncertainty.

---

## What this demonstrates

- Defining a precise policy question and identifying the causal estimand before selecting an empirical design
- Applying appropriate quasi-experimental designs (RDD, DiD) to observational data
- Evaluating identification assumptions explicitly: McCrary density test, parallel-trends testing, covariate placebo regressions
- Implementing robustness checks: donut-hole exclusions, bandwidth sensitivity analysis, heterogeneity analysis
- Communicating uncertainty and limitations clearly — including the boundaries of causal claims

---

## Data

**RDD analysis — Uruguay PANES cash transfer programme:**
Source: PANES programme administrative data (restricted)
Access: Used within LSE research context; not publicly distributable
Nature: Household-level eligibility score and political survey outcomes around the programme's means-testing cutoff

**DiD analysis — Victoria COVID-19 lockdown:**
Source: HILDA (Household, Income and Labour Dynamics in Australia) panel
Access: Requires registration with the Melbourne Institute (free for research purposes)
Nature: Longitudinal panel; 215,733 observations, 16,513 individuals, 20 waves

This case study documents the analytical design and related outputs. The illustrative figures in this folder are reproducible from the included Python script. Stata replication code for the underlying analyses exists but cannot be shared alongside restricted datasets.

---

## Methods

| Method | Application |
|--------|-------------|
| Regression Discontinuity Design (RDD) | Effect of Uruguay's PANES cash transfer programme on political support for the incumbent government |
| Difference-in-Differences (DiD) | Impact of Victoria's COVID-19 lockdown on life satisfaction; HILDA panel |
| Propensity Score Matching (PSM) | Pre-processing for DiD; improves covariate balance between treated and control states |
| Local polynomial regression (rdrobust) | Nonparametric RDD estimation with data-driven bandwidth selection |
| Placebo tests and donut-hole checks | Validation of RDD continuity assumption |
| Parallel-trends testing | Validation of DiD identifying assumption |
| Heterogeneity analysis | Distributional effects by life satisfaction quantile |

**Tools:** Stata (primary econometric implementation), R (supplementary analysis and figures), Python (illustrative figures for this documentation), LaTeX (reports and dissertation), Git/GitHub (version control)

---

## Related analyses

**The Effect of Cash Transfers on Political Support (RDD)**
LSE Quantitative Methods, 2024. Grade: 83% (Distinction).
Full 7-step RDD pipeline: visual inspection, McCrary density test, placebo regressions on pre-determined covariates, OLS (linear and polynomial), donut-hole robustness checks, bandwidth sensitivity, local polynomial estimation (rdrobust).
Core finding: approximately 10% causal increase in political support for the incumbent government from Uruguay's PANES programme. Robust across all specifications.

**Distribution Sensitive Policy Analysis using WELLBYs (DiD + PSM)**
MSc Dissertation, LSE Behavioural Science, 2024. Supervised by Dr. Christian Krekel.
DiD on HILDA longitudinal panel (215,733 observations, 16,513 individuals, 20 waves).
Core finding: −0.030 points on life satisfaction scale (95% CI −0.049 to −0.012). Harm concentrated among the worst-off (LS < 4: additional −0.334 points).

---

## Repository structure

causal-policy-analysis/
├── data/
│   └── README.md                         Data access and licensing notes
├── scripts/
│   └── generate_illustrative_figures.py  Reproducible DiD and RDD design diagrams
├── outputs/
│   └── figures/
│       ├── fig1_did_illustrative.png      DiD design diagram (synthetic data)
│       └── fig2_rdd_illustrative.png      RDD design diagram (synthetic data)
└── README.md

---

## Reproducibility

Install dependencies:
pip install matplotlib numpy

Generate illustrative figures (synthetic data, fully reproducible):
python scripts/generate_illustrative_figures.py

Real empirical figures from the underlying analyses are embedded in the academic essay pages on the website (essay-cash-transfers.html and essay-wellbys.html). Stata replication scripts for the RDD and DiD analyses exist; sharing is subject to data access constraints.

---

## Outputs

- `outputs/figures/fig1_did_illustrative.png` — Difference-in-Differences design diagram (synthetic illustrative data)
- `outputs/figures/fig2_rdd_illustrative.png` — Regression Discontinuity design diagram (synthetic illustrative data)

Real empirical figures from both analyses are linked from the project website page.

---

## Limitations

- This is a methodological case study, not a self-contained replication package; the underlying restricted datasets cannot be included.
- Causal conclusions depend on design assumptions (continuity at the RDD cutoff, parallel pre-trends for DiD) that are tested but cannot be proven with certainty.
- The RDD LATE is local to households near the programme eligibility cutoff; it should not be extrapolated to the full population.
- The DiD estimate captures the effect of a specific lockdown in a specific context; external validity to other lockdowns or jurisdictions is limited.

---

## Website

[jonathan-goedeke.de/project-causal-policy.html](https://jonathan-goedeke.de/project-causal-policy.html)
