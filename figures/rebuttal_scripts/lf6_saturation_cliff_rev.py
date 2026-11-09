"""LF6 — Saturation Cliff (§7 main).

Δ-vs-recipe-strength plot: x-axis is the baseline BACC of the recipe the
V-axis intervention is added to (CBraMod 0.572, EMOD d6 (vanilla) ~0.624, full SOTA d6
0.658). y-axis is Δ from V-axis intervention. Visualizes the transition that
crosses zero between EMOD d6 (vanilla) and the full SOTA recipe.

Top panel: scatter with all 25+ V-axis interventions, colored by
significance tier; visible saturation cliff. Bottom panel zooms into the
3-anchor "component ablation" used in the paper to nail the transition:
CBraMod, EMOD d6 (vanilla), full SOTA recipe.
"""
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

sys.path.insert(0, "/ibex/project/c2323/yousef/EEG_Emotion/figures/landmark/scripts")
from _lf_style import apply_lf_style, COLORS, save_dual, panel_label

OUT_PAPER = "/ibex/project/c2323/yousef/EEG_Emotion/figures/landmark"



# ---- rebuttal revision: authoritative table values -------------------------
import json as _json
_TAB = "/ibex/project/c2323/yousef/EEG_Emotion/indexes/tab_full_vaxis_reproduction.json"
_T = _json.load(open(_TAB))["rows"]
TAB = {r["row"]: r for r in _T}
assert len(TAB) == 25


def _holm(ps):
    ps = np.asarray(ps, float); m = len(ps); o = np.argsort(ps)
    adj = np.empty(m); run = 0.0
    for k, i in enumerate(o):
        run = max(run, (m - k) * ps[i]); adj[i] = min(1.0, run)
    return adj


HOLM = dict(zip([r["row"] for r in _T], _holm([r["p_paired"] for r in _T])))
SIG_HOLM = sorted(k for k in TAB if HOLM[k] < 0.05 and TAB[k]["mine_delta"] < 0)
assert SIG_HOLM == [1, 5, 10, 11, 12, 13, 14, 21, 22, 25], SIG_HOLM


def tier_for(rown, old_tier):
    """Holm tiering over the 25 table rows."""
    d, p = TAB[rown]["mine_delta"], TAB[rown]["p_paired"]
    if rown in SIG_HOLM:
        if d < -0.15:
            return "destruction"
        return "monotonic" if old_tier == "monotonic" else "neg_sig"
    if d < 0 and p < 0.05:
        return "neg_holm_ns"
    return "neg_ns" if d < 0 else "ns_pos"
# ----------------------------------------------------------------------------

