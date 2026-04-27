"""LF2 — EEG-LLM Cohort Circle (§4 main).

Three-panel layout:
 (a) MAIN scatter — 28 video-stim points: CLIP V-axis projection (x) vs cohort
     EEG response at PO3/γ (y), colored by 9-emotion FACED class. Linear fit
     with 95% bootstrap CI band; permutation null inset; the 9 emotional-pole
     stims (Anger×3, Amusement×3, Tenderness×3) are circled.
 (b) NULL — permutation null distribution of r vs the V-axis observation, plus
     a random-CLIP-direction control bar.
 (c) 18-LLM RANK — bar chart showing per-LLM brain-prediction r at PO3/γ for
     all 18 LLMs (Qwen-1.5B leading).

Numbers depicted (from headline_numbers.md, all_findings_catalog.md):
 - cohort r = +0.874 at PO3/γ (clip_bare_emotion → eeg_de_ridge_pred), p<10⁻⁹
 - random-direction control r ≈ 0.07
 - 18 LLMs: Qwen-1.5B leads at r=+0.411, p=0.030
"""
import os
import sys
import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from scipy.stats import pearsonr

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lf_style import apply_lf_style, COLORS, save_dual, panel_label

REPORTS = "/ibex/project/c2323/yousef/reports"
OUT = "/ibex/project/c2323/yousef/paper_neurips26_final/figures/landmark"

EMO_PER_STIM_28 = (["Anger"] * 3 + ["Disgust"] * 3 + ["Fear"] * 3 + ["Sadness"] * 3
                   + ["Neutral"] * 4 + ["Amusement"] * 3 + ["Inspiration"] * 3
                   + ["Joy"] * 3 + ["Tenderness"] * 3)
EMO_ORDER = ["Anger", "Disgust", "Fear", "Sadness", "Neutral",
             "Amusement", "Inspiration", "Joy", "Tenderness"]
# the three "emotional-pole" classes that drive the cohort r
POLE_CLASSES = {"Anger", "Amusement", "Tenderness"}


