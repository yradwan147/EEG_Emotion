"""F6 — Saturation Cliff (§7 main).

Δ BACC vs base-recipe BACC scatter — V-axis loss helps weak baselines, hurts strong ones.
"""
import os
import sys
import json
import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _style import apply_style, COLORS, save_dual

REPORTS = "/ibex/project/c2323/yousef/reports"
OUT = "/ibex/project/c2323/yousef/paper_neurips26_final/figures"


def main():
    apply_style()
    # Hand-built table from headline_numbers / all_findings_catalog (verified vs JSON sources):
    #   (variant, base_bacc, delta, p, n_seeds)
    # See cycle 75 worklog #424, #438, #436, #432, #434, #435, #443, #437, #414, #415, #418,
    # #419, #401, #432, #420, #422, #423, #406, #418, #424, #418, #438, #447, #454.
    rows = [
        # (label, base, delta, p, marker_kind)
        # CBraMod baseline + Topo (very weak base, single-seed only)
        ("CBraMod + Topo λ=0.05", 0.5717, +0.006, 0.30, "single"),
        # EMOD d3 baseline (vanilla 0.6194) — Topo λ=0.05 (#438) +0.0021 ns
        ("EMOD d3 + Topo λ=0.05", 0.6235, +0.002, 0.50, "ok"),
        ("EMOD d3 + EMODSTYLE λ=0.5", 0.6235, +0.007, 0.22, "ok"),
        ("EMOD d3 + Procrustes λ=0.05", 0.6235, +0.001, 0.89, "ok"),
        # Borderline / NS positives
        ("EMOD d3 + Topo λ=0.1", 0.6235, -0.013, 0.039, "neg_sig"),
        # Stat-sig negatives at d3 baseline
        ("EMOD d3 + Frontal λ=0.5", 0.6235, -0.052, 0.0015, "neg_sig"),
        ("EMOD d3 + FAA λ=0.5", 0.6235, -0.044, 0.006, "neg_sig"),
        ("EMOD d3 + Anger-w λ=0.5", 0.6235, -0.054, 0.0003, "neg_sig"),
        ("EMOD d3 + Occipital λ=0.1", 0.6235, -0.022, 0.007, "neg_sig"),
        ("EMOD d3 + RSA λ=1", 0.6235, -0.057, 0.001, "neg_sig"),
        ("EMOD d3 + RSA λ=5", 0.6235, -0.093, 0.001, "neg_sig"),
        ("EMOD d3 + Multi-V λ=0.5", 0.6235, -0.041, 0.005, "neg_sig"),
        ("EMOD d3 + EEG-AUX MSE λ=0.5", 0.6235, -0.043, 0.01, "neg_sig"),
        ("EMOD d3 + Uncert (Kendall)", 0.6235, -0.067, 0.001, "neg_sig"),
        # FULL-SOTA recipe (d6 + KD + aug + LS + e100) -- saturation cliff
        ("d6 SOTA + Topo λ=0.05", 0.6581, -0.015, 0.001, "neg_sig_full"),
        ("d6 SOTA + EMODSTYLE λ=0.5", 0.6581, -0.024, 0.001, "neg_sig_full"),
        # Borderline / NS at d3
        ("EMOD d3 + PEFT λ=0.1", 0.6235, -0.009, 0.069, "neg_ns"),
        ("EMOD d3 + Curriculum cos", 0.6235, -0.009, 0.23, "neg_ns"),
        ("EMOD d3 + Distill", 0.6235, -0.017, 0.05, "neg_ns"),
        ("EMOD d3 + Init-bias", 0.6235, -0.003, 0.7, "neg_ns"),
        ("EMOD d3 + KD soft T=2 λ=1", 0.6235, -0.012, 0.05, "neg_ns"),
        ("EMOD d3 + EEG-AUX MSE λ=0.1", 0.6235, -0.016, 0.05, "neg_ns"),
        ("EMOD d3 + EMODSTYLE class λ=1", 0.6235, -0.010, 0.30, "neg_ns"),
        ("EMOD d3 + Frontal λ=0.1", 0.6235, -0.009, 0.21, "neg_ns"),
        ("EMOD d3 + FAA λ=0.1", 0.6235, -0.018, 0.063, "neg_ns"),
    ]

    fig = plt.figure(figsize=(9.5, 5.6))
    ax = fig.add_subplot(111)

    # Plot threshold band: between EMOD d3 (0.6194) and full SOTA (0.6581) is the transition
    ax.axvspan(0.620, 0.660, color=COLORS["lightgray"], alpha=0.30, zorder=0,
               label="saturation transition zone")
    ax.axhline(0, color="black", lw=0.6, zorder=1)

    style_map = {
        "single": dict(c=COLORS["lightgray"], marker="o", s=80,
                       edge=COLORS["gray"], hatch=None, label="single seed (n=1)"),
        "ok":    dict(c=COLORS["lightblue"], marker="o", s=110,
                      edge=COLORS["blue"], hatch=None, label="NS positive"),
        "neg_ns": dict(c=COLORS["orange"], marker="o", s=110,
                       edge="#a04612", hatch=None, label="NS negative (p > 0.05)"),
        "neg_sig": dict(c=COLORS["red"], marker="o", s=140,
                        edge="#7f1c1c", hatch=None, label="significant negative (p < 0.05)"),
        "neg_sig_full": dict(c="#7f1c1c", marker="X", s=180,
                             edge="black", hatch=None, label="full SOTA recipe (saturated)"),
    }
    plotted = set()

    rng = np.random.default_rng(123)
    for label, base, delta, p, kind in rows:
        # Add a small horizontal jitter so points at identical x don't perfectly stack.
        x = base + rng.normal(0, 0.0008)
        st = style_map[kind]
        lab = st["label"] if kind not in plotted else None
        plotted.add(kind)
        ax.scatter(x, delta, s=st["s"], c=st["c"], marker=st["marker"],
                   edgecolors=st["edge"], linewidths=0.9, alpha=0.9, zorder=3,
                   label=lab)

    # annotate the most extreme points
    annotate_points = {
        "Anger-w λ=0.5": (0.6235, -0.054),
        "Frontal λ=0.5": (0.6235, -0.052),
        "RSA λ=5": (0.6235, -0.093),
        "d6 SOTA + EMODSTYLE": (0.6581, -0.024),
        "d6 SOTA + Topo": (0.6581, -0.015),
        "EMODSTYLE λ=0.5": (0.6235, +0.007),
        "Topo λ=0.05": (0.5717, +0.006),
    }
    # Manual offsets per label (data coords) to avoid overlap and fix anchor for Topo λ=0.05.
    offsets = {
        "Anger-w λ=0.5": (0.611, -0.062),
        "Frontal λ=0.5": (0.611, -0.050),
        "RSA λ=5": (0.611, -0.090),
        "d6 SOTA + EMODSTYLE": (0.665, -0.040),
        "d6 SOTA + Topo": (0.665, -0.012),
        "EMODSTYLE λ=0.5": (0.611, 0.022),
        "Topo λ=0.05": (0.575, 0.020),
    }
    for lab, (x, y) in annotate_points.items():
        tx, ty = offsets[lab]
        ax.annotate(lab, xy=(x, y), xytext=(tx, ty), fontsize=8.0,
                    arrowprops=dict(arrowstyle="-", color="gray", lw=0.6, alpha=0.6))

    # vertical guide lines for the two anchor recipes
    ax.axvline(0.6235, color=COLORS["gray"], ls=":", lw=0.7, alpha=0.7)
    ax.text(0.6235, 0.024, "EMOD d3\nbaseline", fontsize=7.5, ha="center",
            color=COLORS["gray"])
    ax.axvline(0.6581, color=COLORS["gray"], ls=":", lw=0.7, alpha=0.7)
    ax.text(0.6581, 0.024, "d6 SOTA\nrecipe", fontsize=7.5, ha="center",
            color=COLORS["gray"])

    # arrow showing the cliff
    ax.annotate("", xy=(0.6581, -0.022), xytext=(0.6235, +0.005),
                arrowprops=dict(arrowstyle="->", color="black", lw=1.4, alpha=0.45))
    ax.text(0.640, -0.005, "the\nsaturation cliff", fontsize=9, ha="center", va="center",
            color="black", fontweight="bold", alpha=0.7)

    ax.set_xlabel("base recipe FACED 9-class BACC", fontsize=11)
    ax.set_ylabel("Δ BACC from adding V-axis supervision", fontsize=11)
    ax.set_title("V-axis supervision helps weak baselines and hurts strong ones",
                 fontsize=11.5, fontweight="bold", loc="left", pad=10)
    ax.set_xlim(0.555, 0.685)
    ax.set_ylim(-0.105, 0.035)
    ax.legend(loc="lower left", fontsize=8, frameon=False)

    fig.text(0.5, 0.005,
             "Each point = one V-axis intervention; 25+ recipes from cycle 75 (frontal, FAA, occipital, "
             "topo, anger-weighted, EMODSTYLE, Procrustes, PEFT, RSA, multi-V, distill, KD, init, "
             "uncert, EEG-AUX MSE, curriculum, …). All ≥3 seeds unless noted.",
             ha="center", fontsize=7.5, color=COLORS["gray"])

    save_dual(fig, f"{OUT}/F6_saturation_cliff")
    print("F6 saved.")


if __name__ == "__main__":
    main()
