"""LF14 — Ensemble generality across datasets (§8 tab:ensemble-generality).

Replaces Table tab:ensemble-generality. Two-panel figure that visualises
the gain-proportional-to-headroom relationship predicted by the two-tier
theory:
- Left: scatter of Δ-ensemble-gain vs (1 - single-model accuracy), with
  benchmark markers; linear fit visualises the predicted slope ~0.07.
- Right: paired bars of Single-mean (light) vs 5-seed-ensemble (dark) per
  benchmark, sorted by headroom, with Δ annotated.

This makes the saturation/headroom mechanism legible at a glance.
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


# Source: §8 paper / sota_ensemble_theory.md / cycle 75 cross-dataset runs.
# (label, single_acc, ensemble_acc, modality)
ROWS = [
    ("SEED-V 5c\n(EEG, EMOD d=6)",     0.3743, 0.4083, "EEG"),
    ("FACED 9c\n(EEG, EMOD d=6)",      0.6581, 0.6948, "EEG"),
    ("CIFAR-10\n(small CNN)",          0.9015, 0.9253, "Vision"),
    ("MNIST\n(MLP)",                   0.9849, 0.9863, "Vision"),
]

MOD_COLORS = {
    "EEG":    COLORS["darkblue"],
    "Vision": COLORS["orange"],
}


def main():
    apply_lf_style()
    labels = [r[0] for r in ROWS]
    singles = np.array([r[1] for r in ROWS])
    ens = np.array([r[2] for r in ROWS])
    deltas = ens - singles
    headroom = 1.0 - singles
    mods = [r[3] for r in ROWS]

    fig = plt.figure(figsize=(13.0, 5.4))
    gs = fig.add_gridspec(1, 2, left=0.07, right=0.985, bottom=0.24, top=0.83,
                          width_ratios=[1.05, 1.30], wspace=0.27)

    # Panel a: Δ vs headroom scatter + fit
    ax_a = fig.add_subplot(gs[0, 0])

    # Scatter
    for h, d, lab, mod in zip(headroom, deltas, labels, mods):
        col = MOD_COLORS[mod]
        ax_a.scatter([h], [d], s=180, color=col, edgecolor="black",
                     linewidths=0.9, zorder=4)
        # offset annotation depending on point
        dx, dy = 0.012, 0.001
        ha = "left"
        if "MNIST" in lab:
            dx, dy = -0.012, 0.0015; ha = "right"
        if "CIFAR" in lab:
            dx, dy = 0.012, -0.003; ha = "left"
        if "FACED" in lab:
            dx, dy = -0.012, 0.0018; ha = "right"
        ax_a.annotate(lab, xy=(h, d), xytext=(h + dx, d + dy),
                      fontsize=8.5, ha=ha, va="bottom",
                      fontweight="bold")
        ax_a.text(h + dx, d + dy - 0.0035 if ha == "left" else d + dy - 0.0035,
                  fr"$\Delta$ = {d:+.3f}", fontsize=7.5,
                  ha=ha, color=COLORS["gray"])

    # Linear fit (forced through origin not quite — use OLS)
    coef = np.polyfit(headroom, deltas, 1)
    xs = np.linspace(0, max(headroom) * 1.05, 100)
    ys = np.polyval(coef, xs)
    ax_a.plot(xs, ys, ls="--", color=COLORS["gray"], lw=1.3, alpha=0.85,
              label=fr"linear fit: $\Delta \approx {coef[0]:.2f}\,(1-\bar{{\mathrm{{Acc}}}}) + {coef[1]:+.3f}$",
              zorder=2)
    ax_a.axhline(0, color="black", lw=0.7, alpha=0.5, zorder=1)

    ax_a.set_xlabel(r"Single-model headroom $1 - \bar{\mathrm{Acc}}$", fontsize=10.5)
    ax_a.set_ylabel(r"$\Delta$ from 5-seed ensemble", fontsize=10.5)
    ax_a.set_xlim(-0.02, 0.70)
    ax_a.set_ylim(-0.005, 0.05)
    ax_a.set_title("(a) Ensemble gain scales with headroom",
                   fontsize=11, fontweight="bold", loc="left")
    ax_a.legend(loc="lower right", fontsize=8.5, frameon=False)

    # Panel b: paired bars, sorted by headroom
    ax_b = fig.add_subplot(gs[0, 1])
    order = np.argsort(-headroom)  # largest headroom first
    labels_o = [labels[i] for i in order]
    singles_o = singles[order]
    ens_o = ens[order]
    deltas_o = deltas[order]
    mods_o = [mods[i] for i in order]

    x = np.arange(len(ROWS))
    width = 0.35

    cols_single = [COLORS["lightgray"] for _ in range(len(ROWS))]
    cols_ens = [MOD_COLORS[m] for m in mods_o]

    ax_b.bar(x - width/2, singles_o, width=width,
             color=cols_single, edgecolor="black", linewidth=0.6,
             label="single-seed mean", zorder=3)
    ax_b.bar(x + width/2, ens_o, width=width,
             color=cols_ens, edgecolor="black", linewidth=0.6,
             label="5-seed ensemble", zorder=3)

    # value annotation
    for xi, sv, ev, dv in zip(x, singles_o, ens_o, deltas_o):
        ax_b.text(xi - width/2, sv + 0.014, f"{sv:.3f}", ha="center",
                  fontsize=7.5)
        ax_b.text(xi + width/2, ev + 0.014, f"{ev:.3f}", ha="center",
                  fontsize=7.5, fontweight="bold")
        # delta annotation - high above the bars
        ax_b.text(xi, max(sv, ev) + 0.085, fr"$\Delta$={dv:+.3f}",
                  ha="center", va="center", fontsize=8.5,
                  color=COLORS["darkblue"], fontweight="bold",
                  bbox=dict(facecolor="white", edgecolor=COLORS["lightgray"],
                            pad=2, boxstyle="round,pad=0.25"))

    ax_b.set_xticks(x)
    ax_b.set_xticklabels(labels_o, fontsize=8.5)
    ax_b.set_ylim(0, 1.18)
    ax_b.set_ylabel("Accuracy / BACC", fontsize=10.5)
    ax_b.set_title("(b) Single vs ensemble per benchmark (sorted by headroom)",
                   fontsize=11, fontweight="bold", loc="left")
    legend_elems = [
        Patch(facecolor=COLORS["lightgray"], edgecolor="black",
              label="single-seed mean"),
        Patch(facecolor=MOD_COLORS["EEG"], edgecolor="black",
              label="EEG ensemble"),
        Patch(facecolor=MOD_COLORS["Vision"], edgecolor="black",
              label="Vision ensemble"),
    ]
    # No per-axis legend on b; we'll place a unified legend in the figure footer area

    fig.text(0.07, 0.945,
             "Two-tier ensemble gain across four benchmarks: Δ shrinks toward zero as headroom shrinks",
             fontsize=12, fontweight="bold", ha="left")
    fig.text(0.07, 0.905,
             "MNIST (no headroom) gives near-zero gain; SEED-V and FACED (large headroom) give the strongest gain.",
             fontsize=9.5, ha="left", color=COLORS["gray"])

    fig.legend(handles=legend_elems, loc="lower center", ncol=3,
               fontsize=9, frameon=False, bbox_to_anchor=(0.55, 0.060))

    fig.text(0.5, 0.018,
             "Source: §8 ensemble-generality table / sota_ensemble_theory.md. "
             "All ensembles are 5-seed uniform softmax averages on identical recipe per dataset.",
             ha="center", fontsize=7.5, color=COLORS["gray"])

    save_dual(fig, f"{OUT}/lf14_ensemble_generality")
    save_dual(fig, f"{OUT_PAPER}/lf14_ensemble_generality")


if __name__ == "__main__":
    main()
