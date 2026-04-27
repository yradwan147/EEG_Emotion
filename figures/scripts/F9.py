"""F9 (appendix) — All 25 V-axis interventions ranked.

Horizontal bar chart, sorted by Δ. Color by p-value tier.
"""
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _style import apply_style, COLORS, save_dual

OUT = "/ibex/project/c2323/yousef/paper_neurips26_final/figures"


def main():
    apply_style()
    # (label, delta, p_or_None, source, group)
    rows = [
        # negatives, large
        ("Distance-CE τ=5.0",          -0.397, 0.001, "#415", "destruction"),
        ("Pretrain-FT frozen",         -0.401, 0.001, "#416", "destruction"),
        ("Pretrain-FT unfrozen",       -0.190, 0.005, "#416", "destruction"),
        ("RSA λ=5",                    -0.093, 0.001, "#414", "monotonic"),
        ("Uncertainty (Kendall MTL)",  -0.067, 0.001, "#423", "neg_sig"),
        ("RSA λ=1",                    -0.057, 0.001, "#414", "neg_sig"),
        ("Anger-weighted λ=0.5",       -0.054, 0.0003, "#443", "neg_sig"),
        ("Frontal-mask λ=0.5",         -0.052, 0.0015, "#434", "neg_sig"),
        ("FAA λ=0.5",                  -0.044, 0.006, "#435", "neg_sig"),
        ("EEG-AUX MSE λ=0.5",          -0.043, 0.01,  "#401", "neg_sig"),
        ("Multi-V λ=0.5",              -0.041, 0.005, "#419", "neg_sig"),
        ("Distill (V-axis teacher)",   -0.017, 0.05,  "#420", "neg_ns"),
        ("Init weight",                -0.017, 0.05,  "#406", "neg_ns"),
        ("EEG-AUX MSE λ=0.1",          -0.016, 0.05,  "#401", "neg_ns"),
        ("FAA λ=0.1",                  -0.018, 0.063, "#435", "neg_ns"),
        ("Topo-optimal λ=0.1",         -0.013, 0.039, "#438", "neg_sig"),
        ("KD soft T=2 λ=1",            -0.012, 0.05,  "#409", "neg_ns"),
        ("EMODSTYLE class λ=1.0",      -0.010, 0.30,  "#424", "neg_ns"),
        ("PEFT lora λ=0.1",            -0.010, 0.10,  "#432", "neg_ns"),
        ("Frontal-mask λ=0.1",         -0.009, 0.21,  "#434", "neg_ns"),
        ("PEFT fullhead λ=0.1",        -0.009, 0.069, "#432", "neg_ns"),
        ("Curriculum cos li=0.5",      -0.009, 0.23,  "#445", "neg_ns"),
        ("KD soft T=1 λ=1",            -0.007, 0.30,  "#409", "neg_ns"),
        ("KD soft T=0.5 λ=0.5",        -0.005, 0.40,  "#409", "neg_ns"),
        ("Init bias",                  -0.003, 0.70,  "#406", "neg_ns"),
        ("Procrustes λ=0.05",          +0.001, 0.89,  "#436", "ns_pos"),
        ("PRIOR (smooth temp)",        +0.002, 0.40,  "#418", "ns_pos"),
        ("Topo-optimal λ=0.05",        +0.002, 0.50,  "#438", "ns_pos"),
        ("EMODSTYLE λ=0.5 stim",       +0.007, 0.22,  "#424", "ns_pos"),
        ("XEEG (FACED→SEED-V) λ=0.5",  +0.002, 0.97,  "#407", "ns_pos"),
    ]

    rows = sorted(rows, key=lambda r: r[1])

    labels = [r[0] for r in rows]
    deltas = np.array([r[1] for r in rows])
    pvals  = np.array([r[2] if r[2] is not None else 1.0 for r in rows])

    color_for = {
        "destruction":  "#5a0e0e",
        "monotonic":    "#7f1c1c",
        "neg_sig":      COLORS["red"],
        "neg_ns":       COLORS["orange"],
        "ns_pos":       COLORS["lightblue"],
    }
    groups = [r[4] for r in rows]
    bar_colors = [color_for[g] for g in groups]

    fig = plt.figure(figsize=(10.0, 9.6))
    ax = fig.add_subplot(111)
    y = np.arange(len(rows))
    bars = ax.barh(y, deltas, color=bar_colors, edgecolor="white", linewidth=0.6)
    ax.axvline(0, color="black", lw=0.8)
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=8.5)
    ax.set_xlabel("Δ FACED 9-class BACC vs vanilla baseline", fontsize=11)
    ax.set_title("All 25+ V-axis-as-supervision interventions, ranked by Δ\n(none survives at the converged baseline; saturation theorem)",
                 loc="left", fontsize=11)

    # value annotation
    for yi, d, p in zip(y, deltas, pvals):
        x_off = 0.003 if d >= 0 else -0.003
        ha = "left" if d >= 0 else "right"
        if p < 0.001:
            sig_str = "***"
        elif p < 0.01:
            sig_str = "**"
        elif p < 0.05:
            sig_str = "*"
        else:
            sig_str = "ns"
        ax.text(d + x_off, yi, f"{d:+.3f} {sig_str}", ha=ha, va="center",
                fontsize=7.5, color="black")

    ax.set_xlim(min(deltas) * 1.18, max(0.025, max(deltas) * 2.0))

    # legend
    legend_elems = [
        Patch(facecolor=color_for["destruction"], edgecolor="black",
              label="catastrophic (Δ < −0.1)"),
        Patch(facecolor=color_for["monotonic"], edgecolor="black",
              label="monotonic destruction"),
        Patch(facecolor=color_for["neg_sig"], edgecolor="black",
              label="significant negative (p < 0.05)"),
        Patch(facecolor=color_for["neg_ns"], edgecolor="black",
              label="NS negative"),
        Patch(facecolor=color_for["ns_pos"], edgecolor="black",
              label="NS positive"),
    ]
    ax.legend(handles=legend_elems, loc="upper left",
              bbox_to_anchor=(0.0, -0.07), ncol=3,
              fontsize=8.5, frameon=False)

    plt.subplots_adjust(left=0.18, right=0.97, top=0.92, bottom=0.14)
    fig.text(0.5, 0.005,
             "Asterisks: ***p<0.001, **p<0.01, *p<0.05 (paired t-test vs the same-recipe vanilla baseline). "
             "Sources: cycle-75 worklog tasks listed in `notes/all_findings_catalog.md`.",
             ha="center", fontsize=7.5, color=COLORS["gray"])

    save_dual(fig, f"{OUT}/F9_all_interventions")
    print("F9 saved.")


if __name__ == "__main__":
    main()
