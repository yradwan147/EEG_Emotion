"""LF7 — Recipe Ablation Cascade Bar Chart (§8 main).

Horizontal bar chart with cumulative Δ from CBraMod 0.572 → 0.6948 SOTA.
Each bar labeled (replication, +aug, +KD, +d6, +e150, ensemble). Color by
phase (replication / recipe / ensemble). Reference lines for prior SOTA
(EmotionKD 0.628, EMOD AAAI 0.6287).
"""
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lf_style import apply_lf_style, COLORS, save_dual, panel_label

OUT = "/ibex/project/c2323/yousef/paper_neurips26_final/figures/landmark"
OUT_PAPER = "/ibex/project/c2323/yousef/EEG_Emotion/figures/landmark"


# (label, BACC, std_or_None, phase)
ROWS = [
    ("CBraMod   (ICLR 2025 prior SOTA)",       0.5720, 0.0060, "prior"),
    ("EMOD vanilla replication  (d3, race-fix)", 0.6194, 0.0040, "replication"),
    ("+ aug  (p=0.6)",                         0.6343, 0.0040, "recipe"),
    ("+ aug + KD  (rand9 9D)",                 0.6467, 0.0070, "recipe"),
    ("+ d6 depth-doubling",                    0.6581, 0.0066, "recipe"),
    ("+ e150 single-ckpt  (val-selected SOTA)",0.6755, None,   "single_sota"),
    ("5-ckpt ensemble  (e100)",                0.6798, None,   "ensemble"),
    ("10-ckpt ensemble  (e100 + e150) — SOTA", 0.6948, None,   "ensemble_sota"),
]

PHASE_COLOR = {
    "prior":          COLORS["prior"],
    "replication":    COLORS["replication"],
    "recipe":         COLORS["recipe"],
    "single_sota":    COLORS["ensemble"],
    "ensemble":       COLORS["ensemble"],
    "ensemble_sota":  COLORS["sota"],
}
PHASE_LABEL = {
    "prior":         "prior SOTA",
    "replication":   "EMOD replication",
    "recipe":        "recipe build-up",
    "single_sota":   "single-model SOTA",
    "ensemble":      "ensemble (interim)",
    "ensemble_sota": "10-ckpt ensemble SOTA",
}


def main():
    apply_lf_style()
    fig = plt.figure(figsize=(13.5, 6.8))
    gs = fig.add_gridspec(1, 1, left=0.30, right=0.78, bottom=0.10, top=0.86)
    ax = fig.add_subplot(gs[0, 0])

    n = len(ROWS)
    y = np.arange(n)[::-1]  # top-down
    baccs = np.array([r[1] for r in ROWS])
    stds  = np.array([r[2] if r[2] is not None else 0 for r in ROWS])
    phases = [r[3] for r in ROWS]
    labels = [r[0] for r in ROWS]
    bar_colors = [PHASE_COLOR[p] for p in phases]

    bars = ax.barh(y, baccs, xerr=stds, color=bar_colors, height=0.66,
                   edgecolor="white", linewidth=0.8,
                   error_kw=dict(elinewidth=1.0, ecolor="black", capsize=3),
                   zorder=3)

    # value labels at right of bars
    for yi, b, s, p in zip(y, baccs, stds, phases):
        weight = "bold" if "sota" in p else "normal"
        fs = 11 if "sota" in p else 10
        ax.text(b + (s if s else 0) + 0.0015, yi, f"{b:.4f}",
                va="center", ha="left", fontsize=fs, fontweight=weight,
                color="black")

    # Δ labels between consecutive bars (showing the gain at each step)
    for i in range(1, n):
        dy = (y[i - 1] + y[i]) / 2
        d = baccs[i] - baccs[i - 1]
        # arrow + delta
        ax.annotate("", xy=(baccs[i], y[i] + 0.32), xytext=(baccs[i - 1], y[i - 1] - 0.32),
                    arrowprops=dict(arrowstyle="->", color=COLORS["green"],
                                    lw=1.0, alpha=0.7))
        ax.text(min(baccs[i], baccs[i - 1]) - 0.001, dy,
                f"+{d:.4f}", color=COLORS["green"],
                fontsize=8.5, fontweight="bold", va="center", ha="right")

    # axis
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=9.5)
    ax.set_xlabel("FACED 9-class balanced accuracy", fontsize=10.5)

    # vertical ref lines
    ax.axvline(0.5720, color=COLORS["gray"], ls=":", lw=0.9, alpha=0.7)
    ax.axvline(0.6948, color=COLORS["sota"], ls=":", lw=0.9, alpha=0.8)
    ax.axvline(0.6280, color="#666", ls="--", lw=0.7, alpha=0.5)
    ax.axvline(0.6287, color="#666", ls="--", lw=0.7, alpha=0.5)
    ax.text(0.6286, 1.5, "EmotionKD 0.6280\n  EMOD AAAI 0.6287",
            color="#444", fontsize=7.5, va="center", ha="left")

    # final gain arrow
    ax.annotate("", xy=(0.6948, -0.45), xytext=(0.5720, -0.45),
                arrowprops=dict(arrowstyle="<->", color=COLORS["green"], lw=2.0))
    ax.text(0.633, -0.85, "+0.123 BACC absolute   (+21.5% relative over CBraMod)",
            color=COLORS["green"], fontweight="bold", fontsize=10.5,
            ha="center", va="top")

    # legend
    legend_elems = [
        Patch(facecolor=PHASE_COLOR["prior"], edgecolor="black",
              label="prior published SOTA"),
        Patch(facecolor=PHASE_COLOR["replication"], edgecolor="black",
              label="EMOD replication"),
        Patch(facecolor=PHASE_COLOR["recipe"], edgecolor="black",
              label="our recipe (aug, KD, d6)"),
        Patch(facecolor=PHASE_COLOR["ensemble"], edgecolor="black",
              label="ensemble & single-SOTA"),
        Patch(facecolor=PHASE_COLOR["ensemble_sota"], edgecolor="black",
              label="locked SOTA (this paper)"),
    ]
    ax.legend(handles=legend_elems, loc="upper left", frameon=False,
              fontsize=9.5, bbox_to_anchor=(1.02, 0.95))

    ax.set_xlim(0.560, 0.715)
    ax.set_ylim(-1.3, n - 0.4)

    ax.set_title("FACED SOTA cascade:  CBraMod → 0.6948 ensemble in 7 steps",
                 fontsize=12, fontweight="bold", loc="left", pad=12)

    save_dual(fig, f"{OUT}/lf7_recipe_cascade")
    save_dual(fig, f"{OUT_PAPER}/lf7_recipe_cascade")


if __name__ == "__main__":
    main()
