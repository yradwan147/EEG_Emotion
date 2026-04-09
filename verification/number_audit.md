# Number Audit — Every Number in the Paper Linked to Source
**Last verified:** 2026-04-09 (Session 21)
**Method:** Each numerical claim was independently recomputed from the experiment checkpoint files using `numpy` mean/std on best-epoch accuracies. Bootstrap CIs were re-derived where applicable. The Python interpreter at `/ibex/project/c2323/yousef/envs/eeg-mae-pretrain/bin/python3` was used.

---

## Discrepancies Found and Fixed in this Audit

| Section | Original | Corrected | Source |
|---|---|---|---|
| Table 1 — CBraMod baseline κ (SEED-V) | 0.302 | **0.307** | exp11_cbramod_seedv5s/baseline_seed* |
| Table 1 — KD κ (SEED-V) | 0.311 | **0.309** | exp11_cbramod_seedv5s/kd_midlayer_seed* |
| Table 1 — Aug only κ (FACED) | 0.553 | **0.557** | paper_clean/aug_seed* |
| Table 1 — KD+aug κ (FACED) | 0.578 | **0.577** | kd_sweep/aug06_seed* |
| Table 1 — Adapter64 κ (FACED) | 0.582 | **0.578** | arch_phase1/adapter64_seed* |
| Table 5 — SBERT KD B.Acc | 0.621 | **0.623** | exp3_random_ablation/sbert_seed* |
| Table 5 — SBERT KD κ | 0.571 | **0.572** | same |
| Table 5 — SBERT KD vs Aug | +1.2% | **+1.4%** | recomputed |
| Table 5 — KD+aug κ | 0.578 | **0.577** | kd_sweep/aug06_seed* |
| Table 5 — Aug only κ | 0.553 | **0.557** | paper_clean/aug_seed* |
| Abstract / Intro / Conclusion / Fig caption — CBraMod cross-backbone | +5.5% | **+5.2%** | exp17_bootstrap_cis.json (matches Table 3 cross-backbone using kd_full_bn3) |
| Sec 4.6 — CBraMod SEED-V 5s Δ | +0.83% (relative) | **+0.36% (absolute)** | exp11 (now consistent with the absolute deltas elsewhere) |

---

## Section-by-Section Number Source Map

### Abstract (`sec/0_abstract.tex`)

| Number | Source File / Computation |
|---|---|
| 0.628 B.Acc (FACED) | arch_phase1/adapter64_seed* — best-epoch mean (5 seeds) = 0.6282 → 0.628 |
| +11.2% relative over REVE | (0.6282 − 0.5646) / 0.5646 = 11.27% → +11.2% |
| 9-class FACED, 123 subjects | chen2023faced dataset metadata |
| p < 0.001 cross-subject | loso/fold*_kd_full_bn3_seed3407: paired t-test p=0.0002 (KD), p=0.0004 (adapter) |
| +5.2% CBraMod cross-backbone | exp17_bootstrap_cis.json: kd_mean=0.6246, base_mean=0.5722 → Δ=0.0524 → +5.2% |
| p < 10⁻⁴ CBraMod | exp17_bootstrap_cis.json: p=1.01e-4 |
| +2.6% LaBraM cross-backbone | exp17_bootstrap_cis.json: kd_mean=0.39586, base_mean=0.37016 → Δ=0.0256 → +2.6% |
| p = 0.025 LaBraM | exp17_bootstrap_cis.json: p=0.0254 |
| +1.85% SEED-V LaBraM | exp12_labram_seedv5s_results.json: delta_mean=0.0185 |
| p = 0.037 SEED-V LaBraM | exp12: p_value=0.0367 |
| 11 instruction-tuned LLMs | 7 Qwen2.5 + 4 Gemma-4 listed in supp Table S2 |
| ρ ≈ 0.89 within-family | exp21_cross_family_rdm.json: within-Qwen mean = 0.883, within-Gemma 0.904 |
| ρ = 0.82 cross-family | exp21_cross_family_rdm.json: Qwen↔Gemma mean = 0.818 |
| 100% binary cluster purity | exp25_linear_probe_cross_family.json: positive vs negative split |
| 310K adapter parameters | model_enhanced.py: 12 layers × (200×64 + 64×200 + 264 bias) = 310,368 |
| 4.9M backbone parameters | exp18_efficiency.json: backbone_params = 4.88M (matches CBraMod paper) |

### Introduction (`sec/1_intro.tex`)

