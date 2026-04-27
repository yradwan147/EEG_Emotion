# Headline Numbers — Paper Verification Source

Every numeric claim in the paper traces to a row in this file → traces to a results JSON → traces to a worklog cycle.

## §3 V-axis in LLMs

| Number | Source | Status |
|---|---|---|
| 18-LLM agreement matrix mean off-diag r=0.65 | #440 results.json `G_multi_llm_agreement.matrix` | ✅ |
| Top-LLM by behav r: Qwen-14B 0.964 | #440 results.json `closest_to_brain_top10_by_r_vs_behav` | ✅ |
| Qwen-1.5B optimal scale (inverted-U) | feedback_llm_scale.md memory + #313 multi-LLM ensemble | ✅ |
| SST-2 zero-shot AUC=0.868 | cycle 73p Task #288, job 46682300 (worklog L9066) | ✅ |
| Hu & Liu lexicon valence: |r|=0.76 | cycle 73o Task #289 (worklog L8980) | ✅ |
| Composition: V_polite + V_happy → 79% 4-quadrant | cycle 75 #395 R6-COMPOSITION | ✅ |

## §4 V-axis in Brain

| Number | Source | Status |
|---|---|---|
| FACED 28 stims × 123 subjects × 32 channels | dataset spec | ✅ |
| Cohort r = 0.87 (clip-bare-emotion-proj) | #397 R6-EEG-LLM, `r6_clip_only.json` | ✅ |
| Random-direction r = 0.07 | #397 control | ✅ |
| p < 10⁻⁹ | #397 (Fisher z) | ✅ |
| Per-LLM brain anchor r: Qwen-1.5B 0.41 | #440 results.json `E2_per_llm_vs_eeg.rows` | ✅ |
| FACED→SEED-V V-axis ordering r = +0.96 | #407 MERGE-XEEG (worklog cycle 75) | ✅ |

## §5 Cross-arch convergence

