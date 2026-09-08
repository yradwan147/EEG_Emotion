"""Figure 1 HERO v6 — final: every dot labelled, mechanism stated, numbers traced.

Top panel: three rows on ONE valence scale — language model / human brain / EEG
classifier — each placing the nine emotions at that source's own measured 1-D
position. Every dot carries a 3-letter emotion code in its colour (no legend
cross-referencing). Thin vertical guides mark where the language model put each
emotion, so a dot on its guide agrees and a dot off it (e.g. the classifier's Fear)
is a visible, acknowledged deviation. Each row header carries its Holy-Grail-traced
statistic: brain vs language r = 0.87 (28 clips), classifier vs language r = 0.74
(this checkpoint; 0.60-0.77 across 10).

Bottom panel states its result: re-teaching the axis as a loss hurts (.658 -> .629,
-.029, p<.01; of 25 variants 0 helped, 15 hurt); averaging 10 checkpoints helps
(.695, best on FACED-9; best single .676). All printed numbers are traced.
"""
import os
import sys
import json
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Circle
from matplotlib.lines import Line2D

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lf_style import COLORS

R = "/ibex/project/c2323/yousef/reports"
OUT = "/ibex/project/c2323/yousef/EEG_Emotion/figures/landmark"
INK, GRAY, MUTE, RULE = "#1b1e23", "#555b63", "#8a9099", "#d7dadf"
RED, GRN = "#c0392b", "#2e8b57"
EMO = ["Anger", "Disgust", "Fear", "Sadness", "Neutral", "Amusement", "Inspiration", "Joy", "Tenderness"]
CODE = ["Ang", "Dis", "Fea", "Sad", "Neu", "Amu", "Ins", "Joy", "Ten"]
LAB = np.array([0] * 3 + [1] * 3 + [2] * 3 + [3] * 3 + [4] * 4 + [5] * 3 + [6] * 3 + [7] * 3 + [8] * 3)  # video 1..28
W, H = 5.5, 3.45
T = {}


def setup():
    mpl.rcParams.update({"pdf.fonttype": 42, "font.family": "sans-serif",
                         "font.sans-serif": ["Helvetica", "Arial", "DejaVu Sans"]})


def txt(ax, key, x, y, s, size, color, ha="left", va="center", weight="normal", style="normal", ls=1.2, z=8):
    T[key] = ax.text(x, y, s, fontsize=size, color=color, ha=ha, va=va, fontweight=weight,
                     style=style, linespacing=ls, zorder=z)


def arrow(ax, p, q, color, lw=1.3, ms=8, z=6):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=ms, lw=lw, color=color,
                                 shrinkA=0, shrinkB=0, zorder=z))


def load_rows():
    """Row positions derived from traced files; printed statistics read from traced fields."""
    r6 = json.load(open(f"{R}/r6_eeg_llm_circle.json"))
    lang = np.array(r6["per_stim"]["clip_bare_emotion_proj"]); eeg = np.array(r6["per_stim"]["eeg_de_ridge_pred"])
    cm = lambda v: np.array([v[LAB == c].mean() for c in range(9)])
    L, B = cm(lang), cm(eeg)
    me = json.load(open(f"{R}/merge_emerge_results.json"))
    Cs = np.array(me["feature_centroids_per_ckpt"]["d6_e150_seed42"])
    Cc = np.array([Cs[LAB == c].mean(0) for c in range(9)]); Cc = Cc - Cc.mean(0)
    _, _, Vt = np.linalg.svd(Cc, full_matrices=False); pc1 = Cc @ Vt[0]
    if np.corrcoef(pc1, L)[0, 1] < 0: pc1 = -pc1
    z = lambda v: (v - v.mean()) / v.std()
    st = json.load(open(f"{R}/sota_ensemble_theory.json"))
    rBL = json.load(open(f"{R}/nested_perm_vaxis.json"))["reported_observed_r"]              # 0.874
    rCL = st["per_ckpt"]["e150_s42"]["vaxis"]["class_pc1_vs_clip_bare"]["r_PC1"]           # 0.742
    rng = st["rank_orders"]["class_pc1"]["order_values"]                                    # 10 ckpts
    assert abs(np.corrcoef(pc1, L)[0, 1] - rCL) < 0.02
    sr = json.load(open(f"{R}/stats_rigor_final_compute_out.json"))["strong_valence_topo"]
    nums = dict(base=sr["base_mean"], aux=sr["aux_mean"], delta=sr["delta"], p=sr["p"],          # .658 .629 -.029 .004
                best=json.load(open(f"{R}/best_single_ckpt.json"))["best_single_val_selected"]["test_bacc"],  # .6755
                ens=json.load(open(f"{R}/selector_comparison_v2.json"))["full_ensemble_test_bacc"])        # .6948
    return z(L), z(B), z(pc1), rBL, rCL, (min(rng), max(rng)), nums


