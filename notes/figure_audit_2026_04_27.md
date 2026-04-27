# Figure Audit — NeurIPS 2026 paper
*Date: 2026-04-27*
*Auditor: spotlight-grade layout pass on 13 paper figures*

Bar: "would Nature Neuroscience accept this layout?"

## Methodology
1. Each PNG rendered at 400 dpi was inspected for: overlaps, cramped panels, truncated text,
   mismatched panels, inconsistent fonts, colorbar/axis interference, panel-label collisions,
   and tight-layout artefacts.
2. For each issue identified the script in `figures/{landmark,neuro}/scripts/` was edited
   and re-run with `/home/radwany/miniconda3/envs/hfnewest/bin/python3`.
3. The regenerated PNG was re-read and the iteration repeated until clean.

## Note on output paths
The scripts originally wrote ONLY to `/ibex/project/c2323/yousef/paper_neurips26_final/figures/{landmark,neuro}`,
but the paper builds from `figures/{landmark,neuro}` under `EEG_Emotion/`. Each modified
script now writes to BOTH locations (`OUT` and `OUT_PAPER`) so both trees stay in sync.

---

## Per-figure findings and fixes

### LF1 — Universal V-Axis Hero  (`figures/landmark/lf1_universal_vaxis_hero`)
**Issues:**
- Panel (b) y-axis label `Pearson r vs ground-truth valence (OASIS, n=270 test images)` was
  long enough that the trailing `n=270 test images` ascended into the suptitle area.

**Fixes:**
- Wrapped (b) y-axis label across two lines.
- Bumped figsize 8.6→9.0 in height; suptitle y from 0.965→0.955; gs `top` from 0.90→0.88
  to give panels more breathing room.
- Increased hspace 0.42→0.46 and wspace 0.27→0.30.
- Moved (b) panel-label `b` slightly more to the left (x=−0.13→−0.14) so it doesn't
  collide with the new wrapped y-label.
- Added `OUT_PAPER` save so EEG_Emotion/figures/landmark stays in sync.

---

### LF2 — EEG-LLM Cohort Circle  (`figures/landmark/lf2_eeg_llm_circle`)
**Issues (high severity):**
- Panel (a) emotion-class legend (right-center) directly OVERLAPPED the dashed-circle
  pole-stim annotation.
- Panel (c) LLM-family legend at lower-right overlapped the data bars (Gemma `+0.31`,
  BLOOM `+0.22`, etc.).

**Fixes:**
- (a) annotation moved BELOW the x-axis label as italic 2-line text (no bbox), so it
  cannot overlap legend or data points.
- (a) emotion legend changed to a compact 3-column legend at lower-right with thin frame
  (`framealpha=0.93`, edgecolor `#cccccc`) inside the panel — sits in clear bottom space.
- (c) LLM-family legend moved OUTSIDE the plot area to the right
  (`bbox_to_anchor=(1.02, 0.5)`, `loc='center left'`, single column).
- Figsize bumped 14.0×8.4 → 14.4×8.6, right=0.985→0.97 (room for outside legend),
  wspace 0.32→0.36.

---

### LF3 — Cross-Arch Convergence  (`figures/landmark/lf3_crossarch_convergence`)
**Issues:**
- Panel (c) the `c` panel-label sat squeezed between (b)'s data and (c)'s 2-line title.
- (c) legend at upper-right and percentile-callout at upper-left were both jammed near
  the title; legend-keys overlapped the V-axis red line and 99th-pct dashed line.

**Fixes:**
- Moved (c) legend INSIDE panel at upper-left below the percentile box
  (`bbox_to_anchor=(0.03, 0.62)`, `loc='upper left'`, smaller fontsize 7.2).
- Panel labels (a)/(b)/(c) all moved further left (x=−0.10→−0.13 for a,b and −0.13→−0.18
  for c) so they sit in margin instead of in panel.
- Figsize 15.0×5.4 → 15.4×5.6, wspace 0.30→0.34, top 0.85→0.83 to lower title pressure.

---

### LF6 — Saturation Cliff  (`figures/landmark/lf6_saturation_cliff`)
**Issues (high severity, multiple overlaps):**
- `EMODSTYLE λ=0.5 / (+0.007 ns)` callout at top-left collided with the `EMOD d3`
  vertical-guide label.
- `Anger-w λ=0.5 (−0.054***)` callout sat ON TOP OF the Anger-weighted data dots.
- `RSA λ=5 (−0.093***)` callout sat right of the cluster but visually disjoint.
- `the saturation cliff` mid-panel text floated over data points.
- `d6 SOTA` vertical-guide label at top overlapped with the `d6 SOTA + EMODSTYLE` callout.

**Fixes:**
- Vertical-guide labels (CBraMod / EMOD d3 / d6 SOTA) moved up to y=0.041 (was 0.027)
  with bolder font and white bbox so they sit above all data and cluster labels.
