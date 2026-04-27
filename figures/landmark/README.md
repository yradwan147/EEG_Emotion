# Landmark figures (NeurIPS 2026)

This directory contains the eight landmark-grade non-topography figures.
Each figure has both a vector PDF (for the LaTeX submission) and a 400 dpi PNG
(for visual review). Source scripts live under `scripts/`. Topography figures
are produced separately under `../neuro/`. The hero F1-F10 versions in `..` are
the original drafts — landmark counterparts here supersede them visually.

| File | Role | Key numbers shown | Source data |
|------|------|-------------------|-------------|
| `lf1_universal_vaxis_hero.pdf` | Teaser / abstract page. One V-axis recovered across language, vision, EEG, and brain. | text AUC up to 0.95 (Yelp); CLIP V-axis r=+0.869 vs ridge 0.836 (BEATS supervised); cross-arch r=+0.885 (n=36); brain r=+0.874 (n=28) | `reports/p1_task_matrix.json`, `reports/p1_vision_based_v_axis.json`, `reports/crossarch_random_control.json`, `reports/r6_eeg_llm_circle.json` |
| `lf2_eeg_llm_circle.pdf` | §4 main. 28 stim scatter (CLIP V-axis vs PO3/γ EEG); permutation null; 18-LLM brain rank with Qwen3.5-1.7B leading. | r=+0.874, p<10⁻⁹; random-direction r=+0.07; Qwen3.5-1.7B r=+0.411 leads 18-LLM rank | `reports/r6_eeg_llm_circle.json`, `reports/eeg_llm_extra/results.json` |
| `lf3_crossarch_convergence.pdf` | §5 main. 36-ckpt class-PC1 scatter, 26-ckpt within-class residual scatter, 100-direction null distribution. | class-PC1 r=+0.885, p=8e-13; within-class r=+0.735, p=2e-05; V-axis at 93rd percentile of null | `reports/crossarch_random_control.json`, `reports/merge_crossarch_vaxis_results.json` |
| `lf6_saturation_cliff.pdf` | §7 main. Δ-vs-base-recipe scatter for 25 V-axis interventions; 3-anchor mean shows transition crossing zero. | CBraMod 0.572 → +0.006; EMOD-d3 0.624 → +0.002 to +0.007; SOTA 0.658 → −0.015 to −0.024 | `notes/all_findings_catalog.md` (verified table; numbers traceable to merge_*_results.json) |
| `lf7_recipe_cascade.pdf` | §8 main. Horizontal cascade bar chart: CBraMod → 0.6948 SOTA via 7 steps. | CBraMod 0.572 → 0.619 → 0.634 → 0.647 → 0.658 → 0.6755 single → 0.6798 5-ckpt → 0.6948 10-ckpt; +0.123 absolute (+21.5%) | `notes/headline_numbers.md` cascade rows |
| `lf8_two_tier_ensemble_theory.pdf` | §5 secondary, §8 mechanism. Per-ckpt within-resid \|r\| vs LOO contribution scatter (n=10) + bar comparison. | r=+0.743, p=0.014; top-7 = 0.6962, bottom-7 = 0.6829, full = 0.6948 | `reports/sota_ensemble_theory.json` |
| `lf9_all_interventions_forest.pdf` | §7 appendix. Forest plot of all 25+ V-axis interventions ranked by Δ with 95% CI. | Most negative: pretrain-FT frozen −0.401, distance-CE τ=5 −0.397, RSA λ=5 −0.093; most positive: EMODSTYLE λ=0.5 stim +0.007 (ns); zero significant positives | `notes/all_findings_catalog.md` (verified intervention table) |
| `lf10_confusion_matrices.pdf` | §8 appendix. Side-by-side 9×9 confusion matrices for best single ckpt (0.6755) and 10-ckpt ensemble (0.6948). | Per-class accuracies on diagonal; +0.058 Joy, +0.039 Inspiration; −0.014 Sadness, −0.010 Disgust | `reports/sota_ensemble_extension/{labels,probs_*}.npy` (recomputed on the fly) |

## Style & build

- All scripts share `scripts/_lf_style.py` (rcParams, color palette, save-dual helper, panel-label helper).
- Helvetica primary, Arial fallback; bold panel labels (a, b, c) at 12pt; PDF fonts embedded as TrueType (`pdf.fonttype = 42`).
- Diverging RdBu_r is reserved for signed Pearson r (topography figures); landmark figures here use deliberate
  qualitative palettes (FACED 9-emotion order, EMOD vs CBraMod by family, significance tier ramp).
- All figures use `bbox_inches="tight"` and a 400 dpi PNG fallback.
- Each script is self-contained; rerun with the `hfnewest` conda env.

## Data caveats

- LF3 panel (b) (within-class residual) plots only the 26 base ckpts present in `merge_crossarch_vaxis_results.json` — the 10 expanded variants (val-selected single, ensembles of 5, ensembles of 8) inherit ensemble-level statistics that don't have a per-ckpt within-class residual decomposition. The panel still matches the headline within-class r=+0.715 reported in §5.
- LF6, LF9 source rows are constructed from `notes/all_findings_catalog.md` (which is the verified single source of truth assembling per-experiment merge_*_results.json files). 95% CIs in LF9 are paired-t approximations (1.96 × σ/√n) using reported per-seed stds.
- LF10 recomputes BACC on the fly from the saved test-set prob arrays, matching `headline_numbers.md` (0.6755 single, 0.6948 ensemble) to four decimal places.
- LF1 panel (a) "Yelp" AUC of 0.95 is the dev-set value from `p1_task_matrix.json`; this matches `cycle 73x` worklog.

## Reproduction

```bash
source /home/radwany/miniconda3/etc/profile.d/conda.sh && conda activate hfnewest
cd /ibex/project/c2323/yousef/paper_neurips26_final
for f in figures/landmark/scripts/lf*.py; do python3 "$f"; done
```

Each script regenerates one PDF + one PNG in this directory.
