"""LF12 — Multilingual V-axis recovery (§3.5).

Replaces Table tab:multilingual. Grouped bar chart: 5 extractor families
on the x-axis, three coloured bars (Japanese, Arabic, Russian) per group,
y-axis is SST-2 zero-shot AUC (mapped from non-English stories). The
English-extractor reference (Qwen LM at the EN ceiling) is shown
as a horizontal hero line; chance (0.5) shown as a horizontal dotted line.

The visual story: causal English-centric Qwen collapses to chance on
non-English stories (English-bias diagnostic), while the multilingual
encoder-decoder mT0-base RECOVERS and exceeds the English ceiling on all
three languages at 5x smaller parameter count.
"""
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lf_style import apply_lf_style, COLORS, save_dual

OUT = "/ibex/project/c2323/yousef/paper_neurips26_final/figures/landmark"
OUT_PAPER = "/ibex/project/c2323/yousef/EEG_Emotion/figures/landmark"


# Source: reports/p1_lang_multilingual_synthesis.json
# Each row: extractor, params (B), is_multilingual, [ja, ar, ru]
ROWS = [
    ("Qwen-Inst.\n(causal, EN-centric)",                1.7,    False, [0.5145, 0.5185, 0.5524]),
    ("BLOOMZ-1B7\n(multilingual, causal)",              1.7,    True,  [0.6082, 0.5822, 0.5827]),
    ("XLM-RoBERTa-large\n(multilingual, encoder)",      0.560,  True,  [0.6272, 0.5799, 0.5168]),
    ("BLOOMZ-7B1\n(multilingual, causal)",              7.1,    True,  [0.5139, 0.5714, 0.5031]),
    ("mT0-base\n(multilingual, enc--dec)",              0.277,  True,  [0.8908, 0.9120, 0.9133]),
]
EN_BASELINE = 0.832   # Qwen3-4B EN reference (paper lead model)

LANG_COLORS = {
    "ja": COLORS["lightblue"],
    "ar": COLORS["orange"],
    "ru": COLORS["green"],
}

LANG_FULL = {"ja": "Japanese", "ar": "Arabic", "ru": "Russian"}


def main():
    apply_lf_style()
    n_groups = len(ROWS)
    width = 0.25
    x = np.arange(n_groups)

    fig = plt.figure(figsize=(11.0, 5.6))
    gs = fig.add_gridspec(1, 1, left=0.075, right=0.985, bottom=0.20, top=0.84)
    ax = fig.add_subplot(gs[0, 0])

    langs = ["ja", "ar", "ru"]
    for i, lang in enumerate(langs):
        vals = np.array([row[3][i] for row in ROWS])
        offset = (i - 1) * width
        bars = ax.bar(x + offset, vals, width=width,
                      color=LANG_COLORS[lang], edgecolor="black",
                      linewidth=0.6,
                      label=LANG_FULL[lang], zorder=3)
        for xi, v in zip(x + offset, vals):
            ax.text(xi, v + 0.012, f"{v:.2f}", ha="center", va="bottom",
                    fontsize=7.5, color="black")

    # English baseline — label placed on LEFT side at x=-0.45 so it sits
    # in the empty margin and never overlaps the tall mT0 bars on the right.
    ax.axhline(EN_BASELINE, color=COLORS["red"], lw=1.4, ls="--", zorder=4,
               alpha=0.85)
    ax.text(-0.45, EN_BASELINE + 0.012,
            f"Qwen3-4B EN-extractor reference  (SST-2 EN AUC = {EN_BASELINE:.3f})",
            ha="left", va="bottom", fontsize=8.5, color=COLORS["red"])

    # Chance line — label BELOW the line in the left margin (lower ylim slightly
    # so the label has room beneath the chance line without colliding with bars)
    ax.axhline(0.50, color="black", lw=0.8, ls=":", alpha=0.65, zorder=2)
    ax.text(-0.45, 0.494, "chance = 0.50", ha="left", va="top",
            fontsize=7.8, color=COLORS["gray"])

    # Highlight mT0 group
    ax.axvspan(n_groups - 1 - 0.45, n_groups - 1 + 0.45,
               color=COLORS["green"], alpha=0.07, zorder=1)
    ax.annotate("mT0-base recovers\n+ exceeds EN ceiling\n(5$\\times$ fewer params)",
                xy=(n_groups - 1 + 0.30, 0.91), xytext=(n_groups - 1.7, 0.97),
                fontsize=8.5, color=COLORS["darkblue"],
                arrowprops=dict(arrowstyle="->", color=COLORS["darkblue"], lw=0.9),
                ha="center")

    # English-bias annotation on Qwen group
    ax.annotate("Qwen on non-EN\nstories: chance\n(English bias)",
                xy=(0 + 0.0, 0.555), xytext=(-0.15, 0.71),
                fontsize=8.5, color=COLORS["red"],
                arrowprops=dict(arrowstyle="->", color=COLORS["red"], lw=0.9),
                ha="center")

    ax.set_xticks(x)
    ax.set_xticklabels([row[0] for row in ROWS], fontsize=8.5)
    ax.set_ylim(0.43, 1.0)
    ax.set_ylabel("SST-2 zero-shot AUC", fontsize=11)
    ax.set_xlim(-0.55, n_groups - 0.45)

    ax.legend(title="Source language of stories", loc="upper left",
              fontsize=9, title_fontsize=9.5, frameon=False,
              ncol=3, bbox_to_anchor=(0.001, 1.005))

    fig.text(0.075, 0.945,
             "Cross-lingual V-axis recovery: only the multilingual encoder--decoder bridges the English-bias gap",
             fontsize=11.5, fontweight="bold", ha="left")
    fig.text(0.075, 0.905,
             "Same 9-story recipe, English stories translated to Japanese, Arabic, Russian; "
             "evaluated on SST-2 (English).",
             fontsize=9.5, ha="left", color=COLORS["gray"])

    fig.text(0.5, 0.020,
             "Source: reports/p1_lang_multilingual_synthesis.json. "
             "Stories machine-translated EN $\\to$ \\{JA, AR, RU\\}; "
             "V-axis re-extracted per (extractor, language); SST-2 evaluated on English benchmark.",
             ha="center", fontsize=7.5, color=COLORS["gray"])

    save_dual(fig, f"{OUT}/lf12_multilingual_grouped")
    save_dual(fig, f"{OUT_PAPER}/lf12_multilingual_grouped")


if __name__ == "__main__":
    main()
