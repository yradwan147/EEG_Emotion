"""F10 (appendix) — Two-Tier Saturation Schematic.

Conceptual diagram with the V-axis basin (Tier 1, saturated) and the
within-class V-axis residual (Tier 2, where ensemble gain lives).
"""
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, FancyArrowPatch, FancyBboxPatch

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _style import apply_style, COLORS, save_dual

OUT = "/ibex/project/c2323/yousef/paper_neurips26_final/figures"


def main():
    apply_style()
    fig = plt.figure(figsize=(11.5, 5.6))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.0, 1.0], wspace=0.20,
                          left=0.04, right=0.985, bottom=0.06, top=0.92)

    # ---- Left panel: Two-tier representation cartoon ----
    ax = fig.add_subplot(gs[0, 0])
    ax.set_xlim(-3, 3)
    ax.set_ylim(-2.6, 2.6)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("(a) Two-tier representational structure of the V-axis", loc="left", fontsize=11)

    # Draw the V-axis as an arrow
    ax.annotate("", xy=(2.5, 0), xytext=(-2.5, 0),
                arrowprops=dict(arrowstyle="-|>", color="black", lw=1.6))
    ax.text(2.7, 0, "V-axis\n(valence)", va="center", ha="left", fontsize=10)
    ax.text(-2.6, 0.18, "negative", va="center", ha="left", fontsize=8, color=COLORS["red"])
    ax.text(2.4, 0.18, "positive", va="center", ha="right", fontsize=8, color=COLORS["blue"])

    # 9-class centroids along the V-axis (from class_clip_rich values, scaled)
    centroids_x = np.array([-2.1, -1.4, -1.05, -0.85, -0.30,
                            +0.20, +0.85, +1.55, +2.10])
    classes = ["Anger", "Disgust", "Fear", "Sadness", "Neutral",
               "Amusement", "Inspiration", "Joy", "Tenderness"]
    rng = np.random.default_rng(7)
    for ci, (cx, cls) in enumerate(zip(centroids_x, classes)):
        # Tier 2: within-class residual scatter (same color, varying y)
        for j in range(8):
            y = rng.normal(0, 0.55)
            x = cx + rng.normal(0, 0.06)
            ax.scatter(x, y, s=14, c=COLORS["lightgray"], alpha=0.7, zorder=2)
        # Tier 1: class centroid
        col = COLORS["red"] if cx < -0.4 else (COLORS["blue"] if cx > 0.4 else COLORS["gray"])
        ax.scatter(cx, 0, s=170, c=col, edgecolors="black", linewidths=1.0,
                   zorder=4)
        ax.text(cx, -1.2, cls, fontsize=7, rotation=40, ha="right", color="black")

    # Tier 1 box
    ax.text(0, 1.7, "Tier 1: shared class-mean V-axis basin\n(saturated; cross-checkpoint convergence)",
            ha="center", va="center", fontsize=9, fontweight="bold",
            color=COLORS["darkblue"],
            bbox=dict(boxstyle="round,pad=0.4", facecolor="#e8f2fa",
                      edgecolor=COLORS["darkblue"], linewidth=1.0))
    # Tier 2 annotation
    ax.text(0, -2.05, "Tier 2: within-class V-axis residual\n(seed-specific; where the ensemble gain lives)",
            ha="center", va="center", fontsize=9, fontweight="bold",
            color="#7f1c1c",
            bbox=dict(boxstyle="round,pad=0.4", facecolor="#f7e2e2",
                      edgecolor="#7f1c1c", linewidth=1.0))

    # vertical lines from centroid to scatter cluster
    for cx in centroids_x:
        ax.plot([cx, cx], [-0.85, 0.85], color=COLORS["lightgray"],
                lw=0.5, alpha=0.4, zorder=1)

    # ---- Right panel: Saturation transition schematic ----
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0.55, 0.75)
    ax2.set_xlabel("training capacity (depth × epochs × aug × KD)", fontsize=10)
    ax2.set_ylabel("FACED 9-class BACC", fontsize=10)
    ax2.set_title("(b) The saturation transition: V-axis loss helps below, hurts above", loc="left", fontsize=11)

    # vanilla curve (smooth sigmoid going up)
    x = np.linspace(0, 1, 200)
    base = 0.572 + (0.6948 - 0.572) * (1 / (1 + np.exp(-7 * (x - 0.45))))
    # V-axis loss curve: helps slightly low cap, hurts at high cap
    deltas = 0.012 * np.exp(-((x - 0.18) / 0.10) ** 2) - 0.020 * (x - 0.55).clip(0, None) ** 1.5 * 6
    vaxis = base + deltas

    ax2.plot(x, base, color=COLORS["blue"], lw=2.4, label="vanilla recipe")
    ax2.plot(x, vaxis, color=COLORS["red"], lw=2.0, label="vanilla + V-axis loss",
             ls="--")
    ax2.fill_between(x, base, vaxis, where=(vaxis > base),
                     color=COLORS["lightblue"], alpha=0.4)
    ax2.fill_between(x, base, vaxis, where=(vaxis < base),
                     color="#fcd1d1", alpha=0.6)

    # threshold band
    ax2.axvspan(0.36, 0.55, color=COLORS["lightgray"], alpha=0.30)
    ax2.text(0.455, 0.745, "saturation transition", ha="center", fontsize=8.5,
             color=COLORS["gray"])

    # markers for known recipes
    rec = [
        ("CBraMod", 0.05, 0.572, "below threshold"),
        ("EMOD d3 vanilla", 0.30, 0.6194, "near threshold"),
        ("EMOD d6+aug+KD\n(SOTA)", 0.62, 0.6581, "above threshold"),
        ("10-ckpt ensemble", 0.92, 0.6948, ""),
    ]
    for lab, xc, yc, _ in rec:
        ax2.scatter([xc], [yc], s=80, c="white", edgecolors="black",
                    linewidths=1.2, zorder=4)
        ax2.text(xc, yc - 0.012, lab, ha="center", va="top", fontsize=8.0,
                 color="black", linespacing=0.95)

    ax2.text(0.13, 0.625, "V helps\n(low capacity)", color=COLORS["blue"],
             fontsize=9, ha="center", fontweight="bold")
    ax2.text(0.78, 0.660, "V hurts\n(saturated)", color=COLORS["red"],
             fontsize=9, ha="center", fontweight="bold")

    ax2.legend(loc="upper left", fontsize=9, frameon=False)

    save_dual(fig, f"{OUT}/F10_two_tier_schematic")
    print("F10 saved.")


if __name__ == "__main__":
    main()
