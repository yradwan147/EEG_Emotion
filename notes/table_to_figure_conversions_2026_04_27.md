# Table → Figure Conversions, 2026-04-27

Five tables in the NeurIPS 2026 draft were swapped for figures because
their structure (≥10 rows, distribution/trend, or visual-claim hero) is
better served by a glance figure than by a small-font numerical block.
A 6th candidate (§3 sentiment benchmarks) was identified as a "keep"
because it is a 5-row paired-numbers table.

## Conversions executed

| # | Section | Table label | New figure | Why figure is better |
|---|---|---|---|---|
| 1 | §3.6 Compositionality / concept library | `tab:concept-library` (12 rows × 6 cols, 20 concepts + summary) | **LF11** sorted bar chart with tier colours | Sorted bar shows the tail (toxicity at 0.59) and the saturation regime (17 of 20 ≥ 0.95) at a glance; |ρ| inscribed in each bar. Three thresholds (chance, working, full success) annotated. |
| 2 | §3.5 Multilingual transfer | `tab:multilingual` (5 rows × 5 cols, languages × extractors) | **LF12** grouped-bar + EN-baseline line | Visual contrast between the English-bias collapse (Qwen ≈ chance on JA/AR/RU) and mT0 multilingual recovery (above EN ceiling) is dramatic in a figure, lost in a small-font table. |
| 3 | §4 Per-LLM brain rank | `tab:llm-brain` (14 rows × 5 cols with multirow grouping) | **LF13** two-panel forest plot (EEG r ‖ behav r) | Forest plot makes the three-tier structure visible at a glance and replicates *across both panels* (EEG and behavioural), which is the paper's universality claim. Fisher-z 95% CIs added (not in table). |
| 4 | §8 Generality across datasets | `tab:ensemble-generality` (4 rows × 5 cols with headroom) | **LF14** scatter (Δ vs headroom) + paired bars | Scatter shows the gain∝headroom mechanism (the two-tier theory's empirical signature) with linear fit. Paired bars give magnitude. Reading it once shows the saturation prediction. |
| 5 | App §S7 Cross-concept transfer matrix | `tab:concept-library-full` (20 × 20 tiny LaTeX) | **LF15** 20×20 viridis heatmap with row/col marginal generality bars | A 20×20 matrix at footnote-size with rotated labels is unreadable; the heatmap+marginals cleanly displays both the structure (diagonal sharper than off-diagonal) and the per-source / per-target generality at full fidelity. This was the user's explicit prior request. |

## Tables kept (per directive)

| Section | Table | Why kept |
|---|---|---|
| §3.3 | `tab:vaxis-sentiment` (5 sentiment benchmarks × 2 cols) | Small paired-numbers table; figure would not improve. |
| §3.6 | `tab:arousal-asymmetry` (5 rows × 2 cols) | Paired-numbers table with explicit chance comparison; reads better in tabular form. |
| §6 | `tab:anger-contrast` (5-row drop-class diagnostic) | Already small; LF6 covers the saturation cliff narrative. |
| §7 | `tab:negatives` and `tab:monotonic` | Detailed text-data complementary to LF6/LF9 forest plot; tables add specific reference info (RSA / distance-CE / Multi-V cells) that are illegible at the LF9 scale. |
| §8 | `tab:sota` (3-row headline) | Small; serves as paper hero anchor. |
| §8 | `tab:sota-cascade` (10-row cumulative cascade) | LF7 already shows it as a hero bar chart; the table preserves the row-by-row cumulative structure for the reader who wants exact numbers. |
| §8 | `tab:mega-ensemble` (4-row null) | Small; mega-ensemble null is best as table. |
| §10 | `tab:full-vaxis` (~25 rows of intervention details) | LF9 already shows it as forest plot; the table preserves seed/p-value detail. |
| §S4b | three SEED-V tables (FAA / step4 / replication) | All small (≤4 rows × ≤3 cols). |

## Figure files produced

```
figures/landmark/lf11_concept_library_bars.{pdf,png}
figures/landmark/lf12_multilingual_grouped.{pdf,png}
figures/landmark/lf13_llm_brain_forest.{pdf,png}
figures/landmark/lf14_ensemble_generality.{pdf,png}
figures/landmark/lf15_concept_transfer_heatmap.{pdf,png}

figures/landmark/scripts/lf11_concept_library_bars.py
figures/landmark/scripts/lf12_multilingual_grouped.py
figures/landmark/scripts/lf13_llm_brain_forest.py
figures/landmark/scripts/lf14_ensemble_generality.py
figures/landmark/scripts/lf15_concept_transfer_heatmap.py
```

All figures use the existing `_lf_style.py` style (Helvetica sans-serif,
9pt body / 11pt title, RdBu_r/viridis cmaps, no top/right spines,
400 dpi PNG + vector PDF).

## Tex edits

- `sections/03_v_axis_in_llms.tex`: replaced `tab:concept-library` → `fig:concept-library` (LF11), replaced `tab:multilingual` → `fig:multilingual` (LF12), updated cross-ref to `tab:llm-brain` → `fig:llm-brain`.
- `sections/04_v_axis_in_brain.tex`: replaced `tab:llm-brain` → `fig:llm-brain` (LF13).
- `sections/08_ensemble_sota.tex`: replaced `tab:ensemble-generality` → `fig:ensemble-generality` (LF14).
- `sections/10_appendix.tex`: replaced `tab:concept-library-full` → `fig:concept-library-full` (LF15). Appendix label `app:concept-library-full` preserved.

No changes to `main.tex`, `.sty`, or `sections/checklist.tex`.

## Page-count delta

| Build | Pages |
|---|---|
| Pre-conversion (44 in user's note) | 44 |
| Post-conversion (this build) | **50** |

Net delta: **+6 pages**. The directive permitted ≤50, and the build
hits the boundary exactly. The increase is dominated by LF13
(two-panel 18-LLM forest, ~1 page) and LF15 (full-page transfer
heatmap, 1 page); LF11/12/14 are roughly neutral against the tables
they replaced.

## Build status

```
$ pdflatex -interaction=nonstopmode main.tex && bibtex main && pdflatex && pdflatex
Output written on main.pdf (50 pages, 1.78MB).
```

No undefined references, no citation errors, no warnings beyond
benign "h → ht" float-specifier promotions and a few underfull boxes
that are cosmetic.

## Data caveats

- LF13: Fisher-z 95% CIs are derived analytically from the per-LLM
  Pearson r and n=28 (FACED stim count); they are *not* bootstrap CIs
  over subjects. This is appropriate because the brain-prediction r
  is itself a stim-level statistic on the cohort EEG.
- LF11: The toxicity row is the named failure (AUC 0.59, Jigsaw); it
  was already in the prose of §3.6 but not in `tab:concept-library`
  (which only listed working concepts). LF11 includes it for visual
  completeness.
- LF15: Excludes toxicity (consistent with the 20×20 transfer-matrix
  JSON, which only contains working concepts). The "named failure"
  is reported separately in §3.6 prose and shown in LF11.
- All Qwen labels use Qwen3.5 nomenclature in figure labels (per
  memory: `feedback_qwen_version.md`).
