"""LF1 — Universal V-Axis Hero (teaser / abstract page).

The single figure that explains the whole paper: one valence direction,
extracted once from 9 short emotion stories, lights up the same way across
language, vision, EEG, and brain.

Four panels:
 (a) Text  — V-axis matches supervised classifiers (8 sentiment/lexicon tasks).
 (b) Vision — V-axis BEATS supervised ridge on OASIS valence (from CLIP).
 (c) EEG models — 36 checkpoints; better BACC ⇔ stronger V-axis encoding.
 (d) Brain  — 28 stim-points: CLIP V-axis projection vs FACED EEG cohort response.

The vision dot in (b) is the single best supervised-beating finding. The
brain dot in (d) is the headline cohort r=0.87 (p<10⁻⁹).
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


# ---------------------- data loaders ----------------------

def load_text_aucs():
    with open(f"{REPORTS}/p1_task_matrix.json") as f:
        d = json.load(f)
    by_name = {t["task"]: t for t in d["tasks"]}
    rows = [
        ("SST-2",       by_name["SST-2 (dev)"]["ours_value"], "AUC"),
        ("IMDB",        by_name["IMDB"]["ours_value"], "AUC"),
        ("Yelp",        by_name["yelp_polarity"]["ours_value"], "AUC"),
        ("TweetEval",   by_name["tweet_eval_sentiment"]["ours_value"], "AUC"),
        ("RottenTom.",  by_name["rotten_tomatoes"]["ours_value"], "AUC"),
        ("SST-5 binary",by_name["SST-5 (binary collapse)"]["ours_value"], "AUC"),
        ("Hu&Liu lex.", by_name["Hu&Liu-style lexicon (6.8k)"]["ours_value"], "|r|"),
        ("Warriner V",  by_name["Warriner 2013 (3k sampled)"]["ours_value"], "|r|"),
    ]
    return rows


def load_vision():
    with open(f"{REPORTS}/p1_vision_based_v_axis.json") as f:
        d = json.load(f)
    return {
        "vaxis": d["strategy_A_quantile9"]["test_pearson_valence"],
        "ridge": d["supervised_ridge_upper_bound"]["test_pearson_valence"],
        "rand":  d["random_direction_baseline"]["test_pearson_valence"],
        "n":     d["strategy_A_quantile9"]["n_test"],
    }


def load_crossarch():
    with open(f"{REPORTS}/crossarch_random_control.json") as f:
        d = json.load(f)
    bacc = np.array(d["bacc"])
    abs_r = np.array(d["observed"]["per_ckpt_class_pc1_abs_r_v_axis"])
    tags = d["ckpt_order"]
    return abs_r, bacc, tags


def load_brain_circle():
    with open(f"{REPORTS}/r6_eeg_llm_circle.json") as f:
        d = json.load(f)
    clip = np.array(d["per_stim"]["clip_bare_emotion_proj"])
    eeg = np.array(d["per_stim"]["eeg_de_ridge_pred"])
    rand = np.array(d["per_stim"]["clip_random_dir_proj"])
    return clip, eeg, rand


# ---------------------- helpers ----------------------

EMO_PER_STIM_28 = (["Anger"] * 3 + ["Disgust"] * 3 + ["Fear"] * 3 + ["Sadness"] * 3
                   + ["Neutral"] * 4 + ["Amusement"] * 3 + ["Inspiration"] * 3
                   + ["Joy"] * 3 + ["Tenderness"] * 3)
EMO_ORDER = ["Anger", "Disgust", "Fear", "Sadness", "Neutral",
             "Amusement", "Inspiration", "Joy", "Tenderness"]


def main():
    apply_lf_style()
    fig = plt.figure(figsize=(14.2, 9.6))
    gs = fig.add_gridspec(
        2, 2,
        width_ratios=[1.05, 1.05],
        height_ratios=[1.0, 1.0],
        wspace=0.34, hspace=0.55,
        left=0.065, right=0.985, bottom=0.10, top=0.86,
    )

    # ---------------- (a) TEXT ----------------
    ax_a = fig.add_subplot(gs[0, 0])
    rows = load_text_aucs()
    labels = [r[0] for r in rows]
    vals = np.array([r[1] for r in rows])
    units = [r[2] for r in rows]
    y = np.arange(len(rows))[::-1]
    bars = ax_a.barh(y, vals, color=COLORS["recipe"], height=0.62,
                     edgecolor="white", linewidth=0.8, zorder=3)
    for yi, v, lab, u in zip(y, vals, labels, units):
        ax_a.text(v - 0.012, yi, f"{v:.2f}", va="center", ha="right",
                  color="white", fontsize=8.5, fontweight="bold", zorder=4)
        ax_a.text(0.453, yi, f"{u}", va="center", ha="left",
                  color=COLORS["gray"], fontsize=7.0)
    ax_a.set_yticks(y)
    ax_a.set_yticklabels(labels)
    ax_a.axvline(0.5, color=COLORS["gray"], lw=0.7, ls="--", alpha=0.7, zorder=2)
    ax_a.text(0.502, len(rows) - 0.4, "chance", color=COLORS["gray"], fontsize=7.5,
              va="center", ha="left")
    ax_a.set_xlim(0.45, 1.0)
    ax_a.set_ylim(-0.7, len(rows) - 0.3)
    ax_a.set_xlabel("zero-shot probe score (AUC for binary tasks, |r| for lexicons)")
    ax_a.set_title("Text:  one direction matches supervised sentiment classifiers", loc="left")
    panel_label(ax_a, "a", x=-0.18, y=1.04)
    # caption moved BELOW the x-axis label so it cannot collide with bar value labels
    ax_a.text(0.5, -0.24,
              "9 emotion stories  →  PCA  →  V-axis     (0 fine-tuning, 0 sentiment labels seen)",
              transform=ax_a.transAxes,
              fontsize=7.6, color=COLORS["gray"], va="top", ha="center", style="italic")

    # ---------------- (b) VISION ----------------
    ax_b = fig.add_subplot(gs[0, 1])
    v = load_vision()
    bars_x = ["random\ndirection", "supervised\nridge\n(upper bound)", "V-axis\n(zero-shot,\nthis paper)"]
    bars_y = [v["rand"], v["ridge"], v["vaxis"]]
    bar_colors = [COLORS["lightgray"], COLORS["gray"], COLORS["pos_sig"]]
    edge_colors = [COLORS["gray"], "black", "#1a5e1a"]
    bx = np.arange(len(bars_x))
    bs = ax_b.bar(bx, bars_y, color=bar_colors, edgecolor=edge_colors,
                  linewidth=1.0, width=0.62, zorder=3)
    for xi, vv in zip(bx, bars_y):
        if vv >= 0:
            ax_b.text(xi, vv + 0.02, f"r = {vv:+.3f}", ha="center", va="bottom",
                      fontsize=10, fontweight="bold")
        else:
            ax_b.text(xi, vv - 0.02, f"r = {vv:+.3f}", ha="center", va="top",
                      fontsize=10, fontweight="bold", color=COLORS["red"])
    ax_b.axhline(0, color="black", lw=0.7, zorder=1)
    # V-axis beats supervised by this amount
    delta = v["vaxis"] - v["ridge"]
    # short arrow from ridge bar (1) up to V-axis bar (2), placed in the
    # MIDDLE of the bars so it does not collide with bar-tip "r = +x.xxx" labels
    ax_b.annotate("",
                  xy=(2, v["vaxis"] - 0.18), xytext=(1, v["ridge"] - 0.18),
                  arrowprops=dict(arrowstyle="->", color=COLORS["green"], lw=1.6))
    ax_b.text(1.5, (v["vaxis"] + v["ridge"]) / 2 - 0.32,
              f"+{delta:.3f}\nbeats supervised",
              color=COLORS["green"],
              fontweight="bold", fontsize=9, ha="center", va="center",
              bbox=dict(boxstyle="round,pad=0.30", facecolor="white",
                        edgecolor=COLORS["green"], linewidth=0.8))
    ax_b.set_xticks(bx)
    ax_b.set_xticklabels(bars_x, fontsize=8.5)
    ax_b.set_ylabel("Pearson r vs ground-truth valence\n(OASIS, n=270 test images)",
                    fontsize=9, linespacing=1.05)
    ax_b.set_ylim(-0.20, 1.05)
    ax_b.set_title("Vision (CLIP):  same recipe BEATS supervised ridge", loc="left")
    panel_label(ax_b, "b", x=-0.14, y=1.04)

    # ---------------- (c) EEG MODELS ----------------
    ax_c = fig.add_subplot(gs[1, 0])
    abs_r, bacc, tags = load_crossarch()
    is_ens = np.array(["ensemble" in t for t in tags])
    is_cb = np.array([t.startswith("cbramod") for t in tags])
    # single EMOD
    em_single = (~is_ens) & (~is_cb)
    cb_single = (~is_ens) & is_cb
    ax_c.scatter(abs_r[cb_single], bacc[cb_single], s=78, c=COLORS["red"],
                 marker="o", alpha=0.85, edgecolors="white", linewidths=0.9, zorder=3,
                 label="CBraMod (single)")
    ax_c.scatter(abs_r[em_single], bacc[em_single], s=78, c=COLORS["blue"],
                 marker="o", alpha=0.85, edgecolors="white", linewidths=0.9, zorder=3,
                 label="EMOD (single)")
    ax_c.scatter(abs_r[is_ens], bacc[is_ens], s=220, c=COLORS["darkblue"],
                 marker="*", alpha=0.95, edgecolors="white", linewidths=1.0, zorder=4,
                 label="Ensemble")

    # fit + 95% bootstrap CI
    z_fit = np.polyfit(abs_r, bacc, 1)
    xline = np.linspace(abs_r.min() - 0.02, abs_r.max() + 0.02, 80)
    rng = np.random.default_rng(0)
    boots = []
    for _ in range(2000):
        idx = rng.integers(0, len(abs_r), len(abs_r))
        boots.append(np.polyval(np.polyfit(abs_r[idx], bacc[idx], 1), xline))
    boots = np.array(boots)
    ax_c.plot(xline, np.polyval(z_fit, xline), color="black", lw=1.4, alpha=0.65, zorder=2)
    ax_c.fill_between(xline,
                      np.percentile(boots, 2.5, axis=0),
                      np.percentile(boots, 97.5, axis=0),
                      color="black", alpha=0.10, zorder=1)
    r_corr = pearsonr(abs_r, bacc)
    ax_c.text(0.04, 0.97, f"r = +{r_corr.statistic:.3f}\np = {r_corr.pvalue:.0e}\nn = {len(abs_r)} ckpt",
              transform=ax_c.transAxes, fontsize=11, fontweight="bold",
              color="black", va="top",
              bbox=dict(boxstyle="round,pad=0.25", facecolor="white",
                        edgecolor=COLORS["lightgray"], linewidth=0.8, alpha=0.95))
    ax_c.set_xlabel("class-PC1 V-axis |r|  (no V-axis loss in training)")
    ax_c.set_ylabel("FACED 9-class BACC")
    ax_c.set_title("EEG models:  better classifiers spontaneously encode the V-axis", loc="left")
    panel_label(ax_c, "c", x=-0.12, y=1.04)
    ax_c.legend(loc="lower right", frameon=False, fontsize=8)

    # ---------------- (d) BRAIN ----------------
    ax_d = fig.add_subplot(gs[1, 1])
    clip, eeg, rand_dir = load_brain_circle()
    # standardize for visualization
    cz = (clip - clip.mean()) / clip.std()
    ez = (eeg - eeg.mean()) / eeg.std()

    for emo in EMO_ORDER:
        idx = [i for i, e in enumerate(EMO_PER_STIM_28) if e == emo]
        ax_d.scatter(cz[idx], ez[idx], s=80, c=COLORS[emo],
                     edgecolors="white", linewidths=0.9, alpha=0.95, zorder=3,
                     label=emo)
    # fit + CI
    z_fit = np.polyfit(cz, ez, 1)
    xline = np.linspace(cz.min() - 0.15, cz.max() + 0.15, 50)
    ax_d.plot(xline, np.polyval(z_fit, xline), color="black", lw=1.4, alpha=0.65, zorder=2)
    rng = np.random.default_rng(1)
    boots = []
    for _ in range(2000):
        idx = rng.integers(0, len(cz), len(cz))
        boots.append(np.polyval(np.polyfit(cz[idx], ez[idx], 1), xline))
    boots = np.array(boots)
    ax_d.fill_between(xline,
                      np.percentile(boots, 2.5, axis=0),
                      np.percentile(boots, 97.5, axis=0),
                      color="black", alpha=0.10, zorder=1)
    r_brain = pearsonr(cz, ez)
    ax_d.text(0.04, 0.97, f"r = +{r_brain.statistic:.3f}\np < 10⁻⁹\nn = 28 stim",
              transform=ax_d.transAxes, fontsize=11, fontweight="bold",
              color="black", va="top",
              bbox=dict(boxstyle="round,pad=0.25", facecolor="white",
                        edgecolor=COLORS["lightgray"], linewidth=0.8, alpha=0.95))
    ax_d.set_xlabel("CLIP V-axis projection (text description of stimulus)")
    ax_d.set_ylabel("EEG cohort response  (DE-ridge prediction, z-scored)")
    ax_d.set_title("Brain:  same axis predicts human EEG (FACED, 28 video stims)", loc="left")
    panel_label(ax_d, "d", x=-0.12, y=1.04)
    # emotion-class legend BELOW the panel so it cannot overlap any
    # scatter points in the lower-right cluster.
    ax_d.legend(loc="upper center", bbox_to_anchor=(0.50, -0.18),
                fontsize=7.4, ncol=9, frameon=False,
                title="emotion class", title_fontsize=8.0,
                handletextpad=0.35, columnspacing=1.0)

    # ---------------- super-title ----------------
    fig.suptitle(
        "A single valence direction extracted from 9 emotion stories is recovered "
        "across language, vision, EEG, and brain",
        y=0.945, fontsize=13.0, fontweight="bold")

    fig.text(0.5, 0.025,
             "Same V-axis (Qwen3-4B, 9 stories × 50 generations → PC1 at the penultimate layer); "
             "no fine-tuning, no labeled examples seen at probe time.",
             ha="center", fontsize=8.5, color=COLORS["gray"])

    save_dual(fig, f"{OUT}/lf1_universal_vaxis_hero")
    save_dual(fig, f"{OUT_PAPER}/lf1_universal_vaxis_hero")


if __name__ == "__main__":
    main()