# Hand-built table of (label, base_bacc, delta, p, kind) — sourced from
# headline_numbers.md, all_findings_catalog.md (verified against the per-experiment
# JSONs at merge_*_results.json).
ROWS = [
    # CBraMod (very weak base)
    ("CBraMod + Topo λ=0.05",       0.5717, -0.005, 0.30,   "neg_ns"),
    # EMOD d6 vanilla baseline (~0.6235)
    ("EMOD d6 (vanilla) + Topo λ=0.05",       0.6235, +0.002, 0.50,   "ns_pos"),
    ("EMOD d6 (vanilla) + EMODSTYLE λ=0.5",   0.6235, +0.007, 0.22,   "ns_pos"),
    ("EMOD d6 (vanilla) + Procrustes λ=0.05", 0.6235, +0.001, 0.89,   "ns_pos"),
    ("EMOD d6 (vanilla) + PRIOR (smooth)",    0.6235, +0.002, 0.40,   "ns_pos"),
    # NS negatives at d3
    ("EMOD d6 (vanilla) + Topo λ=0.1",        0.6235, -0.013, 0.039,  "neg_sig"),
    ("EMOD d6 (vanilla) + Frontal-mask λ=0.1",0.6235, -0.009, 0.21,   "neg_ns"),
    ("EMOD d6 (vanilla) + FAA λ=0.1",         0.6235, -0.018, 0.063,  "neg_ns"),
    ("EMOD d6 (vanilla) + PEFT λ=0.1",        0.6235, -0.009, 0.069,  "neg_ns"),
    ("EMOD d6 (vanilla) + Curriculum cos",    0.6235, -0.009, 0.23,   "neg_ns"),
    ("EMOD d6 (vanilla) + KD soft T=2 λ=1",   0.6235, -0.012, 0.05,   "neg_ns"),
    ("EMOD d6 (vanilla) + Init weight",       0.6235, -0.017, 0.05,   "neg_ns"),
    ("EMOD d6 (vanilla) + Distill",           0.6235, -0.017, 0.05,   "neg_ns"),
    ("EMOD d6 (vanilla) + EEG-AUX MSE λ=0.1", 0.6235, -0.016, 0.05,   "neg_ns"),
    # Stat-sig negatives at d3
    ("EMOD d6 (vanilla) + Frontal-mask λ=0.5",0.6235, -0.052, 0.0015, "neg_sig"),
    ("EMOD d6 (vanilla) + FAA λ=0.5",         0.6235, -0.044, 0.006,  "neg_sig"),
    ("EMOD d6 (vanilla) + Anger-w λ=0.5",     0.6235, -0.054, 0.0003, "neg_sig"),
    ("EMOD d6 (vanilla) + Occipital λ=0.1",   0.6235, -0.022, 0.007,  "neg_sig"),
    ("EMOD d6 (vanilla) + Multi-V λ=0.5",     0.6235, -0.041, 0.005,  "neg_sig"),
    ("EMOD d6 (vanilla) + EEG-AUX MSE λ=0.5", 0.6235, -0.043, 0.01,   "neg_sig"),
    ("EMOD d6 (vanilla) + Uncert (Kendall)",  0.6235, -0.067, 0.001,  "neg_sig"),
    ("EMOD d6 (vanilla) + RSA λ=1",           0.6235, -0.057, 0.001,  "neg_sig"),
    ("EMOD d6 (vanilla) + RSA λ=5",           0.6235, -0.093, 0.001,  "monotonic"),
    # Full SOTA recipe (saturation cliff)
    ("d6 SOTA + Topo λ=0.1",        0.6581, -0.029, 0.004,  "neg_sig_full"),
    ("d6 SOTA + EMODSTYLE λ=0.5",   0.6581, -0.026, 0.004,  "neg_sig_full"),
]


MAP = {  # script label -> table row
    "EMOD d6 (vanilla) + Topo λ=0.05": 8, "EMOD d6 (vanilla) + EMODSTYLE λ=0.5": 17,
    "EMOD d6 (vanilla) + Procrustes λ=0.05": 9, "EMOD d6 (vanilla) + Topo λ=0.1": 7,
    "EMOD d6 (vanilla) + Frontal-mask λ=0.1": 2, "EMOD d6 (vanilla) + FAA λ=0.1": 4,
    "EMOD d6 (vanilla) + PEFT λ=0.1": 18,  # fullhead (old p=0.069 matches row 18)
    "EMOD d6 (vanilla) + EEG-AUX MSE λ=0.1": 15,
    "EMOD d6 (vanilla) + Frontal-mask λ=0.5": 1, "EMOD d6 (vanilla) + FAA λ=0.5": 3,
    "EMOD d6 (vanilla) + Anger-w λ=0.5": 5, "EMOD d6 (vanilla) + Occipital λ=0.1": 6,
    "EMOD d6 (vanilla) + Multi-V λ=0.5": 13, "EMOD d6 (vanilla) + EEG-AUX MSE λ=0.5": 14,
    "EMOD d6 (vanilla) + Uncert (Kendall)": 25, "EMOD d6 (vanilla) + RSA λ=1": 11,
    "EMOD d6 (vanilla) + RSA λ=5": 10,
}
ROW_OF = {}


def revise(rows):
    out = []
    for (lab, base, dl, p, kind) in rows:
        if lab in MAP:
            r = MAP[lab]; ROW_OF[lab] = r
            nd, np_, nk = TAB[r]["mine_delta"], TAB[r]["p_paired"], tier_for(r, kind)
            print(f"LF6 {lab:42s} row{r:2d} d {dl:+.3f}->{nd:+.3f}  p {p}->{np_:.6f}  tier {kind}->{nk}")
            out.append((lab, base, round(nd, 3), np_, nk))
        else:
            print(f"LF6 {lab:42s} UNCHANGED (not in 25 rows)")
            out.append((lab, base, dl, p, kind))
    return out


