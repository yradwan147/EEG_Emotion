"""F7 — SOTA Ablation Cascade (§8 main).

Step plot: CBraMod 0.572 → +EMOD recipe → +aug → +KD → +d6 → +e150 → +ensemble.
"""
import os
import sys
import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _style import apply_style, COLORS, save_dual

OUT = "/ibex/project/c2323/yousef/paper_neurips26_final/figures"


def main():
    apply_style()
    rows = [
        # (label, BACC, std (or None), color_kind)
        ("CBraMod\n(ICLR 2025)",            0.572, 0.006, "prior"),
        ("EmotionKD\n(ACMMM 2023)",         0.628, None, "prior"),
        ("EMOD AAAI '26\n(paper value)",    0.6287, None, "prior"),
        ("EMOD vanilla\n(d3, race-fix)",    0.6194, 0.004, "ours"),
        ("+ aug (p=0.6)",                   0.6343, 0.004, "ours"),
        ("+ KD (rand9 9D)",                 0.6467, 0.007, "ours"),
        ("+ d6 depth\n(stacking)",          0.6581, 0.0066, "ours"),
        ("+ e150 single-ckpt\n(val-selected)", 0.6755, None, "ours"),
        ("5-ckpt ensemble (e100)",          0.6798, None, "ours_strong"),
        ("10-ckpt ensemble\n(e100+e150) — SOTA", 0.6948, None, "sota"),
    ]

    fig = plt.figure(figsize=(11.5, 5.5))
    ax = fig.add_subplot(111)

    color_map = {
        "prior":       COLORS["gray"],
        "ours":        COLORS["blue"],
        "ours_strong": "#13507a",
        "sota":        COLORS["darkblue"],
    }
    edge_map = {
        "prior":       "black",
        "ours":        "black",
        "ours_strong": "black",
        "sota":        "black",
    }

    n = len(rows)
    x = np.arange(n)
    baccs = np.array([r[1] for r in rows])
    stds  = np.array([r[2] if r[2] is not None else 0 for r in rows])
    kinds = [r[3] for r in rows]
    labels = [r[0] for r in rows]

    bar_colors = [color_map[k] for k in kinds]
    bar_edges = [edge_map[k] for k in kinds]
    bars = ax.bar(x, baccs, yerr=stds, color=bar_colors, edgecolor=bar_edges,
                  linewidth=0.9, capsize=3, error_kw=dict(elinewidth=1.0, ecolor="black"))

    # annotate values
    for xi, b, s, kind in zip(x, baccs, stds, kinds):
        weight = "bold" if kind in ("sota", "ours_strong") else "normal"
        fontsize = 10 if kind == "sota" else 9
        ax.text(xi, b + (s if s else 0) + 0.005,
                f"{b:.4f}", ha="center", va="bottom",
                fontsize=fontsize, fontweight=weight)

    # delta arrows above the cascade
    delta_pairs = [
        (3, 4, "+0.015", 0.001),
        (4, 5, "+0.012", 0.003),
        (5, 6, "+0.011", 0.04),
        (6, 7, "+0.017", None),
        (7, 8, "+0.004", None),
        (8, 9, "+0.015", None),
    ]
    y_delta = baccs.max() + 0.015
    for a, b, d, p in delta_pairs:
        ax.annotate("", xy=(b, y_delta), xytext=(a, y_delta),
                    arrowprops=dict(arrowstyle="->", color=COLORS["green"], lw=1.0))
        ax.text((a + b) / 2, y_delta + 0.0015, d, ha="center", va="bottom",
                fontsize=8, color=COLORS["green"], fontweight="bold")

    # horizontal reference lines at 0.572 (CBraMod) and 0.6948 (final)
    ax.axhline(0.572, color=COLORS["gray"], ls=":", lw=0.8, alpha=0.6)
    ax.axhline(0.6948, color=COLORS["darkblue"], ls=":", lw=0.8, alpha=0.6)

    # final relative gain
    ax.annotate("",
                xy=(n - 0.4, 0.6948), xytext=(n - 0.4, 0.572),
                arrowprops=dict(arrowstyle="<->", color=COLORS["green"], lw=1.5))
    ax.text(n - 0.3, 0.633, "+12.3 pp\n(+21.5%)", color=COLORS["green"],
            fontweight="bold", fontsize=10, va="center")

    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=8.5, rotation=20, ha="right")
    ax.set_ylabel("FACED 9-class balanced accuracy", fontsize=11)
    ax.set_title("FACED SOTA cascade: from CBraMod to a 0.6948 ensemble",
                 fontsize=11.5, fontweight="bold", loc="left", pad=8)
    ax.set_ylim(0.555, 0.730)
    ax.set_xlim(-0.6, n - 0.0)

    # legend (manual)
    from matplotlib.patches import Patch
    legend_elems = [
        Patch(facecolor=COLORS["gray"], edgecolor="black", label="prior published SOTA"),
        Patch(facecolor=COLORS["blue"], edgecolor="black", label="our cascade"),
        Patch(facecolor="#13507a", edgecolor="black", label="ensemble (interim)"),
        Patch(facecolor=COLORS["darkblue"], edgecolor="black", label="locked SOTA (this paper)"),
    ]
    ax.legend(handles=legend_elems, loc="upper left", frameon=False, fontsize=8.5)

    save_dual(fig, f"{OUT}/F7_sota_cascade")
    print("F7 saved.")


if __name__ == "__main__":
    main()
