"""
make_figures.py — Generate figures for the BfV Verfassungsschutzbericht project.

Figures:
  Fig 1: Rechtsextremismus Personalpotenzial trend 2021-2024 (bar chart)
  Fig 2: Personalpotenzial by category 2024 (horizontal bar chart)
  Fig 3: Straftaten mit extremistischem Hintergrund 2022-2024 (bar chart)

All values are from official BfV press releases; provenance in vsb_personalpotenzial.csv
and vsb_straftaten.csv. Run validate_bfv.py first.
"""

import csv
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

DATA_DIR = Path(__file__).parent.parent / "data" / "raw"
OUT_DIR = Path(__file__).parent.parent.parent.parent / "images" / "projects" / "bfv-reports"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Style
BLUE = "#2c3e50"
LIGHT_BLUE = "#3498db"
ACCENT = "#e74c3c"
GRAY = "#95a5a6"
BG = "#ffffff"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.facecolor": BG,
    "figure.facecolor": BG,
    "axes.labelsize": 9,
    "xtick.labelsize": 8.5,
    "ytick.labelsize": 8.5,
})

# Load data
pp_rows = list(csv.DictReader(open(DATA_DIR / "vsb_personalpotenzial.csv", encoding="utf-8")))
st_rows = list(csv.DictReader(open(DATA_DIR / "vsb_straftaten.csv", encoding="utf-8")))

# ─────────────────────────────────────────────────────────────────────────────
# Figure 1: Rechtsextremismus Personalpotenzial 2021–2024
# ─────────────────────────────────────────────────────────────────────────────
rechts_pp = {int(r["observation_year"]): int(r["personalpotenzial"])
             for r in pp_rows if r["category"] == "Rechtsextremismus"}
rechts_gw = {int(r["observation_year"]): int(r["gewaltorientiert"])
             for r in pp_rows if r["category"] == "Rechtsextremismus" and r.get("gewaltorientiert")}

years = sorted(rechts_pp.keys())
vals = [rechts_pp[y] for y in years]
gw_vals = [rechts_gw.get(y, 0) for y in years]

fig, ax = plt.subplots(figsize=(7, 4))
bars = ax.bar(years, vals, color=[BLUE if y < 2024 else ACCENT for y in years],
              width=0.55, zorder=3, label="Gesamt-Personalpotenzial")
ax.bar(years, gw_vals, color=[LIGHT_BLUE if y < 2024 else "#c0392b" for y in years],
       width=0.55, alpha=0.7, zorder=4, label="davon: gewaltorientiert")

for bar, v in zip(bars, vals):
    ax.text(bar.get_x() + bar.get_width() / 2, v + 400, f"{v:,}".replace(",", "."),
            ha="center", va="bottom", fontsize=8.5, color=BLUE, fontweight="bold")

ax.set_xlabel("Jahr", fontsize=9)
ax.set_ylabel("Personalpotenzial (Schätzung BfV)", fontsize=9)
ax.set_title("Rechtsextremismus: Personalpotenzial 2021–2024\n"
             "Quelle: BfV Verfassungsschutzberichte 2022–2024 (Pressemitteilungen)",
             fontsize=9.5, fontweight="bold", pad=10)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}".replace(",", ".")))
ax.set_ylim(0, 60000)
ax.set_xticks(years)
ax.legend(fontsize=8, frameon=False)
ax.grid(axis="y", linestyle="--", alpha=0.35, zorder=0)

note = ("Hinweis: Personalpotenzial = BfV-Schätzung des Gesamtpersonals (Überschneidungen bereinigt).\n"
        "Vorjahreswerte 2021 aus VSB 2022 Pressemitteilung (kein eigenständig abgerufener VSB 2021).")
fig.text(0.5, -0.04, note, ha="center", fontsize=7.5, color="#666", wrap=True)

plt.tight_layout()
out = OUT_DIR / "fig1_rechtsextremismus_pp_trend.png"
plt.savefig(out, dpi=150, bbox_inches="tight")
plt.close()
print(f"Saved: {out}")

# ─────────────────────────────────────────────────────────────────────────────
# Figure 2: Personalpotenzial by category, 2024
# ─────────────────────────────────────────────────────────────────────────────
CATEGORY_LABELS = {
    "Rechtsextremismus": "Rechtsextremismus",
    "Auslandsbezogener_Extremismus": "Auslandsbez. Extremismus",
    "Linksextremismus": "Linksextremismus",
    "Islamismus": "Islamismus",
    "Reichsbuerger_Selbstverwalter": "Reichsbürger /\nSelbstverwalter",
}
pp_2024 = {r["category"]: int(r["personalpotenzial"])
           for r in pp_rows if int(r["observation_year"]) == 2024}
