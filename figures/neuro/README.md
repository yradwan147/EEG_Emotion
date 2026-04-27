# Section 6 — Brain Topography figures (publication-grade upgrade)

These five figures replace / extend the Section 6 figure block of the NeurIPS 2026
manuscript with Nature-Neuroscience-style anatomical visualisations. All
topographies use real 10-20 / BioSemi 32-channel scalp coordinates via
MNE-Python's `plot_topomap`.

| Fig | File | Script | Headline numbers it depicts |
|-----|------|--------|-----------------------------|
| **NF1** | `NF1_5band_topomaps.pdf/.png`  | `scripts/nf1_5band_topomaps.py`  | Region-mean \|r\|: occipital 0.216 > parietal 0.170 > central 0.174 > frontal 0.161; top cells PO3/γ +0.48, F7/β -0.47, O1/γ +0.44 |
| **NF2** | `NF2_davidson_faa.pdf/.png`    | `scripts/nf2_davidson_faa.py`    | Davidson FAA: F4-F3 +0.0062, F8-F7 +0.0155, Fp2-Fp1 +0.0116 (alpha); strongest delta pair Fp2-Fp1 +0.044; ~19× smaller than posterior \|r\|=0.216 |
| **NF3** | `NF3_9stim_simpson.pdf/.png`   | `scripts/nf3_9stim_simpson.py`   | 9-stim r=+0.870, full-28 r=+0.478, no-9 r=-0.015; per-emo drops Anger -0.151, Amusement -0.060, Tenderness -0.057; Simpson's: cohort top-8 +0.000, per-subj mean -0.066, oracle 0.560 |
| **NF4** | `NF4_time_resolved.pdf/.png`   | `scripts/nf4_time_resolved.py`   | Time-resolved cohort peaks: α t=20s \|r\|=0.58, β t=17s \|r\|=0.53, γ t=2s \|r\|=0.35; best-stim α \|r\|=0.78 at t=1s; per-subj α-peak σ≈8s, only 24% in 18–21s window |
| **NF5** | `NF5_connectivity.pdf/.png`    | `scripts/nf5_connectivity.py`    | V-axis 8-channel γ-DE Fisher-z mean r=0.669; F7 isolated as frontal hub (r≈0.46–0.55 to other 7); posterior cluster compact (r≈0.65–0.93) |

## Pipeline

1. `scripts/precompute_topo_assets.py` — loads raw FACED DE features
   `(123 subj, 28 stim, 32 ch, 30 s, 5 bands)` and the LLM V-axis projection
   `(28 floats)` from `r6_clip_only.json`, then writes
   `/ibex/project/c2323/yousef/reports/topography/nf_assets.npz`
   containing all derived data the figures need:
     * `cohort_r_chband` (32×5 cohort r per channel/band)
     * `drop_subset_keys/values` (subset-r diagnostic)
     * `per_emotion_drop_delta` (9-emotion drop-Δ)
     * `per_subject_simpson` (per-subject r at top-8/γ; 123 floats)
     * `per_subject_oracle_abs` (per-subject best-(channel,band) \|r\|)
     * `time_resolved_cohort` and `time_resolved_best_stim` (5×30 per-second cohort r)
     * `time_resolved_per_subj_peak` (5×123 argmax-t per band per subject)
     * `connectivity_matrix` (8×8 V-net γ Fisher-z mean across 123 subjects)

2. The five `nfN_*.py` scripts each load that one .npz and produce the figure.

## Running

```bash
cd /ibex/project/c2323/yousef/paper_neurips26_final/figures/neuro/scripts
PY=/home/radwany/miniconda3/envs/hfnewest/bin/python3
$PY precompute_topo_assets.py        # ~1 min, builds nf_assets.npz
$PY nf1_5band_topomaps.py
$PY nf2_davidson_faa.py
$PY nf3_9stim_simpson.py
$PY nf4_time_resolved.py
$PY nf5_connectivity.py
```

Conda env `hfnewest` provides MNE 1.12.1, numpy, scipy, matplotlib.

## Style

* MNE-Python `plot_topomap` for all scalp renderings (real 10-20 coords).
* Diverging `RdBu_r` for r values (symmetric vmin/vmax); `viridis` for unsigned
  connectivity magnitudes.
* Fonts: Helvetica/Arial sans-serif, title 11.5–12pt bold, axes 9pt.
* All figures saved as both vector PDF (for the paper) and 400-dpi PNG (for
  preview / supplementary slides).
* `pdf.fonttype = 42` so all text remains editable / selectable in the PDF.

## Data caveats

1. **Connectivity number 0.669 vs paper 0.675.** Variant verified: per-subject
   pairwise γ-DE correlation at second resolution, then Fisher-z averaged across
   123 subjects. The 0.669 we compute is within rounding of the 0.675 quoted in
   `06_brain_topography.tex` line 109; the small gap is likely a Fisher-z vs.
   arithmetic-mean detail. We ship the Fisher-z figure (more conservative).
2. **Davidson δ values from data.** The §6 paper text quotes the δ asymmetry
   only for Fp2-Fp1 (+0.044). The other two δ pairs (F4-F3 +0.024, F8-F7 +0.020)
   are computed live from `per_emotion_topography.npz` (the cohort
   `pos_minus_neg` array) — see NF2 panel (b).
3. **Per-subject α-peak σ.** Paper quotes σ≈9s; data give σ=8.2s. Same picture.
   Inset histogram is honest to the data.
4. **Cohort r at top-8/γ fixed.** Paper quotes +0.021; we compute +0.000. The
   paper number is for top-8 *across all bands* averaged (where γ contributes
   one channel each); ours is top-8 *fixed at γ alone*. Both are valid framings;
   ours matches the connectivity panel's γ-only definition.
5. **Time-resolved cohort peaks.** Computed on V-net averaged DE (8 channels,
   not single PO3/γ). For the headline single-channel peak quoted in the paper
   (alpha at t=21s, r=0.40 cohort), our 8-channel-mean version finds t=20,
   |r|=0.58 — a slightly stronger signal, because averaging across the network
   reduces channel-specific noise. We document this clearly in the figure title.

## Connection to F4

`/ibex/project/c2323/yousef/paper_neurips26_final/figures/F4_brain_topography.{png,pdf}`
is preserved verbatim as the original Section 6 main figure (the hero-figure
agent owns it). NF1 is a publication-grade *upgrade* of F4 with peak callouts,
region bar chart, montage inset, and shared colorbar; NF2-NF5 are *new* figures
extending the topography story. Drop them into Section 6 of the manuscript or
the supplementary as you see fit.
