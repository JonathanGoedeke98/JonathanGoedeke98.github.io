#!/usr/bin/env python3
"""
05_visualise.py — Generate publication-quality figures from the analysis outputs.

Produces:
  fig1_speeches_by_party.png   — bar chart: number of speeches per Fraktion
  fig2_top_tfidf_terms.png     — horizontal bar chart: top corpus-level TF-IDF terms
  fig3_topic_terms.png         — subplot grid: top terms per NMF topic
  fig4_speech_length_dist.png  — box plot: speech length distribution by Fraktion

All figures saved to outputs/figures/.

Usage:
  python scripts/05_visualise.py [--dpi 150]
"""

import sys
import logging
import argparse
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
log = logging.getLogger(__name__)

BASE_DIR = Path(__file__).parent.parent
TABLE_DIR = BASE_DIR / "outputs" / "tables"
FIG_DIR = BASE_DIR / "outputs" / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

# ── Style ────────────────────────────────────────────────────────────────────
PRIMARY   = "#2d3e50"   # matches website --primary-color
SECONDARY = "#3498db"   # matches website --secondary-color
ACCENT    = "#1abc9c"   # matches website --accent-color
LIGHT     = "#f8f9fa"
GRID      = "#e0e0e0"

PARTY_COLOURS = {
    "SPD":                          "#E3000F",
    "CDU/CSU":                      "#1C1C1C",
    "BÜNDNIS 90/DIE GRÜNEN":        "#46962B",
    "Bündnis 90/Die Grünen":        "#46962B",
    "FDP":                          "#FFED00",
    "DIE LINKE":                    "#BE3075",
    "Die Linke":                    "#BE3075",
    "AfD":                          "#009EE0",
}

def party_colour(name: str) -> str:
    for key, colour in PARTY_COLOURS.items():
        if key.lower() in name.lower():
            return colour
    return SECONDARY


def apply_style(ax, title: str = "", xlabel: str = "", ylabel: str = ""):
    ax.set_title(title, fontsize=11, fontweight="bold", color=PRIMARY, pad=10)
    ax.set_xlabel(xlabel, fontsize=9, color=PRIMARY)
    ax.set_ylabel(ylabel, fontsize=9, color=PRIMARY)
    ax.spines[["top", "right"]].set_visible(False)
    ax.tick_params(colors=PRIMARY, labelsize=8)
    ax.grid(axis="y", color=GRID, linewidth=0.6, zorder=0)
    ax.set_facecolor(LIGHT)