ROWS = revise(ROWS)


def _d(lab): return ROWS[[r[0] for r in ROWS].index(lab)][2]


def _fmt(v, p):  # annotation string
    s = f"{v:+.3f}".replace("-", "−")
    st = "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else " ns"
    return s + st


# Style mapping
STYLE = {
    "ns_pos":       dict(c=COLORS["pos_ns"],  marker="o", s=120, edge=COLORS["blue"],
                          label="NS positive (Δ ≈ 0)"),
    "neg_holm_ns":  dict(c=COLORS["lightred"], marker="o", s=140, edge="#7f1c1c",
                          label="p < 0.05 uncorrected, n.s. after Holm"),
    "neg_ns":       dict(c=COLORS["neg_ns"],  marker="o", s=120, edge="#a04612",
                          label="NS negative (p > 0.05)"),
    "neg_sig":      dict(c=COLORS["neg_sig"], marker="o", s=160, edge="#7f1c1c",
                          label="significant negative (Holm p < 0.05)"),
    "monotonic":    dict(c=COLORS["monotonic"],marker="o", s=160, edge="black",
                          label="monotonic destruction"),
    "neg_sig_full": dict(c=COLORS["destruction"], marker="X", s=240, edge="black",
                          label="full SOTA recipe (cliff)"),
}