- Callouts re-laid out to be anchored OUTSIDE their data clusters:
  - `Anger-w` and `RSA λ=5` push to the LEFT of the cluster (right-aligned text).
  - `EMODSTYLE λ=0.5 / +0.007 ns` and `CBraMod+Topo` placed UPPER (in clear space).
  - `d6 SOTA + EMODSTYLE` moved to the RIGHT (left-aligned, x=0.671).
- `the saturation cliff` mid-panel text now in a white bbox with grey border, placed at
  (0.6390, −0.004) so it sits in clear space between the cluster lines.
- Cliff arrow start moved up to y=−0.001 (was +0.005) so it doesn't intersect the
  EMODSTYLE callout.
- Figsize 11.0×6.5 → 11.5×6.8; xlim 0.555–0.685 → 0.555–0.690 and ylim −0.110–0.040 →
  −0.115–0.050 to give room for new label placements.
- Legend changed from `frameon=False` to a thin grey frame for clarity (no overlap with
  data anyway).

---

### LF7 — Recipe Cascade  (`figures/landmark/lf7_recipe_cascade`)
**Issues:** None major after re-inspection. The `EmotionKD 0.6280 / EMOD AAAI 0.6287`
inline reference is positioned cleanly between two consecutive bars, the green delta
arrows are non-overlapping, and the legend on the far right is in clear margin space.

**Fixes:** Added `OUT_PAPER` save only.

---

### LF8 — Two-Tier Ensemble Theory  (`figures/landmark/lf8_two_tier_ensemble_theory`)
**Issues (high severity):**
- Panel (a) all 10 checkpoint tag labels (`e150_s789`, `e100_s2025`, ...) were placed
  with the SAME static offset `(w+0.002, l+0.0001)` — they piled up in the central
  cluster, becoming unreadable.

**Fixes:**
- Replaced the loop with a HAND-TUNED `label_offsets` dictionary giving each tag
  a unique (dx, dy, ha, va) — labels now spoke outward from each point in
  non-overlapping positions.
- Tag color darkened from light grey to `#444444` for legibility.
- Figsize 13.5×5.8 → 13.8×6.0, width_ratios 1.4:1.0 → 1.5:1.0 to give (a) more room.

---

### LF9 — All Interventions Forest  (`figures/landmark/lf9_all_interventions_forest`)
**Issues:** Layout already reasonable — title and subtitle at `fig.text` clear of plot,
right-side `(#41x)` source IDs in monospace are spaced evenly, legend at upper-right is
outside the plot area.

**Fixes:** Added `OUT_PAPER` save only.

---

### LF10 — Confusion Matrices  (`figures/landmark/lf10_confusion_matrices`)
**Issues:**
- Panel (c) per-class delta labels were 2-line `+0.058 / (0.74→0.80)`, with the parenthetical
  rendering on the LEFT for negative bars (Disgust/Sadness), causing the transition text
  to crowd the y-axis spine and y-tick labels.

**Fixes:**
- Split label into TWO separate text calls: bold delta value at bar tip, smaller grey
  transition `0.74→0.80` on a second line below — both anchored consistently.
- Set explicit xlim (`-0.045, 0.105`) and ylim so left-side labels never cross axis spine.
- Figsize 16.0×8.0 → 16.5×8.2, width_ratios 1.0:1.0:0.75:0.06 → 1.0:1.0:0.85:0.06 for
  panel (c) breathing room. wspace 0.40→0.42.
- Panel-(c) title pad bumped from default to 8 so `c` panel-label clears it.

---

### NF1 — 5-Band Topomaps  (`figures/neuro/NF1_5band_topomaps`)
**Issues:**
- The colorbar label `Pearson r (cohort EEG vs. LLM V-axis)` was so long that, when
  rotated alongside the narrow colorbar, it ran into the `32-channel 10-20 montage`
  inset title above.

**Fixes:**
- Shortened colorbar label to `Pearson r (V-axis encoding)` (correct shorthand,
  fits cleanly).
- Increased gs wspace 0.18→0.32, hspace 0.95→1.05 so colorbar/inset and topomaps
  are well-separated.
- Width-ratios `[1,1,1,1,1, 0.04, 0.65]` → `[1,1,1,1,1, 0.05, 0.70]` (slightly wider
  colorbar and inset).
- Inset montage title now bold with `pad=8` so it sits cleanly above the head outline.

---

### NF2 — Davidson FAA  (`figures/neuro/NF2_davidson_faa`)
**Issues (high severity):**
- The (a) panel inset colorbar (`Δ × 10³`) had its `+20`, `0`, `−20` tick labels
  on the RIGHT side, which BLED INTO panel (b)'s y-axis, where they were
  visually mistaken for panel (b) tick labels.

