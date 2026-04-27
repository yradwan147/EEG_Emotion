"""LF10 — FACED Test Confusion Matrices (§8 appendix).

Two side-by-side 9×9 confusion matrices on the FACED test set (1932 trials):
  (a) best single checkpoint  (vanilla d6_e150_s789, val-selected)  → BACC 0.6755
  (b) 10-ckpt ensemble (5 e100 + 5 e150)                            → BACC 0.6948
Per-class accuracy on diagonal. Each matrix row-normalised so diagonals are
the per-class true-positive rate. Confused class pairs highlighted with a
ring on the off-diagonal cells with the highest confusion. The ensemble
column shows where the ensemble cancels error (Δ-confusion panel below).
"""
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import balanced_accuracy_score, confusion_matrix

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lf_style import apply_lf_style, COLORS, save_dual, panel_label

REPORTS = "/ibex/project/c2323/yousef/reports"
EXT_DIR = f"{REPORTS}/sota_ensemble_extension"
OUT = "/ibex/project/c2323/yousef/paper_neurips26_final/figures/landmark"
OUT_PAPER = "/ibex/project/c2323/yousef/EEG_Emotion/figures/landmark"

CLASSES = ["Anger", "Disgust", "Fear", "Sadness", "Neutral",
           "Amusement", "Inspiration", "Joy", "Tenderness"]


def load_probs():
    labels = np.load(f"{EXT_DIR}/labels.npy")
    seeds = ["42", "123", "456", "789", "2025"]
    # 10-ckpt ensemble
    all_p = []
    for s in seeds:
        all_p.append(np.load(f"{EXT_DIR}/probs_vanilla_e100_s{s}.npy"))
        all_p.append(np.load(f"{EXT_DIR}/probs_vanilla_e150_s{s}.npy"))
    p_ens = np.mean(all_p, axis=0)
    # best single = vanilla_e150_s789 (val-selected per #448)
    p_best = np.load(f"{EXT_DIR}/probs_vanilla_e150_s789.npy")
    return labels, p_best, p_ens


def plot_cm(ax, cm_norm, cm_count, classes, title, panel, bacc_val):
    im = ax.imshow(cm_norm, cmap="Blues", vmin=0, vmax=0.85, aspect="equal")
    n = len(classes)
    # cell text
    for i in range(n):
        for j in range(n):
            v = cm_norm[i, j]
            cell_color = "white" if v > 0.45 else "black"
            cnt = int(cm_count[i, j])
            if i == j:
                ax.text(j, i, f"{v:.2f}\n({cnt})", ha="center", va="center",
                        fontsize=8, color=cell_color, fontweight="bold")
            elif v >= 0.05:
                ax.text(j, i, f"{v:.2f}", ha="center", va="center",
                        fontsize=7.5, color=cell_color)
    ax.set_xticks(np.arange(n))
    ax.set_yticks(np.arange(n))
    ax.set_xticklabels(classes, rotation=45, ha="right", fontsize=8.5)
    ax.set_yticklabels(classes, fontsize=8.5)
    ax.set_xlabel("predicted class")
    ax.set_ylabel("true class")
    ax.set_title(f"{title}\nBACC = {bacc_val:.4f}", loc="left",
                 fontsize=11.0, pad=8)
    panel_label(ax, panel, x=-0.13, y=1.05)
    # Highlight the most-confused off-diagonal cell per row
    for i in range(n):
        off = cm_norm[i].copy()
        off[i] = -1
        j = int(np.argmax(off))
        if cm_norm[i, j] > 0.10:
            from matplotlib.patches import Rectangle
            rect = Rectangle((j - 0.45, i - 0.45), 0.9, 0.9,
                             fill=False, edgecolor=COLORS["red"], linewidth=1.5,
                             zorder=3, alpha=0.85)
            ax.add_patch(rect)
    return im


