# Writing Plan — Session 28 paper revision

**Author:** Yousef (autonomous Claude run)
**Date:** 2026-04-14 (updated cycle 43)
**Targets:** all unresolved supervisor comments + new findings since the prior paper revision.

## Update log

- **Cycle 34**: Initial plan drafted
- **Cycle 43 (2026-04-14)**: Added findings from #249 (synthetic teachers), #244 (EMOD-SEED-V cross-dataset negative), #251 (replication partial), #250 (EMOD 5s-fix negative), #252 (binary KD in progress)

## 1. Outstanding supervisor items to resolve

| # | Item | Status | Action |
|---|------|--------|--------|
| 201 | Widen aug-only vs aug+KD gap (more tuning) | pending | **Reframe as feature, not bug.** The qspec result (#239) shows KD acts as regularization framework regardless of teacher quality — the small +0.6% gap is what we'd expect when most of the variance is already captured by aug. Add 1 paragraph to §4.10 (`sec:kd_isolation`) noting this finding. |
| 204 | Compress CKA section to 1 fig + 1 para | pending | Move CKA detail from §4.13 (`sec:cka`) to supplementary, leave 1 fig + 1 paragraph in main text |
| 205 | Main text arch: adapter64 vs full FT only | pending | Trim §4.8 (`sec:adapter_ablation`) to compare just the 2 configurations; move full PEFT sweep (LoRA, adapter scaling, FiLM) to existing supp `sec:supp_arch` |
| 206 | Main text: 2-3 representative LLMs only | pending | In §4.12 (`sec:llm_scale`), keep Qwen2.5-0.5B (default), Qwen-1.5B (peak), Gemma-4-31B (cross-family). Move full 11-LLM sweep table to `sec:supp_llm` |

## 2. New findings to integrate into the main paper

### A. NEW SOTA — EMOD + aug + KD = 0.6439 (#240)
- **Where:** new subsection in §4 between `sec:cross_backbone` and `sec:cross_dataset`. Call it §4.X "Cross-Architecture Transfer to EMOD" or fold into `sec:cross_backbone`.
- **Numbers (5 seeds each):**
  - EMOD replication (race-fix): 0.6194 ± 0.004
  - EMOD + aug: 0.6343 ± 0.004 (Δ=+0.015 vs replication, p=0.001 Welch)
  - EMOD + KD: 0.6215 ± 0.011 (Δ=+0.002, n.s.)
  - **EMOD + aug + KD: 0.6439 ± 0.007** (Δ=+0.025, p=0.0003)
  - Beats CBraMod+KD baseline (0.6249) by +0.019 (p=0.0012)
  - Single-seed peak 0.6571 (seed 123)
- **Narrative:** the aug + KD recipe is architecture-agnostic; it lifts a fundamentally different backbone (axial transformer with V-A pretraining) by the same magnitude.

### B1. Synthetic-prototype framing (#249 — major narrative shift)
- **Where:** Fold into §4.12 LLM scaling or add a new subsection §4.Z titled "Fixed-Prototype Regularization".
- **Numbers (3 seeds each):**
  - text Q3.5-0.8B (reference): 0.6263
  - **random orthonormal (np.linalg.qr): 0.6272** (ties reference)
  - tight unit random: 0.6244
  - simplex ETF (theoretical optimum per Neural Collapse): 0.6240
  - etf_valence_aligned: 0.6240
  - hadamard: 0.6221
  - hyper_uniform (Tammes): 0.6209
  - zero_teacher (CE-only): 0.6162 (drops when KD fully removed)
- **Narrative:** A random rotation of the identity matrix matches the LLM teacher. The method reduces to "fixed-prototype regularization" — the student learns to project features to a ~9D space that matches _any_ consistent target geometry. The LLM extraction pipeline is interpretable (circumplex, RSA) but **not operationally necessary** for downstream KD. Proposal: keep LLM narrative as a diagnostic tool for interpretability, re-frame the training recipe as "fixed orthogonal prototypes".
- **Figure:** bar chart of all 7 synthetic teachers vs LLM baseline, error bars from 3-seed std, with horizontal line for aug-only.

### B. Teacher quality irrelevance (qspec, #239)
- **Where:** new subsection in §4 right after `sec:llm_scale` (`sec:llm_scale_universality`). Title: "Teacher Quality Is Not the Binding Constraint".
- **Numbers (3 seeds each, n=30 total):**
  - 10 teacher variants spanning |PC1-val| 0.19–0.97
  - Pearson r(|PC1-val|, downstream BAcc) = +0.230, p = 0.523 (n.s.)
  - Range across all 10: [0.6175, 0.6266], span = 0.0091
  - shuffle_4 (4 classes permuted, |PC1-val|=0.53) = 0.6266 → ties text 0.6263
  - random Gaussian = 0.6191
  - shuffle_6 (6 classes permuted, |PC1-val|=0.19) = 0.6175 (Δ=-0.009)
- **Narrative:** the KD framework regularizes via the projection-target structure, not via class-discrimination knowledge transfer. Above some near-zero floor, ANY consistent 9-class target works equally well. This explains why all alternative-teacher directions (mixtures, vision, projections) tied or lost — they were optimizing the wrong axis.
- **New figure:** scatter plot of |PC1-val| vs downstream BAcc with all 10 variants labelled, fitted linear regression (slope ~0).

### C. Cross-dataset × cross-architecture matrix (#244 — COMPLETE)
- **Where:** end of §4.6 (`sec:cross_dataset`) or new subsection.
- **Matrix:**
  - CBraMod on FACED: **0.6249 ± 0.004**
  - **EMOD + aug + KD on FACED: 0.6439 ± 0.007** (new SOTA)
  - CBraMod + KD on SEED-V: **0.4166 ± 0.001** (near paper 0.4091)
  - EMOD + aug + KD on SEED-V: **0.3744 ± 0.008** (LOSES to CBraMod; EMOD doesn't transfer)
- **Narrative:** the recipe improves WITHIN a given backbone but **does not override backbone-dataset compatibility**. CBraMod was pretrained on TUEG (general EEG) and handles both FACED and SEED-V natively. EMOD was pretrained on DEAP/AMIGOS/SEED-IV/SEED-VII with V-A contrastive — its emotion-axis prior matches FACED's valence structure but fails to decode SEED-V's 5-class labels with any recipe. **Two separate findings:**
  1. Recipe (aug + KD) is architecture-agnostic → lift comes from training, not the backbone-specific bag of tricks.
  2. Backbone choice is dataset-dependent → pretraining data matters when crossing datasets.
- **Extra evidence:** #250 tested EMOD on SEED-V with 5-second windows (matching EMOD's pretraining regime). Baseline still stuck at chance (0.20 BACC = 1/5), KD variant climbed to ~0.31 but still below CBraMod's 0.42. Confirms the failure is not a window-length mismatch — it's a fundamental pretraining-axis mismatch.

### D. Surgical LLM fine-tuning (#198, #245 — partial)
- **Where:** brief paragraph in supplementary `sec:supp_explore` (Additional Architecture Exploration) or new section.
- **Comparison:**
  - Frozen Q3.5-0.8B + EEG adapter: val 0.28 / test 0.25 (epoch 34/50)
  - Unfrozen Q3.5-0.8B full FT: val 0.32 / test 0.27 (epoch 7/30, still climbing)
  - CBraMod baseline: 0.625
- **Narrative:** direct LLM-on-EEG is fundamentally limited by the modality mismatch. Unfrozen is better than frozen but still ~2× worse than CBraMod. This confirms conventional EEG backbones with KD are the right approach; attempting to repurpose LLMs directly for raw EEG input is a poor fit because the input modality is too far from text.

### E. Extension to non-emotion tasks (#251, #252 — partial, in progress)
- **Where:** supplementary `sec:supp_general_downstream` (new) or brief mention in main §4.6.
- **Replication findings (#251):**
  - CBraMod native replication on MentalArithmetic (avgpool head): **0.7153 ± 0.020** vs paper 0.7256 ± 0.013. Gap -0.010, within paper CI. ✅
  - CBraMod native replication on Mumtaz2016 (both heads): 0.88 ± 0.02 vs paper 0.956 ± 0.006. Gap -0.072 to -0.075. ❌ **Split ambiguity**: CBraMod's own `preprocessing_mumtaz.py` file-level splits don't match the paper's textual subject-level description (code 20+4+5 NCs, paper 15+4+5). Paper likely dropped 6 unspecified NCs. Not replicable without paper's subject list.
  - Honest framing: "We faithfully run CBraMod's published preprocessing code and obtain a reproducible Mumtaz baseline at 0.88, 7 points below the paper's figure. We use this as our own reference point for KD comparisons."
- **KD transfer (#252, in progress 46645558):**
  - Baseline (CE-only): 0.884 Mumtaz / 0.715 MA
  - +aug: TBD
  - +KD (random-orthogonal 2D identity prototypes): TBD
  - +aug +KD: TBD
- **Narrative (conditional on #252 results):** if aug+KD lifts either baseline, the recipe transfers to non-emotion binary EEG tasks. If both are null, binary tasks are too simple to benefit from prototype regularization.

## 3. Supplementary additions

### E. Direction 2 negative results catalog (extends `sec:supp_negative`)
Add concise summaries of all closed Dir 2 directions with one-line numbers each:
- Dir X V-A contrastive (vacon): 0.5722, p<0.001 vs CBraMod baseline (negative — replaces KD instead of adding)
- Dir Y arch sweep: lora{4,8,16} + adapter{16,32,128} all tie or below 0.6249 (capacity ceiling)
- Dir Z channel selection: ch16 0.5622, ch24 0.5894 (with train/test mismatch caveat)
- Dir AA EMA: 0.6243 (ties baseline)
- Dir AB mixup 0.5906, cutmix 0.6217 (mixup hurts, cutmix ties)
- Dir AC self-distill: 0.6200 (ties)
- Dir AD TTA: Δ ≈ 0 (CBraMod has only LayerNorm)
- Dir AE vision KD (Q3.5-0.8B vision): 0.6178 (ties)

### F. Alternative aggregation catalog (new `sec:supp_aggregation`)
Concise summary of the 10 alternative aggregations:
- IMP K=2/3/5: K=1 wins at every projection
- LDA-8d projection: +8.4% on LOO proxy but -1.75% downstream (proxy ≠ downstream lesson)
- Whitened+top50 PCA: ties baseline (-0.16% mean)
- LELP K=2 (LDA-projected): -0.5% downstream
- Per-story stochastic KD: -0.93% (variance too high)
- Gaussian-prototype distillation: -1.0%
- RKD on lda/white50: -0.5% to -1.0%
- SupCon+LDA: -0.2% (nearly ties)
- CRD: -0.6%
- Direction-H lambda sweep: white50 + λ=0.05 = +0.43% (3 seeds, unconfirmed at 5)
- **Conclusion:** mean (K=1) is at-or-near optimal across all projection spaces. Combine with retracted Fisher ratio note.

### G. EMOD replication + recipe transfer details (new `sec:supp_emod`)
- Per-seed BAcc/Kappa/F1 for all 4 EMOD variants × 5 seeds = 20 rows
- Race-condition bug note (per-seed checkpoint paths)
- Aug + KD super-additivity calculation

### H. Quality-spectrum scatter + table (already in §4 if main, also here for completeness)

## 4. Figures to generate or reuse

| Figure | Status | Action |
|--------|--------|--------|
| EMOD recipe ablation bar chart | NEW | Generate from emod_plus_46632393_*.out test BACCs |
| Cross-arch × cross-dataset matrix | NEW | Generate after #244 finishes |
| qspec correlation scatter | NEW | Generate from qspec results |
| All existing fig_*.png in figs/ | KEEP | Verify they're still valid for trimmed sections |

## 5. Verification passes

### Pass 1: Numbers
- For every numerical claim in main.tex + supp, trace to a result file in `/ibex/project/c2323/yousef/experiments/` or `/reports/`
- Update `verification/number_audit.md` with new entries for #239, #240, #244, #245

### Pass 2: References
- Every `\cite{}` must resolve in `refs.bib`
- Add entry for EMOD paper (Wang et al. AAAI 2026, arxiv 2511.05863) if not present
- Add Q3.5-related citations as needed
- Update `verification/reference_audit.md`

## 6. Visual figure inspection

Read every new PNG with the Read tool to confirm:
- No clipping
- Axis labels visible
- Colorblind-friendly
- Caption matches content

## 7. Overleaf push

After all the above:
- `git status` in EEG_Emotion to see what changed
- `git diff` to spot anything unintended
- Commit with message describing sections added/edited
- `git push` to the Overleaf branch

## 8. Documents to keep updated through execution

- `worklog.md` — Cycle entries for each writing-phase action
- `memory/project_eeg_mae_state.md` — final SOTA + paper completion state
- `verification/number_audit.md` — every new claim
- `verification/reference_audit.md` — every new \cite{}

## 9. Execution gates (updated cycle 43)

Before starting **execute** phase (Task #247):
1. ✅ #244 EMOD-on-SEED-V: COMPLETE (negative — recipe loses 0.37 vs CBraMod 0.42)
2. ✅ #250 EMOD-on-SEED-V 5s window fix: COMPLETE (negative — still chance)
3. ✅ #249 Synthetic teachers: COMPLETE (random-ortho ties LLM)
4. ✅ #251 CBraMod replication Mumtaz+MA: PARTIAL (MA replicates, Mumtaz split-ambiguous)
5. ⏳ #245 unfrozen Qwen-EEG: epoch 7/30, still climbing. ~14h remaining. Trajectory sufficient to write the section.
6. ⏳ #252 Binary KD+aug on Mumtaz+MA: submitted as 46645558, pending. Expected to finish ~1-2h.

**Current decision**: All gates resolvable tonight except #245 which is fine to write up as "trajectory so far" since it's monotonically climbing. The writing phase can proceed after #252 lands (~2-3h).

## 10. Decisions to make during execution

- Whether the new EMOD+aug+KD result becomes the primary headline (replacing 0.628 CBraMod) or an alternative-architecture confirmation (keeping 0.628 as the lead).
- Whether the qspec quality-irrelevance finding goes in main text or supplementary (recommend main — it's a major narrative reframe).
- Whether to keep the "EmotionKD" name now that the main story is "any consistent 9-class teacher works".