def main():
    apply_lf_style()
    fig = plt.figure(figsize=(11.5, 6.8))
    gs = fig.add_gridspec(1, 1, left=0.090, right=0.985, bottom=0.13, top=0.86)
    ax = fig.add_subplot(gs[0, 0])

    # transition zone
    ax.axvspan(0.620, 0.660, color=COLORS["lightgray"], alpha=0.25, zorder=0)
    ax.axhline(0, color="black", lw=0.7, zorder=1)

    # plot points (jittered slightly horizontally for readability)
    rng = np.random.default_rng(42)
    plotted = set()
    for label, base, delta, p, kind in ROWS:
        x = base + rng.normal(0, 0.0010)
        st = STYLE[kind]
        lab = st["label"] if kind not in plotted else None
        plotted.add(kind)
        ax.scatter(x, delta, s=st["s"], c=st["c"], marker=st["marker"],
                   edgecolors=st["edge"], linewidths=1.0, alpha=0.92, zorder=3,
                   label=lab)

    # Fit a robust trend through (base_x, mean(delta_at_base)) — anchor visualization
    anchor_x = np.array([0.572, 0.6235, 0.6581])
    anchor_y = np.array([
        -0.005,                         # CBraMod (single seed; Table 10: 0.572->0.567)
        np.mean([d for (_, b, d, _, _) in ROWS if abs(b - 0.6235) < 0.001]),
        np.mean([d for (_, b, d, _, _) in ROWS if abs(b - 0.6581) < 0.001]),
    ])
    ax.plot(anchor_x, anchor_y, color=COLORS["darkblue"], lw=2.3, ls="-",
            alpha=0.85, zorder=2,
            label=f"mean Δ at each base recipe")
    for x, y in zip(anchor_x, anchor_y):
        ax.scatter([x], [y], s=200, c="white", edgecolors=COLORS["darkblue"],
                   linewidths=2.0, marker="D", zorder=5)

    # vertical guide lines at the three anchors — labels above the plot top
    for xv, lab_t in [(0.572, "CBraMod"), (0.6235, "EMOD d3 (vanilla)"), (0.6581, "d6 SOTA")]:
        ax.axvline(xv, color=COLORS["gray"], ls=":", lw=0.8, alpha=0.7, zorder=1)
        ax.text(xv, 0.041, lab_t, fontsize=9.0, ha="center",
                color=COLORS["gray"], fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.20", facecolor="white",
                          edgecolor="none", alpha=0.92))

    # callouts on the cliff — placed in clear regions (above and below the
    # main cluster) so the text never sits on data points or guide-line labels.
    KA = "Anger-w λ=0.5\n(" + _fmt(_d("EMOD d6 (vanilla) + Anger-w λ=0.5"), TAB[5]["p_paired"]).strip() + ")"
    KR = "RSA λ=5\n(" + _fmt(_d("EMOD d6 (vanilla) + RSA λ=5"), TAB[10]["p_paired"]).strip() + ")"
    KE = "EMODSTYLE λ=0.5\n(" + _fmt(_d("EMOD d6 (vanilla) + EMODSTYLE λ=0.5"), TAB[17]["p_paired"]).strip() + ")"
    print("callouts:", repr(KA), repr(KR), repr(KE))
    annotate_points = {
        KA:       (0.6235, _d("EMOD d6 (vanilla) + Anger-w λ=0.5")),
        KR:             (0.6235, _d("EMOD d6 (vanilla) + RSA λ=5")),
        "d6 SOTA + EMODSTYLE\n(−0.026***)": (0.6581, -0.026),
        KE:     (0.6235, _d("EMOD d6 (vanilla) + EMODSTYLE λ=0.5")),
        "CBraMod+Topo\n(−0.005 ns)":        (0.5717, -0.005),
    }
    offsets = {
        KA:       (0.595, -0.072),
        KR:             (0.595, -0.097),
        "d6 SOTA + EMODSTYLE\n(−0.026***)": (0.671, -0.018),
        KE:     (0.602, +0.018),
        "CBraMod+Topo\n(−0.005 ns)":        (0.572, +0.018),
    }
    halign = {
        KA:       "right",
        KR:             "right",
        "d6 SOTA + EMODSTYLE\n(−0.026***)": "left",
        KE:     "right",
        "CBraMod+Topo\n(−0.005 ns)":        "left",
    }
    for lab, (x, y) in annotate_points.items():
        tx, ty = offsets[lab]
        ha = halign[lab]
        ax.annotate(lab, xy=(x, y), xytext=(tx, ty), fontsize=8.0,
                    color="black", linespacing=0.95, ha=ha,
                    arrowprops=dict(arrowstyle="-", color=COLORS["gray"],
                                    lw=0.7, alpha=0.7))

    # cliff arrow — placed on the right edge of the d3 cluster down to the SOTA
    # cluster, so it does not visually run through the y=0 line or the cliff label.
    ax.annotate("", xy=(0.6581, -0.022), xytext=(0.6235, -0.018),
                arrowprops=dict(arrowstyle="->", color="black", lw=1.6, alpha=0.55))
    # cliff label LIFTED into clear space above the y=0 line so it never
    # collides with that line, the cluster, or any callouts.
    ax.text(0.6420, 0.014, "the saturation cliff",
            fontsize=10.0, ha="center", va="center",
            fontweight="bold", color="black", alpha=0.95,
            bbox=dict(boxstyle="round,pad=0.25", facecolor="white",
                      edgecolor="#bbbbbb", linewidth=0.6, alpha=0.95))

    ax.set_xlabel("base recipe FACED 9-class BACC  (capacity dimension)", fontsize=10.5)
    ax.set_ylabel("Δ BACC from adding V-axis supervision", fontsize=10.5)
    ax.set_title("V-axis supervision turns negative across the converged d=6 regime (vanilla to full SOTA)",
                 fontsize=11.5, fontweight="bold", loc="left", pad=10)
    panel_label(ax, "", x=-0.06, y=1.02)
    ax.set_xlim(0.555, 0.690)
    ax.set_ylim(-0.115, 0.050)
    ax.legend(loc="lower right", fontsize=8, frameon=True, framealpha=0.95,
              edgecolor="#cccccc", ncol=1)

    fig.text(0.5, 0.015,
             "n=25 V-axis interventions (frontal/FAA/occ/topo/anger-w/EMODSTYLE/Procrustes/PEFT/RSA/multi-V/"
             "EEG-AUX/KD/init/distill/curriculum/uncert/...). All ≥3 seeds unless noted; significance vs paired same-recipe vanilla.",
             ha="center", fontsize=7.8, color=COLORS["gray"])

    save_dual(fig, f"{OUT_PAPER}/lf6_saturation_cliff")


if __name__ == "__main__":
    main()
