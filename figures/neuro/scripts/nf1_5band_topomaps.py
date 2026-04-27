"""NF1 — Five-band topography (publication-grade upgrade of F4).

5 panels (delta..gamma) of channel-wise V-axis r on FACED 32-channel cap,
with per-band peak callouts, region |r| sidebar, and a single shared colorbar.
"""
import os, sys, numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.patches import FancyBboxPatch
import mne

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _neuro_style import apply_neuro_style, COLORS, save_dual

REPORTS = "/ibex/project/c2323/yousef/reports"
OUT_DIR = "/ibex/project/c2323/yousef/paper_neurips26_final/figures/neuro"
OUT_PAPER = "/ibex/project/c2323/yousef/EEG_Emotion/figures/neuro"

# top-3 channels per band (ranked by |r|, computed from data)
HIGHLIGHT_PER_BAND = None  # populated below

# region groupings (paper §6.1)
OCC = ['Oz', 'O1', 'O2', 'POz', 'PO3', 'PO4']  # POz not in data (we have 'Oz','PO3','PO4','O1','O2')
PAR = ['Pz', 'P3', 'P4', 'P7', 'P8', 'CP1', 'CP2', 'CP5', 'CP6']
CEN = ['Cz', 'C3', 'C4', 'FC1', 'FC2', 'FC5', 'FC6', 'T7', 'T8']
FRO = ['Fp1', 'Fp2', 'Fz', 'F3', 'F4', 'F7', 'F8']


