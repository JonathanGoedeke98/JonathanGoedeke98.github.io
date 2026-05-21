#!/usr/bin/env python3
"""
make_figures.py

Generates four publication-quality figures from the processed PMK dataset.

Figures:
  fig1_pmk_2024_composition.png  — 2024 total PMK offenses by Phänomenbereich
  fig2_pmk_2023_vs_2024.png      — 2023 vs 2024 comparison by category
  fig3_pmk_2024_violent.png      — 2024 violent PMK offenses by category
  fig4_pmk_antisemitic_trend.png — Antisemitic offenses 2022–2024

Run from the project root:
  python3 scripts/make_figures.py
"""

import sys
import logging
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
log = logging.getLogger(__name__)

BASE_DIR = Path(__file__).parent.parent
PROC_DIR = BASE_DIR / "data" / "processed"
FIG_DIR  = BASE_DIR / "outputs" / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

SITE_DIR = BASE_DIR.parent.parent / "images" / "projects" / "crime-trends"
SITE_DIR.mkdir(parents=True, exist_ok=True)

# ── Website palette ────────────────────────────────────────────────────────────
PRIMARY   = "#2d3e50"
SECONDARY = "#3498db"
ACCENT    = "#1abc9c"
LIGHT     = "#f8f9fa"
GRID      = "#e0e0e0"

# Neutral categorical palette for 5 Phänomenbereiche — no political colour coding
CATEGORY_COLOURS = {
    "PMK-rechts":                 "#2d3e50",
    "PMK-sonstige":               "#7f8c8d",
    "PMK-links":                  "#3498db",
    "PMK-auslaendische-Ideologie":"#1abc9c",
    "PMK-religioese-Ideologie":   "#95a5a6",
}

CATEGORY_SHORT = {
    "PMK-rechts":                 "PMK -rechts-",
    "PMK-sonstige":               "PMK -sonstige\nZuordnung-",
    "PMK-links":                  "PMK -links-",
    "PMK-auslaendische-Ideologie":"PMK -ausländische\nIdeologie-",
    "PMK-religioese-Ideologie":   "PMK -religiöse\nIdeologie-",
}

CATEGORY_ORDER = [
    "PMK-rechts",
    "PMK-sonstige",
    "PMK-links",
    "PMK-auslaendische-Ideologie",
    "PMK-religioese-Ideologie",
]

SOURCE_NOTE = "Source: BMI/BKA, Politisch motivierte Kriminalität — Jahresbericht 2024/2023"

plt.rcParams.update({
    "font.family":       "sans-serif",
    "axes.facecolor":    LIGHT,
    "figure.facecolor":  "white",
    "axes.spines.top":   False,
    "axes.spines.right": False,
    "axes.grid":         False,
    "axes.titlesize":    11,
    "axes.labelsize":    9,
    "xtick.labelsize":   8,
    "ytick.labelsize":   8.5,
})

DPI = 150


def savefig(fig, name: str):
    for d in [FIG_DIR, SITE_DIR]:
        path = d / name
        fig.savefig(path, dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    log.info("  Saved %s", name)


# ── Fig 1: 2024 Composition — total offenses ──────────────────────────────────
def fig1_composition_2024(cats: pd.DataFrame):
    df = cats[cats["year"] == 2024].set_index("category")
    df = df.loc[CATEGORY_ORDER]

    fig, ax = plt.subplots(figsize=(9, 4.5))

    colours = [CATEGORY_COLOURS[c] for c in df.index]
    labels  = [CATEGORY_SHORT[c] for c in df.index]

    bars = ax.barh(
        labels[::-1], df["offenses"].values[::-1],
        color=colours[::-1], alpha=0.88, height=0.6, zorder=2,
    )

    ax.xaxis.grid(True, color=GRID, linewidth=0.6, zorder=0)
    ax.set_xlabel("Recorded offenses (Straftaten)", fontsize=9)

    for bar, val, share in zip(bars, df["offenses"].values[::-1], df["share_pct"].values[::-1]):
        ax.text(
            bar.get_width() + 300, bar.get_y() + bar.get_height() / 2,
            f"{val:,}  ({share:.1f}%)",
            va="center", ha="left", fontsize=8, color=PRIMARY,
        )

    ax.set_xlim(0, df["offenses"].max() * 1.28)
    ax.set_title(
        "PMK 2024 — Total Recorded Offenses by Phänomenbereich\n"
        f"Total: 84,172 offenses  |  +40.2% vs. 2023",
        fontsize=10.5, fontweight="bold", color=PRIMARY, pad=10,
    )
    ax.text(0.99, -0.14, SOURCE_NOTE, transform=ax.transAxes,
            fontsize=7, color="#888", ha="right")
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
    ax.set_facecolor(LIGHT)

    fig.tight_layout()
    savefig(fig, "fig1_pmk_2024_composition.png")


# ── Fig 2: 2023 vs 2024 comparison by category ────────────────────────────────
def fig2_comparison(cats: pd.DataFrame):
    df23 = cats[cats["year"] == 2023].set_index("category")["offenses"]
    df24 = cats[cats["year"] == 2024].set_index("category")["offenses"]

    cats_ordered = CATEGORY_ORDER
    labels = [CATEGORY_SHORT[c] for c in cats_ordered]

    x = np.arange(len(cats_ordered))
    width = 0.38

    fig, ax = plt.subplots(figsize=(10, 5))

    bars23 = ax.bar(x - width/2, [df23[c] for c in cats_ordered],
                    width, color=SECONDARY, alpha=0.6, label="2023", zorder=2)
    bars24 = ax.bar(x + width/2, [df24[c] for c in cats_ordered],
                    width, color=PRIMARY, alpha=0.88, label="2024", zorder=2)

    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=8)
    ax.yaxis.grid(True, color=GRID, linewidth=0.6, zorder=0)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{int(v):,}"))
    ax.set_ylabel("Recorded offenses (Straftaten)", fontsize=9)
    ax.set_title(
        "PMK — Offenses by Phänomenbereich: 2023 vs. 2024",
        fontsize=10.5, fontweight="bold", color=PRIMARY, pad=10,
    )
    ax.legend(fontsize=9, framealpha=0.9)

    # Annotate percentage change above 2024 bars
    for bar24, bar23, cat in zip(bars24, bars23, cats_ordered):
        v23 = df23[cat]
        v24 = df24[cat]
        pct = (v24 - v23) / v23 * 100
        ax.text(
            bar24.get_x() + bar24.get_width() / 2,
            bar24.get_height() + 200,
            f"+{pct:.0f}%", ha="center", va="bottom", fontsize=7.5, color=PRIMARY,
        )

    ax.text(0.99, -0.16, SOURCE_NOTE, transform=ax.transAxes,
            fontsize=7, color="#888", ha="right")
    ax.set_facecolor(LIGHT)

    fig.tight_layout()
    savefig(fig, "fig2_pmk_2023_vs_2024.png")


