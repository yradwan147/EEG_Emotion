# Full Paper Revision Plan — NeurIPS 2026 EmotionKD

**Date:** 2026-04-09 (Session 21)
**Goal:** Comprehensive revision incorporating all Session 18-20 findings, with new figures, references, and an inclusive narrative covering successes AND failures.

---

## 1. Current State Audit

### Existing Paper (commit 1fb2737)
- **Title:** Bridging LLM Emotion Representations and EEG: Soft-Label Knowledge Distillation with Parameter-Efficient Adaptation
- **Pages:** 22 (main + supplementary)
- **Sections:** abstract, intro, related, method, experiments (10 subsections), conclusion, supplementary
- **Last update:** Session 19 (Apr 9, 1fb2737)

### What's Missing (Session 20 findings)
1. **Cross-dataset KD on SEED-V** — preprocessing fix + 5s windows enable KD where it was zero before
2. **Token threshold story expanded** — now validated across 6 token configurations
3. **Cross-family LLM analysis** — Gemma-4 (4 sizes) added; cross-family RDM agreement
4. **Cross-LLM CKA finding** — Gemma-4-31B has highest CKA with KD-EEG even though training used Qwen-14B
5. **Mid-layer extraction (Exp 9)** — 6 Qwen sizes at 29% depth, with nuanced family-specific findings
6. **Linear probing (Exp 16)** — 100% binary cluster purity for all instruction-tuned LLMs
7. **Bootstrap CIs (Exp 17)** — replaces t-tests for all main results
8. **Computational efficiency (Exp 18)** — backbone vs classifier breakdown
9. **CKA/RSA feature similarity (Exp 15)** — KD increases LLM-EEG alignment
10. **Adapter-on-SEED-V negative finding** — adapters don't help SEED-V (dataset-specific PEFT)
11. **62ch vs 19ch SEED-V channel finding** — channel selection matters for KD-receptivity
12. **Best teacher comparison (Exp 22)** — Qwen-1.5B layer 8 only marginally beats 0.5B 67%

### Outdated/wrong things in current paper
1. **Abstract:** mentions only 6 LLM families — now we have 11+ instruction-tuned models
2. **Cross-backbone table:** says LaBraM SEED-V flat, but new finding shows 19ch×5s WORKS
3. **SEED-V results:** still show old 0.416 baseline (no KD effect); new 5s data has KD working
4. **Token threshold paragraph:** says "zero effect" — now nuanced
5. **Conclusion:** missing the new findings entirely

---

## 2. New Narrative (Strongest Possible)

**Main thesis (unchanged but stronger):**
LLMs and brains share emotion geometry. We exploit this via KD to teach EEG models the relational structure of emotions. The improvement scales with token count and is universal across LLM families and EEG backbones.

**Three pillars (matching the experiments):**
1. **Cross-backbone KD works** — CBraMod + LaBraM both improve significantly on FACED
2. **Cross-dataset KD works (with conditions)** — SEED-V needs longer windows to provide enough tokens for KD
3. **Cross-family LLM universality** — 11 instruction-tuned models, RSA ~0.82 cross-family

**Honest negative findings (also strengthens paper):**
- Adapter PEFT is dataset-specific (helps FACED, not SEED-V)
- 62-channel SEED-V is anomalously KD-resistant (likely channel redundancy)
- Best teacher comparison shows the teacher model choice matters less than the framework
- Llama-4 Scout 17B-16E couldn't be loaded due to library compat issues

---

## 3. Revised Section Structure

### Section 0: Abstract
**Changes:**
- Update LLM family count (6 → 11 instruction-tuned models, 7 Qwen + 4 Gemma)
- Add cross-dataset SEED-V finding (KD works with sufficient tokens)
- Add CKA universality finding (KD increases LLM-EEG alignment)
- Sharpen the "token count threshold" claim with explicit numbers

