# Comprehensive Findings Catalog — NeurIPS 2026 Paper

**Compiled**: 2026-04-27 from worklog.md (15,837 lines, cycles 1-75) + headline_numbers.md + narrative.md  
**Tier legend**: 🟢 paper-grade hero/main · 🟡 supporting/table-row · 🔴 caveat/negative · ⚪ skip

Source roots:
- Worklog: `/ibex/project/c2323/yousef/worklog.md`
- Reports: `/ibex/project/c2323/yousef/reports/`
- References (audited): `/ibex/project/c2323/yousef/reports/PAPER_REFERENCES_AUDITED.md`

---

## §1 Introduction (hero claims for opening)

| # | Finding | Numbers | Source | Tier |
|---|---|---|---|---|
| 1.1 | Universal V-axis: same direction across language, vision, EEG, brain | brain cohort r=0.87 (#397); cross-LLM mean off-diag r=0.654 (#440); vision V/A both BEAT supervised on OASIS (#385) | r6_eeg_llm_circle.json, eeg_llm_extra/results.json | 🟢 |
| 1.2 | EEG models spontaneously converge to V-axis | cross-arch r(BACC, class-PC1)=+0.885 n=36, p=8e-13; within-class residual r=+0.715 (#429) | merge_crossarch_vaxis_results.json | 🟢 |
| 1.3 | 25+ external V-axis supervision interventions all fail or hurt | 6 stat-sig negatives, monotonic destruction with strength | merge_*_results.json (Round 7-11) | 🟢 |
| 1.4 | New FACED 9-class SOTA via principled ensembling | 0.6948 BACC, +21.5% rel over CBraMod 0.572 | sota_ablation_cascade.md, ensemble_d6_d6e150_results.json | 🟢 |
| 1.5 | Within-class V-axis residual explains ensemble gain | r(within-resid, LOO contribution) = +0.743, p=0.014 (#449) | sota_ensemble_theory.md | 🟢 |

---

## §3 V-Axis in LLMs (Universal Few-Shot Probe)

### Core extraction protocol
| # | Finding | Numbers | Source | Tier |
|---|---|---|---|---|
| 3.0 | 9-emotion story-class centroid PCA → V-axis (PC1); single Qwen-1.5B, L28 | 9 stories × 50 generations / class; PC1 var ratio ~0.55 at L28 | cycle 73n+ pipeline | 🟢 |

### Sentiment benchmarks (zero-shot)
| # | Finding | Numbers | Source | Tier |
|---|---|---|---|---|
| 3.1 | SST-2 zero-shot (calibrated) | AUC 0.868 [0.844, 0.890]; 77.75% (median); 79.17% (200-sample calib); supervised LR @5k=0.837 | cycle 73p Task #288b, job 46682300 (worklog L9066) | 🟢 |
| 3.2 | IMDB balanced | AUC 0.895, accuracy 81.0% L28 | cycle 73t (worklog L9133) | 🟡 |
| 3.3 | Yelp Polarity | AUC 0.953, 88.80% accuracy | cycle 73x (worklog L9204) | 🟡 |
| 3.4 | Twitter SemEval 2017 | AUC 0.923, 83.80% | cycle 73x | 🟡 |
| 3.5 | Rotten Tomatoes (MR) | AUC 0.843, 76.55% | cycle 73x | 🟡 |
| 3.6 | SST-5 fine-grained ordinal | r=0.620, ρ=0.627 (n=2210) | cycle 73hh Task #322 | 🟡 |

### Lexicon recovery
| # | Finding | Numbers | Source | Tier |
|---|---|---|---|---|
| 3.7 | Hu & Liu 6789-word lexicon | Pearson \|r\|=0.76 [0.74,0.78], 6.3× random | cycle 73o Task #289b | 🟢 |
| 3.8 | NRC small lexicon (n=32) | \|r\|=0.95 (sign arbitrary) | cycle 73n Task #289 | 🟡 |
| 3.9 | Warriner 3000-word continuous | V Pearson −0.686, ρ=−0.699; 9.5× SNR | cycle 73z Task #305 | 🟢 |
| 3.10 | Arousal axis fails everywhere | EmoBank A \|r\|=0.01-0.06; Warriner A \|r\|=0.16; max 13% recovery | cycles 73g/73m/73o/73z | 🔴 (caveat asymmetry) |

### Multi-LLM universality (cross-family scaling)
| # | Finding | Numbers | Source | Tier |
|---|---|---|---|---|
| 3.11 | 18-LLM agreement matrix mean off-diag r=0.654 | top: Qwen-14B 0.964, Qwen-7B 0.957, Qwen-3B 0.947 | #440 results.json (G_multi_llm_agreement) | 🟢 |
| 3.12 | Inverted-U scale law: Qwen-1.5B optimal | Qwen-1.5B 0.868 > Qwen-7B 0.848 > Mistral 0.862 > OLMo 0.837; 32B WORST | feedback_llm_scale.md, P5b-LATEST-LLMs | 🟢 |
| 3.13 | 6 LLM families confirmed | Qwen, Mistral, Llama-3, OLMo, BLOOM, Gemma-4 — all but Gemma-4 final-layer-peaks | p1_latest_llms_synthesis.md | 🟢 |
| 3.14 | Gemma-4 OUTLIER: V-axis at L1 not L_final | E2B/E4B/26B all peak L1 (0.69-0.74); collapse at final | Round 6 cross-arch | 🟡 (sharpens scope) |
| 3.15 | Cross-family ensembling LOSES vs best single | mean ensemble 0.805 vs Qwen-1.5B alone 0.837 | cycle 73ff Task #313 | 🔴 |
| 3.16 | SBERT sentence-encoder fails same pipeline | SST-2 AUC 0.713 vs Qwen 0.868 (-0.155); IMDB -0.173; lexicon -0.242 | cycle 73bb Task #309 | 🟡 |

### Layer-localized V-shape
| # | Finding | Numbers | Source | Tier |
|---|---|---|---|---|
| 3.17 | Sudden L27 emergence + V-shape (Qwen) | L1 AUC 0.752 → L2-26 ~0.52 → L27 0.836 → L28 0.837 | cycle 73u Task #296 | 🟢 |
| 3.18 | V-shape replicates cross-family | Pythia: L3=0.32 → L4-14 dilute → L19-21=0.50; Bloom: L4=0.26 → mid 0.005-0.10 → L24=0.33 | cycle 73y Task #299 | 🟢 |
| 3.19 | Latent-space metrics: isotropy 0.01→0.58, eff-rank 3.0→6.9, PC1-var 0.97→0.55 | L14 V-axis nearly orthogonal to L28 (cos=0.067) → final-layer V is NEWLY computed | cycle 73cc Task #315 | 🟢 |

### Few-shot data efficiency
| # | Finding | Numbers | Source | Tier |
|---|---|---|---|---|
| 3.20 | n-shot ablation: even n=1 works | n=1 → AUC 0.740±0.043; n=15 → 0.831±0.010 (matches LR @5000) | cycle 73s Task #295 | 🟢 |
| 3.21 | Few-label curve quantification | zero-label probe ≈ supervised LR @ N=80-100; LR @ 5000 = AUC 0.914 | cycle 73y Task #300 | 🟢 |
| 3.22 | PCA > LDA for OOD (despite supervised LDA) | PCA EmoBank V \|r\|=0.475 vs LDA 0.119 | cycle 73n Task #291 | 🟡 |

### Composition / arithmetic
| # | Finding | Numbers | Source | Tier |
|---|---|---|---|---|
| 3.23 | V_polite + V_happy → 4-quadrant 79% (agent-authored) | 3.16× chance; uniform per-cell precision 0.68-0.86 | r6_composition_results.json | 🟡 |
| 3.24 | Composition validation on natural text (HONEST CORRECTION) | GoEmotions 41.8%, SST-5 45.3%, Yelp 46.7% — well above chance but below 79% | R6b validation | 🔴 (scope refinement) |
| 3.25 | Subtractive orthogonalization (Gram-Schmidt) | V_valence⊥polite: happy-AUC 0.912→0.988, polite-AUC 0.793→0.560 | r6_composition | 🟡 |

### Concept library universality
| # | Finding | Numbers | Source | Tier |
|---|---|---|---|---|
| 3.26 | 20 concepts, 17/20 at AUC≥0.95 | fear/urgency/hope/shame/complexity/concreteness/envy/guilt/decisiveness/emotionality/optimism all AUC=1.00 | r6_concept_library, #394 | 🟢 |
| 3.27 | Recipe generalizes beyond emotions | complexity, concreteness, authoritativeness all hit AUC≥0.98 | #394 | 🟡 |
| 3.28 | Toxicity FAILS (Jigsaw) | AUC 0.59 (near random) | cycle 73x Task #303 | 🔴 |

### Prompt steel-manning vs probing
| # | Finding | Numbers | Source | Tier |
|---|---|---|---|---|
| 3.29 | LLM-as-judge BEATS V-axis on quality | SST-2 judge 0.951, judge+5shot 0.957, V-axis 0.868 | r6_steelman_synthesis | 🔴 (honest reframe) |
| 3.30 | V-axis ~4× faster than judge | 165s/1k vs ~50s/1k; speed is the trade-off | P5-DEPLOY | 🟡 |

### Cross-language
| # | Finding | Numbers | Source | Tier |
|---|---|---|---|---|
| 3.31 | mT0-base (encoder-decoder) closes multilingual asymmetry | JA→SST-2 AUC 0.891, AR 0.912, RU 0.913 — BEAT EN baseline | P5-LANG | 🟢 |
| 3.32 | Causal LM English-bias confirmed | Qwen-1.5B JA 0.515 (chance), AR 0.519, RU 0.552 | cycle 73 + R5 | 🟡 |
| 3.33 | Spanish multilingual via Qwen-generated stories | AUC 0.726 on Spanish Twitter (n=296) | cycle 73z Task #301 | 🟡 |
| 3.34 | V-axis cross-language cosines 0.16-0.47 | en-es 0.466, en-fr 0.162, es-fr 0.462; arousal axes orthogonal across langs | cycle 73hh Task #321 | 🟡 |

### Nonce / specificity / controls
| # | Finding | Numbers | Source | Tier |
|---|---|---|---|---|
| 3.35 | Nonce-word ablation: real words 0.868 → nonce 0.524 (chance) | confirms semantic content, not template | P5-DEPTH (#383) | 🟢 |
| 3.36 | Bootstrap CIs tight: SST-2 [0.844,0.890], EmoBank [0.485,0.512], Hu&Liu [0.740,0.776] | 1000-sample bootstrap | cycle 73x Task #298 | 🟡 |
| 3.37 | Random direction baseline: AUC ~0.51, lexicon \|r\|~0.10 | clear separation everywhere | various | 🟡 |
| 3.38 | Controlled generation NULL/WEAK | scale-monotonic shifts noisy; LLM-derived ≈ random for 3/4 emotions | cycle 73r/73l Tasks #273 #293 | 🔴 (scope) |

### Vision V-axis
| # | Finding | Numbers | Source | Tier |
|---|---|---|---|---|
| 3.39 | Vision V-axis BEATS supervised (OASIS) | Valence: V-axis r=0.869 vs Ridge 0.836; arousal V-axis r=0.803 vs Ridge 0.789 | P5-VIS-EXT | 🟢 |
| 3.40 | Aesthetics partial | AADB 9831: V-axis r=0.572 vs Ridge 0.703 (81% of supervised) | P5-VIS-EXT | 🟡 |
| 3.41 | Cross-modal CLIP V-axis on SST-2 | AUC 0.651 (vs random 0.557, words 0.604) | Round 4 cross-modal | 🟡 |
| 3.42 | Arousal axis ⊥ Valence (cos 0.013) on vision | clean dimension separation | P5-VIS-EXT | 🟡 |

---

## §4 V-Axis in Brain (Cross-paper bridge)

| # | Finding | Numbers | Source | Tier |
|---|---|---|---|---|
| 4.1 | EEG-LLM circle: cohort r=0.87 (CLIP rich-text V-axis ↔ EEG-DE-Ridge) | n=28 stim, p=2.7e-05 | r6_eeg_llm_circle.json (#397) | 🟢 |
| 4.2 | CLIP bare-emotion V-axis ↔ EEG | r=0.874, p=1.2e-09 | r6_clip_only.json | 🟢 |
| 4.3 | CLIP valence-category V-axis ↔ EEG | r=0.889, p=2.7e-10 | r6_clip_only.json | 🟢 |
| 4.4 | Random direction control: r=0.07-0.069, p=0.73 | clean null, validates p<10⁻⁹ headline | #397 | 🟢 |
| 4.5 | Trial-level (n=3,444) r=0.17-0.21, all p<1e-23 | trial-level signal real but noisier | #397 | 🟡 |
| 4.6 | Class-level (n=9 emotions): r=+0.886 vs behavioral valence | nearly perfect emotion ranking | #397 | 🟡 |
| 4.7 | Per-stimulus split-half reliability | r=0.988 — very clean stimulus-level signal | #397 | 🟡 |
| 4.8 | 18-LLM brain prediction: top-tier mean r=0.788±0.064 (n=13) | Qwen-14B 0.862, Mistral-7B 0.861 — UNIVERSALITY not scaling | merge_multi_llm_eeg_results.json (#411) | 🟢 |
| 4.9 | Per-LLM brain anchor at PO3/γ: Qwen-1.5B leads at r=+0.411, p=0.030 | inverted-U replicates at brain level | #440 (E2_per_llm_vs_eeg) | 🟡 |
| 4.10 | Within-Qwen scaling: r=0.249 p=0.52 (n.s.) | scaling is NOT the story | #411 | 🟡 |
| 4.11 | Gemma-4 universality SURVIVES | E2B L17 r=0.819 (p=1e-7); E4B L1 r=0.714 — mid-layers carry brain alignment | merge_gemma_eeg_results.json (#427) | 🟡 |
| 4.12 | TinyLlama / BLOOM / Pythia FAIL at brain | LLMs that didn't learn V at SST-2 don't predict brain | #411 | 🟡 |
| 4.13 | FACED→SEED-V semantic-space transfer | r=+0.96 (p=0.008) — happy +2.25, sad −1.07 ordering | merge_xeeg_synthesis (#407) | 🟡 |

---

## §5 Cross-Architecture Convergence (Mechanism)

### Headline result
| # | Finding | Numbers | Source | Tier |
|---|---|---|---|---|
| 5.1 | Cross-arch r(BACC, class-PC1 \|r\|) = +0.885, p=7.8e-13 (n=36) | CBraMod + EMOD + ensembles | merge_crossarch_vaxis_results.json (#429) | 🟢 |
| 5.2 | Within-class residual r = +0.715, p=0.001 | more robust than class-PC1 (lower-dim gotcha) | #429 | 🟢 |
| 5.3 | Per-checkpoint within-resid \|r\| ↔ LOO ensemble contribution: r=+0.743, p=0.014 | TWO-TIER ensemble theory | sota_ensemble_theory.md (#449) | 🟢 |
| 5.4 | Top-7 by within-resid → 0.6962 vs bottom-7 → 0.6829 (z=+2.0 vs random-7) | validation of theory | #449 | 🟢 |

### Random-direction control
| # | Finding | Numbers | Source | Tier |
|---|---|---|---|---|
| 5.5 | Random-direction null: V-axis at 93rd percentile, p_one=0.079 | reframes "smoking gun" to "top-decile" — 9-class PC1 is low-dim | crossarch_random_control.md (#451) | 🔴 (honest scope, paper-strengthening) |

### Per-architecture breakdown
| # | Finding | Numbers | Source | Tier |
|---|---|---|---|---|
| 5.6 | CBraMod class-PC1 V-axis r mean 0.21 (low) | but within-class V r=0.51 — encodes V differently | #429 | 🟡 |
| 5.7 | EMOD vanilla d6 class-PC1 r mean 0.67 | strong encoding, BACC 0.647-0.661 | #429 | 🟡 |
| 5.8 | EMOD d6_e150 class-PC1 r mean 0.69 | longer training → cleaner V | #429 | 🟡 |
| 5.9 | EMOD-only depth sweep: d4=0.426, d6=0.428, d8=0.392, d10=0.382 | depth HURTS within-EMOD class-PC1 (mild) — between-arch dominates | merge_emerge_deep_results.json (#425) | 🟡 |
| 5.10 | Class-level vs stim-level CONTRADICTION RESOLVED | class-mean PC1 r=0.68 + within-class residual r=0.78 (both strong); stim-level PC1 r=0.40 is mixture artefact | merge_contradiction_results.json (#426) | 🟢 |
| 5.11 | V-axis r saturates at K=8 in VARIANCE not magnitude | unifies with PIVOT 2 K=5 compute-optimal law | merge_pivot2_link_results.json (#428) | 🟡 |

---

## §6 Brain Topography

### Posterior-dominant V-axis (overturning Davidson)
| # | Finding | Numbers | Source | Tier |
|---|---|---|---|---|
| 6.1 | Region \|r\|: occipital 0.212 > parietal 0.181 > central 0.180 > frontal 0.162 | POSTERIOR > frontal | merge_topography_synthesis.md (#430) | 🟢 |
| 6.2 | Top channels: PO3/γ r=+0.478, F7/β r=−0.471, O1/γ r=+0.440 | clean parieto-occipital network | #430 | 🟢 |
| 6.3 | Best frequency band (mean): alpha \|r\|=0.233 | alpha is broadly best, but strongest single cells in β/γ | #430 | 🟡 |
| 6.4 | Davidson F4-F3 α = +0.006 | qualitatively right direction but ~10× weaker than posterior | #440 (C_asymmetry.davidson_F4F3_alpha) | 🟢 (challenges classical FAA for video) |
| 6.5 | Fp2-Fp1 α = +0.012, F8-F7 α = +0.016 | minor frontal asymmetry consistent with Davidson direction | #440 | 🟡 |

### Anger contrast (drop-class diagnostic)
| # | Finding | Numbers | Source | Tier |
|---|---|---|---|---|
| 6.6 | Removing Anger drops cohort r by −0.151 (32% of effect) | also Amusement −0.060, Tenderness −0.057 | #440 (D_per_emotion.per_class[Anger].delta_when_drop) | 🟢 |
| 6.7 | Anger+Amus+Tend ALONE (n=9 stim) → cohort r=0.870 | the V-axis IS a 9-stim story | #441 (analysis_3_anger_weighted) | 🟢 |
| 6.8 | Excluding Anger+Amus+Tend (n=19 mid-stim) → cohort r=−0.015 | mid-valence stim contribute pure noise | #441 | 🟢 |
| 6.9 | Anger-weighted analytical ceiling r=0.714 (vs 0.478 baseline at PO3/γ) | weights {Anger:5, Amus:3, Tend:3, others:1} | #441 (analysis_3_anger_weighted) | 🟡 |

### Per-subject Simpson's paradox
| # | Finding | Numbers | Source | Tier |
|---|---|---|---|---|
| 6.10 | Cohort r=0.48 at top-8 channels vs per-subject mean r=−0.06 | classic Simpson's; std 0.28, range [−0.67,+0.79] | #440 (B_per_subject) | 🟢 |
| 6.11 | Per-subject ORACLE all-bands ceiling = +0.616 | massive headroom IF model picks BOTH channel AND band per subject | #441 (analysis_2_per_subject_ceiling) | 🟡 |
| 6.12 | Per-subject FIXED top-8 γ: r=−0.062 | Simpson's confirmed, gamma alone insufficient | #441 | 🟡 |
| 6.13 | Best-channel-per-subject mean=+0.55, max=+0.89 | individual subjects DO show V-axis, just at different channels | #440 | 🟡 |

### Time-resolved peaks (LPP analogue)
| # | Finding | Numbers | Source | Tier |
|---|---|---|---|---|
| 6.14 | Time-resolved α peak at t=21s (cohort r=0.40) | LPP/sustained-attention story | #440 (A_time_resolved) | 🟡 |
| 6.15 | β peaks t=18s (r=0.41), δ/θ t=12s, γ early t=3-6s | matches Müller 1999 early-γ; mid-late α/β | #440 | 🟡 |
| 6.16 | Only 22-24% of subjects peak in cohort 18-21s window | per-subject window required (not fixed cohort window) | #441 (analysis_4_per_subject_peak) | 🟡 |

### Functional connectivity
| # | Finding | Numbers | Source | Tier |
|---|---|---|---|---|
| 6.17 | Top-channel γ functional connectivity r = 0.675 | one tight posterior-occipital network | #440 (H_connectivity) | 🟡 |
| 6.18 | θ-γ PAC (Tort modulation index) — DEFINITIVELY NEGATIVE | r=0.082, p=0.667 (vs naive proxy r=0.20 p=0.30) | #441 (analysis_1_pac) | 🔴 |
| 6.19 | MI vs 200 random directions: linear corr p=0.020 (sig); MI p=0.115 (n.s.) | V-axis is essentially LINEAR; nonlinear has no extra info | #440 | 🟡 |

### Topographic reversals
| # | Finding | Numbers | Source | Tier |
|---|---|---|---|---|
| 6.20 | T8-T7 (β) r=−0.027, PO4-PO3 (γ) r=−0.019 | hemispheric reversal at temporal/parieto-occipital | #440 | 🟡 |

---

## §7 Saturation Theorem (V-axis as Supervision)

### Statistically significant negatives (paper-grade evidence)
| # | Variant | Δ vs baseline | p | Source | Tier |
|---|---|---|---|---|---|
| 7.1 | Frontal-mask λ=0.5 | **−0.052** | **0.0015** | merge_frontal_vaxis_runs (#434) | 🟢 |
| 7.2 | FAA λ=0.5 | **−0.044** | **0.006** | merge_faa_vaxis_runs (#435) | 🟢 |
| 7.3 | Anger-weighted λ=0.5 | **−0.054** | **0.0003** | merge_anger_vaxis_runs (#443) | 🟢 |
| 7.4 | Occipital λ=0.1 | **−0.022** | **0.007** | merge_frontal_vaxis_runs/run_occvaxis (#437) | 🟢 |
| 7.5 | Topo-optimal λ=0.1 | **−0.013** | **0.039** | merge_topo_optimal_vaxis_runs (#438) | 🟢 |
| 7.6 | RSA λ=1.0 | **−0.057** (and λ=5 −0.093) | <0.001 | merge_rsa_results.json (#414) | 🟢 |
| 7.7 | Distance-CE τ=5.0 | **−0.397** (near chance) | <0.001 | merge_distance_ce_results.json (#415) | 🟢 |

### Borderline / directional negatives
| # | Variant | Δ | p | Source | Tier |
|---|---|---|---|---|---|
| 7.8 | FAA λ=0.1 | −0.018 | 0.063 | #435 | 🟡 |
| 7.9 | Frontal-mask λ=0.1 | −0.009 | 0.21 (NS) | #434 | 🟡 |
| 7.10 | PEFT fullhead λ=0.1 | −0.009 | 0.069 | merge_peft_vaxis_runs (#432) | 🟡 |
| 7.11 | Curriculum cosine_decay li=0.5 | −0.009 | 0.23 | merge_warmup_vaxis_runs (#445) | 🟡 |

### Neutral / not-significant positives (proves saturation)
| # | Variant | Δ | p | Source | Tier |
|---|---|---|---|---|---|
| 7.12 | Topo-optimal λ=0.05 | +0.0021 | 0.50 (NS) | #438 | 🟡 |
| 7.13 | Procrustes λ=0.05 | +0.0012 | 0.89 (NEUTRAL) | merge_procrustes_vaxis_runs (#436) | 🟡 |
| 7.14 | EMODSTYLE λ=0.5 stim | +0.0066 | 0.22 (NS, sweet spot) | merge_emodstyle_runs (#424) | 🟡 |
| 7.15 | EMODSTYLE class λ=1.0 | +0.018 (s2025 outlier; full 5-seed −0.010) | NS | #424 | 🟡 |

### Monotonic destruction curves (paper-grade gradient evidence)
| # | Curve | Numbers | Source | Tier |
|---|---|---|---|---|
| 7.16 | RSA λ=0/0.1/0.5/1.0/5.0 | 0.624 → 0.610 → 0.585 → 0.566 → 0.531 | #414 | 🟢 |
| 7.17 | Distance-CE τ=0.5/1.0/2.0/5.0 | 0.516 → 0.476 → 0.395 → 0.227 (chance) | #415 | 🟢 |
| 7.18 | Multi-V λ=0.05/0.1/0.5 | 0.622 → 0.603 → 0.581 | merge_multi_v_runs (#419) | 🟢 |
| 7.19 | EMODSTYLE inverted-U | λ=0/0.1/0.5/1.0/2.0: 0.624 → 0.623 → 0.630* → 0.617 → 0.609 (sweet spot at 0.5) | #424 | 🟡 |
| 7.20 | SCALING data fraction × λ=0.5 | f=0.1: −0.002; f=0.25: −0.029; f=0.5: −0.032; f=1.0: −0.045 | merge_scaling_synthesis (#408) | 🟢 |

### Other negatives (table rows)
| # | Variant | Δ | Source | Tier |
|---|---|---|---|---|
| 7.21 | EEG-AUX MSE λ=0.1/0.5 | −0.016 / −0.043 (monotonic) | merge_eeg_vaxis_aux_runs (#401) | 🟡 |
| 7.22 | KD soft target T=0.5/1.0/2.0 × λ=0.5/1.0 | −0.005 / −0.007 / −0.012 | merge_kd_results.json (#409) | 🟡 |
| 7.23 | Init: bias-init −0.003, weight-init −0.017 | hurts especially at weight-init | merge_init_results.json (#406) | 🟡 |
| 7.24 | PRIOR (smooth temperature) +0.0019 | noise floor; "linear" mode label-leaks (delete) | merge_prior_synthesis (#418) | 🟡 |
| 7.25 | XEEG (FACED→SEED-V) λ=0/0.5 | Δ=+0.0015, p=0.97 (zero effect) | merge_xeeg_synthesis (#407, #412) | 🟡 |
| 7.26 | Pretrain-FT: frozen 0.209 (−0.401), unfrozen 0.419 (−0.190) | catastrophic 1D-bottleneck destruction | merge_pretrain_ft_results.json (#416) | 🟡 |
| 7.27 | INFONCE: vanilla 0.167, with V 0.135 | broken protocol but direction consistent | merge_infonce_results.json (#417) | ⚪ broken |
| 7.28 | Distill (V-axis teacher → student KD): 0.6075 vs vanilla 0.624 | teacher 0.560, student inherits bias | merge_distill_runs (#420) | 🟡 |
| 7.29 | StimAgg: ensemble classifies all 28 stim-IDs → BACC=1.0 | leak by construction; not a win, documents ceiling | merge_distill (#421) | ⚪ |
| 7.30 | SmallLam λ∈{0.001-0.05} | all noise floor (−0.004 to +0.001) | #422 | 🟡 |
| 7.31 | Uncert (Kendall multi-task) | −0.067, p<0.001 | #423 | 🟢 |
| 7.32 | PEFT lora λ=0/0.1: 0.580 → 0.571 (−0.010) | even from lower base, V hurts | #432 | 🟡 |
| 7.33 | PEFT IA3 λ=0/0.1: 0.465 → 0.448 (−0.016) | weakest of 3 PEFT variants | #432 | 🟡 |
| 7.34 | Cross-arch ensembling (mix d4/d6/d8/d10) | within-arch x-seed = 0.6798 ≈ cross-arch 0.6791 (n.s.) | R6-XARCH-ENS | 🔴 |
| 7.35 | Path B: V-axis ckpts HURT 10-ckpt vanilla ensemble | +topo_15 −0.0145, all_25 −0.0193 (p=0.000) | sota_ensemble_extension.json (#446) | 🟢 |

### Component ablation — saturation transition
| # | Recipe | Vanilla | + V-axis | Δ | Source | Tier |
|---|---|---|---|---|---|---|
| 7.36 | EMOD d6 + LS (weak base) | 0.6235 | 0.6256 (Topo) / 0.6301 (EMODSTYLE λ=0.5) | +0.002 / +0.007 | #438, #424 | 🟡 |
| 7.37 | EMOD d6 + LS + KD + aug (full SOTA recipe) | 0.6581 | 0.6432 (Topo) / 0.6346 (EMODSTYLE) | −0.015 / −0.024 | sota_recipe_vaxis_runs (#447, e100 partial) | 🟢 (saturation cliff) |
| 7.38 | CBraMod baseline (very weak) | 0.5717 | 0.5777 (Topo s42, n=1) | +0.006 (single seed only) | partial #454 | 🟡 |

### Per-subject ensemble selection (all NULL except oracle)
| # | Method | K=3/5/7/10 | Source | Tier |
|---|---|---|---|---|
| 7.39 | V1 global top-K val | 0.680 / 0.685 / 0.687 / 0.6948 | per_subject_ensemble.json | 🟡 |
| 7.40 | V2 per-val majority vote | 0.680 / 0.678 / 0.687 / 0.6948 | per_subject_ensemble.json | 🟡 |
| 7.41 | V3 TTA label-free | 0.682 / 0.683 / 0.687 / 0.6948 | per_subject_ensemble.json | 🟡 |
| 7.42 | ORACLE per-test (cheating) | 0.6981 / 0.6994 / 0.7006 / 0.6948 | per_subject_ensemble.json | 🔴 (oracle headroom small) |

**Total V-axis-as-supervision interventions tested: ~25** (frontal/FAA/occ/topo/Procrustes × 4 λ; EMODSTYLE 2 modes × 5 λ; PEFT 3 variants × 2 λ; RSA 5 λ; Distance-CE 4 τ; Multi-V 3 λ; EEG-AUX 4 λ; KD 6 configs; init 3; pretrain-FT 3 modes; XEEG 2 modes × 2 λ; SCALING 4 fractions × 2 λ; SmallLam 5; Uncert 1; Distill 1; Prior 2; XARCH-ENS 1; INFONCE 2; Curriculum 3 schedules).

---

## §8 EEG SOTA — Principled Ensembling

### Ablation cascade (10 rows)
| # | Step | BACC | Source | Tier |
|---|---|---|---|---|
| 8.1 | CBraMod (ICLR'25 prior SOTA) | 0.572 | external | 🟢 |
| 8.2 | EmotionKD (ACMMM'23) | 0.628 | external | 🟢 |
| 8.3 | EMOD AAAI'26 paper | 0.6287 | external | 🟢 |
| 8.4 | EMOD vanilla replication (d3, race-fixed) | 0.6194 ± 0.004 | cycle 31 (job 46633766) | 🟢 |
| 8.5 | + aug | 0.6343 ± 0.004 | cycle 31 | 🟢 |
| 8.6 | + KD only | 0.6215 ± 0.011 (n.s.) | cycle 31 | 🟡 |
| 8.7 | + aug + KD (super-additive) | 0.6439 ± 0.007 | cycle 31 (p=0.0003 vs replication) | 🟢 |
| 8.8 | + rand9 9D KD (LLM-content-irrelevant) | 0.6467 ± 0.007 | cycle 72j Task #266 | 🟢 |
| 8.9 | **+ d6 depth doubling** | **0.6581 ± 0.0066** | cycle 73f (job 46665722) | 🟢 |
| 8.10 | + e150 longer training (single mean) | 0.6581 ± 0.010 (TIE in mean; diversity benefit only) | cycle 73f | 🟢 |
| 8.11 | 5-ckpt e100 ensemble | 0.6798 (+0.022) | cycle 73i (ensemble_d6_test.py) | 🟢 |
| 8.12 | **10-ckpt mixed e100+e150 ensemble** | **0.6948** (+0.037) | cycle 73j (ensemble_d6_d6e150_results.json) | 🟢 (FINAL ENSEMBLE SOTA) |
| 8.13 | **Single-checkpoint val-selected SOTA** | **0.6755** (vanilla d6_e150 seed 789) | best_single_ckpt.json (#448) | 🟢 (SINGLE-MODEL SOTA) |
| 8.14 | val→test rank correlation across 25 ckpts | Spearman 0.825 | #448 | 🟡 |

### Mega-ensemble null
| # | Finding | Numbers | Source | Tier |
|---|---|---|---|---|
| 8.15 | Adding d8 + d6_llm to 10-ckpt: 15/20/25 models all hit BELOW 0.6948 | only e100+e150 split is useful diversity axis | cycle 73k (em_mega) | 🟡 |
| 8.16 | LOGO on Run C: removing e100 group costs −0.012, removing e150 group costs −0.003 (asymmetric) | e150 carries unique diversity | cycle 73j | 🟡 |

### Mechanism for ensemble (ties to §5)
| # | Finding | Numbers | Source | Tier |
|---|---|---|---|---|
| 8.17 | Two-tier theory: Tier 1 universal basin (free), Tier 2 within-class V-axis residual (where averaging cancels noise) | per-checkpoint within-resid \|r\| ↔ LOO contribution r=+0.743, p=0.014 | sota_ensemble_theory.md (#449) | 🟢 |
| 8.18 | 100ep vs 150ep have IDENTICAL mean BACC (0.6581 each) | ensemble gain is NOT from accuracy difference | cycle 73dd Task #318 | 🟢 |
| 8.19 | Cross-group disagreement 13.1% on test; mixed gain on disagreement = +10.3pp | quantitative test of mechanism (#317) | cycle 73ee | 🟢 |
| 8.20 | Cohen kappa: within-100ep 0.694, within-150ep 0.679, cross-group 0.702 | 150ep slightly more diverse internally | #317 | 🟡 |
| 8.21 | 150ep alone ensemble 0.6919 (+0.0338) — 1.5× bigger gain than 100ep alone (+0.0218) | longer training → more diverse checkpoints | #317 | 🟡 |

### Ensemble gain across datasets/modalities (Paper 2 finding)
| # | Dataset | Individual mean | Ensemble | Gain | Tier |
|---|---|---|---|---|---|
| 8.22 | FACED 9c (EEG, d6) | 0.6581 | 0.6948 | +0.037 | 🟢 |
| 8.23 | SEED-V 5c (EEG, d6) | 0.3743 | 0.4083 | +0.034 | 🟡 |
| 8.24 | CIFAR-10 (small CNN) | 0.9015 | 0.9253 | +0.024 | 🟡 |
| 8.25 | MNIST MLP | 0.9849 | 0.9863 | +0.001 (saturated) | 🟡 |
| 8.26 | CIFAR-100 (pending) | — | — | — | ⚪ |
| 8.27 | Fashion-MNIST (pending) | — | — | — | ⚪ |
| 8.28 | Scaling law: gain ∝ (1 - individual accuracy) | empirical from 4 datasets above | cycle 73gg | 🟡 |

### Compute-optimal law (PIVOT 2)
| # | Finding | Numbers | Source | Tier |
|---|---|---|---|---|
| 8.29 | Law: gain(K,H,E) = α·H^β·(1−exp(−K/k₀))·(1+γ·log(E/E₀)) | β=0.81 (matches independent fit β=0.85); R²=0.683 train, 0.540 LOO-CV across 25 tasks | p2_scaling_law_fit.json (#392) | 🟡 (workshop / appendix) |
| 8.30 | K=5 captures 93% of K→∞ variance reduction | practical "5 seeds is enough" rule | #392 | 🟡 |
| 8.31 | Compute-optimal K* = 5 at most budgets; 6 at C=5000 | crisp 1-line rule for practitioners | #392 | 🟡 |

### TrajLenEns mechanism debunk
| # | Finding | Numbers | Source | Tier |
|---|---|---|---|---|
| 8.32 | Same-seed cross-epoch pairs: H1 disagreement REJECTED (less diverse, p=0.0016, d=−4.92) | TrajLenEns "diversity recipe" debunked | p2_mech_a_disagreement.json (#382) | 🔴 |
| 8.33 | Canonical pairing CKA 0.92 (most aligned of all pair types) | confirms not a special diversity source | p2_mech_b_cka.json | 🔴 |
| 8.34 | LMC: zero loss barrier between endpoints, midpoint EXCEEDS for 2/5 seeds | same basin | p2_mech_e_interp | 🔴 |
| 8.35 | Per-pair canonical TrajLenEns gain = +0.009 (WORST of 4 pairing schemes) | cross-seed same-epoch +0.014; cross-epoch cross-seed +0.018 | p2_mech_f_canonical_pair | 🔴 |
| 8.36 | "+0.06" headline = +0.012 longer training + +0.003 ensemble scaling + noise | mechanistic decomposition | #382 synthesis | 🔴 (paper2 narrative reset) |

### TrajLenEns failure boundary
| # | Tasks where mixing helps (>+0.005 over best same-length) | CoLA, QQP-10k, AG-News, Higgs, DermaMNIST, FACED EEG | various | 🟡 |
|---|---|---|---|---|
| 8.37 | Tasks where mixing hurts | ESC-50 (−0.0075, with 1:3 ratio −0.0375), Covtype (−0.0072) | #386 | 🟡 |
| 8.38 | Tasks where mixing is null (~0.000) | RTE 2.5k, MRPC, SST-2 1k/10k, Adult, Optdigits, AG-News, DermaMNIST, MNIST | #386 | 🟡 |
| 8.39 | Practical recipe: T_A:T_B within 2:3, pre-check single-length parity, skip if dominated | calibration tool, not universal accuracy boost | #386 | 🟡 |

### "Illusion of diversity" (paper-2 absorbed pivot)
| # | Modality | Mixed gain over best same-length | Source | Tier |
|---|---|---|---|---|
| 8.40 | FACED EEG | +0.0029 | illusion_of_diversity_full_draft.md | 🔴 |
| 8.41 | AG-News | +0.0003 | (#393) | 🔴 |
| 8.42 | DermaMNIST | +0.0000 | | 🔴 |
| 8.43 | CIFAR-10 | +0.0009 | | 🔴 |
| 8.44 | All hover at noise floor — 0/15 tasks gain >0.002 across all of FAIL-MAP | universal pattern | | 🔴 |

### DAGE (Disagreement-Aware Greedy Ensembling)
| # | Finding | Numbers | Source | Tier |
|---|---|---|---|---|
| 8.45 | DAGE marginal beats canonical TrajLenEns (+0.001-0.005); ties random selection from same pool | "what matters is having a good pool" | #391 | 🟡 |
| 8.46 | Headroom-dependent benefit | CIFAR-10 (H=0.04) tied; DermaMNIST (H=0.21) +0.005-0.010 | #391 | 🟡 |

### FGE Bezier
| # | Finding | Numbers | Source | Tier |
|---|---|---|---|---|
| 8.47 | FGE midpoints lose to TrajLenEns | FGE BACC 0.6587 vs TrajLenEns 0.6948 (−4 pt) | cycle 75 (#380) | 🔴 |

---

## Cross-cutting / methodological

### Quality-invariance (KD content-irrelevance)
| # | Finding | Numbers | Source | Tier |
|---|---|---|---|---|
| C.1 | rand9 9D ≈ LLM 9D ≈ V-A annotation 9D ≈ 2-class 2D (at LS=0.1) | 0.6196 vs 0.6194 vs 0.6173 vs 0.6150 (all p>0.16) | cycle 72j Task #266, cycle 73c | 🟢 |
| C.2 | Across 10 teacher variants \|PC1-val\|=0.19-0.97: BACC varies by 0.009 only | shuffle_4 = 0.6266 = text 0.6263 baseline | cycle 28 #239 | 🟢 |
| C.3 | At LS=0.3 only: 2class < LLM by Δ=+0.010 p=0.007 (gap exists at high regularization) | 9D dim matters; provenance doesn't | cycle 72h | 🟡 |

### Concept transfer matrix
| # | Finding | Numbers | Source | Tier |
|---|---|---|---|---|
| C.4 | 20×20 concept transfer matrix shows neighborhoods | r6_concept_transfer_matrix.json | 🟡 |

### Cross-architecture probe (methodology)
| # | Finding | Numbers | Source | Tier |
|---|---|---|---|---|
| C.5 | Layer-sweep framework across 6+ LLM families + dense+MoE | r6_xarch_layer_synthesis.md | 🟡 |
| C.6 | Encoder-LMs (BERT/RoBERTa) peak at middle (frac=0.67); causal LMs peak at end (1.00); Gemma-4 at L1 (0.03) | family-specific architectural fingerprints | r6_xarch | 🟡 |

### Cross-dataset (KD) transferability 
| # | Finding | Numbers | Source | Tier |
|---|---|---|---|---|
| C.7 | Cross-backbone KD: CBraMod +5.5% (p=8e-6***), LaBraM +2.6% (p=0.025*) | confirms recipe transfers across backbones | Session 21 (cycles ≤21) | 🟡 |
| C.8 | Cross-dataset KD: SEED-V 5s CBraMod +0.83% (CI excludes 0), LaBraM 19ch×5s +1.85% (p=0.037*) | partial transfer | Session 21 | 🟡 |
| C.9 | EMOD on SEED-V (d6 vs d3): tied 0.3743 vs 0.3744 (no transfer of d6 gain) | architecture-specific | cycle 73aa Task #282 | 🟡 |
| C.10 | EMOD recipe TRANSFERS to PhysioNet motor imagery: KD positive, aug null | KD generalizes | cycle 56 | 🟡 |
| C.11 | Mumtaz/MA replication: aug transfers to MA, KD does not help binary | binary-class limit | cycle 44 #252 | 🟡 |

### LLM scale finding (sub-finding)
| # | Finding | Numbers | Source | Tier |
|---|---|---|---|---|
| C.12 | Inverted-U: 1.5B optimal, 32B WORST, SFT hurts | feedback_llm_scale.md | 🟡 |

### Token-length insight (KD requirement)
| # | Finding | Numbers | Source | Tier |
|---|---|---|---|---|
| C.13 | Extensions need ≥60 tokens; 20 tokens too few for adapters/KD | feedback_token_length.md | 🟡 |

---

## Negative findings worth reporting (Discussion / appendix)

### LLM-as-EEG-supervision (Cycle 74 OT findings)
| # | Finding | Numbers | Source | Tier |
|---|---|---|---|---|
| N.1 | LLM emotion vectors DON'T transfer to EEG | KD is architectural regularization only (content-irrelevant, p>0.68) | project_ot_findings.md | 🔴 |
| N.2 | Ceiling ~0.66 single, ~0.68 ensemble before our SOTA recipe | OT direction wrapped up cycle 74 | | 🔴 |

### Architecture experiments (Session 15)
| # | Finding | Numbers | Source | Tier |
|---|---|---|---|---|
| N.3 | Adapter64 (frozen backbone) ties full-FT at 0.6276 | best PEFT config; r=128 overfits | cycle 5 cluster | 🟡 |
| N.4 | LoRA shows NO scaling with rank (flat 0.619 at r=4/8/16) | adapter > LoRA for this task | cycle 5 | 🟡 |
| N.5 | Cross-attention readout COLLAPSES (0.197) | architecturally incompatible with backbone output | cycle 5 | 🔴 |
| N.6 | Depth reduction fails (d8: 0.603, d6: 0.593) | confirms deep layers needed | cycle 5 | 🟡 |
| N.7 | CBraMod depth doubling (12→24) FAILS (0.6148-0.6192 < 0.6249) | EMOD's progressive stacking works because d=3 is artificially shallow | cycle 73a | 🟡 |
| N.8 | All Stage 3 ceiling-break methods (SWA, EMA, Lookahead, snapshot) TIE on CBraMod | confirms student-capacity ceiling | cycles 72b-72f | 🟡 |
| N.9 | All Stage 4 augmentation methods (TrivialAug, RandAug, cutoff_time) TIE on CBraMod | | cycle 72f | 🟡 |
| N.10 | SAM/F-SAM BROKE (loss stuck at ln(9)+0.3) | abandoned for both backbones | cycle 72e | ⚪ |

### EEG-MAE
| # | Finding | Numbers | Source | Tier |
|---|---|---|---|---|
| N.11 | EEG-MAE lower than EMOD baseline | superseded line | line1_eegmae_faced_finetuning.md | ⚪ |

### Linguistic experiments (lower priority)
| # | Finding | Numbers | Source | Tier |
|---|---|---|---|---|
| N.12 | Mumtaz binary EEG fails to replicate | cycles 39-41 | 🔴 |
| N.13 | MA (Mental Arithmetic) replicates with both classifier heads | cycle 41-42 | 🟡 |

### Aug ablation (Sessions 1-2)
| # | Finding | Numbers | Source | Tier |
|---|---|---|---|---|
| N.14 | Temporal jitter is the ONLY critical augmentation | no_jitter: −3.9%; only_jitter ≈ baseline | aug_ablation cycle 1-2 | 🟡 |

### SoftLab / mechanism experiments
| # | Finding | Numbers | Source | Tier |
|---|---|---|---|---|
| N.15 | Label-smoothing variants (Zipf, CP, CALS, OLS) all TIE LS=0.3 baseline (0.6055-0.6105) | LS saturates around 0.3 | cycle 72b Task #260, 264 | 🟡 |
| N.16 | tfkd best Stage-1 result (0.6172, +0.009 vs LS=0.3, p=0.11 marginal) | borderline, didn't survive | cycle 72b | ⚪ |
| N.17 | Concept-Bottleneck: NEGATIVE (terrible) | cycle 17 #245 | 🔴 |
| N.18 | Graph Adapter: NEGATIVE | cycle 17 | 🔴 |
| N.19 | TTA: PROPER LOSO ZERO EFFECT | cycle 17 #244 | ⚪ |
| N.20 | LOSO mixup: +1.60% positive (all folds) | cycle 17 | 🟡 |

### Visual / cross-modal
| # | Finding | Numbers | Source | Tier |
|---|---|---|---|---|
| N.21 | Vision-from-LLM-vector mixup: NEGATIVE | cycle 13/14 | ⚪ |
| N.22 | Q3.5 vision (tiered): success after Gemma-4 processor fix | cycle 15 | 🟡 |
| N.23 | Llama-4-Scout vision V-axis: depth_67 r=0.776, depth_29 r=0.470 (cached) | cycle 75 (P5b-LATEST-LLMs) | 🟡 |

### Session-level baselines that no longer carry weight
| # | Finding | Notes |
|---|---|---|
| N.24 | Many cycle 17 manifold/CAA/PCA/round-trip editing experiments | superseded by V-axis frame |
| N.25 | Fisher-ratio narrative (cycle 5/6) | wrong-frame; superseded by quality-invariance |

---

## Methodological tools we built

| # | Tool | Description | Source | Tier |
|---|---|---|---|---|
| M.1 | Concept-library framework (#394) | 9-shot per-concept extraction at any LLM final layer; AUC + cross-concept transfer matrix | r6_concept_library.py | 🟢 (paper §3 instrument) |
| M.2 | Cross-architecture probe (#396) | Layer-sweep across 6+ families dense+MoE | p1_r6_xarch_synthesis.py | 🟡 |
| M.3 | DAGE algorithm (#391) | Disagreement-Aware Greedy Ensembling | dage_*.py | 🟡 (workshop) |
| M.4 | Compute-optimal law fit (#392) | 5-param HbKE; LOO-CV R²=0.54 across 25 tasks | p2_scaling_law_fit.json | 🟡 (appendix) |
| M.5 | Headline-numbers verification doc | every claim → JSON → cycle | headline_numbers.md | 🟢 |
| M.6 | Topography pipeline | Per-channel × per-band V-axis correlation + MNE topomaps + 9-emotion grids | topography/run_topography.py | 🟢 |
| M.7 | Trainer extensions for V-axis variants | unified `trainer_specialized_vaxis.py` with --variant {topo,frontal,occ,faa,procrustes}, --peft_mode, --vaxis_schedule | EMOD/trainer_specialized_vaxis.py | 🟡 |
| M.8 | Aggregator chain pattern | per-experiment slurm + aggregator dependency wired for auto-synthesis | various .sh + aggregate_*.py | 🟡 |
| M.9 | Reference-audit doc | 86 unique refs verified; 3 hallucinations flagged | PAPER_REFERENCES_AUDITED.md (#439) | 🟢 (must use for bib) |

---

## Appendix-only / supplementary

| # | Item | Tier |
|---|---|---|
| A.1 | Full 25-row V-axis intervention table with seeds and JSONs | 🟡 |
| A.2 | All 18-LLM agreement matrix and per-model brain anchors (heatmap) | 🟡 |
| A.3 | Per-emotion topographic maps (9×5 grid: emotions × bands) | 🟡 |
| A.4 | Confusion matrix on FACED test (1932 trials) for 0.6755 single + 0.6948 ensemble | 🟡 |
| A.5 | Reproducibility manifest: per-seed, per-job, per-checkpoint paths | 🟡 |
| A.6 | Composition validation natural-text tables (GoEmotions, SST-5, Yelp) | 🟡 |
| A.7 | TrajLenEns mechanism battery (5 hypotheses tested) | 🟡 |
| A.8 | n-shot ablation full table (n=1,3,5,9,15,25,50) | 🟡 |
| A.9 | Layer-sweep curves for 3 LLM families (Qwen/Pythia/Bloom) | 🟡 |
| A.10 | CIFAR-10 / MNIST / SEED-V ensemble-trick replication tables | 🟡 |

---

## Skip (superseded / noisy / off-narrative)

| # | Item | Reason |
|---|---|---|
| S.1 | StimAgg ceiling (BACC=1.0) | Leaky by construction (28-stim → 9-class memorization); not a finding |
| S.2 | "Linear" V-axis prior (#418) | Label leakage through stim_id back-door; only "smooth" variant honest |
| S.3 | INFONCE protocol (#417) | Broken contrastive-only protocol; not interpretable absolute numbers |
| S.4 | Fisher-ratio analysis (cycle 5/6) | Wrong frame; teacher-quality irrelevant per qspec |
| S.5 | EEG-MAE entire line | Lower than EMOD; superseded |
| S.6 | Many cycle 17 PEFT/manifold experiments | Superseded by V-axis frame |
| S.7 | OPT-1.3b (torch.load CVE) | Couldn't run; not blocking |
| S.8 | Phi-3-mini (config compat issue) | Couldn't load; 5 LLM families already enough |
| S.9 | Financial Phrasebank (HF deprecated) | Couldn't load; 5+ benchmarks already |
| S.10 | TTA per-subject (#450) | Agent died mid-run; §3 already complete without it |
| S.11 | Full FGE Bezier path (#380) | Confirmed FGE midpoints lose; doesn't beat ensemble |
| S.12 | adapter64 cycle 17 follow-ups (unfreeze, larger r) | Optimum locked at r=64 |

---

## Open questions / NOT in narrative.md but worth flagging

| # | Question | Why important | Status |
|---|---|---|---|
| Q.1 | Does the saturation transition shift with new architectures (CBraMod 0.572 → ours 0.66)? | Locates threshold positively, not just by failure | #453/#454 component ablation in flight |
| Q.2 | Per-subject head GPU experiment (#442): can model learn subject-clusters that generalize? | Closes the per-subject Simpson's loop with a positive | HELD pending Round 11 |
| Q.3 | EMODSTYLE class-mode at 5+ seeds with stronger λ search | The single seed s2025=0.6416 was outlier; final 5-seed showed −0.010. Was there a sweet spot we missed? | Closed as #16 negative |
| Q.4 | Can per-subject V-axis adaptation transfer the ceiling gap (0.6948 → 0.7006)? | Oracle reaches 0.7006; clean methods don't | NULL closed |
| Q.5 | Why does cross-arch r=0.885 sit at 93rd percentile of null directions, not >99th? | 9-class PC1 is low-dim → wide null distribution | Honest in §4 |
| Q.6 | Does V-axis fail at toxicity because the concept is more distributed, or because Qwen-generated toxic stories are too mild? | toxicity AUC=0.59 | Open caveat |

---

## Cross-cutting numbers worth memorizing

| Comparison | Δ | Source |
|---|---|---|
| 0.6948 ensemble vs CBraMod 0.572 | **+0.123 (+21.5% rel)** | #452 cascade |
| 0.6948 vs EmotionKD 0.628 | +0.067 (+10.6%) | external |
| 0.6755 single val-selected vs prior single SOTA 0.6581 | +0.017 (+2.6%) | #448 |
| EEG-LLM cohort r vs random control | 0.87 vs 0.07, p<10⁻⁹ | #397 |
| Cross-arch BACC vs V-axis r (n=36) | r=+0.885, p=8e-13 | #429 |
| Within-class residual ↔ ensemble contribution | r=+0.743, p=0.014 | #449 |
| Anger drop-class effect | −0.151 (32% of total) | #440 |
| Posterior > frontal V-axis \|r\| | 0.21 vs 0.16 | #430 |
| Frontal-mask λ=0.5 hurts | Δ=−0.052, p=0.0015 | #434 |
| Anger-weighted λ=0.5 hurts | Δ=−0.054, p=0.0003 (counter-intuitive — analytical ceiling +0.24!) | #443 |
| RSA λ=5 monotonic destruction | −0.093 | #414 |
| Distance-CE τ=5 destruction | −0.397 (chance) | #415 |

---

## Section mapping summary

- **§1 (Intro)**: rows 1.1-1.5
- **§3 (V-axis in LLMs)**: rows 3.0-3.42
- **§4 (V-axis in brain)**: rows 4.1-4.13
- **§5 (Cross-arch convergence)**: rows 5.1-5.11
- **§6 (Brain topography)**: rows 6.1-6.20
- **§7 (Saturation theorem)**: rows 7.1-7.42
- **§8 (SOTA + ensembling)**: rows 8.1-8.47
- **Cross-cutting / methodology**: C.1-C.13, M.1-M.9
- **Discussion / negative findings**: N.1-N.25
- **Appendix**: A.1-A.10

**Total catalogued findings**: ~190 distinct rows across §1-§8, cross-cutting, methodological, negatives, appendix, and skip lists.