def fig1_speeches_by_party(corpus: pd.DataFrame, dpi: int):
    """Bar chart: number of speeches per parliamentary group."""
    counts = corpus["fraktion"].value_counts().sort_values(ascending=False)
    colours = [party_colour(p) for p in counts.index]

    fig, ax = plt.subplots(figsize=(7, 4))
    bars = ax.bar(counts.index, counts.values, color=colours, width=0.6, zorder=3)

    # Value labels on bars
    for bar, val in zip(bars, counts.values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.05,
                str(val), ha="center", va="bottom", fontsize=9, color=PRIMARY)

    ax.set_xticks(range(len(counts)))
    ax.set_xticklabels(
        [p.replace("BÜNDNIS 90/DIE GRÜNEN", "Grünen").replace("DIE LINKE", "Linke")
         for p in counts.index],
        rotation=20, ha="right", fontsize=8
    )
    apply_style(ax, title="Speeches by Parliamentary Group",
                ylabel="Number of Speeches")
    ax.yaxis.grid(True, color=GRID, linewidth=0.6, zorder=0)

    fig.suptitle("Corpus overview — 3 sample sessions (20th Bundestag)",
                 fontsize=9, color="#888", y=1.01)
    fig.tight_layout()
    out = FIG_DIR / "fig1_speeches_by_party.png"
    fig.savefig(out, dpi=dpi, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    log.info("Saved %s", out)


def fig2_top_tfidf_terms(top_terms: pd.DataFrame, dpi: int):
    """Horizontal bar chart: top corpus-level TF-IDF terms."""
    df = top_terms.head(15).sort_values("mean_tfidf")

    fig, ax = plt.subplots(figsize=(7, 5))
    bars = ax.barh(df["term"], df["mean_tfidf"],
                   color=SECONDARY, alpha=0.85, zorder=3)
    ax.set_xlim(0, df["mean_tfidf"].max() * 1.15)

    for bar, val in zip(bars, df["mean_tfidf"]):
        ax.text(val + df["mean_tfidf"].max() * 0.01, bar.get_y() + bar.get_height() / 2,
                f"{val:.3f}", va="center", fontsize=7.5, color=PRIMARY)

    apply_style(ax, title="Top 15 TF-IDF Terms (corpus-level mean)",
                xlabel="Mean TF-IDF score")
    ax.tick_params(axis="y", labelsize=9)
    ax.xaxis.grid(True, color=GRID, linewidth=0.6, zorder=0)
    ax.yaxis.grid(False)
    ax.spines["left"].set_visible(False)

    fig.suptitle("After German stopword removal — unigrams and bigrams",
                 fontsize=9, color="#888", y=1.01)
    fig.tight_layout()
    out = FIG_DIR / "fig2_top_tfidf_terms.png"
    fig.savefig(out, dpi=dpi, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    log.info("Saved %s", out)


def fig3_topic_terms(topic_terms: pd.DataFrame, dpi: int):
    """Subplot grid: top terms per NMF topic."""
    topics = topic_terms["topic"].unique()
    n_topics = len(topics)
    n_cols = min(3, n_topics)
    n_rows = (n_topics + n_cols - 1) // n_cols

    fig, axes = plt.subplots(n_rows, n_cols, figsize=(5 * n_cols, 3.5 * n_rows))
    axes = np.array(axes).flatten()

    cmap = plt.get_cmap("Blues")
    for i, topic in enumerate(topics):
        ax = axes[i]
        df = topic_terms[topic_terms["topic"] == topic].sort_values("weight")
        colours_topic = [cmap(0.4 + 0.5 * w / df["weight"].max()) for w in df["weight"]]
        ax.barh(df["term"], df["weight"], color=colours_topic, zorder=3)
        ax.set_title(topic, fontsize=10, fontweight="bold", color=PRIMARY, pad=6)
        ax.spines[["top", "right", "left"]].set_visible(False)
        ax.tick_params(colors=PRIMARY, labelsize=7.5)
        ax.xaxis.grid(True, color=GRID, linewidth=0.5, zorder=0)
        ax.set_facecolor(LIGHT)
        ax.set_xlabel("NMF weight", fontsize=8, color=PRIMARY)

    # Hide unused subplots
    for j in range(i + 1, len(axes)):
        axes[j].set_visible(False)

    fig.suptitle("NMF Topic Model — Top Terms per Topic",
                 fontsize=12, fontweight="bold", color=PRIMARY, y=1.02)
    fig.tight_layout()
    out = FIG_DIR / "fig3_topic_terms.png"
    fig.savefig(out, dpi=dpi, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    log.info("Saved %s", out)


def fig4_speech_length(corpus: pd.DataFrame, dpi: int):
    """Box plot: speech length distribution by parliamentary group."""
    # Simplify long party names for display
    def short_name(name: str) -> str:
        replacements = {
            "BÜNDNIS 90/DIE GRÜNEN": "Grünen",
            "Bündnis 90/Die Grünen": "Grünen",
            "DIE LINKE": "Linke",
            "Die Linke": "Linke",
            "CDU/CSU": "CDU/CSU",
        }
        for k, v in replacements.items():
            if k in name:
                return v
        return name

    corpus = corpus.copy()
    corpus["party_short"] = corpus["fraktion"].apply(short_name)
    order = corpus.groupby("party_short")["speech_len"].median().sort_values(ascending=False).index

    colours_map = {short_name(k): v for k, v in PARTY_COLOURS.items()}
    palette = [colours_map.get(p, SECONDARY) for p in order]

    fig, ax = plt.subplots(figsize=(8, 4.5))
    sns.boxplot(
        data=corpus, x="party_short", y="speech_len",
        order=order, palette=palette,
        width=0.55, linewidth=1.2,
        flierprops={"marker": "o", "markersize": 3, "alpha": 0.5},
        ax=ax,
    )
    apply_style(ax, title="Speech Length Distribution by Parliamentary Group",
                xlabel="Parliamentary Group", ylabel="Tokens per Speech")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=15, ha="right", fontsize=8.5)

    fig.suptitle("Box plot: median, IQR, and individual outliers",
                 fontsize=9, color="#888", y=1.01)
    fig.tight_layout()
    out = FIG_DIR / "fig4_speech_length_dist.png"
    fig.savefig(out, dpi=dpi, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    log.info("Saved %s", out)


def main():
    parser = argparse.ArgumentParser(description="Generate analysis figures")
    parser.add_argument("--dpi", type=int, default=150, help="Figure DPI (default: 150)")
    args = parser.parse_args()

    # Load required tables
    def require(path: Path, label: str) -> pd.DataFrame:
        if not path.exists():
            log.error("%s not found at %s. Run the preceding scripts first.", label, path)
            sys.exit(1)
        return pd.read_csv(path, encoding="utf-8")

    corpus     = require(TABLE_DIR / "doc_topics.csv",     "Document–topic table")
    top_terms  = require(TABLE_DIR / "tfidf_top_terms.csv", "TF-IDF top terms")
    topic_terms = require(TABLE_DIR / "topic_terms.csv",   "Topic terms")

    # If doc_topics not available, fall back to corpus_raw for figs 1 & 4
    if "fraktion" not in corpus.columns:
        raw = require(TABLE_DIR / "corpus_raw.csv", "Raw corpus")
        corpus = raw

    fig1_speeches_by_party(corpus, dpi=args.dpi)
    fig2_top_tfidf_terms(top_terms, dpi=args.dpi)
    fig3_topic_terms(topic_terms, dpi=args.dpi)
    fig4_speech_length(corpus, dpi=args.dpi)

    log.info("All figures saved to %s", FIG_DIR)


if __name__ == "__main__":
    main()