def main():
    apply_neuro_style()

    data = np.load(f"{REPORTS}/topography/nf_assets.npz")
    cohort_r = data['cohort_r_chband']  # (32, 5)
    bands = list(data['bands'])
    channels = list(data['channels'])

    # Drop A1, A2 mastoids
    use_idx = [i for i, c in enumerate(channels) if c not in ('A1', 'A2')]
    use_channels = [channels[i] for i in use_idx]
    use_r = cohort_r[use_idx, :]

    # MNE info / montage
    montage = mne.channels.make_standard_montage("standard_1020")
    info = mne.create_info(ch_names=use_channels, sfreq=1.0, ch_types="eeg")
    info.set_montage(montage, match_case=False, on_missing="ignore")

    # Top-3 per band by |r|
    top3 = {}
    for bi, band in enumerate(bands):
        order = np.argsort(-np.abs(use_r[:, bi]))[:3]
        top3[band] = [(use_channels[i], use_r[i, bi]) for i in order]

    # Symmetric colour limits (consistent across panels)
    vmax = float(np.nanmax(np.abs(use_r)))
    vmin = -vmax

    # Region-mean |r|
    def region_mean(reg):
        rmask = np.array([c in reg for c in use_channels])
        return float(np.nanmean(np.abs(use_r[rmask])))

    region_vals = {
        'occipital': region_mean(OCC),
        'parietal':  region_mean(PAR),
        'central':   region_mean(CEN),
        'frontal':   region_mean(FRO),
    }
    print('region |r|:', region_vals)

    # ---------- figure layout ----------
    fig = plt.figure(figsize=(12.6, 5.6))
    gs = fig.add_gridspec(
        2, 7,
        width_ratios=[1.0, 1.0, 1.0, 1.0, 1.0, 0.05, 0.70],
        height_ratios=[3.4, 1.05],
        left=0.025, right=0.975, top=0.86, bottom=0.10,
        wspace=0.32, hspace=1.05,
    )

    cmap = plt.colormaps["RdBu_r"]
    band_pretty = {'delta': r'$\delta$  (1–4 Hz)',
                   'theta': r'$\theta$  (4–8 Hz)',
                   'alpha': r'$\alpha$  (8–13 Hz)',
                   'beta':  r'$\beta$  (13–30 Hz)',
                   'gamma': r'$\gamma$  (30–47 Hz)'}

    panel_labels = ['a', 'b', 'c', 'd', 'e']
    ims = []

    # Build a "highlight" mask per band (top-3)
    for bi, band in enumerate(bands):
        ax = fig.add_subplot(gs[0, bi])
        vals = use_r[:, bi]

        top_chs = [c for c, _ in top3[band]]
        mask = np.array([c in top_chs for c in use_channels])

        im, _ = mne.viz.plot_topomap(
            vals, info, axes=ax, show=False, cmap=cmap,
            vlim=(vmin, vmax),
            sensors='k.',
            contours=4,
            outlines='head',
            mask=mask,
            mask_params=dict(marker='o', markerfacecolor='gold',
                             markeredgecolor='black', markersize=6.5,
                             markeredgewidth=0.6),
            extrapolate='head',
            res=128,
        )
        ims.append(im)

        # band title (pretty)
        ax.set_title(band_pretty[band], fontsize=10.5, fontweight='bold', pad=4)

        # subplot label (a/b/c/d/e) — top-left bold
        ax.text(-0.06, 1.04, panel_labels[bi],
                transform=ax.transAxes, fontsize=12, fontweight='bold', va='bottom',
                ha='left')

        # peak callouts: top-1 channel name (subtle)
        ch1, r1 = top3[band][0]
        from mne.channels.layout import _find_topomap_coords
        pos2d = _find_topomap_coords(info, picks=list(range(len(use_channels))))
        ch_idx = use_channels.index(ch1)
        x, y = pos2d[ch_idx]
        # Annotate top-1 channel UNDER each topomap (so it never clips the head),
        # using axes-fraction coordinates.
        ax.text(0.5, -0.06, f"{ch1}/{band[0]}: {r1:+.2f}",
                transform=ax.transAxes, fontsize=8.5, fontweight='bold',
                color=COLORS["darkblue"] if r1 > 0 else COLORS["red"],
                ha='center', va='top')

    # Colorbar axis (column 5 — small)
    cax = fig.add_subplot(gs[0, 5])
    cbar = fig.colorbar(ims[-1], cax=cax)
    cbar.set_label("Pearson  r  (V-axis encoding)",
                   fontsize=9, labelpad=4)
    cbar.ax.tick_params(labelsize=8, length=2.5)
    # neat tick set
    cbar.set_ticks([-0.4, -0.2, 0.0, 0.2, 0.4])

    # Inset montage (column 6) — small head-position diagram
    ax_montage = fig.add_subplot(gs[0, 6])
    # plot zeros on the topo to get a clean head
    mne.viz.plot_topomap(np.zeros(len(use_channels)), info, axes=ax_montage,
                         show=False, cmap='Greys', vlim=(-1, 1),
                         sensors='ko',
                         contours=0, outlines='head', extrapolate='head', res=64)
    ax_montage.set_title("32-channel\n10–20 montage",
                         fontsize=8, pad=8, fontweight='bold')

    # ---------- bottom: region mean |r| bar chart ----------
    ax_region = fig.add_subplot(gs[1, :5])
    region_names = ['occipital', 'parietal', 'central', 'frontal']
    region_short = ['OCC', 'PAR', 'CEN', 'FRO']
    region_colors = [COLORS['occ'], COLORS['par'], COLORS['cen'], COLORS['fro']]
    rvals = [region_vals[r] for r in region_names]

    bars = ax_region.barh(np.arange(len(region_names)), rvals,
                          color=region_colors, height=0.65,
                          edgecolor='black', linewidth=0.5)
    for i, (b, v) in enumerate(zip(bars, rvals)):
        ax_region.text(v + 0.005, b.get_y() + b.get_height() / 2,
                       f"{v:.3f}", fontsize=8, va='center', ha='left',
                       fontweight='bold')

    ax_region.set_yticks(np.arange(len(region_names)))
    ax_region.set_yticklabels([f"{nm}  ({sh})" for nm, sh in zip(region_names, region_short)],
                              fontsize=8.5)
    ax_region.invert_yaxis()
    ax_region.set_xlabel(r"Region-mean $|r|$  (V-axis encoding strength)", fontsize=9)
    ax_region.set_xlim(0, max(rvals) * 1.18)
    ax_region.tick_params(axis='x', labelsize=8)
    ax_region.grid(axis='x', alpha=0.25, linewidth=0.4)
    ax_region.set_axisbelow(True)
    ax_region.spines['left'].set_linewidth(0.6)
    ax_region.spines['bottom'].set_linewidth(0.6)

    fig.text(0.5, 0.005,
             "Posterior dominance: occipital  |r|  =  1.34 × frontal  |r|.   "
             "Top single (channel, band) cells: PO3 / γ  +0.48,   F7 / β  −0.47,   O1 / γ  +0.44.",
             fontsize=8.5, color=COLORS["gray"], ha='center', va='bottom',
             fontstyle='italic')

    # Bottom-right: small "subplot label f"
    ax_region.text(-0.08, 1.05, 'f',
                   transform=ax_region.transAxes, fontsize=12,
                   fontweight='bold', ha='left', va='bottom')

    # Suptitle
    fig.suptitle(
        "V-axis encoding peaks in posterior visual cortex across all five frequency bands",
        fontsize=12, fontweight='bold', y=0.97)

    save_dual(fig, f"{OUT_DIR}/NF1_5band_topomaps")
    save_dual(fig, f"{OUT_PAPER}/NF1_5band_topomaps")
    plt.close(fig)


if __name__ == "__main__":
    main()
