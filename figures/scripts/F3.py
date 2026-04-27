"""F3 — Cross-arch Convergence (§5 main).

(a) 36-checkpoint scatter: x=class-PC1 V-axis |r|, y=BACC. Color by architecture, shape by training-length.
(b) Random-direction null distribution histogram, V-axis observation marked at 93rd percentile.
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


def get_arch_marker(tag):
    if tag.startswith("cbramod"):
        if "ensemble" in tag:
            return "CBraMod (ensemble)", COLORS["cbra"], "*"
        return "CBraMod (single)", COLORS["cbra"], "o"
    if "e150" in tag:
        if "ensemble" in tag:
            return "EMOD d6 e150 (ensemble)", "#a83232", "*"
        return "EMOD d6 e150 (single)", "#d62728", "s"
    if "e250" in tag:
        if "ensemble" in tag:
            return "EMOD d6 e250 (ensemble)", "#9c2929", "*"
        return "EMOD d6 e250 (single)", "#ef6b6c", "^"
    # default = e100
    if "ensemble" in tag:
        return "EMOD d6 e100 (ensemble)", "#7d1f1f", "*"
    return "EMOD d6 e100 (single)", "#ff8b8b", "D"


def main():
    apply_style()
    with open(f"{REPORTS}/crossarch_random_control.json") as f:
        ctrl = json.load(f)

    bacc = np.array(ctrl["bacc"])
    abs_r = np.array(ctrl["observed"]["per_ckpt_class_pc1_abs_r_v_axis"])
    tags = ctrl["ckpt_order"]

    null_meta_r = np.array(ctrl["null_distribution"]["meta_r"])
    obs_meta_r = ctrl["observed"]["meta_r"]
    p_one = ctrl["empirical_p"]["one_sided_p"]
    pct = ctrl["empirical_p"]["observed_percentile_in_null"]

    fig = plt.figure(figsize=(11.0, 4.5))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.55, 1.0], wspace=0.35,
                          left=0.07, right=0.985, bottom=0.13, top=0.88)

    # ========== Panel (a) scatter ==========
    ax = fig.add_subplot(gs[0, 0])

    plotted_labels = set()
    for i, t in enumerate(tags):
        label, color, marker = get_arch_marker(t)
        size = 200 if marker == "*" else 70
        lab = label if label not in plotted_labels else None
        plotted_labels.add(label)
        ax.scatter(abs_r[i], bacc[i], s=size, c=color, marker=marker,
                   alpha=0.92, edgecolors="white", linewidths=0.8, zorder=3,
                   label=lab)

    # linear fit
    z_fit = np.polyfit(abs_r, bacc, 1)
    xline = np.linspace(abs_r.min() - 0.02, abs_r.max() + 0.02, 60)
    ax.plot(xline, np.polyval(z_fit, xline), color="black", lw=1.3, alpha=0.55, zorder=2)
    # bootstrap CI
    rng = np.random.default_rng(0)
    boots = []
    for _ in range(1000):
        idx = rng.integers(0, len(abs_r), len(abs_r))
        boots.append(np.polyfit(abs_r[idx], bacc[idx], 1))
    yhi = np.percentile([np.polyval(b, xline) for b in boots], 97.5, axis=0)
    ylo = np.percentile([np.polyval(b, xline) for b in boots], 2.5, axis=0)
    ax.fill_between(xline, ylo, yhi, color="black", alpha=0.10, zorder=1)

    r_corr = pearsonr(abs_r, bacc).statistic
    p_corr = pearsonr(abs_r, bacc).pvalue
    ax.text(0.04, 0.96, f"r = +{r_corr:.3f}\np = {p_corr:.1e}\nn = {len(abs_r)} ckpt",
            transform=ax.transAxes, fontsize=14, fontweight="bold",
            color="black", va="top",
            bbox=dict(facecolor="white", edgecolor="none", alpha=0.85))
    ax.set_xlabel("class-PC1 V-axis |r|  (no V-axis loss in training)", fontsize=10)
    ax.set_ylabel("FACED 9-class BACC", fontsize=10)
    ax.set_title("(a) Better EEG models encode the LLM V-axis more strongly", loc="left", fontsize=10.5)
    ax.legend(loc="lower right", fontsize=7.0, ncol=2, frameon=False)

    # ========== Panel (b) null hist ==========
    ax = fig.add_subplot(gs[0, 1])
    ax.hist(null_meta_r, bins=24, color=COLORS["gray"], alpha=0.85,
            edgecolor="white", lw=0.4)
    ax.axvline(obs_meta_r, color=COLORS["red"], lw=2.0,
               label=f"V-axis r = {obs_meta_r:.3f}")
    # mark 95th percentile
    p95 = np.percentile(null_meta_r, 95)
    ax.axvline(p95, color="black", ls="--", lw=0.9, alpha=0.5,
               label=f"95th percentile null = {p95:.2f}")
    ax.set_xlabel("Pearson r between BACC and |r|(direction)", fontsize=10)
    ax.set_ylabel("count over 100 random directions", fontsize=10)
    ax.set_title("(b) The convergence direction is the V-axis,\nnot a generic correlation",
                 loc="left", fontsize=10)
    ax.text(0.03, 0.95,
            f"observed = {pct:.0f}th\npercentile of null\n(p₁ = {p_one:.3f})",
            transform=ax.transAxes, fontsize=9.5, va="top", fontweight="bold",
            color=COLORS["red"],
            bbox=dict(facecolor="white", edgecolor="none", alpha=0.9))
    ax.legend(loc="upper right", fontsize=7.5, frameon=False,
              bbox_to_anchor=(1.0, 0.85))

    save_dual(fig, f"{OUT}/F3_crossarch_convergence")
    print("F3 saved.")


if __name__ == "__main__":
    main()
