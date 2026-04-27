"""LF9 — All 25+ V-axis interventions ranked, forest plot (§7 appendix).

Forest plot showing each intervention's Δ with 95% CI from a paired t-test
(approximated from reported std ÷ √n). Colored by tier (sig.negative red,
n.s.+ grey, n.s. light grey, sig.positive green - none should be green).
Vertical zero line. Sorted by Δ.
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


# Format: (label, delta, p, source_id, n_seeds, std, tier)
# n_seeds and std drive the 95% CI half-width (1.96 * std/sqrt(n)).
ROWS = [
    # Catastrophic
    ("Pretrain-FT (frozen)",        -0.401, 0.001, "#416", 3, 0.040, "destruction"),
    ("Distance-CE τ=5.0",           -0.397, 0.001, "#415", 3, 0.030, "destruction"),
    ("Pretrain-FT (unfrozen)",      -0.190, 0.005, "#416", 3, 0.025, "destruction"),
    # Monotonic
    ("RSA λ=5",                     -0.093, 0.001, "#414", 5, 0.013, "monotonic"),
    ("Uncertainty (Kendall MTL)",   -0.067, 0.001, "#423", 5, 0.012, "neg_sig"),
    ("RSA λ=1",                     -0.057, 0.001, "#414", 5, 0.011, "neg_sig"),
    ("Anger-weighted λ=0.5",        -0.054, 0.0003, "#443", 5, 0.009, "neg_sig"),
    ("Frontal-mask λ=0.5",          -0.052, 0.0015, "#434", 5, 0.011, "neg_sig"),
    ("FAA λ=0.5",                   -0.044, 0.006, "#435", 5, 0.014, "neg_sig"),
    ("EEG-AUX MSE λ=0.5",           -0.043, 0.010, "#401", 5, 0.014, "neg_sig"),
    ("Multi-V λ=0.5",               -0.041, 0.005, "#419", 5, 0.013, "neg_sig"),
    ("Occipital λ=0.1",             -0.022, 0.007, "#437", 5, 0.011, "neg_sig"),
    ("FAA λ=0.1",                   -0.018, 0.063, "#435", 5, 0.012, "neg_ns"),
    ("Init weight",                 -0.017, 0.05,  "#406", 5, 0.011, "neg_ns"),
    ("Distill (V-axis teacher)",    -0.017, 0.05,  "#420", 5, 0.012, "neg_ns"),
    ("EEG-AUX MSE λ=0.1",           -0.016, 0.05,  "#401", 5, 0.012, "neg_ns"),
    ("Topo-optimal λ=0.1",          -0.013, 0.039, "#438", 5, 0.010, "neg_sig"),
    ("KD soft T=2 λ=1",             -0.012, 0.05,  "#409", 5, 0.011, "neg_ns"),
    ("EMODSTYLE class λ=1.0",       -0.010, 0.30,  "#424", 5, 0.013, "neg_ns"),
    ("PEFT lora λ=0.1",             -0.010, 0.10,  "#432", 5, 0.011, "neg_ns"),
    ("Frontal-mask λ=0.1",          -0.009, 0.21,  "#434", 5, 0.012, "neg_ns"),
    ("PEFT fullhead λ=0.1",         -0.009, 0.069, "#432", 5, 0.010, "neg_ns"),
    ("Curriculum cos li=0.5",       -0.009, 0.23,  "#445", 5, 0.012, "neg_ns"),
    ("KD soft T=1 λ=1",             -0.007, 0.30,  "#409", 5, 0.011, "neg_ns"),
    ("KD soft T=0.5 λ=0.5",         -0.005, 0.40,  "#409", 5, 0.011, "neg_ns"),
    ("Init bias",                   -0.003, 0.70,  "#406", 5, 0.012, "neg_ns"),
    ("Procrustes λ=0.05",           +0.001, 0.89,  "#436", 5, 0.011, "ns_pos"),
    ("PRIOR (smooth temp)",         +0.002, 0.40,  "#418", 5, 0.012, "ns_pos"),
    ("Topo-optimal λ=0.05",         +0.002, 0.50,  "#438", 5, 0.010, "ns_pos"),
    ("XEEG (FACED→SEED-V) λ=0.5",   +0.002, 0.97,  "#407", 5, 0.013, "ns_pos"),
    ("EMODSTYLE λ=0.5 stim",        +0.007, 0.22,  "#424", 5, 0.013, "ns_pos"),
]


COLOR_FOR = {
    "destruction":  "#5a0e0e",
    "monotonic":    "#7f1c1c",
    "neg_sig":      COLORS["red"],
    "neg_ns":       COLORS["orange"],
    "ns":           COLORS["lightgray"],
    "ns_pos":       COLORS["lightblue"],
    "pos_sig":      COLORS["pos_sig"],
}


def main():
    apply_lf_style()
    rows = sorted(ROWS, key=lambda r: r[1])  # most negative first
    labels = [r[0] for r in rows]
    deltas = np.array([r[1] for r in rows])
    pvals = np.array([r[2] for r in rows])
    n_seeds = np.array([r[4] for r in rows])
    stds = np.array([r[5] for r in rows])
    sources = [r[3] for r in rows]
    tiers = [r[6] for r in rows]
    # 95% CI half-width (paired t-test SE)
    ci_half = 1.96 * stds / np.sqrt(n_seeds)

    bar_colors = [COLOR_FOR[t] for t in tiers]

    fig = plt.figure(figsize=(13.0, 11.5))
    gs = fig.add_gridspec(1, 1, left=0.20, right=0.66, bottom=0.085, top=0.93)
    ax = fig.add_subplot(gs[0, 0])

    y = np.arange(len(rows))[::-1]  # top-down ascending = top is most negative
    # Wait: we want most negative at TOP; sorted asc puts most-neg first; with y[0] at top this is correct
    # Actually we want most negative AT BOTTOM with 0 in middle; rethink: forest plots conventionally
    # have most-positive on top. Reverse the order here so top of axis = most negative.
    # We'll keep most-negative on top to highlight the destruction.
    y = np.arange(len(rows))[::-1]

    # error bars
    ax.errorbar(deltas, y, xerr=ci_half, fmt="none", ecolor="black",
                elinewidth=1.0, capsize=3.0, capthick=1.0, zorder=3)
    # markers
    sizes = np.array([90 if t in ("destruction", "monotonic") else 75 for t in tiers])
    ax.scatter(deltas, y, s=sizes, c=bar_colors, edgecolor="black", linewidths=0.7,
               zorder=4)

    ax.axvline(0, color="black", lw=1.0, zorder=2)
    ax.axvspan(-0.005, 0.005, color=COLORS["lightgray"], alpha=0.30, zorder=1)

    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=9)

    # right-side annotation: source + delta + p + significance stars (outside plot area)
    for yi, d, p, src in zip(y, deltas, pvals, sources):
        sig = "***" if p < 0.001 else ("**" if p < 0.01 else ("*" if p < 0.05 else "ns"))
        ax.text(1.012, yi, f"{d:+.3f}  {sig:>3}  ({src})",
                transform=ax.get_yaxis_transform(),
                ha="left", va="center", fontsize=8, color="black",
                family="monospace")

    ax.set_xlabel("Δ FACED 9-class BACC vs vanilla baseline", fontsize=11)
    ax.set_xlim(-0.42, 0.025)
    ax.set_ylim(-0.5, len(rows) - 0.5)

    # legend
    legend_elems = [
        Patch(facecolor=COLOR_FOR["destruction"], edgecolor="black",
              label="catastrophic (Δ < −0.1)"),
        Patch(facecolor=COLOR_FOR["monotonic"], edgecolor="black",
              label="monotonic destruction"),
        Patch(facecolor=COLOR_FOR["neg_sig"], edgecolor="black",
              label="significant negative (p < 0.05)"),
        Patch(facecolor=COLOR_FOR["neg_ns"], edgecolor="black",
              label="NS negative"),
        Patch(facecolor=COLOR_FOR["ns_pos"], edgecolor="black",
              label="NS positive"),
        Patch(facecolor=COLOR_FOR["pos_sig"], edgecolor="black",
              label="significant positive  (none observed)"),
    ]
    ax.legend(handles=legend_elems, loc="upper left",
              bbox_to_anchor=(1.40, 0.95), ncol=1,
              fontsize=9, frameon=False, title="significance tier",
              title_fontsize=9.5)

    fig.text(0.05, 0.96,
             "All 25+ V-axis-as-supervision interventions, ranked by Δ",
             fontsize=12.5, fontweight="bold", ha="left")
    fig.text(0.05, 0.940,
             "Forest plot of the saturation theorem: zero successful interventions at the converged baseline",
             fontsize=10, ha="left", color=COLORS["gray"])

    fig.text(0.5, 0.025,
             "Bars = 95% CI from a paired t-test (1.96 × σ/√n).  "
             "Asterisks: ***p<0.001, **p<0.01, *p<0.05.  "
             "Source IDs reference cycle-75 worklog tasks (notes/all_findings_catalog.md).",
             ha="center", fontsize=8.0, color=COLORS["gray"])

    save_dual(fig, f"{OUT}/lf9_all_interventions_forest")
    save_dual(fig, f"{OUT_PAPER}/lf9_all_interventions_forest")


if __name__ == "__main__":
    main()
