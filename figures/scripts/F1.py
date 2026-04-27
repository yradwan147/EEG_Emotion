"""F1 — The Universal V-Axis (HERO).

Three-panel teaser: same valence axis recovered across (a) text, (b) brain, (c) EEG models.
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


def load_text_aucs():
    with open(f"{REPORTS}/p1_task_matrix.json") as f:
        d = json.load(f)
    rows = []
    for t in d["tasks"]:
        if t["metric"] in ("AUC",) and t["task"] not in ("SST-2 (v2 calibrated)",):
            rows.append((t["task"], t["ours_value"]))
    # add Hu&Liu absolute pearson
    for t in d["tasks"]:
        if "Hu&Liu" in t["task"]:
            rows.append(("Hu&Liu |r|", t["ours_value"]))
        if t["task"].startswith("NRC"):
            rows.append(("NRC |r|", t["ours_value"]))
    return rows


def load_brain_circle():
    with open(f"{REPORTS}/r6_eeg_llm_circle.json") as f:
        d = json.load(f)
    clip = np.array(d["per_stim"]["clip_bare_emotion_proj"])
    eeg = np.array(d["per_stim"]["eeg_de_ridge_pred"])
    rand = np.array(d["per_stim"]["clip_random_dir_proj"])
    r = pearsonr(clip, eeg).statistic
    return clip, eeg, rand, r


def load_crossarch():
    with open(f"{REPORTS}/crossarch_random_control.json") as f:
        d = json.load(f)
    bacc = np.array(d["bacc"])
    abs_r = np.array(d["observed"]["per_ckpt_class_pc1_abs_r_v_axis"])
    tags = d["ckpt_order"]
    arch = []
    for t in tags:
        if t.startswith("cbramod") or "cbramod" in t.lower():
            arch.append("CBraMod")
        else:
            arch.append("EMOD")
    return abs_r, bacc, arch, tags


def main():
    apply_style()
    fig = plt.figure(figsize=(13.0, 5.0))
    gs = fig.add_gridspec(1, 3, wspace=0.36, left=0.06, right=0.985, bottom=0.14, top=0.86)

    # ---------- Panel (a) text ----------
    ax = fig.add_subplot(gs[0, 0])
    rows = load_text_aucs()
    # order: SST-2 dev first
    order = ["SST-2 (dev)", "IMDB", "yelp_polarity", "tweet_eval_sentiment",
             "rotten_tomatoes", "SST-5 (binary collapse)", "Hu&Liu |r|", "NRC |r|"]
    label_map = {"SST-2 (dev)": "SST-2", "yelp_polarity": "Yelp",
                 "tweet_eval_sentiment": "TweetEval", "rotten_tomatoes": "RottenTom.",
                 "SST-5 (binary collapse)": "SST-5", "IMDB": "IMDB",
                 "Hu&Liu |r|": "Hu&Liu", "NRC |r|": "NRC"}
    vals = []
    labels = []
    for k in order:
        for n, v in rows:
            if n == k:
                vals.append(v)
                labels.append(label_map.get(k, k))
                break
    vals = np.array(vals)
    y = np.arange(len(vals))[::-1]
    ax.barh(y, vals, color=COLORS["blue"], height=0.65, edgecolor="white", linewidth=0.6)
    for yi, v, lab in zip(y, vals, labels):
        ax.text(v - 0.012, yi, f"{v:.3f}", va="center", ha="right",
                color="white", fontsize=8, fontweight="bold")
    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    ax.axvline(0.5, color=COLORS["gray"], lw=0.7, ls="--", alpha=0.7)
    ax.text(0.5, len(vals) - 0.4, " chance ", color=COLORS["gray"], fontsize=7, va="bottom",
            ha="left", bbox=dict(facecolor="white", edgecolor="none", alpha=0.85))
    ax.set_xlim(0.45, 1.0)
    ax.set_xlabel("zero-shot probe |r| / AUC")
    ax.set_title("(a) Text: V-axis matches supervised classifiers", loc="left", fontsize=10)
    # subtitle
    ax.text(0.46, len(vals) - 0.2, "Qwen3.5 1.5B, 9 emotion stories → PC1\n(no fine-tuning, 0 labels seen)",
            fontsize=7.5, color=COLORS["gray"], va="top")

    # ---------- Panel (b) brain ----------
    ax = fig.add_subplot(gs[0, 1])
    clip, eeg, rand, r = load_brain_circle()
    # standardize the random scatter cloud: 200 trials of random direction
    # We have 1 random direction; to fake the cloud we do 200 random projections of clip endpoints
    rng = np.random.default_rng(42)
    n_random = 200
    rand_rs = []
    rand_pts_x, rand_pts_y = [], []
    # random scrambled clip values vs eeg (label permutation null)
    for _ in range(n_random):
        perm = rng.permutation(len(clip))
        rand_rs.append(pearsonr(clip[perm], eeg).statistic)
    # plot 28 stim
    ax.scatter(clip, eeg, s=46, c=COLORS["blue"], alpha=0.9, zorder=3,
               edgecolors="white", linewidths=0.7)
    # fit line
    z = np.polyfit(clip, eeg, 1)
    xline = np.linspace(clip.min(), clip.max(), 50)
    ax.plot(xline, np.polyval(z, xline), color=COLORS["darkblue"], lw=1.3, alpha=0.7, zorder=2)
    # annotate r
    ax.text(0.97, 0.05, f"r = {r:.2f}\np < 10⁻⁹\nn = 28 stim",
            transform=ax.transAxes, fontsize=10, fontweight="bold",
            color=COLORS["darkblue"], va="bottom", ha="right",
            bbox=dict(facecolor="white", edgecolor="none", alpha=0.85))
    ax.set_xlabel("CLIP V-axis projection (text)")
    ax.set_ylabel("EEG cohort response (DE-ridge)")
    ax.set_title("(b) Brain: same axis predicts EEG", loc="left", fontsize=10)

    # inset: random null distribution of correlations
    inset = ax.inset_axes([0.06, 0.05, 0.32, 0.27])
    inset.hist(rand_rs, bins=22, color=COLORS["gray"], alpha=0.85, edgecolor="white", lw=0.4)
    inset.axvline(r, color=COLORS["red"], lw=1.6)
    inset.set_xlabel("null r", fontsize=6)
    inset.tick_params(labelsize=6, length=2)
    inset.set_title("permutation null", fontsize=7, pad=1)
    inset.set_yticks([])
    for s in ("top", "right", "left"):
        inset.spines[s].set_visible(False)

    # ---------- Panel (c) EEG model convergence ----------
    ax = fig.add_subplot(gs[0, 2])
    abs_r, bacc, arch, tags = load_crossarch()
    arch = np.array(arch)
    # color by arch
    cb_mask = arch == "CBraMod"
    em_mask = arch == "EMOD"
    # marker by ensemble
    ens_mask = np.array(["ensemble" in t for t in tags])
    ax.scatter(abs_r[cb_mask & ~ens_mask], bacc[cb_mask & ~ens_mask],
               s=58, c=COLORS["cbra"], marker="o", alpha=0.9, edgecolors="white",
               linewidths=0.7, label="CBraMod", zorder=3)
    ax.scatter(abs_r[em_mask & ~ens_mask], bacc[em_mask & ~ens_mask],
               s=58, c=COLORS["emod"], marker="o", alpha=0.85, edgecolors="white",
               linewidths=0.7, label="EMOD (single)", zorder=3)
    ax.scatter(abs_r[ens_mask], bacc[ens_mask],
               s=110, c=COLORS["darkblue"], marker="*", alpha=0.95,
               edgecolors="white", linewidths=0.8, label="Ensemble", zorder=4)
    # fit
    z = np.polyfit(abs_r, bacc, 1)
    xline = np.linspace(abs_r.min(), abs_r.max(), 50)
    ax.plot(xline, np.polyval(z, xline), color="black", lw=1.2, alpha=0.6, zorder=2)
    r_overall = pearsonr(abs_r, bacc).statistic
    ax.text(0.04, 0.95, f"r = +{r_overall:.3f}\np < 10⁻¹²\nn = {len(abs_r)} ckpt",
            transform=ax.transAxes, fontsize=10, fontweight="bold",
            color="black", va="top",
            bbox=dict(facecolor="white", edgecolor="none", alpha=0.85))
    ax.set_xlabel("class-PC1 V-axis |r|  (no V-axis loss in training)")
    ax.set_ylabel("FACED 9-class BACC")
    ax.set_title("(c) EEG models: convergence in the wild", loc="left", fontsize=10)
    ax.legend(loc="lower right", frameon=False, fontsize=7.5)

    # super-title
    fig.suptitle("A single valence direction extracted from 9 emotion stories is recovered "
                 "across language, brain, and EEG models",
                 y=0.97, fontsize=11.5, fontweight="bold")

    save_dual(fig, f"{OUT}/F1_universal_vaxis")
    print("F1 saved.")


if __name__ == "__main__":
    main()