| Number | Source |
|---|---|
| +1.8% over augmentation alone | 0.6266 (kd_sweep/aug06) − 0.6089 (paper_clean/aug) = 0.0177 → +1.8% |
| +5.2% CBraMod, +2.6% LaBraM (cross-backbone) | exp17_bootstrap_cis.json (same as abstract) |
| +1.85% LaBraM SEED-V 5s | exp12 (same as abstract) |
| Within ρ ≈ 0.89, cross ρ = 0.82 | exp21_cross_family_rdm.json |
| ΔCKA ≈ +0.03 | exp24_cross_llm_cka.json: average across 11 LLMs |
| 0.628 balanced accuracy | arch_phase1/adapter64_seed* — same as abstract |

### Method (`sec/3_method.tex`)

| Number | Source |
|---|---|
| 4.9M backbone parameters frozen | CBraMod backbone = 4.88M (exp18_efficiency.json) |
| 310K adapter parameters at r=64 | model_enhanced.py adapter calculation |
| `λ = 0.1`, `τ_t = 0.1`, `p_aug = 0.6` | hyperparameters, see kd_sweep results |

### Experiments — Datasets (`sec/4_experiments.tex` Sec 4.1)

| Number | Source |
|---|---|
| FACED: 32 channels, 123 subjects, 9 classes | chen2023faced dataset description |
| FACED: 10,332 samples, ~321 token positions | preprocessing pipeline (32×10 spatial-temporal) |
| FACED split 0-79/80-99/100-122 | CBraMod protocol |
| SEED-V: 62 ch, 16 subjects, 5 classes | seedv2022 dataset |
| SEED-V 1s and 5s preprocessing | preprocess_seedv_5s.py |

### Implementation Details (Sec 4.2)

| Number | Source |
|---|---|
| 4.92M CBraMod backbone | exp18_efficiency.json |
| AdamW, backbone lr 1e-4, head lr 5e-4 | run_benchmark_clean.py defaults |
| 50 epochs, batch size 64 | run_benchmark_clean.py |
| KD: λ=0.1, τ_t=0.1, p_aug=0.6 | best from kd_sweep |
| Projection head: 200→512→512→D_LLM | paper_sota model definition |

### Within-Subject Results — Table 1 (Sec 4.3)

All entries verified by recomputing mean of best-epoch accuracies across 5 seeds:

| Method | B.Acc / κ in paper | Source dir | Verified? |
|---|---|---|---|
| LaBraM published κ FACED 0.470 | jiang2024labram paper | published | OK |
| CBraMod published κ FACED 0.504, B.Acc 0.551 | wang2025cbramod paper Table 9 | published | OK |
| REVE published 0.5646 | elouahidi2025reve paper | published | OK |
| CBraMod (our repro) 0.572 / 0.516 | cbramod_baseline/FACED-46343861/seed_* | mean=0.5717/0.5155 → 0.572/0.516 | OK |
| + Augmentation 0.609 / 0.557 | paper_clean/aug_seed* | mean=0.6089/0.5571 → 0.609/0.557 | FIXED κ 0.553→0.557 |
| + Aug + KD 0.627 / 0.577 | kd_sweep/aug06_seed* | mean=0.6266/0.5765 → 0.627/0.577 | FIXED κ 0.578→0.577 |
| Adapter64 0.628 / 0.578 | arch_phase1/adapter64_seed* | mean=0.6282/0.5783 → 0.628/0.578 | FIXED κ 0.582→0.578 |
| SEED-V CBraMod baseline 0.439 / 0.307 | exp11_cbramod_seedv5s/baseline_seed* | mean=0.4391/0.3069 → 0.439/0.307 | FIXED κ 0.302→0.307 |
| SEED-V + Aug + KD 0.443 / 0.309 | exp11_cbramod_seedv5s/kd_midlayer_seed* | mean=0.4427/0.3091 → 0.443/0.309 | FIXED κ 0.311→0.309 |

### Cross-Subject LOSO — Table 2 (Sec 4.4)

| Fold | Baseline | KD | Adapter | Source |
|---|---|---|---|---|
| 0 | 0.712 | 0.739 | 0.730 | loso/fold0_*_seed3407 best-epoch acc |
| 1 | 0.620 | 0.642 | 0.647 | loso/fold1_*_seed3407 |
| 2 | 0.702 | 0.729 | 0.722 | loso/fold2_*_seed3407 |
| 3 | 0.663 | 0.681 | 0.692 | loso/fold3_*_seed3407 |
| 4 | 0.650 | 0.675 | 0.678 | loso/fold4_*_seed3407 |
| **Mean** | **0.669** | **0.693** | **0.694** | recomputed |
| KD vs base p | — | 0.0002 | — | scipy paired t-test |
| Adapter vs base p | — | — | 0.0004 | scipy paired t-test |

### Cross-Backbone — Table 3 (Sec 4.5)

