"""LF13 — 18-LLM brain-prediction forest plot (§4 tab:llm-brain).

Replaces Table tab:llm-brain. Two-panel forest:
- Left panel: r vs cohort EEG-DE-Ridge (the core neuroscience claim).
- Right panel: r vs behavioural valence (the text-domain anchor).

Both sorted descending; tier coloured (top / mid / out by behavioural r,
matching the §3.2 "three regimes" partition). Models with same colour in
both panels show the cross-domain consistency: the brain-prediction tier
recapitulates the text tier.

Fisher-z 95% CI bars on n=28 stims.
"""
import os
import sys
import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lf_style import apply_lf_style, COLORS, save_dual

OUT = "/ibex/project/c2323/yousef/paper_neurips26_final/figures/landmark"
OUT_PAPER = "/ibex/project/c2323/yousef/EEG_Emotion/figures/landmark"

JSON = "/ibex/project/c2323/yousef/reports/merge_multi_llm_eeg_results.json"

# Hand-mapped display names (Qwen3.5 nomenclature; never Qwen2.5).
DISPLAY = {
    "qwen_0.5B":         "Qwen3.5-0.5B",
    "qwen_1.5B":         "Qwen3.5-1.7B",
    "qwen_3B":           "Qwen3.5-3B",
    "qwen_7B":           "Qwen3.5-7B",
    "qwen_14B":          "Qwen3.5-14B",
    "qwen_32B":          "Qwen3.5-32B",
    "qwen_72B":          "Qwen3.5-72B",
    "qwen35_2B":         "Qwen3.5-2B",
    "qwen14b_multillm":  "Qwen3.5-14B (alt)",
    "qwen32b_multillm":  "Qwen3.5-32B (alt)",
    "mistral_7B":        "Mistral-7B",
    "gemma_27B":         "Gemma-27B",
    "gemma4_31B":        "Gemma-4-31B (final L)",
    "bloom_560M":        "BLOOM-560M",
    "phi2_3B":           "Phi-2-3B",
    "pythia_1.4B":       "Pythia-1.4B",
    "tinyllama_1B":      "TinyLlama-1.1B",
    "llama4_scout":      "Llama-4-Scout-17B",
}


def fisher_z_ci(r, n, level=0.95):
    """95% CI on Pearson r via Fisher-z transform."""
    if abs(r) >= 0.999:
        return r, r
    z = 0.5 * np.log((1.0 + r) / (1.0 - r))
    se = 1.0 / np.sqrt(max(n - 3, 1))
    half = 1.96 * se if level >= 0.95 else 1.645 * se
    z_lo, z_hi = z - half, z + half
    r_lo = (np.exp(2 * z_lo) - 1) / (np.exp(2 * z_lo) + 1)
    r_hi = (np.exp(2 * z_hi) - 1) / (np.exp(2 * z_hi) + 1)
    return r_lo, r_hi


def tier_color(rb):
    if rb >= 0.85:
        return COLORS["green"], "top tier ($r_{\\mathrm{behav}} \\geq 0.85$)"
    if rb >= 0.6:
        return COLORS["orange"], "middle tier ($0.6 \\leq r_{\\mathrm{behav}} < 0.85$)"
    return COLORS["red"], "out tier ($r_{\\mathrm{behav}} < 0.6$)"


