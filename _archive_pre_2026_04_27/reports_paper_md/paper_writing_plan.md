# Plan: Write NeurIPS 2026 Paper — LLM-Guided EEG Emotion Recognition

## Context

All experiments are complete (~400 runs across FACED and SEED-V). The last few SEED-V LOSO jobs are finishing. We need to write an extended first draft of the NeurIPS 2026 paper, following the `write-research-paper` skill, then commit and push to the `EEG_Emotion` repo (linked to Overleaf). The draft should be long (15-18 pages) — supervisors will trim to the 10-page limit.

---

## Step 1: Wait for All Jobs to Complete

1. Poll `squeue -u radwany` until SEED-V LOSO (job 46374694) finishes (all 12 tasks)
2. Collect all results, compute means and p-values
3. Update `worklog.md`, `experiment_history.md`, `paper_statistics.md` with final numbers
4. Verify zero remaining jobs

---

## Step 2: Literature Layout Review

Search for recent accepted papers in EEG emotion recognition at top venues:
- NeurIPS 2025, ICLR 2025-2026, AAAI 2026
- Study section structure, figure placement, table design, how they present ablations
- Note layout patterns to adopt (e.g., teaser figure style, table format, appendix structure)
- Check the reference examples in `write-research-paper/references/` (ReefNet, Fishnet)

---

## Step 3: Generate ALL Missing Figures

Before writing any LaTeX, generate every figure needed:

1. **Pipeline diagram (TikZ)** — main architecture figure showing:
   - Raw EEG → CBraMod backbone (frozen) → adapters → classifier + KD head
   - LLM emotion vector extraction branch
2. **Cross-subject (LOSO) bar chart** — both datasets side-by-side
3. **Confusion matrix comparison** — baseline vs adapter64 on FACED
4. **Cross-dataset comparison** — FACED vs SEED-V bar charts
5. **Adapter scaling curve** — both datasets
6. **LLM universality heatmap** — cross-family RDM agreement
7. **Statistical significance heatmap** — p-value matrices
8. **Improvement waterfall** — component-by-component contribution
9. Verify existing figures: t-SNE, PCA circumplex, per-subject, aug ablation

Copy all figures into `EEG_Emotion/figs/`.

---

## Step 4: Write the Paper (Following write-research-paper Skill)

### Phase 0: Context Validation (quick — already done)
### Phase 1: Deep Project Scan (already done — use worklog/experiment_history)

### Phase 2: Paper Planning — Section Outline

**Title:** "Bridging LLM Emotion Representations and EEG: Soft-Label Knowledge Distillation with Parameter-Efficient Adaptation"

**Method name:** `EmotionKD` (macro: `\ours`)

**Section mapping:**

| Section | Content | Tables/Figures |
|---------|---------|----------------|
| Abstract | Problem, method, scale, results, finding | — |
| Introduction | Motivation, gaps, contributions | Teaser/pipeline fig |
| Related Work | EEG foundation models, LLM emotions, KD, PEFT | Comparison table |
| Methodology | LLM vectors, KD loss, augmentation, adapters | Pipeline diagram, loss equations |
| Experiments | Within-subject, cross-subject, cross-dataset | Tables 1-3, multiple figures |
| Ablations | Aug ablation, KD alternatives, adapter scaling, architecture | Tables 4-7 |
| Analysis | Error pattern, t-SNE, per-subject, LLM universality | Analysis figures |
| Conclusion | Summary, limitations, future work | — |
| Supplementary | Extended tables, per-fold LOSO, all architecture results | Supp tables/figs |

### Phase 3: Create Directory Structure

```
EEG_Emotion/
  main.tex              # Main document
  neurips_2026.sty      # Already exists
  sec/
    0_abstract.tex
    1_intro.tex
    2_related.tex
    3_method.tex
    4_experiments.tex
    5_conclusion.tex
    supplementary.tex
  tables/
    (separate .tex for each table)
  figs/
    pipeline.tex         # TikZ
    (all PNG/PDF figures)
  refs.bib
  checklist.tex          # Already exists
  verification/
    number_audit.md      # Every number mapped to source
    reference_audit.md   # Every citation verified
```

### Phase 4: Write All Sections

Write in order: abstract → intro → related → method → experiments → analysis → conclusion → supplementary → checklist. Include ALL experiments (even failures like cross-attention collapse, MAE pretraining). Extended draft (15-18 pages).

---

## Step 5: Number Verification (MANDATORY)

Create `verification/number_audit.md`:
- Map EVERY number in the paper to its source log/file
- Format: `| Paper Location | Number | Source | Verification |`
- Cross-check against `worklog.md` and `paper_statistics.md`

---

## Step 6: Reference Audit (MANDATORY)

Create `verification/reference_audit.md`:
- For EVERY `\cite{}` in the paper, verify:
  - The cited paper exists (cross-check with `memory/reference_paper_citations.md`)
  - The claim made about the cited paper is accurate
  - No fabricated attributes or results assigned to cited works
- Web search any uncertain citations
- Flag anything unverifiable with `% TODO: verify`

---

## Step 7: Compile, Verify, Push

1. Compile: `pdflatex → bibtex → pdflatex → pdflatex` (4 passes)
2. Fix any compilation errors
3. Verify: zero errors, all references resolved, all figures rendered
4. Check page count (~15-18 pages extended draft)
5. Git add, commit, push to `EEG_Emotion` repo (→ Overleaf)

---

## Key Data Sources

| Data | File |
|------|------|
| All experiment numbers | `worklog.md` (Session 14-15) |
| Statistical tests | `reports/paper_statistics.md` |
| Experiment history | `reports/experiment_history.md` |
| References (21 verified) | `memory/reference_paper_citations.md` |
| Figures | `reports/figures/` |
| Architecture code | `paper_sota/model_enhanced.py` |
| Training code | `paper_sota/trainer_enhanced.py` |
| Loss functions | `paper_sota/semantic_contrastive_loss.py` |