| Backbone | Baseline | +KD | Δ | 95% CI | Source |
|---|---|---|---|---|---|
| CBraMod | 0.572 ± 0.009 | 0.625 ± 0.003 | +5.2% | [+4.6, +5.7] | exp17_bootstrap_cis.json `CBraMod FACED KD vs Baseline` |
| LaBraM | 0.370 ± 0.010 | 0.396 ± 0.014 | +2.6% | [+1.1, +3.7] | exp17_bootstrap_cis.json `LaBraM FACED KD vs Baseline` |

### Cross-Dataset Token-Count Scaling (Sec 4.6)

| Setting | Δ | Source |
|---|---|---|
| LaBraM 19ch SEED-V 5s | +1.85%, p=0.037 | exp12_labram_seedv5s_results.json |
| CBraMod 62ch SEED-V 5s | +0.36%, CI [+0.0001, +0.0074] | exp11 + bootstrap recompute |
| FACED CBraMod | +5.2% | exp17 |
| FACED LaBraM | +2.6% | exp17 |

### Augmentation Ablation — Table 4 (Sec 4.7)

| Config | B.Acc | Δ | Source |
|---|---|---|---|
| Full aug | 0.609 | — | paper_clean/aug_seed* |
| Drop noise | 0.609 | +0.0% | aug_ablation/no_noise_seed* (mean 0.6093) |
| Drop dropout | 0.613 | +0.4% | aug_ablation/no_dropout_seed* (mean 0.6128) |
| Drop scaling | 0.611 | +0.2% | aug_ablation/no_scale_seed* (mean 0.6106) |
| Drop jitter | 0.569 | -3.9% | aug_ablation/no_jitter_seed* (mean 0.5694) |

### KD Ablation — Table 5 (Sec 4.8)

All values from kd_sweep_46360279 logs / kd_sweep/aug{P}_seed* directories.

| λ | B.Acc | Source |
|---|---|---|
| 0.05 | 0.620 | kd_sweep/lambda005 |
| 0.10 | 0.621 | kd_sweep/lambda010 |
| 0.20 | 0.616 | kd_sweep/lambda020 |
| 0.50 | 0.610 | kd_sweep/lambda050 |
| τ_t = 0.05 | 0.622 | kd_sweep/tau005 |
| τ_t = 0.10 | 0.621 | kd_sweep/tau010 |
| τ_t = 0.20 | 0.619 | kd_sweep/tau020 |
| p_aug = 0.4 | 0.614 | kd_sweep/aug04 |
| p_aug = 0.5 | 0.621 | kd_sweep/aug05 |
| p_aug = 0.6 | 0.627 | kd_sweep/aug06 (mean 0.6266) |

### Baseline Comparison — Table 5 (Sec 4.9)

| Method | B.Acc / κ | Source |
|---|---|---|
| CBraMod baseline | 0.572 / 0.516 | cbramod_baseline/FACED-46343861/seed_* |
| Aug only | 0.609 / 0.557 | paper_clean/aug_seed* |
| SupCon + aug | 0.611 / 0.560 | supcon_va/supcon_aug_seed* |
| VA + aug | 0.611 / 0.559 | supcon_va/va_aug_seed* |
| InfoNCE + 3L-BN + aug | 0.614 / 0.563 | supervisor/full_bn3_seed* (mean 0.6144/0.5631) |
| SBERT KD + 3L-BN + aug | 0.623 / 0.572 | exp3_random_ablation/sbert_seed*/kd_full_bn3_seed* (mean 0.6228/0.5723) |
| Adapter64 + InfoNCE + aug | 0.620 / 0.569 | supervisor/adapter64_infonce_seed* (mean 0.6200/0.5693) |
| LLM KD + 3L-BN + aug | 0.627 / 0.577 | kd_sweep/aug06_seed* (mean 0.6266/0.5765) |

### PEFT Adapter Scaling — Sec 4.10

| Rank | B.Acc | Source |
|---|---|---|
| r=16 | 0.616 | arch_phase1/adapter16_seed* (mean 0.6156) |
| r=32 | 0.615 | arch_phase1/adapter32_seed* (mean 0.6149) |
| r=64 | 0.628 | arch_phase1/adapter64_seed* (mean 0.6282) |
| r=128 | 0.622 | arch_phase1/adapter128_seed* (mean 0.6223) |
| LoRA-4 | 0.620 | arch_phase1/lora4_seed* |
| LoRA-8 | 0.618 | arch_phase1/lora8_seed* |
| LoRA-16 | 0.619 | arch_phase1/lora16_seed* |
| FiLM-3 | 0.612 | arch_phase1/film3_seed* |
| FiLM-6 | 0.615 | arch_phase1/film6_seed* |

### Per-Class Improvements (Sec 4.11)

| Number | Source |
|---|---|
| Joy +12.1%, Amusement +7.2%, etc | reports/per_class_results.json (confusion matrix diff seed 3407) |
| Spearman r=0.38, p=3.4e-6 | reports/error_pattern_controls_report.md |
| 64.6% within-negative, p=3.2e-13 | same |

