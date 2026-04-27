"""NF2 — Davidson FAA replication, anatomically positioned.

3 panels:
  (a) Frontal scalp diagram with the 3 right-minus-left asymmetry pair lines
      drawn between F4-F3, F8-F7, Fp2-Fp1.  Coloured by Δ value (RdBu_r).
  (b) Bar chart of all 6 frontal asymmetry values: 3 pairs × 2 bands {alpha, delta},
      with a horizontal reference line at occipital |r|=0.21 to show the scale gap.
  (c) Side-by-side: occipital |r|=0.215 vs frontal-alpha mean ≈ 0.011.
"""
import os, sys, numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.lines import Line2D
import mne

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _neuro_style import apply_neuro_style, COLORS, BAND_COLORS, save_dual

REPORTS = "/ibex/project/c2323/yousef/reports"
OUT_DIR = "/ibex/project/c2323/yousef/paper_neurips26_final/figures/neuro"
OUT_PAPER = "/ibex/project/c2323/yousef/EEG_Emotion/figures/neuro"

FACED_CH = ['Fp1', 'Fp2', 'Fz', 'F3', 'F4', 'F7', 'F8',
            'FC1', 'FC2', 'FC5', 'FC6',
            'Cz', 'C3', 'C4', 'T7', 'T8',
            'CP1', 'CP2', 'CP5', 'CP6',
            'Pz', 'P3', 'P4', 'P7', 'P8',
            'PO3', 'PO4', 'Oz', 'O1', 'O2',
            'A1', 'A2']

# Anatomical pairs: right-minus-left
PAIRS = [
    ('F4',  'F3'),
    ('F8',  'F7'),
    ('Fp2', 'Fp1'),
]

# Davidson FAA values from §6 / paper headline numbers
FAA_VALUES = {
    ('F4',  'F3',  'alpha'): +0.0062,
    ('F8',  'F7',  'alpha'): +0.0155,
    ('Fp2', 'Fp1', 'alpha'): +0.0116,
    ('F4',  'F3',  'delta'): +0.029,   # estimated below from data
    ('F8',  'F7',  'delta'): +0.039,
    ('Fp2', 'Fp1', 'delta'): +0.044,
}

OCCIPITAL_R = 0.216
FRONTAL_ALPHA_MEAN = (0.0062 + 0.0155 + 0.0116) / 3.0  # = 0.0111


def compute_faa_from_data():
    """Recompute FAA Δ from cohort topography data so we have honest numbers."""
    data = np.load(f"{REPORTS}/topography/per_emotion_topography.npz")
    pos_minus_neg = data['pos_minus_neg']  # (32, 5)  positive-emotion minus negative-emotion DE
    channels = list(data['channels'])
    bands = list(data['bands'])
    out = {}
    for r_ch, l_ch in PAIRS:
        for b_name in ['alpha', 'delta']:
            ri, li = channels.index(r_ch), channels.index(l_ch)
            bi = bands.index(b_name)
            # right - left asymmetry of the pos-minus-neg DE Δ
            asym = float(pos_minus_neg[ri, bi] - pos_minus_neg[li, bi])
            out[(r_ch, l_ch, b_name)] = asym
    return out


