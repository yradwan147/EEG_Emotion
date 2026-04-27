"""NF3 — 9-stim emotional pole contrast + Simpson's paradox.

2 rows × 3 columns:
  Row 1 (top — drop-class diagnostics):
    (a) Subset r bars: full / 9-stim / 25-no-Anger / 19-no-9
    (b) Per-emotion drop-Δ bars (sorted descending)
    (c) PO3/γ scatter: EEG response vs V-axis projection across 28 stim,
        coloured by emotion class, with the 9 emotional-pole stim circled.

  Row 2 (bottom — Simpson's paradox):
    (d) per-subject r distribution at fixed top-8 channels (gamma)
    (e) per-subject best-channel oracle |r| distribution
    (f) text/summary panel
"""
import os, sys, numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.patches import Circle, Patch

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _neuro_style import apply_neuro_style, COLORS, save_dual

REPORTS = "/ibex/project/c2323/yousef/reports"
OUT_DIR = "/ibex/project/c2323/yousef/paper_neurips26_final/figures/neuro"
OUT_PAPER = "/ibex/project/c2323/yousef/EEG_Emotion/figures/neuro"

EMOTIONS = ['Anger', 'Disgust', 'Fear', 'Sadness', 'Neutral',
            'Amusement', 'Inspiration', 'Joy', 'Tenderness']
EMO_IDX = {
    'Anger':       list(range(0, 3)),
    'Disgust':     list(range(3, 6)),
    'Fear':        list(range(6, 9)),
    'Sadness':     list(range(9, 12)),
    'Neutral':     list(range(12, 16)),
    'Amusement':   list(range(16, 19)),
    'Inspiration': list(range(19, 22)),
    'Joy':         list(range(22, 25)),
    'Tenderness':  list(range(25, 28)),
}

EMO_COLORS = {
    'Anger':       '#c0392b',
    'Disgust':     '#7f8c8d',
    'Fear':        '#34495e',
    'Sadness':     '#2980b9',
    'Neutral':     '#95a5a6',
    'Amusement':   '#f39c12',
    'Inspiration': '#27ae60',
    'Joy':         '#f1c40f',
    'Tenderness':  '#e91e63',
}


