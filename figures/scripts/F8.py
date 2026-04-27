"""F8 — Ensemble Theory (§8 secondary).

(a) per-checkpoint within-class V-axis r vs LOO ensemble contribution. r=+0.74, p=0.014.
(b) top-7 by within-resid → 0.6962, bottom-7 → 0.6829, random-7 baseline distribution.
"""
import os
import sys
import json
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _style import apply_style, COLORS, save_dual

REPORTS = "/ibex/project/c2323/yousef/reports"
OUT = "/ibex/project/c2323/yousef/paper_neurips26_final/figures"


def main():
    apply_style()
    with open(f"{REPORTS}/sota_ensemble_theory.json") as f:
        d = json.load(f)
    arr = d["arrays_for_plot"]
    within = np.array(arr["vaxis_within_abs_r"])
    loo = np.array(arr["loo_contrib"])
    tags = arr["tags"]
    full_ens = d["full_ensemble_bacc"]

    # top-7/bottom-7 from topk_vs_bottomk.within_resid.k7
    k7 = d["topk_vs_bottomk"]["within_resid"]["k7"]
    top_b = k7["top_bacc"]
    bot_b = k7["bot_bacc"]
    rand_mean = k7["rand_mean_bacc"]
    rand_std = k7["rand_std_bacc"]

    fig = plt.figure(figsize=(11.5, 4.6))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.1, 1.0], wspace=0.3,
                          left=0.07, right=0.985, bottom=0.13, top=0.88)

    # ---- (a) scatter ----
    ax = fig.add_subplot(gs[0, 0])
    # color by e100 vs e150
    is150 = np.array(["e150" in t for t in tags])
    ax.scatter(within[~is150], loo[~is150], s=140, c=COLORS["blue"],
               marker="o", edgecolors="white", linewidths=0.9, alpha=0.92,
               label="e100 ckpt", zorder=3)
    ax.scatter(within[is150], loo[is150], s=140, c=COLORS["darkblue"],
               marker="s", edgecolors="white", linewidths=0.9, alpha=0.92,
               label="e150 ckpt", zorder=3)
    # fit line
    z = np.polyfit(within, loo, 1)
    xline = np.linspace(within.min() - 0.005, within.max() + 0.005, 50)
    ax.plot(xline, np.polyval(z, xline), color="black", lw=1.3, alpha=0.6, zorder=2)
    # bootstrap CI
    rng = np.random.default_rng(0)
    boots = []
    for _ in range(1000):
        idx = rng.integers(0, len(within), len(within))
        boots.append(np.polyfit(within[idx], loo[idx], 1))
    yhi = np.percentile([np.polyval(b, xline) for b in boots], 97.5, axis=0)
    ylo = np.percentile([np.polyval(b, xline) for b in boots], 2.5, axis=0)
    ax.fill_between(xline, ylo, yhi, color="black", alpha=0.10, zorder=1)

    r_c = pearsonr(within, loo)
    ax.text(0.04, 0.96, f"r = +{r_c.statistic:.2f}\np = {r_c.pvalue:.3f}\nn = 10",
            transform=ax.transAxes, fontsize=14, fontweight="bold",
            color="black", va="top",
            bbox=dict(facecolor="white", edgecolor="none", alpha=0.85))

    # tag annotations
    for w, l, t in zip(within, loo, tags):
        ax.text(w + 0.001, l, t, fontsize=6.5, va="center", color=COLORS["gray"])

    ax.set_xlabel("within-class V-axis residual |r|  (per ckpt)", fontsize=10)
    ax.set_ylabel("leave-one-out ensemble contribution  Δ BACC", fontsize=10)
    ax.set_title("(a) Within-class V-axis residual predicts ensemble value",
                 loc="left", fontsize=10.5)
    ax.legend(loc="lower right", fontsize=8.5, frameon=False)

    # ---- (b) top-7 vs bot-7 vs random ----
    ax2 = fig.add_subplot(gs[0, 1])
    # random distribution as cloud (gaussian approximation)
    rand_xs = np.linspace(rand_mean - 4 * rand_std, rand_mean + 4 * rand_std, 200)
    pdf = (1.0 / (rand_std * np.sqrt(2 * np.pi))) * np.exp(-(rand_xs - rand_mean) ** 2 / (2 * rand_std ** 2))

    # show as horizontal density, baseline = full 10-ckpt ensemble
    ax2.fill_betweenx(rand_xs, 0.7, 0.7 + 0.7 * pdf / pdf.max(),
                      color=COLORS["gray"], alpha=0.30, label="random-7 ensembles\n(N=120)")
    # top / bottom / full markers
    ax2.scatter([0.4], [top_b], s=320, c=COLORS["blue"], marker="*",
                edgecolors="black", linewidths=1.0, zorder=4,
                label=f"top-7 by within-resid = {top_b:.4f}")
    ax2.scatter([0.4], [bot_b], s=160, c=COLORS["red"], marker="v",
                edgecolors="black", linewidths=1.0, zorder=4,
                label=f"bottom-7 by within-resid = {bot_b:.4f}")
    ax2.scatter([0.4], [rand_mean], s=120, c=COLORS["gray"], marker="o",
                edgecolors="black", linewidths=0.6, zorder=3,
                label=f"random-7 mean = {rand_mean:.4f}\n(σ = {rand_std:.4f})")
    ax2.axhline(full_ens, color=COLORS["darkblue"], lw=1.2, ls="--", alpha=0.7)
    ax2.text(0.05, full_ens + 0.0007, f"full 10-ckpt ensemble = {full_ens:.4f}",
             color=COLORS["darkblue"], fontsize=8.5, fontweight="bold")

    ax2.set_xlim(0, 1.6)
    ax2.set_xticks([])
    ax2.set_ylabel("ensemble FACED 9-class BACC", fontsize=10)
    ax2.set_title("(b) Selecting by V-axis residual gives a 0.013 BACC gain over the bottom-7",
                  loc="left", fontsize=10.5)
    # delta annotation
    ax2.annotate("", xy=(0.55, top_b), xytext=(0.55, bot_b),
                 arrowprops=dict(arrowstyle="<->", color=COLORS["green"], lw=1.4))
    ax2.text(0.58, (top_b + bot_b) / 2, f"+{top_b - bot_b:.4f}",
             color=COLORS["green"], fontweight="bold", fontsize=10, va="center")
    ax2.legend(loc="lower right", fontsize=7.5, frameon=False)

    save_dual(fig, f"{OUT}/F8_ensemble_theory")
    print("F8 saved.")


if __name__ == "__main__":
    main()