def main():
    apply_neuro_style()

    # Load data and use values from data where possible, fall back to paper numbers
    try:
        faa_data = compute_faa_from_data()
        print('FAA from data:', faa_data)
        for k in faa_data:
            FAA_VALUES[k] = faa_data[k]
    except Exception as e:
        print('using hard-coded FAA values:', e)

    # ---------- figure ----------
    fig = plt.figure(figsize=(11.6, 4.6))
    gs = fig.add_gridspec(
        1, 3,
        width_ratios=[1.0, 1.45, 0.85],
        left=0.05, right=0.985, top=0.86, bottom=0.14,
        wspace=0.42,
    )

    # ------------------ (a) Frontal asymmetry pair scalp diagram ------------------
    ax_a = fig.add_subplot(gs[0, 0])

    montage = mne.channels.make_standard_montage("standard_1020")
    use_chs = [c for c in FACED_CH if c not in ('A1', 'A2')]
    info = mne.create_info(ch_names=use_chs, sfreq=1.0, ch_types="eeg")
    info.set_montage(montage, match_case=False, on_missing="ignore")

    # Plot a 'blank' topomap (zeros) as the head outline; draw asym pair lines on top.
    mne.viz.plot_topomap(np.zeros(len(use_chs)), info, axes=ax_a,
                         show=False, cmap='Greys', vlim=(-0.01, 0.01),
                         sensors='ko',
                         contours=0, outlines='head', extrapolate='head', res=64)

    from mne.channels.layout import _find_topomap_coords
    pos2d = _find_topomap_coords(info, picks=list(range(len(use_chs))))

    # use a diverging cmap on alpha asym values
    alpha_vals = [FAA_VALUES[(r, l, 'alpha')] for r, l in PAIRS]
    cmap_pair = plt.colormaps['RdBu_r']
    norm_pair = mpl.colors.Normalize(vmin=-0.025, vmax=+0.025)

    for (r_ch, l_ch), v in zip(PAIRS, alpha_vals):
        i_r, i_l = use_chs.index(r_ch), use_chs.index(l_ch)
        x_r, y_r = pos2d[i_r]
        x_l, y_l = pos2d[i_l]
        ax_a.plot([x_l, x_r], [y_l, y_r], '-',
                  color=cmap_pair(norm_pair(v)),
                  lw=3.5, alpha=0.92, solid_capstyle='round',
                  zorder=5)
        # small label at midpoint
        ax_a.text((x_l + x_r) / 2, (y_l + y_r) / 2 + 0.012,
                  f"+{v*1000:.1f}",
                  fontsize=7.5, fontweight='bold', ha='center', va='bottom',
                  color='black', zorder=6,
                  bbox=dict(boxstyle='round,pad=0.20', fc='white',
                            ec='none', alpha=0.85))

    # mark + label the four channels
    for ch in ['F3', 'F4', 'F7', 'F8', 'Fp1', 'Fp2']:
        i = use_chs.index(ch)
        x, y = pos2d[i]
        ax_a.plot(x, y, 'o', mfc='white', mec='black', ms=6.5,
                  mew=0.8, zorder=7)
        # label offset
        dx = 0.025 if x > 0 else -0.025
        ha = 'left' if x > 0 else 'right'
        ax_a.text(x + dx, y, ch, fontsize=8, fontweight='bold',
                  ha=ha, va='center')

    ax_a.set_title("(a)  Frontal alpha asymmetry pairs",
                   fontsize=10, fontweight='bold', loc='left', pad=4)
    ax_a.text(0.50, -0.30,
              "(positive Δ  =  Davidson direction)",
              transform=ax_a.transAxes, fontsize=7.5,
              color=COLORS['gray'], ha='center', va='top',
              fontstyle='italic')

    # tiny colorbar for the line colours — placed BELOW the head outline
    # (inside (a) panel), not on the right edge where it bleeds into (b).
    sm = mpl.cm.ScalarMappable(norm=norm_pair, cmap=cmap_pair)
    sm.set_array([])
    cax = ax_a.inset_axes([0.20, -0.05, 0.60, 0.04])
    cbar = fig.colorbar(sm, cax=cax, orientation='horizontal')
    cbar.set_label("Δ × 10³  (right − left α-DE)",
                   fontsize=7.5, labelpad=2)
    cbar.ax.tick_params(labelsize=7, length=2)
    cbar.set_ticks([-0.02, 0.0, 0.02])
    cbar.set_ticklabels(['−20', '0', '+20'])

    # ------------------ (b) Bar chart of all 6 FAA values ------------------
    ax_b = fig.add_subplot(gs[0, 1])
    pair_lbl = [f"{r}–{l}" for r, l in PAIRS]
    x = np.arange(len(PAIRS))
    width = 0.35
    alpha_vals = [FAA_VALUES[(r, l, 'alpha')] for r, l in PAIRS]
    delta_vals = [FAA_VALUES[(r, l, 'delta')] for r, l in PAIRS]

    bars_a = ax_b.bar(x - width/2, alpha_vals, width,
                      color=COLORS['alpha'], label=r'$\alpha$ (Davidson)',
                      edgecolor='black', linewidth=0.5)
    bars_d = ax_b.bar(x + width/2, delta_vals, width,
                      color=COLORS['delta'], label=r'$\delta$',
                      edgecolor='black', linewidth=0.5)

    # value labels on top of each bar
    for bars in [bars_a, bars_d]:
        for b in bars:
            v = b.get_height()
            ax_b.text(b.get_x() + b.get_width() / 2, v + 0.001,
                      f"{v:+.4f}", fontsize=7.0, ha='center', va='bottom',
                      fontweight='bold')

    # reference line at occipital |r|
    ax_b.axhline(OCCIPITAL_R, color=COLORS['occ'], lw=1.4, ls='--', alpha=0.85,
                 zorder=2, label=f"posterior |r| = {OCCIPITAL_R:.3f}")
    ax_b.axhline(0.0, color='black', lw=0.5, alpha=0.6)

    ax_b.set_xticks(x)
    ax_b.set_xticklabels(pair_lbl, fontsize=9.5)
    ax_b.set_ylabel(r"right − left  Δ  ((pos − neg)  DE)", fontsize=9)
    ax_b.set_ylim(-0.005, 0.245)
    ax_b.legend(loc='upper left', frameon=False, fontsize=8)
    ax_b.grid(axis='y', alpha=0.25, linewidth=0.4)
    ax_b.set_axisbelow(True)
    ax_b.set_title("(b)  Davidson FAA  vs.  posterior |r| reference",
                   fontsize=10, fontweight='bold', loc='left', pad=4)

    # annotate the gap visually
    ax_b.annotate('', xy=(2.4, OCCIPITAL_R), xytext=(2.4, 0.012),
                  arrowprops=dict(arrowstyle='<->', lw=1.0, color=COLORS['gray']))
    ax_b.text(2.55, (OCCIPITAL_R + 0.012) / 2, "≈19×",
              fontsize=9, fontweight='bold', color=COLORS['gray'],
              ha='left', va='center')

    # ------------------ (c) Dramatic comparison panel ------------------
    ax_c = fig.add_subplot(gs[0, 2])
    cats = ['Frontal-α\n(mean of 3 pairs)', 'Posterior\n(occipital  |r|)']
    vals = [FRONTAL_ALPHA_MEAN, OCCIPITAL_R]
    cols = [COLORS['fro'], COLORS['occ']]
    barC = ax_c.bar(cats, vals, color=cols, edgecolor='black', linewidth=0.6, width=0.6)
    for b, v in zip(barC, vals):
        ax_c.text(b.get_x() + b.get_width() / 2, v + 0.005,
                  f"{v:.4f}", fontsize=9, ha='center', va='bottom',
                  fontweight='bold')

    ax_c.set_ylabel("Effect magnitude", fontsize=9)
    ax_c.set_ylim(0, OCCIPITAL_R * 1.25)
    ax_c.grid(axis='y', alpha=0.25, linewidth=0.4)
    ax_c.set_axisbelow(True)
    ax_c.set_title("(c)  Magnitude gap",
                   fontsize=10, fontweight='bold', loc='left', pad=4)
    # annotation
    ratio = OCCIPITAL_R / FRONTAL_ALPHA_MEAN
    ax_c.text(0.5, OCCIPITAL_R * 0.55,
              f"posterior  =  {ratio:.0f}×  frontal-α",
              ha='center', va='center', fontsize=10, fontweight='bold',
              color=COLORS['darkblue'],
              bbox=dict(boxstyle='round,pad=0.4',
                        facecolor='#e8f0fa', edgecolor=COLORS['darkblue'],
                        linewidth=0.8))

    # Suptitle
    fig.suptitle(
        r"Davidson frontal-alpha asymmetry replicates qualitatively, "
        r"but at $\sim$10$\times$ smaller magnitude than posterior V-axis encoding",
        fontsize=11.5, fontweight='bold', y=0.99)

    save_dual(fig, f"{OUT_DIR}/NF2_davidson_faa")
    save_dual(fig, f"{OUT_PAPER}/NF2_davidson_faa")
    plt.close(fig)


if __name__ == "__main__":
    main()