def main():
    apply_neuro_style()
    data = np.load(f"{REPORTS}/topography/nf_assets.npz")
    drop_keys   = list(data['drop_subset_keys'])
    drop_vals   = data['drop_subset_values']
    per_emo_dd  = data['per_emotion_drop_delta']
    emos        = list(data['emotions'])
    v           = data['v_axis']
    po3_g       = data['po3_gamma_per_stim']
    simpson     = data['per_subject_simpson']
    cohort_top8 = float(data['cohort_r_top8_fixed'])
    oracle      = data['per_subject_oracle_abs']

    # --------------- figure layout ----------------
    fig = plt.figure(figsize=(13.6, 8.4))
    gs = fig.add_gridspec(
        2, 3,
        left=0.06, right=0.985, top=0.91, bottom=0.075,
        wspace=0.40, hspace=0.55,
    )

    # =========================================================================
    # (a) Drop-class subset r bars
    # =========================================================================
    ax_a = fig.add_subplot(gs[0, 0])
    labels = ['All 28\nstimuli',
              '9-stim pole\n(Ang+Amus\n+Tend)',
              'No Anger\n(n = 25)',
              'No 9-stim\n(n = 19)']
    ord_keys = ['all_28', 'anger_amus_tend_9', 'no_anger_25', 'no_9emot_19']
    vals_o = [drop_vals[drop_keys.index(k)] for k in ord_keys]
    bar_cols = [COLORS['darkblue'], '#0d4373', COLORS['blue'], COLORS['gray']]

    bars = ax_a.bar(np.arange(4), vals_o,
                    color=bar_cols, edgecolor='black', linewidth=0.5,
                    width=0.7)
    # Highlight the 9-stim bar with thicker edge
    bars[1].set_edgecolor(COLORS['red'])
    bars[1].set_linewidth(2.0)

    for b, v_ in zip(bars, vals_o):
        ax_a.text(b.get_x() + b.get_width() / 2,
                  v_ + (0.025 if v_ >= 0 else -0.05),
                  f"{v_:+.3f}", fontsize=9, ha='center',
                  va='bottom' if v_ >= 0 else 'top',
                  fontweight='bold')

    ax_a.axhline(0, color='black', lw=0.5, alpha=0.6)
    ax_a.set_xticks(np.arange(4))
    ax_a.set_xticklabels(labels, fontsize=8.0, linespacing=1.05)
    ax_a.set_ylabel(r"Cohort $r$ at PO3 / $\gamma$", fontsize=9)
    ax_a.set_ylim(-0.20, 1.15)
    ax_a.grid(axis='y', alpha=0.25, linewidth=0.4)
    ax_a.set_axisbelow(True)
    ax_a.set_title("(a)  Cohort r collapses without 9 pole stim",
                   fontsize=9.5, fontweight='bold', loc='left', pad=6)

    # =========================================================================
    # (b) Per-emotion drop Δ
    # =========================================================================
    ax_b = fig.add_subplot(gs[0, 1])
    order = np.argsort(per_emo_dd)
    ord_emos = [emos[i] for i in order]
    ord_vals = per_emo_dd[order]
    bar_cols_b = [EMO_COLORS[e] for e in ord_emos]
    barsb = ax_b.barh(np.arange(len(ord_emos)), ord_vals,
                      color=bar_cols_b, edgecolor='black', linewidth=0.5,
                      height=0.65)
    for b, vb in zip(barsb, ord_vals):
        ax_b.text(vb + (0.004 if vb >= 0 else -0.004),
                  b.get_y() + b.get_height() / 2,
                  f"{vb:+.3f}", fontsize=8.5, ha='left' if vb >= 0 else 'right',
                  va='center', fontweight='bold')

    ax_b.axvline(0, color='black', lw=0.5, alpha=0.6)
    ax_b.set_yticks(np.arange(len(ord_emos)))
    ax_b.set_yticklabels(ord_emos, fontsize=9)
    ax_b.set_xlabel(r"$\Delta r$  when class is dropped",
                    fontsize=9)
    ax_b.set_xlim(-0.21, 0.11)
    ax_b.grid(axis='x', alpha=0.25, linewidth=0.4)
    ax_b.set_axisbelow(True)
    ax_b.invert_yaxis()
    ax_b.set_title("(b)  Anger drives 32 % of the cohort signal",
                   fontsize=9.5, fontweight='bold', loc='left', pad=6)

    # =========================================================================
    # (c) Scatter PO3/γ vs V-axis
    # =========================================================================
    ax_c = fig.add_subplot(gs[0, 2])

    nine_set = set(EMO_IDX['Anger'] + EMO_IDX['Amusement'] + EMO_IDX['Tenderness'])

    legend_handles = []
    for emo in EMOTIONS:
        idxs = EMO_IDX[emo]
        col = EMO_COLORS[emo]
        ax_c.scatter(v[idxs], po3_g[idxs],
                     s=42, color=col, edgecolor='black', linewidth=0.5,
                     zorder=3, label=emo)
        legend_handles.append(Patch(facecolor=col, edgecolor='black',
                                    linewidth=0.4, label=emo))

    # Circle the 9 emotional-pole stim
    for idx in nine_set:
        ax_c.scatter(v[idx], po3_g[idx], s=180, facecolor='none',
                     edgecolor=COLORS['red'], linewidth=1.4, zorder=2)

    # regression line for full set + for 9-stim subset
    fit_full = np.polyfit(v, po3_g, 1)
    xf = np.linspace(v.min() - 0.1, v.max() + 0.1, 50)
    ax_c.plot(xf, np.polyval(fit_full, xf), '-', color='black',
              lw=1.2, alpha=0.7, label=f"all 28: r = {np.corrcoef(v,po3_g)[0,1]:+.2f}")
    n9 = sorted(nine_set)
    fit9 = np.polyfit(v[n9], po3_g[n9], 1)
    ax_c.plot(xf, np.polyval(fit9, xf), '--', color=COLORS['red'],
              lw=1.4, alpha=0.85,
              label=f"9-stim: r = {np.corrcoef(v[n9],po3_g[n9])[0,1]:+.2f}")

    ax_c.set_xlabel(r"V-axis projection  (LLM)", fontsize=9)
    ax_c.set_ylabel(r"PO3 / $\gamma$  cohort DE", fontsize=9)
    # Legend pushed BELOW the panel — keeps the scatter cloud uncluttered.
    ax_c.legend(loc='upper left', bbox_to_anchor=(-0.02, -0.18),
                frameon=False, fontsize=6.8, ncol=4,
                handletextpad=0.3, columnspacing=0.7,
                labelspacing=0.25)
    ax_c.grid(alpha=0.2, linewidth=0.4)
    ax_c.set_axisbelow(True)
    ax_c.set_title("(c)  Per-stim view: PO3 / γ × V-axis",
                   fontsize=9.5, fontweight='bold', loc='left', pad=4)

    # =========================================================================
    # (d) per-subject r at fixed top-8 channels (gamma)
    # =========================================================================
    ax_d = fig.add_subplot(gs[1, 0])
    bins = np.linspace(-0.8, 0.8, 25)
    ax_d.hist(simpson, bins=bins, color=COLORS['lightblue'],
              edgecolor='black', linewidth=0.5, alpha=0.92)

    mu_subj = float(np.mean(simpson))
    ax_d.axvline(mu_subj, color=COLORS['red'], lw=1.5, ls='-',
                 label=f"per-subject mean = {mu_subj:+.3f}")
    ax_d.axvline(cohort_top8, color=COLORS['darkblue'], lw=1.5, ls='--',
                 label=f"cohort r = {cohort_top8:+.3f}")
    ax_d.axvline(0, color='black', lw=0.5, alpha=0.5)

    ax_d.set_xlabel(r"per-subject  $r$  (V-axis vs top-8 / γ DE, 28 stim)",
                    fontsize=9)
    ax_d.set_ylabel("# subjects", fontsize=9)
    ax_d.legend(loc='upper left', fontsize=7.5, frameon=False)
    ax_d.grid(axis='y', alpha=0.25, linewidth=0.4)
    ax_d.set_axisbelow(True)
    ax_d.set_title("(d)  Simpson's paradox: cohort ≠ per-subject",
                   fontsize=9.5, fontweight='bold', loc='left', pad=4)

    # =========================================================================
    # (e) per-subject oracle |r| distribution
    # =========================================================================
    ax_e = fig.add_subplot(gs[1, 1])
    bins_e = np.linspace(0, 1, 25)
    ax_e.hist(oracle, bins=bins_e, color='#a3d977',
              edgecolor='black', linewidth=0.5, alpha=0.95)
    mu_or = float(np.mean(oracle))
    ax_e.axvline(mu_or, color=COLORS['green'], lw=1.6, ls='-',
                 label=f"mean oracle |r| = {mu_or:.3f}")
    ax_e.axvline(abs(cohort_top8), color=COLORS['darkblue'], lw=1.5, ls='--',
                 label=f"cohort fixed |r| = {abs(cohort_top8):.3f}")
    ax_e.set_xlabel(r"per-subject  best-(channel,band)  $|r|$",
                    fontsize=9)
    ax_e.set_ylabel("# subjects", fontsize=9)
    ax_e.legend(loc='upper left', fontsize=7.5, frameon=False)
    ax_e.grid(axis='y', alpha=0.25, linewidth=0.4)
    ax_e.set_axisbelow(True)
    ax_e.set_title("(e)  Per-subject oracle: 0.55 mean, 0.89 best",
                   fontsize=9.5, fontweight='bold', loc='left', pad=4)

    # =========================================================================
    # (f) Summary text panel
    # =========================================================================
    ax_f = fig.add_subplot(gs[1, 2])
    ax_f.set_xlim(0, 1); ax_f.set_ylim(0, 1)
    ax_f.axis('off')
    ax_f.set_title("(f)  Take-home", fontsize=9.5, fontweight='bold',
                   loc='left', pad=4)

    summary_lines = [
        ("Cohort signal", f"   r = {cohort_top8:+.3f}", COLORS['darkblue']),
        ("Per-subject mean", f"   r = {mu_subj:+.3f}", COLORS['red']),
        ("Per-subject oracle", f"   |r| = {mu_or:.3f}", COLORS['green']),
    ]
    y = 0.85
    for label, val, col in summary_lines:
        ax_f.text(0.05, y, label, fontsize=10, fontweight='bold', va='top',
                  color='black')
        ax_f.text(0.95, y, val, fontsize=11, fontweight='bold', va='top',
                  ha='right', color=col,
                  family='monospace')
        y -= 0.13

    ax_f.text(0.05, 0.42,
              "The cohort summary HIDES large per-subject signal that lives on "
              "idiosyncratic (channel, band) cells.",
              fontsize=8.5, va='top', ha='left',
              wrap=True, color=COLORS['gray'], fontstyle='italic')
    ax_f.text(0.05, 0.20,
              "Population-level claim:  POSITIVE   ✓\nWithin-subject claim:    requires per-subject channel selection",
              fontsize=8.5, va='top', ha='left', color='black',
              fontfamily='monospace')

    # ---------------- suptitle ----------------
    fig.suptitle(
        "The cohort V-axis is a 9-stimulus contrast, not a within-subject phenomenon",
        fontsize=12, fontweight='bold', y=0.97)

    save_dual(fig, f"{OUT_DIR}/NF3_9stim_simpson")
    save_dual(fig, f"{OUT_PAPER}/NF3_9stim_simpson")
    plt.close(fig)


if __name__ == "__main__":
    main()