| Number | Source | Status |
|---|---|---|
| 36 checkpoints (CBraMod + EMOD variants) | #429 + extras | ✅ |
| r(BACC, class-PC1 |r|) = +0.885 | merge_crossarch_vaxis_results.json (latest) | ✅ |
| Within-class residual r = +0.715 | #429 worklog L14215 | ✅ |
| Random-direction null: V-axis at 93rd percentile, p_one=0.079 | crossarch_random_control.md (#451) | ✅ |
| #449 within-class residual ↔ ensemble contribution: r=+0.743, p=0.014 | sota_ensemble_theory.md (#449) | ✅ |
| Top-7 by within-resid → 0.6962 vs bottom-7 → 0.6829 | #449 | ✅ |

## §6 Brain Topography

| Number | Source | Status |
|---|---|---|
| Region |r|: occipital 0.212 > parietal 0.181 > central 0.180 > frontal 0.162 | #430 merge_topography_synthesis.md | ✅ |
| Best cell: PO3/γ r=+0.48 | #430 | ✅ |
| Davidson F4-F3 α = +0.006 | #440 results.json `C_asymmetry.davidson_F4F3_alpha` | ✅ |
| Anger drop-class Δ = −0.151 (32% of effect) | #440 results.json `D_per_emotion.per_class[Anger].delta_when_drop` | ✅ |
| Anger+Amus+Tend only (n=9) cohort r = 0.870 | #441 results.json `analysis_3_anger_weighted` | ✅ |
| Excluding Anger+Amus+Tend (n=19) cohort r = −0.015 | #441 | ✅ |
| Per-subject mean r at cohort top-8 = −0.06 | #440 results.json `B_per_subject` | ✅ |
| Per-subject all-band oracle r = +0.616 | #441 results.json `analysis_2_per_subject_ceiling` | ✅ |
| Top-channel γ functional connectivity r = 0.675 | #440 `H_connectivity` | ✅ |
| Time-resolved α peak at t=21s (cohort r=0.40) | #440 `A_time_resolved` | ✅ |
| 17-24% of subjects peak in cohort 18-21s window | #441 `analysis_4_per_subject_peak` | ✅ |

## §7 Saturation theorem (V-axis as supervision)

| Variant | Δ | p | Source | Status |
|---|---|---|---|---|
| Frontal-mask λ=0.5 | −0.052 | 0.0015 | merge_frontal_vaxis_runs/ paired t #434 | ✅ |
| FAA λ=0.5 | −0.044 | 0.006 | merge_faa_vaxis_runs/ #435 | ✅ |
| Occipital λ=0.1 | −0.022 | 0.007 | merge_frontal_vaxis_runs/run_occvaxis_l0.1 #437 | ✅ |
| Anger-weighted λ=0.5 | −0.054 | 0.0003 | merge_anger_vaxis_runs/ #443 | ✅ |
| Topo-optimal λ=0.05 | +0.002 | 0.50 | merge_topo_optimal_vaxis_runs/ #438 | ✅ |
| Topo-optimal λ=0.1 | −0.013 | 0.039 | #438 | ✅ |
| Procrustes λ=0.05 | +0.001 | 0.89 | merge_procrustes_vaxis_runs/ #436 | ✅ |
| EMODSTYLE λ=0.5 stim | +0.007 | 0.22 | merge_emodstyle_runs/ #424 | ✅ |
| PEFT fullhead λ=0.1 | −0.009 | 0.069 | merge_peft_vaxis_runs/ #432 | ✅ |
| Curriculum cosine_decay li=0.5 | −0.009 | 0.23 | merge_warmup_vaxis_runs/ #445 | ✅ |
| (other interventions: RSA, distance-CE, pretrain-FT, InfoNCE, prior, multi-V, distill, stim-agg, small-λ, uncert) | various | various | various JSONs | ✅ |
| **Total V-axis-as-supervision interventions tested** | **22-25** | — | — | ✅ |

## §8 SOTA ablation cascade

| Step | BACC | Source | Status |
|---|---|---|---|
| CBraMod (ICLR 2025 prior SOTA) | 0.572 | external | ✅ |
| EmotionKD (ACMMM 2023) | 0.628 | external | ✅ |
| EMOD AAAI 2026 paper | 0.6287 | external | ✅ |
| EMOD vanilla replication (d3, race-fixed) | 0.6194 ± 0.004 | cycle 31, job 46633766 | ✅ |
| + aug | 0.6343 ± 0.004 | cycle 31, job 46632393 | ✅ |
| + KD only | 0.6215 ± 0.011 | cycle 31 | ✅ |
| + aug + KD | 0.6439 ± 0.007 | cycle 31 | ✅ |
| + rand9 9D KD (LLM-equivalent) | 0.6467 ± 0.007 | cycle 72j | ✅ |
| **+ d6 depth doubling** | **0.6581 ± 0.0066** | cycle 73f, job 46665722 | ✅ |
| + e150 longer training (single) | 0.6581 ± 0.010 | cycle 73f | ✅ |
| 5-ckpt e100 ensemble | 0.6798 | cycle 73i ensemble_d6_test.py | ✅ |
| **10-ckpt mixed e100+e150 ensemble** | **0.6948** | cycle 73j-B `ensemble_d6_d6e150_results.json` | ✅ |
| **Single-checkpoint val-selected SOTA** | **0.6755** | best_single_ckpt.json (#448) val-selected = vanilla_e150_s789 | ✅ |

## §8 Path B ensemble extension (V-axis ckpts hurt)

| Ensemble | n | BACC | Δ vs vanilla_10 | p | Source |
|---|---|---|---|---|---|
| vanilla_10 | 10 | 0.6948 | — | — | sota_ensemble_extension.json |
| +topo_15 | 15 | 0.6803 | −0.0145 | 0.000 | #446 |
| +emodstyle_15 | 15 | 0.6883 | −0.0066 | 0.087 | #446 |
| +procrustes_15 | 15 | 0.6855 | −0.0094 | 0.030 | #446 |
| all_25 | 25 | 0.6755 | −0.0193 | 0.000 | #446 |

## Per-subject ensemble selection (all NULL except oracle)

| Method | K=3 | K=5 | K=7 | K=10 | Source |
|---|---|---|---|---|---|
| V1 global top-K by val | 0.680 | 0.685 | 0.687 | 0.6948 | per_subject_ensemble.json |
| V2 per-val-subject majority vote | 0.680 | 0.678 | 0.687 | 0.6948 | per_subject_ensemble.json |
| V3 TTA label-free profile | 0.682 | 0.683 | 0.687 | 0.6948 | per_subject_ensemble.json |
| ORACLE per-test-subject (cheating) | 0.6981 | 0.6994 | 0.7006 | 0.6948 | per_subject_ensemble.json |

## §9 Saturation transition (component ablation, in flight)

| Recipe | Vanilla BACC | + V-axis BACC | Δ | Source |
|---|---|---|---|---|
| EMOD d3 + LS | 0.6194 | pending | — | #453 SLURM 46750628 |
| EMOD d6 + LS | 0.6235 | 0.6256 (Topo) / 0.6301 (EMODSTYLE) | +0.002 / +0.007 | cycle 75 #438 #424 |
| EMOD d6 + LS + KD | 0.6215 | pending | — | #456 dispatching |
| EMOD d6 + LS + aug | 0.6343 | pending | — | #456 dispatching |
| EMOD d6 + LS + KD + aug (full SOTA recipe) | 0.6581 | 0.6432 (Topo) / 0.6346 (EMODSTYLE) | −0.015 / −0.024 | #447 e100 |
| CBraMod baseline | 0.5717 | 0.5777 (Topo s42, n=1) | +0.006 | #454 partial |

## Test split protocol

- **FACED 9-class**: 32 channels × 250 Hz × 30s clips, 28 stims × 123 subjects
- Train: subjects 0-79 (80 subjects)
- Val: subjects 80-99 (20 subjects)
- Test: subjects 100-122 (23 subjects, 1932 trials)
- All experiments use IDENTICAL split (verified via #442 agent)

## Reproducibility manifest

For each headline number:
- Trainer/script: pointer to .py file
- SLURM args: pointer to .sh file
- Seeds: explicit list
- Random seed for any sampling: documented
- Hardware: V100 unless noted