def main():
    apply_lf_style()
    labels, p_best, p_ens = load_probs()
    pred_best = p_best.argmax(axis=1)
    pred_ens = p_ens.argmax(axis=1)
    bacc_best = balanced_accuracy_score(labels, pred_best)
    bacc_ens = balanced_accuracy_score(labels, pred_ens)
    print(f"  best BACC: {bacc_best:.4f}  ensemble BACC: {bacc_ens:.4f}")

    cm_best = confusion_matrix(labels, pred_best)
    cm_ens = confusion_matrix(labels, pred_ens)
    # row-normalize
    cm_best_n = cm_best / cm_best.sum(axis=1, keepdims=True).clip(1e-9)
    cm_ens_n = cm_ens / cm_ens.sum(axis=1, keepdims=True).clip(1e-9)

    fig = plt.figure(figsize=(16.5, 8.2))
    gs = fig.add_gridspec(
        1, 4,
        width_ratios=[1.0, 1.0, 0.85, 0.06],
        wspace=0.42,
        left=0.05, right=0.985, bottom=0.10, top=0.84,
    )

    ax_a = fig.add_subplot(gs[0, 0])
    plot_cm(ax_a, cm_best_n, cm_best, CLASSES,
            "Best single checkpoint  (vanilla d6_e150 seed 789)",
            "a", bacc_best)

    ax_b = fig.add_subplot(gs[0, 1])
    im_b = plot_cm(ax_b, cm_ens_n, cm_ens, CLASSES,
                   "10-ckpt ensemble  (5 × e100  +  5 × e150)",
                   "b", bacc_ens)

    # ---------------- (c) per-class accuracy improvement ----------------
    ax_c = fig.add_subplot(gs[0, 2])
    diag_best = np.diag(cm_best_n)
    diag_ens = np.diag(cm_ens_n)
    delta = diag_ens - diag_best
    # sort by delta
    order = np.argsort(delta)[::-1]
    y = np.arange(len(CLASSES))[::-1]
    colors_for = [COLORS["pos_sig"] if delta[i] > 0 else
                  (COLORS["red"] if delta[i] < 0 else COLORS["gray"])
                  for i in order]
    bars = ax_c.barh(y, delta[order], color=colors_for, height=0.66,
                     edgecolor="white", linewidth=0.7, zorder=3)
    # primary delta values to the right of bars; transition (best→ens) to the
    # FAR right margin for ALL rows, so left side stays clean for y-tick labels.
    for yi, di, ci in zip(y, delta[order], order):
        # delta value just past bar tip
        ax_c.text(di + (0.0030 if di >= 0 else -0.0030), yi,
                  f"{di:+.3f}",
                  va="center", ha="left" if di >= 0 else "right",
                  fontsize=8.5, color="black", fontweight="bold")
        # transition (small, lower line)
        ax_c.text(di + (0.0030 if di >= 0 else -0.0030), yi - 0.40,
                  f"{diag_best[ci]:.2f}→{diag_ens[ci]:.2f}",
                  va="top", ha="left" if di >= 0 else "right",
                  fontsize=6.8, color="#666666")
    ax_c.axvline(0, color="black", lw=0.8)
    ax_c.set_yticks(y)
    ax_c.set_yticklabels([CLASSES[i] for i in order], fontsize=9)
    ax_c.set_xlabel("Δ per-class accuracy  (ensemble − single)")
    ax_c.set_title("Where the ensemble fixes the single",
                   loc="left", fontsize=11.0, pad=8)
    panel_label(ax_c, "c", x=-0.30, y=1.05)
    ax_c.set_xlim(-0.045, 0.105)
    ax_c.set_ylim(-0.7, len(CLASSES) - 0.3)

    # colorbar for confusion matrices (on the right)
    cax = fig.add_subplot(gs[0, 3])
    cbar = fig.colorbar(im_b, cax=cax)
    cbar.set_label("row-normalised proportion", fontsize=9.5)
    cbar.ax.tick_params(labelsize=8)

    # super-title
    fig.suptitle(
        "FACED 9-class confusion matrices on test (n = 1,932 trials, 23 unseen subjects)",
        y=0.945, fontsize=13, fontweight="bold")
    fig.text(0.5, 0.018,
             "Red box: most-confused off-diagonal cell per row.  "
             "Diagonal cells show row-normalised true-positive rate (parenthesis = raw count).  "
             "Per-class accuracies sum to overall BACC.",
             ha="center", fontsize=8.5, color=COLORS["gray"])

    save_dual(fig, f"{OUT}/lf10_confusion_matrices")
    save_dual(fig, f"{OUT_PAPER}/lf10_confusion_matrices")


if __name__ == "__main__":
    main()