def main():
    apply_lf_style()
    with open(f"{REPORTS}/r6_eeg_llm_circle.json") as f:
        d = json.load(f)
    clip = np.array(d["per_stim"]["clip_bare_emotion_proj"])
    eeg = np.array(d["per_stim"]["eeg_de_ridge_pred"])
    rand = np.array(d["per_stim"]["clip_random_dir_proj"])

    # standardize for visualization (preserves r exactly)
    cz = (clip - clip.mean()) / clip.std()
    ez = (eeg - eeg.mean()) / eeg.std()
    rz = (rand - rand.mean()) / rand.std()

    r_obs = pearsonr(cz, ez)
    r_rand = pearsonr(rz, ez)

    # permutation null
    rng = np.random.default_rng(42)
    null = np.array([pearsonr(rng.permutation(cz), ez).statistic for _ in range(5000)])

    # 18-LLM rank
    with open(f"{REPORTS}/eeg_llm_extra/results.json") as f:
        ed = json.load(f)
    llm_rows = ed["E2_per_llm_vs_eeg"]["rows"]  # [llm, family, r, p]
    llm_rows = sorted(llm_rows, key=lambda x: x[2], reverse=True)

    fig = plt.figure(figsize=(14.0, 8.4))
    gs = fig.add_gridspec(
        2, 3,
        width_ratios=[1.6, 1.0, 1.0],
        height_ratios=[1.0, 1.0],
        wspace=0.32, hspace=0.55,
        left=0.06, right=0.985, bottom=0.07, top=0.85,
    )

    # ---------------- (a) MAIN scatter ----------------
    ax_a = fig.add_subplot(gs[:, 0])
    # plot per emotion class
    for emo in EMO_ORDER:
        idx = [i for i, e in enumerate(EMO_PER_STIM_28) if e == emo]
        ax_a.scatter(cz[idx], ez[idx], s=130, c=COLORS[emo],
                     edgecolors="white", linewidths=1.2, alpha=0.95, zorder=3,
                     label=emo)
    # circle the 9 pole stims
    for i, emo in enumerate(EMO_PER_STIM_28):
        if emo in POLE_CLASSES:
            circ = Circle((cz[i], ez[i]), 0.20, fill=False,
                          edgecolor="black", linewidth=1.4, alpha=0.55,
                          linestyle="--", zorder=4)
            ax_a.add_patch(circ)
    # fit + 95% bootstrap CI
    z_fit = np.polyfit(cz, ez, 1)
    xline = np.linspace(cz.min() - 0.2, cz.max() + 0.2, 60)
    ax_a.plot(xline, np.polyval(z_fit, xline), color="black", lw=1.6, alpha=0.65, zorder=2)
    boots = []
    for _ in range(2000):
        idx = rng.integers(0, len(cz), len(cz))
        boots.append(np.polyval(np.polyfit(cz[idx], ez[idx], 1), xline))
    boots = np.array(boots)
    ax_a.fill_between(xline,
                      np.percentile(boots, 2.5, axis=0),
                      np.percentile(boots, 97.5, axis=0),
                      color="black", alpha=0.10, zorder=1)
    # r-stat box
    ax_a.text(0.03, 0.97, f"r = +{r_obs.statistic:.3f}\np < 10⁻⁹\nn = 28 stim",
              transform=ax_a.transAxes, fontsize=14, fontweight="bold",
              color=COLORS["darkblue"], va="top",
              bbox=dict(boxstyle="round,pad=0.30", facecolor="white",
                        edgecolor=COLORS["lightgray"], linewidth=0.8, alpha=0.95))
    # subtitle annotation about pole stims
    ax_a.text(0.97, 0.18,
              "dashed circle: 9 stimuli from the three emotional poles\n"
              "(Anger × 3, Amusement × 3, Tenderness × 3) — these alone\n"
              "drive the cohort signal (n=9 → r = 0.870; n=19 mid-stim → r ≈ 0)",
              transform=ax_a.transAxes, fontsize=7.8, color=COLORS["gray"],
              va="bottom", ha="right",
              bbox=dict(boxstyle="round,pad=0.25", facecolor="white",
                        edgecolor=COLORS["lightgray"], linewidth=0.6, alpha=0.92))

    ax_a.set_xlabel("CLIP V-axis projection of stimulus description  (z)",
                    fontsize=10)
    ax_a.set_ylabel("Cohort EEG response at PO3/γ  (DE-ridge prediction, z)",
                    fontsize=10)
    ax_a.set_title("Stimulus-level alignment: LLM V-axis vs FACED EEG (n=28)",
                   loc="left", fontsize=10.5, fontweight="bold")
    panel_label(ax_a, "a", x=-0.085, y=1.025)
    ax_a.legend(loc="upper right", bbox_to_anchor=(0.99, 0.50),
                fontsize=7.8, ncol=1, frameon=False,
                title="emotion class", title_fontsize=8.0,
                handletextpad=0.4)

    # ---------------- (b) NULL distribution ----------------
    ax_b = fig.add_subplot(gs[0, 1:])
    ax_b.hist(null, bins=60, color=COLORS["lightgray"], alpha=0.95,
              edgecolor="white", lw=0.4, zorder=2)
    ax_b.axvline(r_obs.statistic, color=COLORS["red"], lw=2.4,
                 label=f"observed V-axis r = {r_obs.statistic:+.2f}", zorder=4)
    ax_b.axvline(r_rand.statistic, color=COLORS["gray"], lw=1.6, ls="--",
                 label=f"random-direction r = {r_rand.statistic:+.2f}", zorder=3)
    p95 = np.percentile(null, 95)
    p995 = np.percentile(null, 99.5)
    ax_b.axvline(p95, color="black", lw=0.8, ls=":", alpha=0.6)
    ax_b.text(p95, ax_b.get_ylim()[1] * 0.85, "  95th\n  pct.", fontsize=7,
              color=COLORS["gray"], va="top")
    ax_b.set_xlabel("Pearson r between V-axis projection and EEG response", fontsize=9.5)
    ax_b.set_ylabel("permutation count (n=5000)", fontsize=9.5)
    ax_b.set_title("Permutation null:  the alignment is not coincidence",
                   loc="left", fontsize=11, fontweight="bold")
    ax_b.legend(loc="upper left", fontsize=8.5, frameon=False)
    ax_b.set_xlim(-1.0, 1.0)
    panel_label(ax_b, "b", x=-0.085, y=1.05)

    # ---------------- (c) 18-LLM RANK ----------------
    ax_c = fig.add_subplot(gs[1, 1:])
    llm_names = [r[0] for r in llm_rows]
    llm_rs = np.array([r[2] for r in llm_rows])
    llm_ps = np.array([r[3] for r in llm_rows])
    families = [r[1] for r in llm_rows]
    family_colors = {
        "Qwen": "#1f77b4", "Mistral": "#9467bd", "Llama4": "#2ca02c",
        "Gemma": "#ff7f0e", "Gemma4": "#d4ac0d", "Pythia": "#8c564b",
        "BLOOM": "#e377c2", "TinyLlama": "#7f7f7f", "Phi2": "#17becf",
        "Qwen3.5": "#06aef0",
    }
    bar_colors = [family_colors.get(f, "#999999") for f in families]
    y = np.arange(len(llm_names))[::-1]
    bars = ax_c.barh(y, llm_rs, color=bar_colors, edgecolor="white", linewidth=0.7,
                     height=0.78, zorder=3)
    # thicker outline for Qwen-1.5B (top entry)
    bars[0].set_edgecolor("black")
    bars[0].set_linewidth(1.5)
    # value labels
    for yi, r_val, p_val in zip(y, llm_rs, llm_ps):
        sig = "*" if p_val < 0.05 else ("." if p_val < 0.10 else "")
        x_off = 0.012 if r_val >= 0 else -0.012
        ha = "left" if r_val >= 0 else "right"
        ax_c.text(r_val + x_off, yi, f"{r_val:+.2f}{sig}",
                  ha=ha, va="center", fontsize=7.5, color="black",
                  fontweight="bold" if abs(r_val) > 0.35 else "normal")
    # readable LLM labels
    pretty = []
    for n, f in zip(llm_names, families):
        # collapse internal "_multillm" tag suffix
        pn = n.replace("_multillm", "*").replace("_", "-")
        pretty.append(pn)
    ax_c.set_yticks(y)
    ax_c.set_yticklabels(pretty, fontsize=7.5)
    ax_c.axvline(0, color="black", lw=0.6, zorder=1)
    ax_c.axvline(0.30, color=COLORS["gray"], ls=":", lw=0.7, alpha=0.7, zorder=1)
    ax_c.set_xlabel("Per-LLM brain-anchor Pearson r at PO3/γ  (* p<0.05)", fontsize=9.5)
    ax_c.set_title("18 LLMs predict the same EEG signal — Qwen-1.5B leads",
                   loc="left", fontsize=11, fontweight="bold")
    panel_label(ax_c, "c", x=-0.085, y=1.05)
    # family legend
    used = []
    for f in families:
        if f not in used:
            used.append(f)
    handles = [plt.Rectangle((0, 0), 1, 1, color=family_colors.get(f, "#999")) for f in used]
    ax_c.legend(handles, used, loc="lower right", fontsize=6.5, ncol=2, frameon=False,
                title="LLM family", title_fontsize=7, handlelength=1.0, handletextpad=0.4,
                columnspacing=0.8)
    ax_c.set_xlim(-0.32, 0.55)

    # ---------------- super-title ----------------
    fig.suptitle(
        "The LLM valence axis predicts a clean, lateralised EEG response "
        "at PO3/γ across 28 stimuli and 18 LLMs",
        y=0.94, fontsize=12.5, fontweight="bold")

    save_dual(fig, f"{OUT}/lf2_eeg_llm_circle")


if __name__ == "__main__":
    main()