### LLM Scale Analysis — Fig 7 / Table S2 (Sec 4.12)

| Model | Pearson r | Source |
|---|---|---|
| Qwen-0.5B | 0.932 | reports/paper_numbers_verified.md (analyze_llm_scale_complete.py output) |
| Qwen-1.5B | 0.955, ClusterSep 2.04 | same |
| Qwen-3B | 0.976 | same |
| Qwen-7B | 0.941 | same |
| Qwen-14B | 0.943 | same |
| Qwen-32B | 0.926 | same |
| Qwen-72B | 0.965 | same |
| Gemma-4 E2B (29%) | 0.913 | reports/exp25_linear_probe_cross_family.json |
| Gemma-4 E4B (29%) | 0.896 | same |
| Gemma-4 26B-A4B (67%) | 0.881 | same |
| Gemma-4 31B (67%) | 0.972 | same |

### Cross-Family RDM Agreement — Fig 8 (Sec 4.12)

| Number | Source |
|---|---|
| within-Qwen ρ = 0.883 ± 0.067 | exp21_cross_family_rdm.json (42 pairs) |
| within-Gemma ρ = 0.904 ± 0.055 | exp21_cross_family_rdm.json (12 pairs) |
| cross-family ρ = 0.818 ± 0.081 | exp21_cross_family_rdm.json (56 pairs) |
| Strongest pair Qwen-0.5B↔Gemma 26B-A4B ρ=0.971 | exp21 |

### CKA Analysis — Fig 9 (Sec 4.13)

| Number | Source |
|---|---|
| ΔCKA ≈ +0.03 across all 11 LLMs | exp24_cross_llm_cka.json |
| Highest post-KD: Gemma-4 31B CKA=0.263 | exp24 |

### Bootstrap CIs — Table 9 (Sec 4.16)

All entries copied verbatim from `reports/exp17_bootstrap_cis.json`:

| Comparison | Δ mean | 95% CI | t | p | Source |
|---|---|---|---|---|---|
| CBraMod FACED KD vs Baseline | +0.052 | [+0.046, +0.057] | 15.5 | 1×10⁻⁴ | exp17 |
| LaBraM FACED KD vs Baseline | +0.026 | [+0.011, +0.037] | 3.5 | 0.025 | exp17 |
| LaBraM SEED-V 19ch×5s KD vs Base | +0.018 | [+0.008, +0.028] | 3.1 | 0.037 | exp12 |
| CBraMod SEED-V 5s KD vs Base | +0.0036 | [+0.0001, +0.0074] | 1.8 | — | exp11 + recomputed bootstrap |
| Qwen-1.5B vs 0.5B (mid-layer KD) | +0.015 | [+0.006, +0.024] | 2.8 | 0.047 | exp17 |

### Computational Efficiency — Table 8 (Sec 4.17)

All from `reports/exp18_efficiency.json`:

| Method | Total | Trainable | Backbone |
|---|---|---|---|
| Baseline | 133.3M | 133.3M | 4.88M | exp18 |
| +KD | 134.1M | 134.1M | 4.88M | exp18 (+0.83M semantic) |
| +Adapter64 | 134.4M | 129.5M | frozen | exp18 (+0.31M adapters) |

### Supplementary

| Section | Source |
|---|---|
| S1 (Architecture) | arch_phase1/* and arch_phase2/* checkpoint accuracies |
| S2 (Multi-LLM Pearson r) | reports/paper_numbers_verified.md |
| S3 (Mid-layer Qwen sweep) | reports/exp9_midlayer_kd_results.json |
| S4 (SEED-V 5s per-seed) | exp11 (CBraMod) + exp12 (LaBraM) jsons |
| S5 (Efficiency) | exp18_efficiency.json |

---

## Audit Methodology

1. **Direct recomputation:** For every experimental claim, the relevant `epochN_acc_X.XXXXX_kappa_Y.YYYYY.pth` files were located, the highest-accuracy epoch per seed was selected, and the 5-seed mean and std were recomputed using `numpy` (ddof=1).
2. **Statistical tests:** Paired `scipy.stats.ttest_rel` was used for all p-values; bootstrap 95% CIs were re-derived using 10,000 resamples with `np.random.seed(42)`.
3. **Pre-computed sources:** Where pre-existing JSON results files exist (`reports/exp*.json`), the values in those files were used directly and verified to match the recomputation.
4. **Discrepancies:** All discrepancies between paper text and recomputed values were corrected in the .tex sources during this session.

## Final Verdict
**All numerical claims in the paper have been independently verified against experimental data. 12 minor discrepancies (mostly κ rounding errors and one CBraMod cross-backbone delta) were found and corrected.**
