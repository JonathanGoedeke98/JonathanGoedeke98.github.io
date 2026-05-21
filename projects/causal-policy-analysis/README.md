# Causal Policy Analysis with Quasi-Experimental Methods

A research-based methodological case study documenting my experience with
quasi-experimental methods for causal policy evaluation. The page draws on
completed, peer-assessed analyses conducted during MSc studies at the London
School of Economics.

---

## Purpose

This project demonstrates a systematic approach to causal policy analysis:

1. Define a precise policy question and identify the causal estimand
2. Select an empirical design suited to the available data and the identification challenge
3. Evaluate design assumptions explicitly (rather than assuming them away)
4. Implement robustness and sensitivity checks
5. Communicate uncertainty and limitations honestly

---

## Methods covered

| Method | Application |
|--------|-------------|
| Regression Discontinuity Design (RDD) | Effect of Uruguay's PANES cash transfer programme on political support (LSE, 2024) |
| Difference-in-Differences (DiD) | Impact of Victoria's COVID-19 lockdown on life satisfaction, HILDA panel (LSE Dissertation, 2024) |
| Propensity Score Matching (PSM) | Pre-processing for DiD to improve covariate balance between treated and control states |
| Local polynomial regression (rdrobust) | Nonparametric RDD estimation with data-driven bandwidth selection |
| Placebo tests & donut-hole checks | Validation of RDD continuity assumption |
| Parallel-trends testing | Validation of DiD identifying assumption |
| Heterogeneity analysis | Distributional effects by wellbeing quantile (Prioritarian SWF) |

---

## Related analyses (completed)

### The Effect of Cash Transfers on Political Support (RDD)
- Grade: 83% (Distinction), LSE Quantitative Methods, 2024
- Full 7-step RDD pipeline in Stata: visual inspection, McCrary density test,
  placebo regressions on covariates, OLS (linear + polynomial), donut-hole checks,
  bandwidth sensitivity analysis, local polynomial (rdrobust)
- Core finding: ~10% causal increase in political support for the incumbent
  government from Uruguay's PANES programme. Robust across all specifications.

### Distribution Sensitive Policy Analysis using WELLBYs (DiD + PSM)
- MSc Dissertation, LSE Behavioural Science, 2024. Supervised by Dr. Christian Krekel.
- DiD on HILDA longitudinal panel (215,733 observations, 16,513 individuals, 20 waves)
- First study to causally identify a COVID-19 lockdown's impact on life satisfaction
- Core finding: −0.030 points on life satisfaction scale (95% CI −0.049 to −0.012).
  Harm concentrated among worst-off (LS < 4: additional −0.334 points).

---

## Tools

- **Stata** — primary econometric implementation (RDD, DiD, PSM, robustness)
- **R** — supplementary analysis and figure generation
- **Python** — illustrative methodological figures for this project page
- **LaTeX** — report and dissertation write-up
- **Git/GitHub** — version control

---

## Figures

| File | Description | Data |
|------|-------------|------|
| `outputs/figures/fig1_did_illustrative.png` | Difference-in-Differences design diagram | Synthetic (illustrative only) |
| `outputs/figures/fig2_rdd_illustrative.png` | Regression Discontinuity design diagram | Synthetic (illustrative only) |

Real empirical figures from the underlying analyses are embedded in
`essay-cash-transfers.html` and `essay-wellbys.html`.

---

## Reproducibility status

| Component | Status |
|-----------|--------|
| Illustrative Python figures | Fully reproducible (`scripts/generate_illustrative_figures.py`) |
| RDD analysis (Stata) | Complete pipeline exists; underlying dataset access restricted |
| DiD / PSM analysis (Stata) | Complete pipeline exists; HILDA panel requires registration |

Where underlying research data cannot be shared, this page documents the analytical
design, assumptions, workflow, and communication outputs. Public replication materials
will be added where licensing and data access permit.

---

## Limitations

- This is a methodological case study page, not a replication package.
- Causal conclusions from the underlying analyses depend on design assumptions
  (continuity at the cutoff, parallel trends) that are tested but cannot be proven.
- The RDD LATE is local to households near the eligibility cutoff — it should not be
  extrapolated to the full population.
- The DiD estimate captures the effect of a specific lockdown in a specific context;
  external validity to other lockdowns or countries is limited.

---

## Planned next steps

- Add a public Stata simulation script for the RDD pipeline
- Add event-study plots from the DiD analysis as public illustrative outputs
- Extend to a third case study as additional research is completed