### Section 1: Introduction
**Changes:**
- Update teaser figure to show all 5 main findings (waterfall is fine, may add inset)
- Update contribution list:
  - (1) LLM-KD framework — unchanged
  - (2) Cross-backbone validation (CBraMod+LaBraM, both significant)
  - (3) Cross-dataset validation with token threshold finding
  - (4) Cross-family LLM universality (11 models, 2 families)
  - (5) Empirical CKA + RSA evidence of LLM-EEG alignment increase

### Section 2: Related Work
**Changes:**
- Add new paragraph on **cross-modal/representational alignment** (CKA literature)
- Add new paragraph on **EEG channel montage / spatial selection**
- Cite recent NeurIPS 2024-2025 brain-LLM alignment papers

### Section 3: Methodology
**Mostly unchanged but:**
- Update the LLM emotion vector subsection with the cross-family results
- Add the "token count requirement" as an explicit method-level discussion (not just an empirical observation)
- Update LLM teacher choice rationale (Qwen-0.5B used for paper SOTA, 1.5B-L8 marginally better but not worth swapping)

### Section 4: Experiments
**Major restructuring:**

**4.1 Main Results (FACED + SEED-V)**
- Updated main table with both datasets, both backbones, baseline + KD + adapter
- SEED-V row updated to show 5s preprocessing + KD works

**4.2 Cross-Backbone Validation** (expanded)
- Add the multi-configuration comparison (62ch×1s, 19ch×1s, 19ch×5s)
- Token threshold story with clear table

**4.3 Cross-Dataset (SEED-V)** [NEW SECTION]
- 5s preprocessing motivation
- Results on both backbones
- Why SEED-V is harder than FACED

**4.4 Augmentation Ablation** (unchanged)

**4.5 KD Loss Ablation** (unchanged)

**4.6 Baseline Comparison** (unchanged)

**4.7 PEFT Analysis** (expanded with negative SEED-V finding)
- Adapter helps FACED (+9.8%) but HURTS SEED-V (-5%)
- Dataset-specific PEFT story

**4.8 Error Pattern + LLM Geometry** (unchanged but updated figures)

**4.9 LLM Scale Analysis** (expanded)
- 7 Qwen sizes
- Mid-layer vs late-layer comparison
- Family-specific findings (Gemma-4)

**4.10 Cross-Family LLM Universality** [NEW SECTION]
- 11 instruction-tuned models
- RDM agreement matrix
- Gemma-4 vs Qwen comparison
- The "depth pattern reverses with scale" finding

**4.11 Representational Alignment (CKA/RSA)** [NEW SECTION]
- Linear CKA increases with KD
- Cross-LLM CKA — universal absorption finding (Gemma-4-31B best aligned)
- Linear probing of LLM features
- RDM-based RSA analysis

**4.12 Statistical Robustness** [NEW SECTION]
- Bootstrap 95% CIs for all main results
- Effect sizes
- Subject-level analysis

**4.13 Computational Efficiency** [NEW SECTION]
- Backbone vs classifier params
- KD inference cost (zero — only training)
- Adapter savings narrative

### Section 5: Conclusion
- Updated with all new findings
- Honest limitations including SEED-V channel sensitivity, Llama-4 incompatibility

### Supplementary
- Add Exp 9 mid-layer table (all 6 Qwen sizes)
- Add Exp 19 Gemma-4 table (all 4 sizes, both depths)
- Add Exp 17 bootstrap CIs as standalone table
- Add Exp 21 cross-family RDM matrix
- Add Exp 25 linear probe extended table
- Add adapter-on-SEED-V negative result
- Failed experiments section: Llama-4 attempts, EEG-DINO attempts, REVE attempts (lessons learned)

---

## 4. New Figures Needed

