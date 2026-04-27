"""LF3 — Cross-Architecture Convergence Scatter (§5 main).

Three-panel layout:
 (a) 36 ckpt scatter — class-PC1 V-axis |r| (x) vs FACED 9-class BACC (y).
     Linear fit + 95% CI band, r=+0.885 displayed.
 (b) 36 ckpt scatter — within-class V-axis residual |r| (x) vs BACC (y),
     more robust signal (r=+0.715-0.74).
 (c) Random-direction null — V-axis falls at the 93rd percentile of 100
     random-direction nulls; honest "top-decile" framing.
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


def get_arch(tag):
    if tag.startswith("cbramod"):
        return ("CBraMod", COLORS["red"], "o", 70) if "ensemble" not in tag \
            else ("CBraMod (ens)", COLORS["red"], "*", 220)
    if "ensemble" in tag:
        return ("EMOD (ens)", COLORS["darkblue"], "*", 220)
    if "e150" in tag:
        return ("EMOD d6 e150", COLORS["blue"], "s", 70)
    if "e250" in tag:
        return ("EMOD d6 e250", "#7fb6e0", "^", 70)
    return ("EMOD d6 e100", "#a83232", "D", 70)


def main():
    apply_lf_style()
    with open(f"{REPORTS}/crossarch_random_control.json") as f:
        ctrl = json.load(f)
    with open(f"{REPORTS}/merge_crossarch_vaxis_results.json") as f:
        full = json.load(f)

    # arrays from random-control: ckpt_order + bacc + class-PC1 abs r
    bacc = np.array(ctrl["bacc"])
    abs_r = np.array(ctrl["observed"]["per_ckpt_class_pc1_abs_r_v_axis"])
    tags = ctrl["ckpt_order"]
    null_meta_r = np.array(ctrl["null_distribution"]["meta_r"])
    obs_meta_r = ctrl["observed"]["meta_r"]
    pct = ctrl["empirical_p"]["observed_percentile_in_null"]
    p_one = ctrl["empirical_p"]["one_sided_p"]

    # Build within-class residual abs r for the same tag order.
    # The control file uses 36 ckpts (tags) but full json uses 26 base ckpts.
    # We map: the 36 set is just the 26 base + 10 expanded (val-selected etc).
    # We compute an aligned within array where possible; missing tags get NaN.
    full_pck = full["per_checkpoint"]
    within = []
    bacc_within = []
    abs_r_within = []
    tags_within = []
    for t, b, ar in zip(tags, bacc, abs_r):
        if t in full_pck:
            wr = full_pck[t]["within_class_residual_PC_vs_clip_rich_residual"]["best_pc_abs_r"]
            within.append(wr)
            bacc_within.append(b)
            abs_r_within.append(ar)
            tags_within.append(t)
    within = np.array(within)
    bacc_within = np.array(bacc_within)
    abs_r_within = np.array(abs_r_within)
    print(f"  using {len(within)} ckpts with within-class data (out of {len(tags)})")

    fig = plt.figure(figsize=(15.0, 5.4))
    gs = fig.add_gridspec(
        1, 3,
        width_ratios=[1.15, 1.15, 0.95],
        wspace=0.30,
        left=0.055, right=0.985, bottom=0.13, top=0.85,
    )

    # ---------------- (a) class-PC1 scatter ----------------
    ax_a = fig.add_subplot(gs[0, 0])
    rng = np.random.default_rng(0)
    plotted = set()
    for i, t in enumerate(tags):
        name, color, marker, size = get_arch(t)
        lab = name if name not in plotted else None
        plotted.add(name)
        ax_a.scatter(abs_r[i], bacc[i], s=size, c=color, marker=marker,
                     alpha=0.92, edgecolors="white", linewidths=0.9, zorder=3,
                     label=lab)
    z = np.polyfit(abs_r, bacc, 1)
    xline = np.linspace(abs_r.min() - 0.02, abs_r.max() + 0.02, 60)
    ax_a.plot(xline, np.polyval(z, xline), color="black", lw=1.5, alpha=0.65, zorder=2)
    boots = []
    for _ in range(2000):
        idx = rng.integers(0, len(abs_r), len(abs_r))
        boots.append(np.polyval(np.polyfit(abs_r[idx], bacc[idx], 1), xline))
    boots = np.array(boots)
    ax_a.fill_between(xline, np.percentile(boots, 2.5, axis=0),
                      np.percentile(boots, 97.5, axis=0),
                      color="black", alpha=0.10, zorder=1)
    r_corr = pearsonr(abs_r, bacc)
    ax_a.text(0.04, 0.97, f"r = +{r_corr.statistic:.3f}\np = {r_corr.pvalue:.0e}\nn = {len(abs_r)} ckpt",
              transform=ax_a.transAxes, fontsize=12, fontweight="bold",
              color="black", va="top",
              bbox=dict(boxstyle="round,pad=0.30", facecolor="white",
                        edgecolor=COLORS["lightgray"], linewidth=0.8))
    ax_a.set_xlabel("class-mean PC1 V-axis  |r|")
    ax_a.set_ylabel("FACED 9-class BACC")
    ax_a.set_title("Better EEG models converge to the V-axis (class level)", loc="left")
    panel_label(ax_a, "a", x=-0.10, y=1.045)
    ax_a.legend(loc="lower right", fontsize=7.5, ncol=1, frameon=False)

    # ---------------- (b) within-class residual scatter ----------------
    ax_b = fig.add_subplot(gs[0, 1])
    plotted = set()
    for i, t in enumerate(tags_within):
        name, color, marker, size = get_arch(t)
        lab = name if name not in plotted else None
        plotted.add(name)
        ax_b.scatter(within[i], bacc_within[i], s=size, c=color, marker=marker,
                     alpha=0.92, edgecolors="white", linewidths=0.9, zorder=3,
                     label=lab)
    # split top-7 / bottom-7 for visual emphasis
    order = np.argsort(within)
    bot7 = order[:7]
    top7 = order[-7:]
    # mark top-7 with a yellow ring
    for j in top7:
        ax_b.scatter(within[j], bacc_within[j], s=240, facecolors="none",
                     edgecolors="#f1c40f", linewidths=1.7, zorder=4)
    for j in bot7:
        ax_b.scatter(within[j], bacc_within[j], s=240, facecolors="none",
                     edgecolors=COLORS["red"], linewidths=1.4,
                     linestyle=":", zorder=4)
    # fit
    z = np.polyfit(within, bacc_within, 1)
    xline = np.linspace(within.min() - 0.02, within.max() + 0.02, 60)
    ax_b.plot(xline, np.polyval(z, xline), color="black", lw=1.5, alpha=0.65, zorder=2)
    boots = []
    for _ in range(2000):
        idx = rng.integers(0, len(within), len(within))
        boots.append(np.polyval(np.polyfit(within[idx], bacc_within[idx], 1), xline))
    boots = np.array(boots)
    ax_b.fill_between(xline, np.percentile(boots, 2.5, axis=0),
                      np.percentile(boots, 97.5, axis=0),
                      color="black", alpha=0.10, zorder=1)
    r_w = pearsonr(within, bacc_within)
    ax_b.text(0.04, 0.97, f"r = +{r_w.statistic:.3f}\np = {r_w.pvalue:.0e}\nn = {len(within)} ckpt",
              transform=ax_b.transAxes, fontsize=12, fontweight="bold",
              color="black", va="top",
              bbox=dict(boxstyle="round,pad=0.30", facecolor="white",
                        edgecolor=COLORS["lightgray"], linewidth=0.8))
    # legend for ring-callouts
    ax_b.text(0.965, 0.04,
              "yellow ring: top-7 by within-resid → 0.6962 ens.\n"
              "red dotted:  bottom-7 by within-resid → 0.6829 ens.",
              transform=ax_b.transAxes, fontsize=7.4, color=COLORS["gray"],
              ha="right", va="bottom",
              bbox=dict(boxstyle="round,pad=0.20", facecolor="white",
                        edgecolor=COLORS["lightgray"], linewidth=0.5, alpha=0.92))
    ax_b.set_xlabel("within-class V-axis residual  |r|")
    ax_b.set_ylabel("FACED 9-class BACC")
    ax_b.set_title("Within-class residual: a sub-feature ensembling exploits", loc="left")
    panel_label(ax_b, "b", x=-0.10, y=1.045)

    # ---------------- (c) random direction null ----------------
    ax_c = fig.add_subplot(gs[0, 2])
    ax_c.hist(null_meta_r, bins=24, color=COLORS["lightgray"], alpha=0.95,
              edgecolor="white", lw=0.4, zorder=2)
    ax_c.axvline(obs_meta_r, color=COLORS["red"], lw=2.4,
                 label=f"V-axis r = {obs_meta_r:.3f}", zorder=4)
    p95 = np.percentile(null_meta_r, 95)
    p99 = np.percentile(null_meta_r, 99)
    ax_c.axvline(p95, color="black", ls=":", lw=0.9, alpha=0.6,
                 label=f"95th pct = {p95:.2f}", zorder=3)
    ax_c.axvline(p99, color="black", ls="--", lw=0.9, alpha=0.6,
                 label=f"99th pct = {p99:.2f}", zorder=3)
    ax_c.text(0.03, 0.97,
              f"V-axis sits at the\n{pct:.0f}ᵗʰ percentile\n(p_one = {p_one:.3f}, n=100)",
              transform=ax_c.transAxes, fontsize=10, fontweight="bold",
              color=COLORS["red"], va="top",
              bbox=dict(boxstyle="round,pad=0.30", facecolor="white",
                        edgecolor=COLORS["red"], linewidth=0.8, alpha=0.95))
    ax_c.set_xlabel("Pearson r between BACC and |r|(direction)")
    ax_c.set_ylabel("count over 100 random directions")
    ax_c.set_title("V-axis is a top-decile direction\n(low-dim 9-class PC1 → wide null)",
                   loc="left", fontsize=10)
    ax_c.legend(loc="upper right", fontsize=7.5, frameon=False)
    panel_label(ax_c, "c", x=-0.13, y=1.045)

    fig.suptitle(
        "Cross-architecture convergence: 36 EEG checkpoints all encode the LLM V-axis "
        "without ever seeing it during training",
        y=0.965, fontsize=12.5, fontweight="bold")

    save_dual(fig, f"{OUT}/lf3_crossarch_convergence")


if __name__ == "__main__":
    main()