# ── Fig 3: 2024 violent offenses by category ──────────────────────────────────
def fig3_violent_2024(cats: pd.DataFrame):
    df = cats[cats["year"] == 2024].set_index("category")
    df = df.loc[CATEGORY_ORDER]

    fig, ax = plt.subplots(figsize=(9, 4.5))

    colours = [CATEGORY_COLOURS[c] for c in df.index]
    labels  = [CATEGORY_SHORT[c] for c in df.index]

    v_share = (df["violent_offenses"] / df["violent_offenses"].sum() * 100).round(1)

    bars = ax.barh(
        labels[::-1], df["violent_offenses"].values[::-1],
        color=colours[::-1], alpha=0.88, height=0.6, zorder=2,
    )
    ax.xaxis.grid(True, color=GRID, linewidth=0.6, zorder=0)
    ax.set_xlabel("Violent offenses (Gewalttaten)", fontsize=9)

    for bar, val, share in zip(bars, df["violent_offenses"].values[::-1], v_share.values[::-1]):
        ax.text(
            bar.get_width() + 10, bar.get_y() + bar.get_height() / 2,
            f"{val:,}  ({share:.1f}%)",
            va="center", ha="left", fontsize=8, color=PRIMARY,
        )

    ax.set_xlim(0, df["violent_offenses"].max() * 1.32)
    ax.set_title(
        "PMK 2024 — Violent Offenses (Gewalttaten) by Phänomenbereich\n"
        f"Total: 4,107 violent offenses  |  +15.3% vs. 2023",
        fontsize=10.5, fontweight="bold", color=PRIMARY, pad=10,
    )
    ax.text(0.99, -0.14, SOURCE_NOTE, transform=ax.transAxes,
            fontsize=7, color="#888", ha="right")
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
    ax.set_facecolor(LIGHT)

    fig.tight_layout()
    savefig(fig, "fig3_pmk_2024_violent.png")


# ── Fig 4: Antisemitic offenses trend 2022–2024 ───────────────────────────────
def fig4_antisemitic_trend(subs: pd.DataFrame):
    df = subs[subs["subcategory"] == "antisemitic-offenses"].sort_values("year")

    fig, ax = plt.subplots(figsize=(7, 4.5))

    ax.bar(df["year"], df["count"], color=SECONDARY, alpha=0.85, width=0.55, zorder=2)
    ax.yaxis.grid(True, color=GRID, linewidth=0.6, zorder=0)

    for _, row in df.iterrows():
        ax.text(
            row["year"], row["count"] + 80, f"{int(row['count']):,}",
            ha="center", va="bottom", fontsize=9, fontweight="600", color=PRIMARY,
        )

    ax.set_xticks(df["year"].tolist())
    ax.set_xticklabels([str(y) for y in df["year"]])
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{int(v):,}"))
    ax.set_ylabel("Recorded antisemitic offenses", fontsize=9)
    ax.set_ylim(0, df["count"].max() * 1.2)
    ax.set_title(
        "Antisemitic Offenses (Antisemitische Straftaten) — 2022 to 2024\n"
        "Highest recorded level since systematic tracking began",
        fontsize=10.5, fontweight="bold", color=PRIMARY, pad=10,
    )
    ax.text(
        0.99, -0.14,
        "Source: BMI/BKA PMK-Jahresberichte 2022–2024",
        transform=ax.transAxes, fontsize=7, color="#888", ha="right",
    )
    ax.set_facecolor(LIGHT)

    fig.tight_layout()
    savefig(fig, "fig4_pmk_antisemitic_trend.png")


def main():
    log.info("=== PMK Dashboard: Generating figures ===")

    cats = pd.read_csv(PROC_DIR / "pmk_categories.csv")
    subs = pd.read_csv(PROC_DIR / "pmk_subcategories.csv")

    fig1_composition_2024(cats)
    fig2_comparison(cats)
    fig3_violent_2024(cats)
    fig4_antisemitic_trend(subs)

    log.info("=== All figures saved to %s ===", FIG_DIR)


if __name__ == "__main__":
    main()
