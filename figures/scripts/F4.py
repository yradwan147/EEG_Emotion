"""F4 — Brain Topography (§6 main).

5-panel topomap (one per band: δ θ α β γ) showing per-channel V-axis r on FACED.
"""
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

import mne

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _style import apply_style, COLORS, save_dual

REPORTS = "/ibex/project/c2323/yousef/reports"
OUT = "/ibex/project/c2323/yousef/paper_neurips26_final/figures"

# FACED 32-channel layout (10-20)
FACED_CHANNELS = ['Fp1', 'Fp2', 'Fz', 'F3', 'F4', 'F7', 'F8', 'FC1', 'FC2',
                  'FC5', 'FC6', 'Cz', 'C3', 'C4', 'T7', 'T8', 'CP1', 'CP2',
                  'CP5', 'CP6', 'Pz', 'P3', 'P4', 'P7', 'P8', 'PO3', 'PO4',
                  'Oz', 'O1', 'O2', 'A1', 'A2']
HIGHLIGHT = ["PO3", "F7", "O1"]


def main():
    apply_style()
    data = np.load(f"{REPORTS}/topography/per_channel_band_v_axis_r.npz")
    cohort_r = data["cohort_r"]  # (32, 5)
    bands = list(data["bands"])
    channels = list(data["channels"])

    # Drop A1, A2 (mastoids) for the topomap (10-20 system)
    use_idx = [i for i, c in enumerate(channels) if c not in ("A1", "A2")]
    use_channels = [channels[i] for i in use_idx]
    use_r = cohort_r[use_idx, :]  # (30, 5)

    # Build MNE info for topo plotting
    montage = mne.channels.make_standard_montage("standard_1020")
    info = mne.create_info(ch_names=use_channels, sfreq=1.0, ch_types="eeg")
    info.set_montage(montage, match_case=False, on_missing="ignore")

    # Symmetric color limits using global max abs
    vmax = float(np.nanmax(np.abs(use_r)))
    vmin = -vmax

    fig = plt.figure(figsize=(13.0, 3.6))
    gs = fig.add_gridspec(1, 6, width_ratios=[1, 1, 1, 1, 1, 0.07],
                          left=0.02, right=0.97, top=0.86, bottom=0.06,
                          wspace=0.18)
    cmap = plt.colormaps["RdBu_r"]
    ims = []
    for bi, band in enumerate(bands):
        ax = fig.add_subplot(gs[0, bi])
        vals = use_r[:, bi]
        im, _ = mne.viz.plot_topomap(
            vals, info, axes=ax, show=False, cmap=cmap,
            vlim=(vmin, vmax),
            sensors=True, contours=4, outlines="head",
            mask=np.array([c in HIGHLIGHT for c in use_channels]),
            mask_params=dict(marker="o", markerfacecolor="yellow",
                             markeredgecolor="black", markersize=7, linewidth=0.8),
            extrapolate="head",
        )
        ax.set_title(f"{band}", fontsize=11, fontweight="bold", pad=4)
        # peak channel + value annotation
        peak_i = np.nanargmax(np.abs(vals))
        peak_ch = use_channels[peak_i]
        peak_val = vals[peak_i]
        ax.text(0.5, -0.06, f"peak: {peak_ch} ({peak_val:+.2f})",
                transform=ax.transAxes, ha="center", va="top", fontsize=8,
                color=COLORS["darkblue"] if peak_val > 0 else COLORS["red"])
        ims.append(im)

    # Colorbar
    cax = fig.add_subplot(gs[0, 5])
    cbar = fig.colorbar(ims[-1], cax=cax)
    cbar.set_label("Pearson r (cohort)", fontsize=9)
    cbar.ax.tick_params(labelsize=8)

    # Super-title with key finding
    fig.suptitle("Per-channel V-axis encoding peaks in posterior cortex, "
                 "not the frontal asymmetry sites of classical FAA",
                 fontsize=11, fontweight="bold", y=0.99)

    # Region annotation on bottom
    fig.text(0.5, 0.005,
             "Highlighted: PO3, F7, O1 (top channels by |r|).  "
             "Region |r| ranking: occipital (0.21) > parietal (0.18) > central (0.18) > frontal (0.16).",
             fontsize=8.5, ha="center", color=COLORS["gray"])

    save_dual(fig, f"{OUT}/F4_brain_topography")
    print("F4 saved.")


if __name__ == "__main__":
    main()
