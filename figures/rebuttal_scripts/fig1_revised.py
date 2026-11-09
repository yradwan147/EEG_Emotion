"""Revised Figure 1: conventional 3-panel matplotlib figure. All numbers read from data files."""
import os, sys, json, importlib.util
import numpy as np
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

FIG = "/ibex/project/c2323/yousef/EEG_Emotion/figures"
R = "/ibex/project/c2323/yousef/reports"
sys.path.insert(0, f"{FIG}/landmark/scripts")
from _lf_style import COLORS
spec = importlib.util.spec_from_file_location("v6", f"{FIG}/landmark/scripts/fig1_hero_v6.py")
v6 = importlib.util.module_from_spec(spec); spec.loader.exec_module(v6)  # reuse load_rows (main() not run)
EMO = v6.EMO

L, B, C, rBL, rCL, _, _ = v6.load_rows()
rows = [("CLIP text", L), ("Cohort EEG ridge", B), ("EEG classifier PC1", C)]

a4 = json.load(open(f"{R}/a4a_transition.json"))["groups"]
base = np.array(list(a4["sota_base_e150"]["per_seed"].values()))
import glob as _g, re as _re
# canonical +V-axis runs (same files as stats_rigor_final_compute.py val_topo_e150; topo lambda=0.05), seed-aligned to base
_aux = {int(_re.search(r"_s(\d+)\.json$", f)[1]): json.load(open(f))["test_bacc"]
        for f in _g.glob(f"{R}/sota_recipe_vaxis_runs/run_sota_topo_l0.05_e150_l0.05_s*.json")}
_bs = {int(k): v for k, v in a4["sota_base_e150"]["per_seed"].items()}
base = np.array([_bs[k] for k in sorted(_bs)]); aux = np.array([_aux[k] for k in sorted(_bs)])
assert abs((aux - base).mean() - (-0.0290)) < 5e-4, (aux - base).mean()
sem = lambda x: x.std(ddof=1) / np.sqrt(len(x))
bm, am = base.mean(), aux.mean()
assert abs(bm - 0.658) < 0.001 and 0.626 < am < 0.630, (bm, am)

w = json.load(open(f"{R}/rebuttal_2026_11/wave2b_analysis.json"))
emod = [w["C_base_curve"]["1"]["mean"], w["C_base_curve"]["10"]["mean"]]
sat = [w["B_curve_e150"]["1"]["mean"], w["C_matched_10v10"]["sat_ens10"]]
delta = w["C_matched_10v10"]["delta"]
for v, e in zip(emod + sat, (0.624, 0.662, 0.658, 0.694)):
    assert abs(v - e) < 0.001, (v, e)

mpl.rcParams.update({"pdf.fonttype": 42, "font.family": "sans-serif",
                     "font.sans-serif": ["Helvetica", "Arial", "DejaVu Sans"],
                     "font.size": 7, "axes.labelsize": 7, "axes.titlesize": 7.5,
                     "xtick.labelsize": 7, "ytick.labelsize": 7, "legend.fontsize": 7,
                     "axes.spines.top": False, "axes.spines.right": False, "axes.linewidth": 0.7})
fig = plt.figure(figsize=(7.0, 2.55))
gs = fig.add_gridspec(1, 3, width_ratios=[4.7, 1.9, 2.7], left=0.155, right=0.985, bottom=0.30, top=0.88, wspace=0.62)
axa, axb, axc = (fig.add_subplot(g) for g in gs)

# (a)
for i, (name, v) in enumerate(rows):
    y = 2 - i
    axa.axhline(y, color="#d0d0d0", lw=0.7, zorder=1)
    for z, e in zip(v, EMO):
        axa.scatter(z, y, s=28, color=COLORS[e], edgecolor="white", lw=0.5, zorder=3)
axa.set_yticks([2, 1, 0]); axa.set_yticklabels([r[0] for r in rows])
axa.set_ylim(-0.6, 2.6); axa.spines["left"].set_visible(False); axa.tick_params(axis="y", length=0)
axa.set_xlabel("Standardized class position (negative → positive valence)")
axa.set_title("(a) A concept already represented", loc="left", fontweight="bold")
axa.legend(handles=[Line2D([], [], marker="o", ls="", color=COLORS[e], markersize=4.5, label=e) for e in EMO] + [Line2D([], [], ls="", label=" ")],
           ncol=5, loc="upper center", bbox_to_anchor=(0.5, -0.26), frameon=False, handletextpad=0.1,
           columnspacing=0.8, fontsize=6.8)
axa.set_xlim(-2.2, 2.2)

# (b)
ymin, ymax = 0.60, 0.74
for x, v, s, c in ((0, bm, sem(base), "#4c78a8"), (1, am, sem(aux), "#e08a3c")):
    axb.bar(x, v, 0.65, color=c, yerr=s, capsize=2.5, error_kw=dict(lw=0.8), zorder=2)
    axb.text(x, v + s + 0.003, f"{v:.3f}", ha="center", va="bottom", fontsize=7)
axb.set_xticks([0, 1]); axb.set_xticklabels(["Base", "+V-axis"], fontsize=6.5)
axb.set_ylim(ymin, ymax); axb.set_xlim(-0.55, 1.55); axb.set_ylabel("Balanced accuracy")
axb.set_title("(b) Extra supervision", loc="left", fontweight="bold")
axb.text(0.5, 0.985, "0/25 auxiliary\nrecipes give a\nsignificant gain", transform=axb.transAxes,
         ha="center", va="top", fontsize=6.5, style="italic")
axb.set_ylim(ymin, ymax + 0.0)

# (c)
x = np.arange(2); wd = 0.36
axc.bar(x - wd / 2, emod, wd, color="#4c78a8", label="EMOD", zorder=2)
axc.bar(x + wd / 2, sat, wd, color="#2a9d8f", label="SatEnsemble", zorder=2)
for xs, vs in ((x - wd / 2, emod), (x + wd / 2, sat)):
    for xx, v in zip(xs, vs):
        axc.text(xx, v + 0.002, f"{v:.3f}", ha="center", va="bottom", fontsize=6.2)
top = max(sat[1], emod[1]) + 0.016
axc.plot([1 - wd / 2, 1 - wd / 2, 1 + wd / 2, 1 + wd / 2], [emod[1] + 0.015, top, top, sat[1] + 0.012], color="k", lw=0.7)
axc.text(1, top + 0.001, f"+{delta*100:.1f} pp", ha="center", va="bottom", fontsize=7, fontweight="bold")
axc.set_xticks(x); axc.set_xticklabels(["1", "10"])
axc.set_ylim(ymin, ymax); axc.set_xlim(-0.6, 1.6); axc.set_xlabel("Checkpoints averaged (k)"); axc.set_ylabel("Balanced accuracy")
axc.set_title("(c) SatEnsemble", loc="left", fontweight="bold")
axc.legend(loc="upper left", ncol=2, frameon=False, fontsize=6.3, columnspacing=0.6, handletextpad=0.3, handlelength=0.9, bbox_to_anchor=(-0.04, 1.02))

os.makedirs(f"{FIG}/landmark", exist_ok=True)
fig.savefig(f"{FIG}/landmark/fig1_final.pdf")
fig.savefig(f"{FIG}/landmark/fig1_final_preview.png", dpi=200)
print("base per-seed", base, "mean", bm, "sem", sem(base)); print("aux per-seed", aux, "mean", am, "sem", sem(aux))
print("emod", emod, "sat", sat, "delta", delta, "rBL", rBL, "rCL", rCL)
