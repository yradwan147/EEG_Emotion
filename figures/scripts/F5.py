"""F5 — Anger Contrast / 9-Stim Story (§6 sub).

(a) Drop-class diagnostic bar chart: Δ cohort r when class removed. Highlight Anger.
(b) Per-subject distribution histograms: cohort r=0.48 (fixed), per-subj r=−0.06 (Simpson), oracle |r|=0.62.
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
    with open(f"{REPORTS}/eeg_llm_extra/results.json") as f:
        d_extra = json.load(f)
    with open(f"{REPORTS}/merge_followup_ceiling/results.json") as f:
        d_ceiling = json.load(f)

    fig = plt.figure(figsize=(11.5, 4.5))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.0, 1.4], wspace=0.30,
                          left=0.07, right=0.985, bottom=0.13, top=0.88)

    # ---- Panel (a) drop-class bar ----
    ax = fig.add_subplot(gs[0, 0])
    classes = [c["emotion"] for c in d_extra["D_per_emotion"]["per_class"]]
    deltas = [c["delta_when_drop"] for c in d_extra["D_per_emotion"]["per_class"]]
    deltas = np.array(deltas)
    # sort: most negative left
    order = np.argsort(deltas)
    classes = np.array(classes)[order]
    deltas = deltas[order]
    base = d_extra["D_per_emotion"]["cohort_r"]
    ax.set_title("(a) Anger drives a third of cohort V-axis encoding", loc="left", fontsize=10.5)
    colors = [COLORS["red"] if v < -0.1 else (COLORS["lightblue"] if v < 0 else COLORS["lightgray"])
              for v in deltas]
    bars = ax.bar(np.arange(len(classes)), deltas, color=colors,
                  edgecolor="white", linewidth=0.8)
    ax.axhline(0, color="black", lw=0.6)
    for i, (c, v) in enumerate(zip(classes, deltas)):
        ax.text(i, v + (0.005 if v >= 0 else -0.005),
                f"{v:+.3f}", ha="center", va="bottom" if v >= 0 else "top",
                fontsize=7.5,
                color=COLORS["red"] if v < -0.1 else "black",
                fontweight="bold" if v < -0.1 else "normal")
    ax.set_xticks(np.arange(len(classes)))
    ax.set_xticklabels(classes, rotation=35, ha="right", fontsize=8)
    ax.set_ylabel("Δ cohort r when class is dropped", fontsize=10)
    # baseline annotation
    ax.text(0.97, 0.95, f"baseline cohort r = {base:.3f}\n(PO3, γ band, all 28 stims)",
            transform=ax.transAxes, ha="right", va="top", fontsize=8.5,
            color=COLORS["gray"])
    # arrow on Anger
    anger_i = list(classes).index("Anger")
    ax.annotate("Anger removed\n→ r drops by 0.151\n(32% of total)",
                xy=(anger_i + 0.35, deltas[anger_i] + 0.020),
                xytext=(len(classes) - 0.6, deltas[anger_i] + 0.045),
                fontsize=9, color=COLORS["red"], fontweight="bold", ha="right",
                arrowprops=dict(arrowstyle="->", color=COLORS["red"], lw=1.0,
                                connectionstyle="arc3,rad=-0.3"))

    # ---- Panel (b) per-subject ----
    ax = fig.add_subplot(gs[0, 1])
    rs_fixed = np.array(d_ceiling["analysis_2_per_subject_ceiling"]["rs_fixed"])
    rs_oracle_gamma = np.array(d_ceiling["analysis_2_per_subject_ceiling"]["rs_oracle_gamma"])
    rs_oracle_all = np.array(d_ceiling["analysis_2_per_subject_ceiling"]["rs_oracle_allbands"])

    bins = np.linspace(-1, 1, 41)
    ax.hist(rs_fixed, bins=bins, color=COLORS["lightblue"], alpha=0.85,
            edgecolor=COLORS["blue"], linewidth=0.7,
            label=f"fixed channels (PO3 etc.)  mean = {rs_fixed.mean():+.2f}")
    ax.hist(rs_oracle_gamma, bins=bins,
            edgecolor=COLORS["orange"], linewidth=1.4, histtype="step",
            label=f"oracle channel (γ)         |r| = {np.abs(rs_oracle_gamma).mean():.2f}")
    ax.hist(rs_oracle_all, bins=bins,
            edgecolor=COLORS["darkblue"], linewidth=1.4, histtype="step", linestyle="--",
            label=f"oracle channel × band     |r| = {np.abs(rs_oracle_all).mean():.2f}")

    ax.axvline(0, color="black", lw=0.6, alpha=0.4)
    # cohort marker
    ax.axvline(0.478, color=COLORS["red"], lw=1.6, ls=":",
               label="cohort r at PO3/γ = 0.48")

    ax.set_xlabel("per-subject Pearson r (V-axis vs EEG)", fontsize=10)
    ax.set_ylabel("count of subjects (n=123)", fontsize=10)
    ax.set_title("(b) Simpson's paradox: cohort hides per-subject scatter,\noracle reveals real ceiling",
                 loc="left", fontsize=10.5)
    ax.legend(loc="upper right", fontsize=7.5, frameon=False)

    save_dual(fig, f"{OUT}/F5_anger_per_subject")
    print("F5 saved.")


if __name__ == "__main__":
    main()
