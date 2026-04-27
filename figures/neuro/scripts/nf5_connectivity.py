"""NF5 — V-axis functional connectivity network.

(a) Scalp-rendered network graph: 32-channel BioSemi montage; the 8 V-axis-aligned
    channels (PO3, F7, O1, P3, Oz, O2, P4, PO4) are larger filled red circles,
    others are small grey dots.  Edges between V-axis channels weighted by
    pairwise gamma-DE correlation (Fisher-z mean across subjects). Edge thickness
    proportional to r, edge colour green for r > 0.6.

(b) 8x8 connectivity heatmap with annotations.
"""
import os, sys, numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.lines import Line2D
import mne
from scipy.cluster.hierarchy import linkage, dendrogram, leaves_list
from scipy.spatial.distance import squareform

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _neuro_style import apply_neuro_style, COLORS, save_dual

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
VNET = ['PO3', 'F7', 'O1', 'P3', 'Oz', 'O2', 'P4', 'PO4']


def main():
    apply_neuro_style()
    data = np.load(f"{REPORTS}/topography/nf_assets.npz")
    M = data['connectivity_matrix']  # 8x8 Fisher-z mean
    labels = list(data['vaxis_top8'])
    print('connectivity matrix:')
    print(M)
    off = M[~np.eye(8, dtype=bool)]
    print(f"off-diag mean (Fisher-z) = {off.mean():.3f}")

    fig = plt.figure(figsize=(12.0, 6.0))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.05, 1.10],
                          left=0.04, right=0.985, top=0.85, bottom=0.13,
                          wspace=0.18)

    # ===================================================================
    # (a) Network graph on scalp
    # ===================================================================
    ax_a = fig.add_subplot(gs[0, 0])
    use_chs = [c for c in FACED_CH if c not in ('A1', 'A2')]
    montage = mne.channels.make_standard_montage("standard_1020")
    info = mne.create_info(ch_names=use_chs, sfreq=1.0, ch_types="eeg")
    info.set_montage(montage, match_case=False, on_missing="ignore")

    # blank head outline
    mne.viz.plot_topomap(np.zeros(len(use_chs)), info, axes=ax_a,
                         show=False, cmap='Greys', vlim=(-0.01, 0.01),
                         sensors=False,
                         contours=0, outlines='head', extrapolate='head', res=64)

    from mne.channels.layout import _find_topomap_coords
    pos2d = _find_topomap_coords(info, picks=list(range(len(use_chs))))

    # Draw all small grey dots for non-V-net channels
    vnet_set = set(VNET)
    for i, ch in enumerate(use_chs):
        x, y = pos2d[i]
        if ch in vnet_set:
            continue
        ax_a.plot(x, y, 'o', mfc='#d0d0d0', mec='#666666',
                  ms=5, mew=0.4, zorder=4)

    # Draw edges between V-net channels
    cmap_edge = plt.colormaps['viridis']
    norm_edge = mpl.colors.Normalize(vmin=0.4, vmax=0.95)
    edges = []
    for i in range(len(VNET)):
        for j in range(i + 1, len(VNET)):
            edges.append((i, j, M[i, j]))

    # sort by weight, draw weakest first (so strong edges sit on top)
    edges = sorted(edges, key=lambda e: e[2])
    for i, j, w in edges:
        ci = use_chs.index(VNET[i])
        cj = use_chs.index(VNET[j])
        x1, y1 = pos2d[ci]
        x2, y2 = pos2d[cj]
        # Edge style:
        #   weight in [0.4, 0.95] -> linewidth 0.5..3.5
        lw = 0.5 + 3.0 * (w - 0.4) / 0.55
        # Colour: green for w >= 0.6, gray for w < 0.6
        if w >= 0.6:
            ecolor = '#2ca02c'
        else:
            ecolor = '#bbbbbb'
        ax_a.plot([x1, x2], [y1, y2], '-',
                  color=ecolor, lw=lw,
                  alpha=0.85, solid_capstyle='round',
                  zorder=5 + (w > 0.6) * 1)

    # Draw V-net channels on top: red filled circles
    # Hand-tuned label offsets to avoid overlaps near posterior cluster
    label_offsets = {
        'F7':  (-0.030, +0.014, 'right', 'center'),
        'PO3': (-0.038, -0.018, 'right', 'top'),
        'PO4': (+0.038, -0.018, 'left',  'top'),
        'O1':  (-0.030, -0.040, 'right', 'top'),
        'O2':  (+0.030, -0.040, 'left',  'top'),
        'Oz':  (+0.025, -0.005, 'left',  'center'),
        'P3':  (-0.025, +0.018, 'right', 'bottom'),
        'P4':  (+0.025, +0.018, 'left',  'bottom'),
    }
    for i, ch in enumerate(VNET):
        ci = use_chs.index(ch)
        x, y = pos2d[ci]
        ax_a.plot(x, y, 'o', mfc='#d62728', mec='black',
                  ms=10, mew=1.0, zorder=10)
        dx, dy, ha, va = label_offsets.get(ch, (0.020, -0.018, 'left', 'top'))
        ax_a.text(x + dx, y + dy, ch, fontsize=8.5, fontweight='bold',
                  ha=ha, va=va, zorder=11,
                  bbox=dict(boxstyle='round,pad=0.15',
                            facecolor='white', edgecolor='none', alpha=0.85))

    ax_a.set_title("(a)  V-axis functional network on scalp",
                   fontsize=10, fontweight='bold', loc='left', pad=4)

    # legend for the edge styles
    leg_lines = [
        Line2D([0], [0], color='#2ca02c', lw=3.0, label='r ≥ 0.60  (within-network)'),
        Line2D([0], [0], color='#bbbbbb', lw=1.5, label='r < 0.60  (F7 frontal hub)'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='#d62728',
               markeredgecolor='black', markersize=9, label='V-axis channel (8)'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='#d0d0d0',
               markeredgecolor='#666666', markersize=5, label='other channel (22)'),
    ]
    ax_a.legend(handles=leg_lines, loc='lower left', fontsize=7.5,
                frameon=True, framealpha=0.95,
                handletextpad=0.5, labelspacing=0.4,
                bbox_to_anchor=(-0.02, -0.18))

    # subtle annotation about off-diagonal mean
    ax_a.text(0.02, 0.95,
              f"⟨ off-diag ⟩  =  {off.mean():.3f}\n"
              "Fisher-z mean  (n = 123)",
              transform=ax_a.transAxes,
              fontsize=8, fontweight='bold',
              ha='left', va='top',
              bbox=dict(boxstyle='round,pad=0.30', facecolor='#fff9d6',
                        edgecolor='#999999', linewidth=0.5))

    # ===================================================================
    # (b) 8x8 correlation matrix heatmap
    # ===================================================================
    ax_b = fig.add_subplot(gs[0, 1])
    # Hierarchical clustering reorder for clarity
    M_clust = M.copy()
    np.fill_diagonal(M_clust, 1.0)
    dist = 1.0 - M_clust
    # Make sure dist is symmetric and nonneg
    dist = (dist + dist.T) / 2.0
    np.fill_diagonal(dist, 0.0)
    sq = squareform(np.clip(dist, 0, None), checks=False)
    Z = linkage(sq, method='average')
    order = leaves_list(Z)
    print('cluster order:', [labels[i] for i in order])
    Mr = M[np.ix_(order, order)]
    labels_r = [labels[i] for i in order]

    # Mask diagonal
    Mvis = Mr.copy()
    np.fill_diagonal(Mvis, np.nan)

    cmap_ht = plt.colormaps['viridis'].copy()
    cmap_ht.set_bad('#222222', alpha=1.0)
    im = ax_b.imshow(Mvis, cmap=cmap_ht, vmin=0.4, vmax=0.95, aspect='equal')

    ax_b.set_xticks(np.arange(8))
    ax_b.set_yticks(np.arange(8))
    ax_b.set_xticklabels(labels_r, fontsize=9)
    ax_b.set_yticklabels(labels_r, fontsize=9)
    ax_b.tick_params(axis='x', length=2, top=False, bottom=True)
    ax_b.tick_params(axis='y', length=2, left=True, right=False)

    # cell annotations
    for i in range(8):
        for j in range(8):
            if i == j:
                continue
            v = Mr[i, j]
            color = 'white' if v < 0.7 else 'black'
            ax_b.text(j, i, f"{v:.2f}", ha='center', va='center',
                      fontsize=7.5, color=color, fontweight='bold')

    cb = fig.colorbar(im, ax=ax_b, fraction=0.045, pad=0.02)
    cb.set_label("γ-DE pairwise  r  (Fisher-z mean)", fontsize=9)
    cb.ax.tick_params(labelsize=8, length=2.5)

    ax_b.set_title("(b)  V-axis 8 × 8 connectivity matrix",
                   fontsize=10, fontweight='bold', loc='left', pad=4)

    # callout: F7 hub — placed BELOW colorbar/heatmap (no clipping)
    ax_b.text(0.5, -0.18,
              "F7 row/column carry the weakest links: the frontal hub joins the "
              "posterior cluster through long-range gamma coupling.",
              transform=ax_b.transAxes, fontsize=8,
              color=COLORS['gray'], ha='center', va='top',
              fontstyle='italic', wrap=True)

    # ---------------- suptitle ----------------
    fig.suptitle(
        "V-axis-aligned channels form a tight posterior-occipital network with F7 as frontal hub",
        fontsize=12, fontweight='bold', y=0.98)

    save_dual(fig, f"{OUT_DIR}/NF5_connectivity")
    save_dual(fig, f"{OUT_PAPER}/NF5_connectivity")
    plt.close(fig)


if __name__ == "__main__":
    main()
