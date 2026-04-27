"""LF15 — 20x20 cross-concept transfer heatmap (Appendix tab:concept-library-full).

Replaces the tiny LaTeX table in the appendix with a proper heatmap. Each
cell = best-orientation AUC of source concept's V-axis applied to target
concept's pole-vs-pole benchmark. Diagonal = self-AUC. Sorted by mean
off-diagonal AUC (top = most-general source axes; bottom = most-specific).

User's explicit request: 'compositionality, you only give 2 or 3 lines
when you can show the transfer matrix' — this delivers the matrix at full
fidelity.
"""
import os
import sys
import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lf_style import apply_lf_style, COLORS, save_dual

OUT = "/ibex/project/c2323/yousef/paper_neurips26_final/figures/landmark"
OUT_PAPER = "/ibex/project/c2323/yousef/EEG_Emotion/figures/landmark"

JSON = "/ibex/project/c2323/yousef/reports/r6_concept_transfer_matrix.json"


def main():
    apply_lf_style()
    with open(JSON) as f:
        d = json.load(f)
    concepts = d["concepts"]
    M = np.array(d["auc_matrix_best_orientation"])  # M[i, j] = src i applied to tgt j
    n = len(concepts)

    # Sort by mean off-diagonal AUC (descending = most general at top)
    off = M.copy()
    np.fill_diagonal(off, np.nan)
    mean_off_src = np.nanmean(off, axis=1)
    order = np.argsort(-mean_off_src)
    concepts_o = [concepts[i] for i in order]
    M_o = M[order, :][:, order]
    mean_off_o = mean_off_src[order]

    # Per-target captured-by-others mean (col-wise, off diagonal)
    off_o = M_o.copy()
    np.fill_diagonal(off_o, np.nan)
    mean_off_tgt = np.nanmean(off_o, axis=0)

    # ----- Figure layout -----
    fig = plt.figure(figsize=(13.5, 12.0))
    gs = fig.add_gridspec(
        2, 3,
        left=0.11, right=0.96, bottom=0.16, top=0.93,
        width_ratios=[1.0, 0.16, 0.04],
        height_ratios=[0.16, 1.0],
        wspace=0.06, hspace=0.06,
    )

    ax_top    = fig.add_subplot(gs[0, 0])  # column-mean bar (mean off-diag captured by others)
    ax_main   = fig.add_subplot(gs[1, 0])  # heatmap
    ax_right  = fig.add_subplot(gs[1, 1])  # row-mean bar (mean off-diag from this source)
    ax_cbar   = fig.add_subplot(gs[1, 2])  # colorbar

    # Heatmap: viridis, vmin=0.5 (chance), vmax=1.0
    cmap = plt.get_cmap("viridis")
    norm = mcolors.Normalize(vmin=0.50, vmax=1.0)
    im = ax_main.imshow(M_o, cmap=cmap, norm=norm, aspect="auto",
                        interpolation="nearest")

    # Cell value annotations (small font, black/white based on intensity)
    for i in range(n):
        for j in range(n):
            v = M_o[i, j]
            color = "white" if v < 0.78 else "black"
            txt = f"{v:.2f}"
            # bold for diagonal
            weight = "bold" if i == j else "normal"
            ax_main.text(j, i, txt, ha="center", va="center",
                         fontsize=6.0, color=color, fontweight=weight)

    # Diagonal highlight: thin black square per cell on the diagonal
    for i in range(n):
        ax_main.add_patch(plt.Rectangle((i - 0.5, i - 0.5), 1, 1,
                                        fill=False, edgecolor="white",
                                        linewidth=1.2, zorder=4))

    # Cell borders (lightly)
    ax_main.set_xticks(np.arange(-0.5, n, 1), minor=True)
    ax_main.set_yticks(np.arange(-0.5, n, 1), minor=True)
    ax_main.grid(which="minor", color="white", lw=0.3, alpha=0.4)
    ax_main.tick_params(which="minor", bottom=False, left=False)

    # Axis labels
    ax_main.set_xticks(np.arange(n))
    ax_main.set_yticks(np.arange(n))
    ax_main.set_xticklabels(concepts_o, rotation=55, ha="right", fontsize=8.5)
    ax_main.set_yticklabels(concepts_o, fontsize=8.5)
    ax_main.set_xlabel("target concept (pole-vs-pole benchmark)", fontsize=10.5)
    ax_main.set_ylabel("source concept (V-axis applied)", fontsize=10.5)

    # Colorbar
    cb = plt.colorbar(im, cax=ax_cbar)
    cb.set_label("AUC", fontsize=9.5)
    cb.ax.tick_params(labelsize=8)
    cb.ax.axhline(0.5, color="black", lw=0.8, ls=":")
    cb.ax.axhline(0.95, color="black", lw=0.8, ls="--")

    # Right marginal: mean off-diag per source row
    y_pos = np.arange(n)
    ax_right.barh(y_pos, mean_off_o, color=COLORS["lightblue"],
                  edgecolor="black", linewidth=0.5)
    for yi, mv in zip(y_pos, mean_off_o):
        ax_right.text(mv + 0.005, yi, f"{mv:.2f}", ha="left", va="center",
                      fontsize=7.0, family="monospace")
    ax_right.set_xlim(0.7, 0.95)
    ax_right.set_ylim(n - 0.5, -0.5)  # invert
    ax_right.set_yticks([])
    ax_right.set_xlabel("mean off-diag\n(generality)", fontsize=9)
    ax_right.tick_params(axis="x", labelsize=7.5)
    ax_right.spines["left"].set_visible(False)

    # Top marginal: mean off-diag per target col (captured-by-others)
    ax_top.bar(np.arange(n), mean_off_tgt, color=COLORS["orange"],
               edgecolor="black", linewidth=0.5)
    for xi, mv in zip(np.arange(n), mean_off_tgt):
        ax_top.text(xi, mv + 0.01, f"{mv:.2f}", ha="center", va="bottom",
                    fontsize=6.5, family="monospace")
    ax_top.set_xlim(-0.5, n - 0.5)
    ax_top.set_ylim(0.6, 1.02)
    ax_top.set_xticks([])
    ax_top.set_ylabel("mean off-diag\n(captured by others)", fontsize=9)
    ax_top.tick_params(axis="y", labelsize=7.5)
    ax_top.spines["bottom"].set_visible(False)

    fig.text(0.11, 0.965,
             "Cross-concept transfer matrix: the recipe extracts concept-specific late-layer directions",
             fontsize=12.5, fontweight="bold", ha="left")
    fig.text(0.11, 0.945,
             f"Mean self-AUC (diagonal) = 0.97  |  mean off-diagonal AUC = 0.84  |  "
             f"self-vs-other gap = +0.13 ({n}$\\times${n} concepts; rows sorted by generality)",
             fontsize=9.5, ha="left", color=COLORS["gray"])

    fig.text(0.5, 0.012,
             "Source: reports/r6_concept_transfer_matrix.json (Qwen3.5-1.7B, layer 27, "
             "12 train + 8 test stories per concept). "
             "Cell $(i, j)$ = source concept $i$'s V-axis classifying target concept $j$'s pole-vs-pole benchmark.",
             ha="center", fontsize=8.0, color=COLORS["gray"])

    save_dual(fig, f"{OUT}/lf15_concept_transfer_heatmap")
    save_dual(fig, f"{OUT_PAPER}/lf15_concept_transfer_heatmap")


if __name__ == "__main__":
    main()