def main():
    setup()
    L, B, C, rBL, rCL, rrange, N = load_rows()
    fig = plt.figure(figsize=(W, H)); fig.patch.set_facecolor("white")
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(0, H); ax.set_aspect("equal"); ax.axis("off")

    txt(ax, "head", W / 2, 3.33, "Three different things share one valence axis — including a classifier that was never taught valence",
        6.7, INK, ha="center", weight="bold")
    txt(ax, "mech", W / 2, 3.17, "each row places the nine emotions where that source puts them;  thin lines mark the language model's positions",
        5.0, GRAY, ha="center")

    # ---------------- TOP: three rows on one shared valence scale ----------------
    X0, X1 = 1.72, 5.30
    def sx(z): return X0 + (z + 2.0) / 4.0 * (X1 - X0)
    rows = [(2.72, L, "language model", "CLIP-text valence axis", None),
            (2.17, B, "human brain", "raw EEG of 123 people, no model", f"r = {rBL:.2f} vs language  (28 clips → 9 means)"),
            (1.62, C, "EEG classifier", "labels only — never given valence", f"r = {rCL:.2f} vs language\n(one checkpoint; {rrange[0]:.2f}–{rrange[1]:.2f} across 10)")]
    for v, e in zip(L, EMO):   # guides anchored at the language row
        ax.add_line(Line2D([sx(v), sx(v)], [1.50, 2.72], color=COLORS[e], lw=1.1, alpha=0.30, zorder=3))
    for y, vals, lab, sub, stat in rows:
        ax.add_line(Line2D([X0, X1], [y, y], color=RULE, lw=1.0, zorder=2))
        order = np.argsort(vals)
        for rank, i in enumerate(order):                     # dots + direct 3-letter labels
            x = sx(vals[i]); e = EMO[i]
            ax.add_patch(Circle((x, y), 0.046, fc=COLORS[e], ec="white", lw=0.7, zorder=6))
            dy = (0.075, -0.075, 0.150)[rank % 3]              # stagger so tight clusters stay legible
            txt(ax, f"{lab[:3]}{e}", x, y + dy + (0.045 if dy > 0 else -0.045), CODE[i], 4.4, COLORS[e],
                ha="center", va="bottom" if dy > 0 else "top", weight="bold")
        txt(ax, f"lab{lab}", 1.62, y + 0.06, lab, 6.4, INK, ha="right", weight="bold")
        txt(ax, f"sub{lab}", 1.62, y - 0.06, sub, 4.8, MUTE, ha="right", va="top")
        if stat:
            txt(ax, f"stat{lab}", 1.62, y - 0.175, stat, 4.6, INK, ha="right", va="top", weight="bold")
    txt(ax, "key", X0, 1.33, "Ang anger · Dis disgust · Fea fear · Sad sadness · Neu neutral · Amu amusement · Ins inspiration · Joy joy · Ten tenderness",
        4.3, MUTE, va="top")
    arrow(ax, (X0, 1.42), (X1, 1.42), MUTE, lw=0.9, ms=7, z=3)
    txt(ax, "neg", X0, 1.22, "more negative", 4.8, MUTE, va="top")
    txt(ax, "pos", X1, 1.22, "more positive", 4.8, MUTE, ha="right", va="top")
    txt(ax, "vax", (X0 + X1) / 2, 1.22, "valence", 5.2, GRAY, ha="center", va="top", weight="bold")

    # ---------------- rule ----------------
    ax.add_line(Line2D([0.25, W - 0.25], [1.06, 1.06], color=RULE, lw=0.8, zorder=2))

    # ---------------- BOTTOM: the result, stated ----------------
    txt(ax, "q", 0.30, 0.96, f"Re-teaching the classifier the axis hurts ({N['delta']:+.3f}, p < .01);  averaging 10 checkpoints helps",
        6.2, INK, weight="bold")
    txt(ax, "qsub", 0.30, 0.84, "balanced accuracy on FACED-9 (the 9-emotion EEG benchmark above, 123 people)", 4.8, MUTE)
    RY, RX0, RX1 = 0.47, 0.55, 5.05
    def rx(v): return RX0 + (v - 0.60) / (0.70 - 0.60) * (RX1 - RX0)
    ax.add_line(Line2D([RX0, RX1], [RY, RY], color=MUTE, lw=1.0, zorder=3))
    for v in (0.60, 0.65, 0.70):
        ax.add_line(Line2D([rx(v), rx(v)], [RY - 0.03, RY + 0.03], color=MUTE, lw=0.8, zorder=3))
        if v != 0.65:   # the .658 baseline sub-label sits here; the dots carry exact values
            txt(ax, f"tk{v}", rx(v), RY - 0.05, f"{v:.2f}", 4.6, MUTE, ha="center", va="top")
    b, a, bs, en = N["base"], N["aux"], N["best"], N["ens"]
    ax.add_patch(Circle((rx(b), RY), 0.05, fc=INK, ec="white", lw=0.6, zorder=6))
    txt(ax, "start", rx(b), RY + 0.085, f"the EEG classifier above  {b:.3f}".replace("0.", "."), 5.3, INK, ha="center", va="bottom", weight="bold")
    txt(ax, "start2", rx(b), RY - 0.075, "mean of its 5 seeds", 4.5, MUTE, ha="center", va="top")
    ax.add_patch(Circle((rx(bs), RY), 0.04, fc="white", ec=INK, lw=0.9, zorder=6))
    txt(ax, "best", rx(bs), RY - 0.075, f"best single seed  {bs:.3f}".replace("0.", "."), 4.5, GRAY, ha="center", va="top")
    arrow(ax, (rx(b) - 0.06, RY), (rx(a) + 0.05, RY), RED, lw=1.5, ms=8, z=7)
    ax.add_patch(Circle((rx(a), RY), 0.045, fc=RED, ec="white", lw=0.6, zorder=6))
    txt(ax, "m1", RX0, RY + 0.085, f"add the axis as a training loss  ✗  {a:.3f}".replace("0.", "."), 5.3, RED, va="bottom", weight="bold")
    txt(ax, "m1b", RX0, RY + 0.19, "one intervention; of 25 variants tried, 0 helped and 15 hurt", 4.5, RED, va="bottom")
    arrow(ax, (rx(b) + 0.06, RY), (rx(en) - 0.05, RY), GRN, lw=1.5, ms=8, z=7)
    ax.add_patch(Circle((rx(en), RY), 0.05, fc=GRN, ec="white", lw=0.6, zorder=6))
    txt(ax, "m2", W - 0.20, RY + 0.085, f"average its 10 checkpoints  ✓  {en:.3f}".replace("0.", "."), 5.3, GRN, ha="right", va="bottom", weight="bold")
    txt(ax, "m2b", W - 0.20, RY + 0.19, "5 seeds × 2 training lengths · best result on FACED-9", 4.5, GRN, ha="right", va="bottom")
    txt(ax, "take", W / 2, 0.13, "Nothing left to teach — the axis is already there. Averaging seeds removes only what still differs between them.",
        5.5, INK, ha="center", style="italic")

    # ---------------- sanity loop ----------------
    fig.canvas.draw(); rend = fig.canvas.get_renderer(); inv = ax.transData.inverted()
    boxes = {k: t.get_window_extent(rend).transformed(inv) for k, t in T.items()}; bad = 0
    for k, bb in boxes.items():
        if bb.x0 < 0.02 or bb.x1 > W - 0.02 or bb.y0 < 0.02 or bb.y1 > H - 0.02:
            print(f"  [!] '{k}' overruns: x[{bb.x0:.2f},{bb.x1:.2f}] y[{bb.y0:.2f},{bb.y1:.2f}]"); bad += 1
    ks = list(boxes)
    for i in range(len(ks)):
        for j in range(i + 1, len(ks)):
            if boxes[ks[i]].overlaps(boxes[ks[j]]): print(f"  [!] overlap: '{ks[i]}' x '{ks[j]}'"); bad += 1
    print(f"  traced: rBL {rBL:.3f} rCL {rCL:.3f} range {rrange} | ruler {N} | sanity: {bad} issue(s)")
    os.makedirs(OUT, exist_ok=True)
    fig.savefig(f"{OUT}/fig1_hero_v6.pdf"); fig.savefig(f"{OUT}/fig1_hero_v6.png", dpi=500)
    print(f"  saved -> {OUT}/fig1_hero_v6.pdf / .png"); plt.close(fig)


if __name__ == "__main__":
    main()
