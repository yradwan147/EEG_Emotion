"""LF8 — Two-Tier Ensemble Theory Scatter (§5 secondary, §8 mechanism).

Per-checkpoint within-residual |r| (x) vs LOO ensemble contribution Δ (y),
n=10, with the Pearson r=+0.74, p=0.014 prominently displayed.
Linear fit + 95% CI band. Top-7 vs bottom-7 by within-resid highlighted.

Right panel: comparing the resulting top-7 / bot-7 / random-7 ensembles in
balanced accuracy.
"""
import os
import sys
import json
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lf_style import apply_lf_style, COLORS, save_dual, panel_label

REPORTS = "/ibex/project/c2323/yousef/reports"
OUT = "/ibex/project/c2323/yousef/paper_neurips26_final/figures/landmark"
OUT_PAPER = "/ibex/project/c2323/yousef/EEG_Emotion/figures/landmark"


def main():
    apply_lf_style()
    with open(f"{REPORTS}/sota_ensemble_theory.json") as f:
        d = json.load(f)
    arr = d["arrays_for_plot"]
    within = np.array(arr["vaxis_within_abs_r"])
    loo = np.array(arr["loo_contrib"])
    tags = arr["tags"]
    full_ens = d["full_ensemble_bacc"]

    # top-7 / bot-7 by within_resid
    k7 = d["topk_vs_bottomk"]["within_resid"]["k7"]
    top_b = k7["top_bacc"]
    bot_b = k7["bot_bacc"]
    rand_mean = k7["rand_mean_bacc"]
    rand_std = k7["rand_std_bacc"]

    fig = plt.figure(figsize=(13.8, 6.0))
    gs = fig.add_gridspec(
        1, 2,
        width_ratios=[1.5, 1.0],
        wspace=0.28,
        left=0.06, right=0.985, bottom=0.13, top=0.84,
    )

    # ---------------- (a) scatter ----------------
    ax_a = fig.add_subplot(gs[0, 0])
    is150 = np.array(["e150" in t for t in tags])
    # split top-7/bot-7 by within
    order = np.argsort(within)
    top7_idx = set(order[-7:].tolist())
    bot7_idx = set(order[:7].tolist())

    # plot
    for i, t in enumerate(tags):
        c = COLORS["darkblue"] if is150[i] else COLORS["blue"]
        marker = "s" if is150[i] else "o"
        ax_a.scatter(within[i], loo[i], s=170, c=c, marker=marker,
                     edgecolors="white", linewidths=1.0, alpha=0.92, zorder=3)
        # rings
        if i in top7_idx:
            ax_a.scatter(within[i], loo[i], s=290, facecolors="none",
                         edgecolors="#f1c40f", linewidths=1.8, zorder=4)
        if i in bot7_idx:
            ax_a.scatter(within[i], loo[i], s=290, facecolors="none",
                         edgecolors=COLORS["red"], linewidths=1.4,
                         linestyle=":", zorder=4)

    # legend handles (manual since we did custom plotting)
    legend_handles = [
        plt.Line2D([0], [0], marker="o", color="w", markerfacecolor=COLORS["blue"],
                   markersize=11, label="e100 ckpt"),
        plt.Line2D([0], [0], marker="s", color="w", markerfacecolor=COLORS["darkblue"],
                   markersize=11, label="e150 ckpt"),
        plt.Line2D([0], [0], marker="o", color="w", markerfacecolor="none",
                   markeredgecolor="#f1c40f", markeredgewidth=1.8, markersize=14,
                   label="top-7 by within-resid"),
        plt.Line2D([0], [0], marker="o", color="w", markerfacecolor="none",
                   markeredgecolor=COLORS["red"], markeredgewidth=1.2,
                   linestyle=":", markersize=14, label="bottom-7 by within-resid"),
    ]

    # fit + 95% CI
    z = np.polyfit(within, loo, 1)
    xline = np.linspace(within.min() - 0.005, within.max() + 0.005, 60)
    ax_a.plot(xline, np.polyval(z, xline), color="black", lw=1.6, alpha=0.65, zorder=2)
    rng = np.random.default_rng(0)
    boots = []
    for _ in range(2000):
        idx = rng.integers(0, len(within), len(within))
        boots.append(np.polyval(np.polyfit(within[idx], loo[idx], 1), xline))
    boots = np.array(boots)
    ax_a.fill_between(xline, np.percentile(boots, 2.5, axis=0),
                      np.percentile(boots, 97.5, axis=0),
                      color="black", alpha=0.10, zorder=1)
    r_c = pearsonr(within, loo)
    ax_a.text(0.04, 0.97, f"r = +{r_c.statistic:.3f}\np = {r_c.pvalue:.3f}\nn = {len(within)} ckpt",
              transform=ax_a.transAxes, fontsize=14, fontweight="bold",
              color="black", va="top",
              bbox=dict(boxstyle="round,pad=0.30", facecolor="white",
                        edgecolor=COLORS["lightgray"], linewidth=0.8))
    # tag annotations — hand-tuned offsets so labels don't pile up.
    # Layout: place each tag adjacent to its point in a non-overlapping
    # spoke pattern around the central cluster.
    label_offsets = {
        # tag             dx        dy        ha       va
        "e100_s42":    (-0.004,  +0.0008, "right", "bottom"),
        "e100_s123":   (+0.003,  -0.0008, "left",  "top"),
        "e100_s456":   (-0.004,  -0.0009, "right", "top"),
        "e100_s789":   (+0.003,  -0.0009, "left",  "top"),
        "e100_s2025":  (-0.004,  +0.0009, "right", "bottom"),
        "e150_s42":    (+0.003,  +0.0010, "left",  "bottom"),
        "e150_s123":   (-0.001,  +0.0010, "right", "bottom"),
        "e150_s456":   (+0.003,  +0.0009, "left",  "bottom"),
        "e150_s789":   (-0.001,  +0.0010, "right", "bottom"),
        "e150_s2025":  (+0.003,  -0.0009, "left",  "top"),
    }
    for w, l, t in zip(within, loo, tags):
        dx, dy, ha, va = label_offsets.get(
            t, (+0.003, +0.0001, "left", "center"))
        ax_a.text(w + dx, l + dy, t,
                  fontsize=7.0, color="#444444", ha=ha, va=va,
                  zorder=6)

    ax_a.set_xlabel("within-class V-axis residual |r|  (per ckpt)", fontsize=10.5)
    ax_a.set_ylabel("leave-one-out ensemble contribution  Δ BACC", fontsize=10.5)
    ax_a.set_title("Within-class V-axis residual predicts ensemble value",
                   loc="left", fontsize=11.5)
    panel_label(ax_a, "a", x=-0.075, y=1.04)
    ax_a.legend(handles=legend_handles, loc="lower right", fontsize=8.5, frameon=False)

    # ---------------- (b) bacc comparison ----------------
    ax_b = fig.add_subplot(gs[0, 1])
    # vertical scatter with horizontal categories
    cats = [
        ("bottom-7\n(within-resid)", bot_b, COLORS["red"]),
        ("random-7\n(N=120)",        rand_mean, COLORS["gray"]),
        ("top-7\n(within-resid)",    top_b, "#1f77b4"),
        ("full 10-ckpt\nensemble (SOTA)",  full_ens, COLORS["darkblue"]),
    ]
    xs = np.arange(len(cats))
    ys = [c[1] for c in cats]
    cs = [c[2] for c in cats]
    bars = ax_b.bar(xs, ys, color=cs, width=0.55, edgecolor="white", linewidth=0.8,
                    zorder=3)
    # Random-7 with error bar (gaussian)
    ax_b.errorbar([1], [rand_mean], yerr=rand_std, color="black", capsize=4,
                  elinewidth=1.2, zorder=4)
    # value labels
    for x, c in zip(xs, cats):
        ax_b.text(x, c[1] + 0.0015, f"{c[1]:.4f}", ha="center", va="bottom",
                  fontsize=10.5, fontweight="bold")
    ax_b.set_xticks(xs)
    ax_b.set_xticklabels([c[0] for c in cats], fontsize=9, linespacing=0.95)
    ax_b.set_ylabel("FACED 9-class BACC (test)", fontsize=10.5)
    ax_b.set_ylim(0.670, 0.704)

    # delta annotation top vs bot
    ax_b.annotate("", xy=(2, top_b - 0.0007), xytext=(0, bot_b - 0.0007),
                  arrowprops=dict(arrowstyle="<->", color=COLORS["green"], lw=1.6))
    ax_b.text(1, (top_b + bot_b) / 2 - 0.001, f"+{top_b - bot_b:.4f}",
              color=COLORS["green"], fontweight="bold", fontsize=10.5,
              ha="center", va="center",
              bbox=dict(boxstyle="round,pad=0.20", facecolor="white",
                        edgecolor=COLORS["green"], lw=0.8))
    ax_b.set_title("Selecting by within-resid > random > bottom-7",
                   loc="left", fontsize=11.5)
    panel_label(ax_b, "b", x=-0.13, y=1.04)

    fig.suptitle(
        "Two-tier theory:  the ensemble gain lives in the within-class V-axis "
        "residual that diversifies across checkpoints",
        y=0.96, fontsize=12.5, fontweight="bold")

    save_dual(fig, f"{OUT}/lf8_two_tier_ensemble_theory")
    save_dual(fig, f"{OUT_PAPER}/lf8_two_tier_ensemble_theory")


if __name__ == "__main__":
    main()
