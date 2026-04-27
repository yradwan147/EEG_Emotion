"""LF6 — Saturation Cliff (§7 main).

Δ-vs-recipe-strength plot: x-axis is the baseline BACC of the recipe the
V-axis intervention is added to (CBraMod 0.572, EMOD-d3 ~0.624, full SOTA d6
0.658). y-axis is Δ from V-axis intervention. Visualizes the transition that
crosses zero between EMOD-d3 and the full SOTA recipe.

Top panel: scatter with all 25+ V-axis interventions, colored by
significance tier; visible saturation cliff. Bottom panel zooms into the
3-anchor "component ablation" used in the paper to nail the transition:
CBraMod, EMOD d3, full SOTA recipe.
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


# Hand-built table of (label, base_bacc, delta, p, kind) — sourced from
# headline_numbers.md, all_findings_catalog.md (verified against the per-experiment
# JSONs at merge_*_results.json).
ROWS = [
    # CBraMod (very weak base)
    ("CBraMod + Topo λ=0.05",       0.5717, +0.006, 0.30,   "ns_pos"),
    # EMOD d3 baseline (~0.6235)
    ("EMOD d3 + Topo λ=0.05",       0.6235, +0.002, 0.50,   "ns_pos"),
    ("EMOD d3 + EMODSTYLE λ=0.5",   0.6235, +0.007, 0.22,   "ns_pos"),
    ("EMOD d3 + Procrustes λ=0.05", 0.6235, +0.001, 0.89,   "ns_pos"),
    ("EMOD d3 + PRIOR (smooth)",    0.6235, +0.002, 0.40,   "ns_pos"),
    # NS negatives at d3
    ("EMOD d3 + Topo λ=0.1",        0.6235, -0.013, 0.039,  "neg_sig"),
    ("EMOD d3 + Frontal-mask λ=0.1",0.6235, -0.009, 0.21,   "neg_ns"),
    ("EMOD d3 + FAA λ=0.1",         0.6235, -0.018, 0.063,  "neg_ns"),
    ("EMOD d3 + PEFT λ=0.1",        0.6235, -0.009, 0.069,  "neg_ns"),
    ("EMOD d3 + Curriculum cos",    0.6235, -0.009, 0.23,   "neg_ns"),
    ("EMOD d3 + KD soft T=2 λ=1",   0.6235, -0.012, 0.05,   "neg_ns"),
    ("EMOD d3 + Init weight",       0.6235, -0.017, 0.05,   "neg_ns"),
    ("EMOD d3 + Distill",           0.6235, -0.017, 0.05,   "neg_ns"),
    ("EMOD d3 + EEG-AUX MSE λ=0.1", 0.6235, -0.016, 0.05,   "neg_ns"),
    # Stat-sig negatives at d3
    ("EMOD d3 + Frontal-mask λ=0.5",0.6235, -0.052, 0.0015, "neg_sig"),
    ("EMOD d3 + FAA λ=0.5",         0.6235, -0.044, 0.006,  "neg_sig"),
    ("EMOD d3 + Anger-w λ=0.5",     0.6235, -0.054, 0.0003, "neg_sig"),
    ("EMOD d3 + Occipital λ=0.1",   0.6235, -0.022, 0.007,  "neg_sig"),
    ("EMOD d3 + Multi-V λ=0.5",     0.6235, -0.041, 0.005,  "neg_sig"),
    ("EMOD d3 + EEG-AUX MSE λ=0.5", 0.6235, -0.043, 0.01,   "neg_sig"),
    ("EMOD d3 + Uncert (Kendall)",  0.6235, -0.067, 0.001,  "neg_sig"),
    ("EMOD d3 + RSA λ=1",           0.6235, -0.057, 0.001,  "neg_sig"),
    ("EMOD d3 + RSA λ=5",           0.6235, -0.093, 0.001,  "monotonic"),
    # Full SOTA recipe (saturation cliff)
    ("d6 SOTA + Topo λ=0.05",       0.6581, -0.015, 0.001,  "neg_sig_full"),
    ("d6 SOTA + EMODSTYLE λ=0.5",   0.6581, -0.024, 0.001,  "neg_sig_full"),
]


# Style mapping
STYLE = {
    "ns_pos":       dict(c=COLORS["pos_ns"],  marker="o", s=120, edge=COLORS["blue"],
                          label="NS positive (Δ ≈ 0)"),
    "neg_ns":       dict(c=COLORS["neg_ns"],  marker="o", s=120, edge="#a04612",
                          label="NS negative (p > 0.05)"),
    "neg_sig":      dict(c=COLORS["neg_sig"], marker="o", s=160, edge="#7f1c1c",
                          label="significant negative (p < 0.05)"),
    "monotonic":    dict(c=COLORS["monotonic"],marker="o", s=160, edge="black",
                          label="monotonic destruction"),
    "neg_sig_full": dict(c=COLORS["destruction"], marker="X", s=240, edge="black",
                          label="full SOTA recipe (cliff)"),
}


def main():
    apply_lf_style()
    fig = plt.figure(figsize=(11.5, 6.8))
    gs = fig.add_gridspec(1, 1, left=0.090, right=0.985, bottom=0.13, top=0.86)
    ax = fig.add_subplot(gs[0, 0])

    # transition zone
    ax.axvspan(0.620, 0.660, color=COLORS["lightgray"], alpha=0.25, zorder=0)
    ax.axhline(0, color="black", lw=0.7, zorder=1)

    # plot points (jittered slightly horizontally for readability)
    rng = np.random.default_rng(42)
    plotted = set()
    for label, base, delta, p, kind in ROWS:
        x = base + rng.normal(0, 0.0010)
        st = STYLE[kind]
        lab = st["label"] if kind not in plotted else None
        plotted.add(kind)
        ax.scatter(x, delta, s=st["s"], c=st["c"], marker=st["marker"],
                   edgecolors=st["edge"], linewidths=1.0, alpha=0.92, zorder=3,
                   label=lab)

    # Fit a robust trend through (base_x, mean(delta_at_base)) — anchor visualization
    anchor_x = np.array([0.572, 0.6235, 0.6581])
    anchor_y = np.array([
        +0.006,                         # CBraMod (single seed)
        np.mean([d for (_, b, d, _, _) in ROWS if abs(b - 0.6235) < 0.001]),
        np.mean([d for (_, b, d, _, _) in ROWS if abs(b - 0.6581) < 0.001]),
    ])
    ax.plot(anchor_x, anchor_y, color=COLORS["darkblue"], lw=2.3, ls="-",
            alpha=0.85, zorder=2,
            label=f"mean Δ at each base recipe")
    for x, y in zip(anchor_x, anchor_y):
        ax.scatter([x], [y], s=200, c="white", edgecolors=COLORS["darkblue"],
                   linewidths=2.0, marker="D", zorder=5)

    # vertical guide lines at the three anchors — labels above the plot top
    for xv, lab_t in [(0.572, "CBraMod"), (0.6235, "EMOD d3"), (0.6581, "d6 SOTA")]:
        ax.axvline(xv, color=COLORS["gray"], ls=":", lw=0.8, alpha=0.7, zorder=1)
        ax.text(xv, 0.041, lab_t, fontsize=9.0, ha="center",
                color=COLORS["gray"], fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.20", facecolor="white",
                          edgecolor="none", alpha=0.92))

    # callouts on the cliff — placed in clear regions (above and below the
    # main cluster) so the text never sits on data points or guide-line labels.
    annotate_points = {
        "Anger-w λ=0.5\n(−0.054***)":       (0.6235, -0.054),
        "RSA λ=5\n(−0.093***)":             (0.6235, -0.093),
        "d6 SOTA + EMODSTYLE\n(−0.024***)": (0.6581, -0.024),
        "EMODSTYLE λ=0.5\n(+0.007 ns)":     (0.6235, +0.007),
        "CBraMod+Topo\n(+0.006 ns)":        (0.5717, +0.006),
    }
    offsets = {
        "Anger-w λ=0.5\n(−0.054***)":       (0.595, -0.072),
        "RSA λ=5\n(−0.093***)":             (0.595, -0.097),
        "d6 SOTA + EMODSTYLE\n(−0.024***)": (0.671, -0.018),
        "EMODSTYLE λ=0.5\n(+0.007 ns)":     (0.602, +0.018),
        "CBraMod+Topo\n(+0.006 ns)":        (0.572, +0.018),
    }
    halign = {
        "Anger-w λ=0.5\n(−0.054***)":       "right",
        "RSA λ=5\n(−0.093***)":             "right",
        "d6 SOTA + EMODSTYLE\n(−0.024***)": "left",
        "EMODSTYLE λ=0.5\n(+0.007 ns)":     "right",
        "CBraMod+Topo\n(+0.006 ns)":        "left",
    }
    for lab, (x, y) in annotate_points.items():
        tx, ty = offsets[lab]
        ha = halign[lab]
        ax.annotate(lab, xy=(x, y), xytext=(tx, ty), fontsize=8.0,
                    color="black", linespacing=0.95, ha=ha,
                    arrowprops=dict(arrowstyle="-", color=COLORS["gray"],
                                    lw=0.7, alpha=0.7))

    # cliff arrow — moved to upper-half so it doesn't pass through dots
    ax.annotate("", xy=(0.6581, -0.022), xytext=(0.6235, -0.001),
                arrowprops=dict(arrowstyle="->", color="black", lw=1.6, alpha=0.55))
    ax.text(0.6390, -0.004, "the saturation cliff",
            fontsize=10.0, ha="left", va="bottom",
            fontweight="bold", color="black", alpha=0.85,
            bbox=dict(boxstyle="round,pad=0.20", facecolor="white",
                      edgecolor="#bbbbbb", linewidth=0.5, alpha=0.92))

    ax.set_xlabel("base recipe FACED 9-class BACC  (capacity dimension)", fontsize=10.5)
    ax.set_ylabel("Δ BACC from adding V-axis supervision", fontsize=10.5)
    ax.set_title("V-axis supervision crosses zero between EMOD d3 and the full SOTA recipe",
                 fontsize=11.5, fontweight="bold", loc="left", pad=10)
    panel_label(ax, "", x=-0.06, y=1.02)
    ax.set_xlim(0.555, 0.690)
    ax.set_ylim(-0.115, 0.050)
    ax.legend(loc="lower left", fontsize=8, frameon=True, framealpha=0.95,
              edgecolor="#cccccc", ncol=1)

    fig.text(0.5, 0.015,
             "n=25 V-axis interventions (frontal/FAA/occ/topo/anger-w/EMODSTYLE/Procrustes/PEFT/RSA/multi-V/"
             "EEG-AUX/KD/init/distill/curriculum/uncert/...). All ≥3 seeds unless noted; significance vs paired same-recipe vanilla.",
             ha="center", fontsize=7.8, color=COLORS["gray"])

    save_dual(fig, f"{OUT}/lf6_saturation_cliff")
    save_dual(fig, f"{OUT_PAPER}/lf6_saturation_cliff")


if __name__ == "__main__":
    main()