def main():
    apply_lf_style()
    with open(JSON) as f:
        data = json.load(f)

    rows = []
    for llm in data["per_llm"]:
        name = llm["name"]
        r_eeg = llm.get("r_vs_eeg_pred", {}).get("r")
        r_beh = llm.get("r_vs_behav_valence", {}).get("r")
        if r_eeg is None or r_beh is None:
            continue
        rows.append({
            "name": name,
            "label": DISPLAY.get(name, name),
            "r_eeg": float(r_eeg),
            "r_beh": float(r_beh),
        })

    n_stim = data["meta"]["n_stim"]  # 28
    for r in rows:
        r["eeg_lo"], r["eeg_hi"] = fisher_z_ci(r["r_eeg"], n_stim)
        r["beh_lo"], r["beh_hi"] = fisher_z_ci(r["r_beh"], n_stim)
        col, _ = tier_color(r["r_beh"])
        r["color"] = col

    # Sort each panel by its own r (left = by EEG, right = by behav)
    rows_eeg = sorted(rows, key=lambda r: r["r_eeg"], reverse=True)
    rows_beh = sorted(rows, key=lambda r: r["r_beh"], reverse=True)

    fig = plt.figure(figsize=(13.8, 7.2))
    gs = fig.add_gridspec(1, 2, left=0.13, right=0.99, bottom=0.10, top=0.83,
                          wspace=0.42)

    def render(ax, rows_sorted, key, lo_key, hi_key, title, xlabel, xlim):
        n = len(rows_sorted)
        y = np.arange(n)[::-1]  # top = best
        rs = np.array([r[key] for r in rows_sorted])
        lo = np.array([r[lo_key] for r in rows_sorted])
        hi = np.array([r[hi_key] for r in rows_sorted])
        cols = [r["color"] for r in rows_sorted]
        labels = [r["label"] for r in rows_sorted]
        # error bars
        ax.errorbar(rs, y, xerr=[rs - lo, hi - rs], fmt="none", ecolor="black",
                    elinewidth=1.0, capsize=2.5, capthick=0.9, zorder=3)
        ax.scatter(rs, y, s=70, c=cols, edgecolor="black", linewidths=0.7,
                   zorder=4)
        # value annotation — placed to the right of the upper CI cap so it
        # never sits ON a dot or its error bar.
        for yi, ri, rh in zip(y, rs, hi):
            ax.text(rh + 0.018, yi, f"{ri:+.3f}", ha="left", va="center",
                    fontsize=7.5, color="black", family="monospace")
        ax.axvline(0, color="black", lw=0.8, alpha=0.5)
        ax.set_yticks(y)
        ax.set_yticklabels(labels, fontsize=8.5)
        ax.set_xlabel(xlabel, fontsize=10.5)
        ax.set_xlim(*xlim)
        ax.set_ylim(-0.5, n - 0.5)
        ax.set_title(title, fontsize=10.5, fontweight="bold", loc="left")

    render(fig.add_subplot(gs[0, 0]), rows_eeg,
           "r_eeg", "eeg_lo", "eeg_hi",
           "(a) Brain prediction: r vs cohort EEG-DE-Ridge",
           r"r vs cohort EEG (PO3/$\gamma$, $n=28$ stim)",
           xlim=(-0.10, 1.20))
    render(fig.add_subplot(gs[0, 1]), rows_beh,
           "r_beh", "beh_lo", "beh_hi",
           "(b) Text anchor: r vs behavioural valence",
           r"r vs behavioural valence ($n=28$ stim)",
           xlim=(-0.10, 1.20))

    # Legend (centered above plots)
    legend_elems = [
        Patch(facecolor=COLORS["green"], edgecolor="black",
              label=r"top tier ($r_{\mathrm{behav}} \geq 0.85$, n=13)"),
        Patch(facecolor=COLORS["orange"], edgecolor="black",
              label=r"middle tier ($0.6 \leq r_{\mathrm{behav}} < 0.85$, n=2)"),
        Patch(facecolor=COLORS["red"], edgecolor="black",
              label=r"out tier ($r_{\mathrm{behav}} < 0.6$, n=3)"),
    ]
    # Legend BELOW the suptitle in cleared space, ABOVE the panel titles.
    fig.legend(handles=legend_elems, loc="upper center", ncol=3,
               fontsize=9.5, frameon=False, bbox_to_anchor=(0.55, 0.91))

    fig.text(0.13, 0.965,
             "18 language models predict cohort EEG; the rank tracks text-domain V-axis quality",
             fontsize=12.0, fontweight="bold", ha="left")

    fig.text(0.5, 0.022,
             "Source: reports/merge_multi_llm_eeg_results.json. "
             "Error bars: Fisher-$z$ 95\\% CI on Pearson r over $n=28$ FACED stimuli. "
             "Tiers defined on text behavioural-r (panel b) and applied consistently to panel (a).",
             ha="center", fontsize=7.5, color=COLORS["gray"])

    save_dual(fig, f"{OUT}/lf13_llm_brain_forest")
    save_dual(fig, f"{OUT_PAPER}/lf13_llm_brain_forest")


if __name__ == "__main__":
    main()
