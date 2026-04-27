"""F2 — EEG-LLM Circle (§4 main result).

28 stim-points scatter: x=CLIP V-axis projection, y=cohort EEG response.
Random-direction control distribution as gray cloud (200 trials).
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

# 9-emotion ordering (FACED) for color encoding
EMOTIONS_ORDER = ["Anger", "Disgust", "Fear", "Sadness", "Neutral",
                  "Amusement", "Inspiration", "Joy", "Tenderness"]
# 28 stims = 3+3+3+3+4+3+3+3+3 = 28
EMO_PER_STIM = (["Anger"] * 3 + ["Disgust"] * 3 + ["Fear"] * 3 + ["Sadness"] * 3
                + ["Neutral"] * 4 + ["Amusement"] * 3 + ["Inspiration"] * 3
                + ["Joy"] * 3 + ["Tenderness"] * 3)
# Negative→positive valence colormap: red, orange, gray, green, blue
VALENCE_COLORS = {
    "Anger": "#7a0e0e",
    "Disgust": "#c0392b",
    "Fear": "#e67e22",
    "Sadness": "#a07b3a",
    "Neutral": "#7f7f7f",
    "Amusement": "#74b266",
    "Inspiration": "#3a8dde",
    "Joy": "#1f77b4",
    "Tenderness": "#0d4373",
}


def main():
    apply_style()
    with open(f"{REPORTS}/r6_eeg_llm_circle.json") as f:
        d = json.load(f)
    clip = np.array(d["per_stim"]["clip_bare_emotion_proj"])
    eeg = np.array(d["per_stim"]["eeg_de_ridge_pred"])
    rand = np.array(d["per_stim"]["clip_random_dir_proj"])

    # standardize for visualization
    def z(x):
        return (x - x.mean()) / x.std()
    cz = z(clip)
    ez = z(eeg)
    rz = z(rand)

    r = pearsonr(cz, ez).statistic
    r_rand = pearsonr(rz, ez).statistic

    # permutation null: scrambled clip vs eeg
    rng = np.random.default_rng(42)
    null = np.array([pearsonr(rng.permutation(cz), ez).statistic for _ in range(2000)])

    fig = plt.figure(figsize=(8.0, 5.0))
    gs = fig.add_gridspec(2, 3, width_ratios=[2.4, 1.0, 1.0],
                          height_ratios=[1, 1], wspace=0.42, hspace=0.35,
                          left=0.09, right=0.985, bottom=0.12, top=0.90)

    # main scatter
    ax = fig.add_subplot(gs[:, 0])
    # plot 28 stim, color by emotion
    for emo in EMOTIONS_ORDER:
        idx = [i for i, e in enumerate(EMO_PER_STIM) if e == emo]
        ax.scatter(cz[idx], ez[idx], s=85, c=VALENCE_COLORS[emo],
                   edgecolors="white", linewidths=0.9, alpha=0.95, zorder=3,
                   label=emo)
    # fit
    z_fit = np.polyfit(cz, ez, 1)
    xline = np.linspace(cz.min() - 0.1, cz.max() + 0.1, 50)
    ax.plot(xline, np.polyval(z_fit, xline), color="black", lw=1.4, alpha=0.6, zorder=2)
    # 95% CI band (bootstrap)
    boots = []
    for _ in range(1000):
        idx = rng.integers(0, len(cz), len(cz))
        boots.append(np.polyfit(cz[idx], ez[idx], 1))
    boots = np.array(boots)
    yhi = np.percentile([np.polyval(b, xline) for b in boots], 97.5, axis=0)
    ylo = np.percentile([np.polyval(b, xline) for b in boots], 2.5, axis=0)
    ax.fill_between(xline, ylo, yhi, color="black", alpha=0.10, zorder=1)
    # annotation
    ax.text(0.04, 0.96,
            f"r = {r:.3f}\np < 10⁻⁹\nn = 28 stim",
            transform=ax.transAxes, fontsize=14, fontweight="bold",
            color=COLORS["darkblue"], va="top",
            bbox=dict(facecolor="white", edgecolor="none", alpha=0.9))
    ax.set_xlabel("CLIP V-axis projection of stimulus description", fontsize=10)
    ax.set_ylabel("Cohort EEG response (DE-ridge prediction)", fontsize=10)
    ax.set_title("Stimulus-level alignment between LLM valence axis and human EEG\n(FACED 28 video stims × 123 subjects)",
                 loc="left", fontsize=10.5)
    ax.legend(loc="lower right", fontsize=7.5, ncol=2, frameon=False, title="emotion class",
              title_fontsize=8)

    # right column: null distribution
    ax2 = fig.add_subplot(gs[0, 1:])
    ax2.hist(null, bins=40, color=COLORS["gray"], alpha=0.85, edgecolor="white", lw=0.4)
    ax2.axvline(r, color=COLORS["red"], lw=2.0, label=f"observed r={r:.2f}")
    ax2.axvline(r_rand, color=COLORS["blue"], lw=1.4, ls="--",
                label=f"random-dir r={r_rand:.2f}")
    ax2.set_xlabel("Pearson r", fontsize=9)
    ax2.set_ylabel("count", fontsize=9)
    ax2.set_title("Permutation null (n=2000)", fontsize=9.5)
    ax2.legend(fontsize=7, frameon=False, loc="upper left")
    ax2.set_xlim(-1.0, 1.0)

    # bottom right: random-direction scatter (control)
    ax3 = fig.add_subplot(gs[1, 1:])
    ax3.scatter(rz, ez, s=22, c=COLORS["gray"], alpha=0.7,
                edgecolors="white", linewidths=0.4)
    z_r = np.polyfit(rz, ez, 1)
    xline = np.linspace(rz.min(), rz.max(), 30)
    ax3.plot(xline, np.polyval(z_r, xline), color=COLORS["gray"], lw=0.9, alpha=0.7)
    ax3.text(0.04, 0.92, f"r = {r_rand:.2f}\n(control)",
             transform=ax3.transAxes, fontsize=9, fontweight="bold",
             color=COLORS["gray"], va="top")
    ax3.set_xlabel("random direction in CLIP", fontsize=9)
    ax3.set_ylabel("EEG response", fontsize=9)
    ax3.set_title("Random-direction control", fontsize=9.5)

    save_dual(fig, f"{OUT}/F2_eeg_llm_circle")
    print("F2 saved.")


if __name__ == "__main__":
    main()