cats_ordered = ["Rechtsextremismus", "Auslandsbezogener_Extremismus",
                "Linksextremismus", "Islamismus", "Reichsbuerger_Selbstverwalter"]
labels = [CATEGORY_LABELS[c] for c in cats_ordered]
values_2024 = [pp_2024.get(c, 0) for c in cats_ordered]

fig, ax = plt.subplots(figsize=(7, 4))
colors = [ACCENT if c == "Rechtsextremismus" else BLUE for c in cats_ordered]
hbars = ax.barh(range(len(cats_ordered)), values_2024, color=colors,
                height=0.6, zorder=3)
ax.set_yticks(range(len(cats_ordered)))
ax.set_yticklabels(labels, fontsize=8.5)
ax.invert_yaxis()
ax.set_xlabel("Personalpotenzial (Schätzung BfV, 2024)", fontsize=9)
ax.set_title("BfV Personalpotenzial nach Phänomenbereich, 2024\n"
             "Quelle: BfV VSB 2024 Pressemitteilung (2025-06-10)",
             fontsize=9.5, fontweight="bold", pad=10)
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}".replace(",", ".")))
ax.set_xlim(0, 58000)

for bar, v in zip(hbars, values_2024):
    ax.text(v + 400, bar.get_y() + bar.get_height() / 2,
            f"{v:,}".replace(",", "."), va="center", fontsize=8.5, color=BLUE, fontweight="bold")

ax.grid(axis="x", linestyle="--", alpha=0.35, zorder=0)
note = "Hinweis: Kategorien sind nicht addierbar — ein Individuum kann mehreren Kategorien zugeordnet sein."
fig.text(0.5, -0.03, note, ha="center", fontsize=7.5, color="#666")

plt.tight_layout()
out = OUT_DIR / "fig2_personalpotenzial_2024.png"
plt.savefig(out, dpi=150, bbox_inches="tight")
plt.close()
print(f"Saved: {out}")

# ─────────────────────────────────────────────────────────────────────────────
# Figure 3: Straftaten mit extremistischem Hintergrund 2022–2024
# ─────────────────────────────────────────────────────────────────────────────
st_gesamt = {int(r["observation_year"]): int(r["value"])
             for r in st_rows if r["indicator"] == "straftaten_gesamt_extremismus"}
st_gw = {int(r["observation_year"]): int(r["value"])
         for r in st_rows if r["indicator"] == "gewalttaten_gesamt_extremismus"}

years_st = sorted(st_gesamt.keys())
vals_st = [st_gesamt[y] for y in years_st]
vals_gw = [st_gw.get(y, 0) for y in years_st]

fig, ax = plt.subplots(figsize=(7, 4))
bar_colors = [BLUE, BLUE, ACCENT][:len(years_st)]
bars = ax.bar(years_st, vals_st, color=bar_colors, width=0.55, zorder=3,
              label="Straftaten gesamt")
ax.bar(years_st, vals_gw, color=[LIGHT_BLUE, LIGHT_BLUE, "#c0392b"][:len(years_st)],
       width=0.55, alpha=0.8, zorder=4, label="davon: Gewalttaten")

for bar, v in zip(bars, vals_st):
    ax.text(bar.get_x() + bar.get_width() / 2, v + 400, f"{v:,}".replace(",", "."),
            ha="center", va="bottom", fontsize=8.5, color=BLUE, fontweight="bold")

ax.set_xlabel("Jahr", fontsize=9)
ax.set_ylabel("Erfasste Straftaten (BfV)", fontsize=9)
ax.set_title("Straftaten mit extremistischem Hintergrund 2022–2024\n"
             "Quelle: BfV Verfassungsschutzberichte 2022–2024 (Pressemitteilungen)",
             fontsize=9.5, fontweight="bold", pad=10)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}".replace(",", ".")))
ax.set_ylim(0, 68000)
ax.set_xticks(years_st)
ax.legend(fontsize=8, frameon=False)
ax.grid(axis="y", linestyle="--", alpha=0.35, zorder=0)

note = ("Hinweis: BfV-Straftaten mit extremistischem Hintergrund verwenden eine andere Zählsystematik\n"
        "als die BKA/BMI-PMK-Statistik und sind nicht mit PMK-Daten zu vergleichen.")
fig.text(0.5, -0.05, note, ha="center", fontsize=7.5, color="#666")

plt.tight_layout()
out = OUT_DIR / "fig3_straftaten_trend.png"
plt.savefig(out, dpi=150, bbox_inches="tight")
plt.close()
print(f"Saved: {out}")

print("\nAll figures generated successfully.")