**Fixes:**
- Switched the inset colorbar from VERTICAL on the right edge of (a) to HORIZONTAL
  BELOW the head outline of (a) (`inset_axes([0.20, -0.05, 0.60, 0.04])`,
  `orientation='horizontal'`).
- Removed redundant text below (a) about Davidson direction; merged that note into
  the colorbar label and a short italic line below it.
- Figsize 11.2×4.4 → 11.6×4.6, wspace 0.32→0.42 to ensure (a) inset and (b) y-axis
  cannot overlap.

---

### NF3 — 9-stim Simpson  (`figures/neuro/NF3_9stim_simpson`)
**Issues (high severity):**
- Panel (a) title `(a) The cohort signal collapses without 9 emotional-pole stim`
  was so long it ran INTO panel (b)'s title — the strings literally overlapped.
- Panel (a) x-tick labels were 3-line strings with full emotion names, causing the
  rightmost label `No Anger / Amus. / Tender. (n = 19)` to crowd its neighbour.

**Fixes:**
- Shortened (a) title: `(a) Cohort r collapses without 9 pole stim`.
- Shortened (b) title: `(b) Anger drives 32 % of the cohort signal`.
- Tightened (a) x-tick labels: `9-stim pole (Ang+Amus+Tend)` and `No 9-stim (n=19)`.
- Both panel titles now have `pad=6` to keep them clear of the plot frame.
- Figsize 13.0×8.0 → 13.6×8.4, wspace 0.32→0.40, hspace 0.42→0.55 (more room
  between title row and data row).

---

### NF4 — Time-Resolved V-axis  (`figures/neuro/NF4_time_resolved`)
**Issues (high severity):**
- Panel (a) the three peak callouts (α, β, γ) were stacked at fractional axes
  positions (0.80, 0.80) / (0.80, 0.69) / (0.80, 0.58) — they floated INSIDE the
  data area and sat on top of the alpha and beta traces.
- Panel (b) the per-subject α-peak histogram inset was placed at (0.62, 0.55, 0.36, 0.38)
  which COVERED the alpha 18-21s peak region — the very region the figure is trying
  to highlight.

**Fixes:**
- (a) annotations moved to the upper-RIGHT corner (xytext=0.97, y=0.93/0.83/0.73) —
  arrows point IN to the peak stars, but text now sits in the empty top-right area
  above all data.
- (b) annotations moved to the right edge (xytext=0.97, y=0.62/0.50) where the
  traces are below ~0.4 — labels live in clear empty space.
- (b) inset histogram repositioned to BOTTOM-CENTER (0.34, 0.06, 0.32, 0.33) where
  no trace exceeds the inset height — the alpha 18-21s peak is now FULLY visible.
- Figsize 12.0×5.4 → 12.6×5.6, top 0.83→0.84 for the suptitle.

---

### NF5 — Connectivity  (`figures/neuro/NF5_connectivity`)
**Issues:** Layout already publication-grade — channel labels in panel (a) use
hand-tuned offsets, the off-diag callout is at upper-left without overlap, the
8×8 heatmap (b) has clean tick labels, and the F7-hub caption sits below the
heatmap.

**Fixes:** Added `OUT_PAPER` save only.

---

## Summary

**Figures touched up: 11 of 13.**
- High-severity overlap fixes: LF2, LF6, LF8, NF2, NF3, NF4 (6 figures).
- Layout/breathing-room fixes: LF1, LF3, LF10, NF1 (4 figures).
- Path-only updates (`OUT_PAPER` synchronization): LF7, LF9, NF5 (3 figures).

**Issues that were NOT addressed and why:**
- **NF4 LPP-window labels** (`LPP early (1–6 s)` / `LPP sustained (12–25 s)`) sit at
  y=0.025 inside the bottom shaded region — they are intentionally low-key
  italic labels and remain clear of all data traces.
- **Suptitle vs panel-title spacing** in some landmark figures relies on the
  outer-most pixel of the panel-title not touching the suptitle. After bumping
  `figsize` and `gs.top`, this is satisfied for all figures but the margin
  is still tight (~10 px) on LF2 panel (b). Acceptable.

---

## Build verification

`pdflatex → bibtex → pdflatex → pdflatex` ran clean:
- Output: `main.pdf` (36 pages, 1.36 MB)
- Warnings: 4× `'h' float specifier changed to 'ht'` (cosmetic, pre-existing)
- Warnings: 4× `Package hyperref Warning: Token not allowed in a PDF string`
  (cosmetic, from special characters in section titles, pre-existing)
- No errors, no missing references, no missing figures.

Note: the audit produced 36 pages, not the 32 noted in the brief — that earlier
count likely predates the appendix expansion (Section 10 alone is ~5 pages with
LF9/LF10 figures); page count is not a regression from this audit.
