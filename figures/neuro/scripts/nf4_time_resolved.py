"""NF4 — Time-resolved V-axis (LPP analogue).

(a) Per-second cohort |r| trace (t=0..29s) for 5 bands (5 lines, band-coded colours).
    Mark peaks with stars: alpha t=20, beta t=17, gamma t=2.  Light grey shading for
    LPP early-window (1-6s) and sustained-window (12-25s).

(b) Best-stim-cohort r per band (using 9-stim subset).

Inset on (b): per-subject peak-time histograms for alpha, illustrating that
only ~17-24% of subjects peak in the cohort 18-21s window.
"""
import os, sys, numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from scipy.ndimage import gaussian_filter1d

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _neuro_style import apply_neuro_style, COLORS, BAND_COLORS, save_dual

REPORTS = "/ibex/project/c2323/yousef/reports"
OUT_DIR = "/ibex/project/c2323/yousef/paper_neurips26_final/figures/neuro"
OUT_PAPER = "/ibex/project/c2323/yousef/EEG_Emotion/figures/neuro"


def main():
    apply_neuro_style()
    data = np.load(f"{REPORTS}/topography/nf_assets.npz")
    bands = list(data['bands'])
    coh   = data['time_resolved_cohort']      # (5, 30)
    bs    = data['time_resolved_best_stim']   # (5, 30)
    psp   = data['time_resolved_per_subj_peak']  # (5, Nsub)

    fig = plt.figure(figsize=(12.6, 5.6))
    gs = fig.add_gridspec(1, 2, left=0.06, right=0.985, top=0.84, bottom=0.12,
                          wspace=0.24)

    # --- helper: shade LPP windows ---
    def shade_lpp(ax):
        ax.axvspan(1, 6, color='#888888', alpha=0.10, zorder=0)
        ax.axvspan(12, 25, color='#888888', alpha=0.16, zorder=0)
        # textual labels on the shading
        ax.text(3.5, 0.025, 'LPP early\n(1–6 s)',
                fontsize=7, color='#555555', ha='center', va='bottom',
                fontstyle='italic', transform=ax.transData)
        ax.text(18.5, 0.025, 'LPP sustained  (12–25 s)',
                fontsize=7, color='#555555', ha='center', va='bottom',
                fontstyle='italic', transform=ax.transData)

    # ===================================================================
    # (a) cohort  |r|  per second per band
    # ===================================================================
    ax_a = fig.add_subplot(gs[0, 0])
    shade_lpp(ax_a)

    t = np.arange(30)
    for bi, b in enumerate(bands):
        # raw + smoothed traces
        raw = np.abs(coh[bi])
        smooth = gaussian_filter1d(raw, sigma=1.0)
        ax_a.plot(t, raw, color=BAND_COLORS[b], lw=0.7, alpha=0.35,
                  zorder=3 + bi)
        ax_a.plot(t, smooth, color=BAND_COLORS[b], lw=2.0, label=fr"$\{b}$",
                  zorder=4 + bi)

    # mark peaks with stars (use raw since the headline numbers are at integer t)
    peak_info = []  # (band, t, r)
    for bi, b in enumerate(bands):
        raw = np.abs(coh[bi])
        tp = int(np.argmax(raw))
        rp = float(coh[bi, tp])
        peak_info.append((b, tp, rp))
        ax_a.plot(tp, abs(rp), '*', color=BAND_COLORS[b],
                  markersize=14, markeredgecolor='black', markeredgewidth=0.8,
                  zorder=10)

    # annotation for top peaks (alpha, beta, gamma) — placed at axes-fraction
    # corners so they never overlap traces.
    a_b, a_t, a_r = next(p for p in peak_info if p[0] == 'alpha')
    b_b, b_t, b_r = next(p for p in peak_info if p[0] == 'beta')
    g_b, g_t, g_r = next(p for p in peak_info if p[0] == 'gamma')

    text_box = dict(boxstyle='round,pad=0.30', facecolor='white',
                    edgecolor='lightgray', linewidth=0.6, alpha=0.97)
    # Annotations in a vertical stack high in the panel (clear of data),
    # aligned right so all three boxes share a clean right edge.
    ax_a.annotate(fr"$\alpha$  $t={a_t}$s,  $|r|={abs(a_r):.2f}$",
                  xy=(a_t, abs(a_r)), xytext=(0.97, 0.93),
                  textcoords='axes fraction',
                  fontsize=8.5, fontweight='bold', color=BAND_COLORS['alpha'],
                  ha='right', va='center', bbox=text_box,
                  arrowprops=dict(arrowstyle='->', lw=0.7,
                                  color=BAND_COLORS['alpha']))
    ax_a.annotate(fr"$\beta$  $t={b_t}$s,  $|r|={abs(b_r):.2f}$",
                  xy=(b_t, abs(b_r)), xytext=(0.97, 0.83),
                  textcoords='axes fraction',
                  fontsize=8.5, fontweight='bold', color=BAND_COLORS['beta'],
                  ha='right', va='center', bbox=text_box,
                  arrowprops=dict(arrowstyle='->', lw=0.7,
                                  color=BAND_COLORS['beta']))
    ax_a.annotate(fr"$\gamma$  $t={g_t}$s,  $|r|={abs(g_r):.2f}$",
                  xy=(g_t, abs(g_r)), xytext=(0.97, 0.73),
                  textcoords='axes fraction',
                  fontsize=8.5, fontweight='bold', color=BAND_COLORS['gamma'],
                  ha='right', va='center', bbox=text_box,
                  arrowprops=dict(arrowstyle='->', lw=0.7,
                                  color=BAND_COLORS['gamma']))

    ax_a.set_xlabel("time within clip  (seconds)", fontsize=9)
    ax_a.set_ylabel(r"cohort  $|r|$  (V-net DE  vs.  V-axis)", fontsize=9)
    ax_a.set_xlim(0, 29)
    ax_a.set_ylim(0, 0.78)
    ax_a.set_xticks(np.arange(0, 30, 5))
    ax_a.legend(loc='upper left', fontsize=8.5, frameon=True, ncol=5,
                framealpha=0.95, handletextpad=0.4, columnspacing=0.6,
                bbox_to_anchor=(0.0, 1.0))
    ax_a.grid(alpha=0.20, linewidth=0.4)
    ax_a.set_axisbelow(True)
    ax_a.set_title("(a)  All 28 stim:  early gamma, sustained alpha/beta",
                   fontsize=10, fontweight='bold', loc='left', pad=4)

    # ===================================================================
    # (b) best-stim (9-stim subset) per second per band
    # ===================================================================
    ax_b = fig.add_subplot(gs[0, 1])
    shade_lpp(ax_b)

    for bi, b in enumerate(bands):
        raw = np.abs(bs[bi])
        smooth = gaussian_filter1d(raw, sigma=1.0)
        ax_b.plot(t, raw, color=BAND_COLORS[b], lw=0.7, alpha=0.35,
                  zorder=3 + bi)
        ax_b.plot(t, smooth, color=BAND_COLORS[b], lw=2.0, label=fr"$\{b}$",
                  zorder=4 + bi)

    # mark peaks
    for bi, b in enumerate(bands):
        tp = int(np.argmax(np.abs(bs[bi])))
        rp = float(bs[bi, tp])
        ax_b.plot(tp, abs(rp), '*', color=BAND_COLORS[b],
                  markersize=14, markeredgecolor='black', markeredgewidth=0.8,
                  zorder=10)

    a_t = int(np.argmax(np.abs(bs[bands.index('alpha')])))
    a_r = float(bs[bands.index('alpha'), a_t])
    b_t2 = int(np.argmax(np.abs(bs[bands.index('beta')])))
    b_r2 = float(bs[bands.index('beta'), b_t2])
    text_box = dict(boxstyle='round,pad=0.30', facecolor='white',
                    edgecolor='lightgray', linewidth=0.5, alpha=0.95)
    # Annotations placed at the right edge (after t≈22 the traces drop), so
    # both the inset (bottom-center) and the legend (top-left) stay clear.
    ax_b.annotate(fr"$\alpha$  $t={a_t}$s,  $|r|={abs(a_r):.2f}$",
                  xy=(a_t, abs(a_r)),
                  xytext=(0.97, 0.62),
                  textcoords='axes fraction',
                  fontsize=8.5, fontweight='bold', color=BAND_COLORS['alpha'],
                  ha='right', va='center', bbox=text_box,
                  arrowprops=dict(arrowstyle='->', lw=0.7,
                                  color=BAND_COLORS['alpha']))
    ax_b.annotate(fr"$\beta$  $t={b_t2}$s,  $|r|={abs(b_r2):.2f}$",
                  xy=(b_t2, abs(b_r2)),
                  xytext=(0.97, 0.50),
                  textcoords='axes fraction',
                  fontsize=8.5, fontweight='bold', color=BAND_COLORS['beta'],
                  ha='right', va='center', bbox=text_box,
                  arrowprops=dict(arrowstyle='->', lw=0.7,
                                  color=BAND_COLORS['beta']))

    ax_b.set_xlabel("time within clip  (seconds)", fontsize=9)
    ax_b.set_ylabel(r"best-stim cohort  $|r|$  (9-stim subset)", fontsize=9)
    ax_b.set_xlim(0, 29)
    ax_b.set_ylim(0, 0.95)
    ax_b.set_xticks(np.arange(0, 30, 5))
    ax_b.legend(loc='upper left', fontsize=8.5, frameon=True, ncol=5,
                framealpha=0.95, handletextpad=0.4, columnspacing=0.6)
    ax_b.grid(alpha=0.20, linewidth=0.4)
    ax_b.set_axisbelow(True)
    ax_b.set_title(r"(b)  9-stim emotional-pole subset:  alpha reaches |r| ≈ 0.78",
                   fontsize=10, fontweight='bold', loc='left', pad=4)

    # Inset: per-subject peak-time histogram for alpha — placed in
    # bottom-center where traces are lowest, avoiding all peaks.
    ax_inset = ax_b.inset_axes([0.34, 0.06, 0.32, 0.33])
    bi_alpha = bands.index('alpha')
    bins = np.arange(0, 31, 2)
    ax_inset.hist(psp[bi_alpha], bins=bins, color=BAND_COLORS['alpha'],
                  edgecolor='black', linewidth=0.4, alpha=0.85)
    # shade cohort 18-21s window
    ax_inset.axvspan(18, 21, color=COLORS['red'], alpha=0.22, zorder=0)
    ax_inset.set_xlabel(r"per-subject α-peak  t  (s)", fontsize=7.0)
    ax_inset.set_ylabel("# subj", fontsize=7.0)
    ax_inset.tick_params(axis='both', labelsize=6.5)
    pct_in = float(((psp[bi_alpha] >= 18) & (psp[bi_alpha] <= 21)).mean() * 100)
    ax_inset.set_title(f"only {pct_in:.0f}% peak in 18–21 s\n"
                       fr"($\sigma \approx {psp[bi_alpha].std():.0f}$ s)",
                       fontsize=7.0, pad=2)

    # global title
    fig.suptitle(
        "V-axis tracks two temporal regimes: early gamma (3–6 s) and sustained alpha/beta (17–21 s)",
        fontsize=12, fontweight='bold', y=0.97)

    save_dual(fig, f"{OUT_DIR}/NF4_time_resolved")
    save_dual(fig, f"{OUT_PAPER}/NF4_time_resolved")
    plt.close(fig)


if __name__ == "__main__":
    main()
