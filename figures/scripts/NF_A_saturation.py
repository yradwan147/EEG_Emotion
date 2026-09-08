#!/usr/bin/env python3
"""NF-A (main hero): the saturation transition.
Auxiliary supervision helps a weak network and hurts a converged one,
regardless of content -- shown on CIFAR-10 (continuous transition) and
FACED EEG (two concepts: valence + arousal).

Provenance (Holy Grail): all numbers read live from
  /ibex/project/c2323/yousef/reports/stats_rigor_final_compute_out.json
Producing/anchor scripts: stats_rigor_final_compute.py, aggregate_transition.py.
Output: figures/NF_A_saturation.pdf
"""
import json, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

DATA = "/ibex/project/c2323/yousef/reports/stats_rigor_final_compute_out.json"
OUT  = os.path.join(os.path.dirname(__file__), "..", "NF_A_saturation.pdf")

d = json.load(open(DATA))

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["DejaVu Serif"],
    "mathtext.fontset": "dejavuserif",
    "font.size": 8.5,
    "axes.linewidth": 0.7,
    "xtick.major.width": 0.7, "ytick.major.width": 0.7,
    "xtick.labelsize": 7.5, "ytick.labelsize": 7.5,
})
C_REAL   = "#2166ac"   # real vs none (the aux benefit)
C_RAND   = "#9a9a9a"   # real vs random (content control)
C_WEAK   = "#7fb3d5"   # weak backbone
C_STRONG = "#c0392b"   # converged backbone
NEG      = "#b2182b"

fig, (axA, axB) = plt.subplots(1, 2, figsize=(7.1, 2.7),
                               gridspec_kw={"width_ratios": [1.35, 1.0]})

# ---------- Panel A: CIFAR-10 continuous transition ----------
rn  = d["cifar10_transition"]["real_vs_none"]
rr  = d["cifar10_transition"]["real_vs_random"]
base = np.array([p["baseacc"] for p in rn]) * 100.0
dnone = np.array([p["delta"] for p in rn]) * 100.0
holm  = np.array([p["holm"]  for p in rn])
drand = np.array([p["delta"] for p in rr]) * 100.0

axA.axhline(0, color="k", lw=0.6, zorder=1)
# real - none
axA.plot(base, dnone, "-", color=C_REAL, lw=1.6, zorder=3, label="aligned $-$ no aux")
sig = holm < 0.05
axA.scatter(base[sig],  dnone[sig],  s=42, color=C_REAL, zorder=4, edgecolor="white", linewidth=0.6)
axA.scatter(base[~sig], dnone[~sig], s=42, facecolor="white", edgecolor=C_REAL, linewidth=1.3, zorder=4)
# real - random (content-irrelevance control)
axA.plot(base, drand, "--", color=C_RAND, lw=1.3, zorder=2, label="aligned $-$ random")

axA.axvspan(88, 100, color="#f2e6e6", alpha=0.6, zorder=0)
axA.text(93.5, axA.get_ylim()[1]*0.02 - 0.15, "converged", color=NEG,
         fontsize=6.8, ha="center", style="italic")
axA.text(45, 0.85, "aux helps\n(undertrained)", color=C_REAL, fontsize=6.8, ha="center")
axA.set_xlabel("backbone base accuracy (%)")
axA.set_ylabel(r"$\Delta$ test accuracy (%)")
axA.set_title("(a) CIFAR-10: the benefit saturates", fontsize=8.5, loc="left")
axA.yaxis.set_major_formatter(FormatStrFormatter("%+.1f"))
axA.legend(frameon=False, fontsize=6.6, loc="upper right", handlelength=1.6)

# ---------- Panel B: EEG two concepts, weak vs converged ----------
def pct(x): return 100.0 * x
vals = {
    ("Valence", "weak"):   d["weak_valence_WEAK_d3_topo"],
    ("Valence", "strong"): d["strong_valence_topo"],
    ("Arousal", "weak"):   d["weak_arousal_topo"],
    ("Arousal", "strong"): d["strong_arousal_topo"],
}
groups = ["Valence", "Arousal"]
x = np.arange(len(groups)); w = 0.36
axB.axhline(0, color="k", lw=0.6, zorder=1)
for i, strength in enumerate(["weak", "strong"]):
    dy, err, col = [], [], (C_WEAK if strength == "weak" else C_STRONG)
    for g in groups:
        v = vals[(g, strength)]
        dy.append(pct(v["delta"]))
        if "ci95" in v:
            err.append(pct((v["ci95"][1]-v["ci95"][0]) / 2.0))
        elif "per_seed" in v:
            arr = np.array(list(v["per_seed"].values())); err.append(pct(arr.std(ddof=1)/np.sqrt(len(arr))))
        else:
            err.append(0.0)
    xpos = x + (i-0.5)*w
    lbl = "weak (d3)" if strength == "weak" else "converged (SOTA)"
    axB.bar(xpos, dy, w, yerr=err, capsize=2.5, color=col, edgecolor="k",
            linewidth=0.5, error_kw=dict(lw=0.8), label=lbl, zorder=3)
    if strength == "strong":
        for xp, yv in zip(xpos, dy):
            axB.text(xp, yv - 0.55, "$\\ast$", ha="center", va="top", fontsize=8, color="white")
axB.set_xticks(x); axB.set_xticklabels(groups)
axB.set_ylabel(r"$\Delta$ balanced accuracy (%)")
axB.set_title("(b) EEG: sign-flips, both concepts", fontsize=8.5, loc="left")
axB.yaxis.set_major_formatter(FormatStrFormatter("%+.1f"))
axB.legend(frameon=False, fontsize=6.6, loc="lower left", handlelength=1.2)

for ax in (axA, axB):
    ax.spines[["top", "right"]].set_visible(False)

fig.tight_layout(w_pad=1.4)
fig.savefig(OUT, bbox_inches="tight", dpi=300)
fig.savefig(OUT.replace(".pdf", ".png"), bbox_inches="tight", dpi=150)
print("wrote", os.path.abspath(OUT))