### Critical (must generate)
1. **fig_token_threshold.pdf** — bar chart showing KD Δ vs token count across 6 configurations, with significance stars
2. **fig_cross_family_rdm.pdf** — 11×11 RSA heatmap showing within-Qwen, within-Gemma, cross-family agreement
3. **fig_llm_scale_dual.pdf** — Pearson r AND cluster separation across Qwen sizes (already have data)
4. **fig_gemma_qwen_comparison.pdf** — Side-by-side scale curves for Qwen vs Gemma-4
5. **fig_cka_increase.pdf** — Bar chart of CKA(LLM, EEG) before/after KD across all 11 LLMs
6. **fig_seedv_tsne.pdf** — Already generated, needs to be added (was Exp 26)
7. **fig_per_class_seedv.pdf** — Per-class recall changes for SEED-V (already generated)

### Nice-to-have
8. **fig_adapter_dataset_specific.pdf** — Bar chart showing adapter effect on FACED vs SEED-V (positive vs negative)
9. **fig_efficiency_breakdown.pdf** — Pie chart or bar showing backbone vs classifier vs KD overhead

---

## 5. New References Needed

From the literature review and NeurIPS trends:
1. **CKA references:**
   - Kornblith et al. ICML 2019 (Linear CKA original)
   - Rethinking CKA in KD IJCAI 2024
   - Attention-weighted CKA for KD in Audio-LLMs
2. **RSA / brain-LLM alignment:**
   - NeurIPS 2023 "Increasing Brain-LLM Alignment via Information-Theoretic Compression"
3. **Bootstrap CIs / statistical practice:**
   - NeurIPS 2024 "Testing KD theories with dataset size"
4. **Channel selection in EEG:**
   - any standard 10-20 vs 10-10 montage paper
5. **Gemma-4:** Google DeepMind technical report (if available)
6. **Llama-4:** Meta Llama-4 announcement
7. **AMP/KD compatibility:**
   - Original ViTKD paper (relevant to our debugging finding)
8. **Cross-modal KD relational:**
   - CMCRD 2025 (already cited)
   - Original Hinton 2015 (already cited)

---

## 6. Plan Execution Steps

### Step 1: Backup current paper
```bash
cd /ibex/project/c2323/yousef/EEG_Emotion
cp -r . ../EEG_Emotion_backup_pre_session21
```

### Step 2: Generate new figures (CPU-only mostly)
- **Script 1:** `figs_session20.py` — generates token threshold bar, cross-family RDM heatmap, LLM scale dual axis, CKA increase bars
- **Script 2:** Run existing per-class SEED-V plot
- All figures saved to `EEG_Emotion/figs/`

### Step 3: Update bibliography
- Edit `refs.bib` with new entries
- Verify with bibtex pass

### Step 4: Rewrite sections in this order:
1. **Section 4 (experiments)** — biggest changes, new sections, new tables
2. **Section 0 (abstract)** — incorporate latest findings
3. **Section 1 (intro)** — update contributions, may revise teaser
4. **Section 5 (conclusion)** — add new findings
5. **Section 2 (related work)** — add CKA, channel selection paragraphs
6. **Section 3 (methodology)** — minor updates
7. **Supplementary** — add new tables and figures

### Step 5: Compile and verify
- pdflatex 4 passes (with bibtex)
- Check for warnings, undefined refs/cites
- Verify page count (target ~10 main + supp)

### Step 6: Final audit
- Cross-check all numbers against verified results files
- Ensure no fabricated results
- Verify figure labels match captions

### Step 7: Commit and push
- Save plan + commit message documenting all changes

---

## 7. Risk Management

**Risks:**
1. **Page limit overflow** — current is ~10 pages, adding sections may push past
   - Mitigation: Move detailed tables to supp, use compact tables, leverage spacing tricks
2. **LaTeX compilation errors** — new figures or refs may break
   - Mitigation: Compile incrementally, test after each section change
3. **Inconsistent numbers** — different exps have slightly different setups
   - Mitigation: Verify everything against `paper_numbers_verified.md` and result JSONs
4. **Time** — full revision is large
   - Mitigation: Prioritize Section 4 first (most impactful), incremental compilation

**Success criteria:**
- Paper compiles cleanly (zero errors, minimal warnings)
- All Session 20 findings included
- New figures look professional
- Page count within limits
- Numbers verified against artifacts
- Pushed to GitHub
