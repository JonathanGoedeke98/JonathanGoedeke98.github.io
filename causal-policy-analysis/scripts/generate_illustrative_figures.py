#!/usr/bin/env python3
"""
generate_illustrative_figures.py

Generates two illustrative figures for the causal policy analysis project:
  fig1_did_illustrative.png  — Difference-in-Differences design diagram
  fig2_rdd_illustrative.png  — Regression Discontinuity Design diagram

Both figures use synthetic/simulated data and are clearly labelled as such.
They are methodological illustrations, not empirical findings.
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path

# ── Website palette ────────────────────────────────────────────────────────────
PRIMARY   = "#2d3e50"
SECONDARY = "#3498db"
ACCENT    = "#1abc9c"
LIGHT     = "#f8f9fa"
GRID      = "#e0e0e0"
RED       = "#e74c3c"
ORANGE    = "#e67e22"

plt.rcParams.update({
    "font.family":       "sans-serif",
    "axes.facecolor":    LIGHT,
    "figure.facecolor":  "white",
    "axes.spines.top":   False,
    "axes.spines.right": False,
    "axes.grid":         True,
    "grid.color":        GRID,
    "grid.linewidth":    0.6,
    "axes.titlesize":    11,
    "axes.labelsize":    9,
    "xtick.labelsize":   8,
    "ytick.labelsize":   8,
})

DPI = 150
OUT_DIR = Path(__file__).parent.parent / "outputs" / "figures"
OUT_DIR.mkdir(parents=True, exist_ok=True)

SITE_DIR = Path(__file__).parent.parent.parent.parent / "images" / "projects" / "causal-policy-analysis"
SITE_DIR.mkdir(parents=True, exist_ok=True)


def savefig(fig, name: str):
    for d in [OUT_DIR, SITE_DIR]:
        fig.savefig(d / name, dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Saved {name}")


# ── Fig 1: Difference-in-Differences ──────────────────────────────────────────
def fig1_did():
    rng = np.random.default_rng(42)

    # Time periods: -3, -2, -1 (pre); 1, 2, 3 (post). Treatment at t=0.
    t_pre  = np.array([-3, -2, -1])
    t_post = np.array([1, 2, 3])

    # Treated group: base trend slope + treatment effect post
    treated_pre  = 5.0 + 0.3 * t_pre  + rng.normal(0, 0.08, len(t_pre))
    treated_post = 5.0 + 0.3 * t_post + 1.1 + rng.normal(0, 0.08, len(t_post))

    # Control group: same pre-treatment slope (parallel trends), no jump
    control_pre  = 3.8 + 0.3 * t_pre  + rng.normal(0, 0.08, len(t_pre))
    control_post = 3.8 + 0.3 * t_post + rng.normal(0, 0.08, len(t_post))

    # Counterfactual treated (what treated would look like without treatment)
    cf_post = 5.0 + 0.3 * t_post

    fig, ax = plt.subplots(figsize=(8, 5))

    # Shaded treatment region
    ax.axvspan(0, 3.5, alpha=0.07, color=SECONDARY, zorder=0)
    ax.axvline(0, color=PRIMARY, linewidth=1.2, linestyle="--", alpha=0.6)
    ax.text(0.1, ax.get_ylim()[0] + 0.05 if ax.get_ylim()[0] > 0 else 2.8,
            "Treatment\npoint", fontsize=7.5, color=PRIMARY, alpha=0.7, va="bottom")

    # Plot treated
    ax.plot(t_pre,  treated_pre,  "o-", color=ACCENT,    linewidth=2, markersize=6, label="Treated group", zorder=3)
    ax.plot(t_post, treated_post, "o-", color=ACCENT,    linewidth=2, markersize=6, zorder=3)

    # Plot control
    ax.plot(t_pre,  control_pre,  "s-", color=SECONDARY, linewidth=2, markersize=6, label="Control group", zorder=3)
    ax.plot(t_post, control_post, "s-", color=SECONDARY, linewidth=2, markersize=6, zorder=3)

    # Counterfactual
    ax.plot(t_post, cf_post, "--", color=ACCENT, linewidth=1.5, alpha=0.55, label="Counterfactual (treated, no treatment)")

    # Connect pre to post at t=0 (extrapolation lines from t=-1)
    ax.plot([t_pre[-1], t_post[0]], [treated_pre[-1], treated_post[0]],
            "o-", color=ACCENT, linewidth=2, markersize=0, zorder=3)
    ax.plot([t_pre[-1], t_post[0]], [control_pre[-1], control_post[0]],
            "s-", color=SECONDARY, linewidth=2, markersize=0, zorder=3)
    ax.plot([t_pre[-1], t_post[0]], [treated_pre[-1], cf_post[0]],
            "--", color=ACCENT, linewidth=1.5, alpha=0.55, markersize=0)

    # DiD brace annotation at t=2
    y_treat  = treated_post[1]
    y_cf     = cf_post[1]
    ax.annotate("",
        xy=(2.05, y_treat), xytext=(2.05, y_cf),
        arrowprops=dict(arrowstyle="<->", color=RED, lw=1.5))
    ax.text(2.2, (y_treat + y_cf) / 2, "DiD\nestimate", fontsize=8,
            color=RED, va="center", fontweight="600")

    ax.set_xlabel("Time period (0 = treatment date)", fontsize=9)
    ax.set_ylabel("Outcome variable", fontsize=9)
    ax.set_title("Difference-in-Differences: Design Diagram",
                 fontsize=11, fontweight="bold", color=PRIMARY)
    ax.set_xticks(list(t_pre) + [0] + list(t_post))
    ax.set_xticklabels(["t−3", "t−2", "t−1", "t₀", "t+1", "t+2", "t+3"])
    ax.legend(fontsize=8, framealpha=0.9, loc="upper left")

    # Parallel-trends annotation
    ax.text(-2.9, 4.25, "↕ Parallel pre-treatment trends", fontsize=7.5,
            color="#666", style="italic")

    # Watermark
    ax.text(0.99, 0.01, "Illustrative simulated data", transform=ax.transAxes,
            fontsize=7, color="#aaa", ha="right", va="bottom", style="italic")

    fig.tight_layout()
    savefig(fig, "fig1_did_illustrative.png")


# ── Fig 2: Regression Discontinuity ───────────────────────────────────────────
def fig2_rdd():
    rng = np.random.default_rng(99)
    n = 300

    x = rng.uniform(-1, 1, n)
    # True relationship: linear with a jump at x=0
    treatment = (x < 0).astype(float)
    y = 3.0 + 0.8 * x + 1.2 * treatment + rng.normal(0, 0.25, n)

    fig, ax = plt.subplots(figsize=(8, 5))

    # Scatter: left (treated) and right (control)
    left  = x < 0
    right = x >= 0
    ax.scatter(x[left],  y[left],  color=ACCENT,    alpha=0.45, s=18, zorder=2, label="Treated (below cutoff)")
    ax.scatter(x[right], y[right], color=SECONDARY,  alpha=0.45, s=18, zorder=2, label="Control (above cutoff)")

    # Linear fits on each side
    for mask, colour in [(left, ACCENT), (right, SECONDARY)]:
        xi = x[mask]
        yi = y[mask]
        coef = np.polyfit(xi, yi, 1)
        xfit = np.linspace(xi.min(), xi.max(), 200)
        ax.plot(xfit, np.polyval(coef, xfit), color=colour, linewidth=2.2, zorder=3)

    # Cutoff line
    ax.axvline(0, color=PRIMARY, linewidth=1.4, linestyle="--", alpha=0.7, zorder=4)
    ax.text(0.02, 2.5, "Eligibility\ncutoff", fontsize=8, color=PRIMARY, alpha=0.75)

    # Jump annotation
    y_left_at0  = np.polyval(np.polyfit(x[left],  y[left],  1), 0)
    y_right_at0 = np.polyval(np.polyfit(x[right], y[right], 1), 0)
    ax.annotate("",
        xy=(-0.05, y_left_at0), xytext=(-0.05, y_right_at0),
        arrowprops=dict(arrowstyle="<->", color=RED, lw=1.5))
    ax.text(-0.38, (y_left_at0 + y_right_at0) / 2,
            "Treatment\neffect (LATE)", fontsize=8, color=RED, va="center", fontweight="600")

    ax.set_xlabel("Running variable (centred at cutoff = 0)", fontsize=9)
    ax.set_ylabel("Outcome variable", fontsize=9)
    ax.set_title("Regression Discontinuity Design: Illustration",
                 fontsize=11, fontweight="bold", color=PRIMARY)
    ax.legend(fontsize=8, framealpha=0.9, loc="lower right")

    # Watermark
    ax.text(0.99, 0.01, "Illustrative simulated data", transform=ax.transAxes,
            fontsize=7, color="#aaa", ha="right", va="bottom", style="italic")

    fig.tight_layout()
    savefig(fig, "fig2_rdd_illustrative.png")


if __name__ == "__main__":
    fig1_did()
    fig2_rdd()
    print("Done. Figures saved to outputs/figures/ and images/projects/causal-policy-analysis/")
