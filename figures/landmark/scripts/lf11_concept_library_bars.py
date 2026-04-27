"""LF11 — 20-concept generality, sorted bar chart (§3.6).

Replaces Table tab:concept-library. Each concept is a bar with binary
pole-vs-pole AUC on the y-axis, sorted descending. Tier-coloured:
- AUC >= 0.95: green (full success)
- 0.65 <= AUC < 0.95: amber (working but imperfect)
- AUC < 0.65: red (failure — toxicity at 0.59 is the named failure)

Horizontal threshold lines at 0.95 (full success) and 0.65 (working).
Mean monotonicity |rho| annotated above each bar where present.
"""
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lf_style import apply_lf_style, COLORS, save_dual

OUT = "/ibex/project/c2323/yousef/paper_neurips26_final/figures/landmark"
OUT_PAPER = "/ibex/project/c2323/yousef/EEG_Emotion/figures/landmark"


# Source: reports/r6_concept_library_synthesis.md (binary AUC, |rho|).
# Toxicity row from §3 paper text (Jigsaw, AUC 0.59 — the named failure).
ROWS = [
    ("complexity",        1.000, 0.950),
    ("concreteness",      1.000, 0.800),
    ("decisiveness",      1.000, 0.683),
    ("emotionality",      1.000, 0.750),
    ("envy",              1.000, 0.567),
    ("fear",              1.000, 0.833),
    ("guilt",             1.000, 0.467),
    ("hope",              1.000, 0.533),
    ("optimism",          1.000, 0.500),
    ("shame",             1.000, 0.800),
    ("urgency",           1.000, 0.767),
    ("authoritativeness", 0.984, 0.883),
    ("contempt",          0.984, 0.733),
    ("gratitude",         0.984, 0.783),
    ("pride",             0.984, 0.483),
    ("surprise",          0.984, 0.683),
    ("hostility",         0.953, 0.883),
    ("sarcasm",           0.906, 0.367),
    ("certainty",         0.781, 0.167),
    ("specificity",       0.781, 0.717),
    # Named failure (Jigsaw toxicity)
    ("toxicity (Jigsaw)", 0.590, None),
]


def main():
    apply_lf_style()
    rows = sorted(ROWS, key=lambda r: -r[1])
    labels = [r[0] for r in rows]
    aucs = np.array([r[1] for r in rows])
    rhos = [r[2] for r in rows]
    n = len(rows)

    def color_for(a):
        if a >= 0.95:
            return COLORS["green"]
        if a >= 0.65:
            return COLORS["orange"]
        return COLORS["red"]

    bar_colors = [color_for(a) for a in aucs]

    fig = plt.figure(figsize=(11.4, 5.8))
    gs = fig.add_gridspec(1, 1, left=0.075, right=0.975, bottom=0.32, top=0.81)
    ax = fig.add_subplot(gs[0, 0])

    x = np.arange(n)
    bars = ax.bar(x, aucs, color=bar_colors, edgecolor="black",
                  linewidth=0.7, width=0.78, zorder=3)

    # Threshold lines — labels placed on the LEFT spine in clear space below
    # each line, so they never collide with bar tips on the right side.
    ax.axhline(0.95, color="black", lw=0.8, ls="--", alpha=0.55, zorder=2)
    ax.axhline(0.65, color="black", lw=0.8, ls=":",  alpha=0.55, zorder=2)
    ax.axhline(0.50, color=COLORS["gray"], lw=0.8, ls="-", alpha=0.55, zorder=2)
    ax.text(-0.55, 0.945, "AUC = 0.95", ha="left", va="top",
            fontsize=7.5, color=COLORS["gray"], style="italic")
    ax.text(-0.55, 0.645, "AUC = 0.65", ha="left", va="top",
            fontsize=7.5, color=COLORS["gray"], style="italic")
    ax.text(-0.55, 0.495, "chance = 0.50", ha="left", va="top",
            fontsize=7.0, color=COLORS["gray"], style="italic")

    # Annotate AUC value on top of each bar
    for xi, a in zip(x, aucs):
        ax.text(xi, a + 0.01, f"{a:.2f}", ha="center", va="bottom",
                fontsize=7.0, color="black")

    # Annotate monotonicity |rho| inside the bar
    for xi, a, r in zip(x, aucs, rhos):
        if r is None:
            continue
        ax.text(xi, max(a - 0.05, 0.05), fr"$|\rho|{{=}}{r:.2f}$",
                ha="center", va="top", fontsize=7.0, color="white",
                rotation=90)

    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=55, ha="right", fontsize=8.5)
    ax.set_ylim(0.40, 1.06)
    ax.set_ylabel("Binary AUC (pole vs pole)", fontsize=10.5)
    ax.set_xlim(-0.7, n - 0.3)

    # Hero stat box — placed at the TOP centred above the bars, in the
    # cleared space (top=0.81 leaves ~0.19 of figure for title/subtitle/box).
    fig.text(0.5, 0.86,
            f"17 / 20 concepts at AUC $\\geq$ 0.95   |   "
            f"11 / 20 perfect (AUC = 1.00)   |   "
            f"20 / 20 working (AUC $\\geq$ 0.65)   |   "
            f"1 named failure: toxicity",
            ha="center", va="center",
            fontsize=8.8, color="black",
            bbox=dict(facecolor="white", edgecolor=COLORS["lightgray"],
                      pad=5, boxstyle="round,pad=0.30"))

    legend_elems = [
        Patch(facecolor=COLORS["green"],  edgecolor="black",
              label=r"AUC $\geq$ 0.95 (full success)"),
        Patch(facecolor=COLORS["orange"], edgecolor="black",
              label=r"0.65 $\leq$ AUC $<$ 0.95 (working)"),
        Patch(facecolor=COLORS["red"],    edgecolor="black",
              label=r"AUC $<$ 0.65 (failure)"),
    ]
    ax.legend(handles=legend_elems, loc="lower left",
              fontsize=8, frameon=False, ncol=1, bbox_to_anchor=(0.005, 0.005))

    fig.text(0.075, 0.965,
             "The 9-story V-axis recipe is concept-generic across 20 unrelated dimensions",
             fontsize=12, fontweight="bold", ha="left")
    fig.text(0.075, 0.93,
             "Binary pole-vs-pole AUC, sorted; coloured by tier. Toxicity (Jigsaw) is the only substantive failure.",
             fontsize=9.5, ha="left", color=COLORS["gray"])

    fig.text(0.5, 0.015,
             "Source: reports/r6_concept_library_synthesis.md (Qwen3.5-1.7B, layer 27).  "
             r"$|\rho|$ = Spearman monotonicity over 9 ordered classes.",
             ha="center", fontsize=7.5, color=COLORS["gray"])

    save_dual(fig, f"{OUT}/lf11_concept_library_bars")
    save_dual(fig, f"{OUT_PAPER}/lf11_concept_library_bars")


if __name__ == "__main__":
    main()
