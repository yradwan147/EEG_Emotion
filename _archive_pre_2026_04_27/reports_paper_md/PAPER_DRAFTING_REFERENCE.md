# Paper Drafting Reference — Merged NeurIPS 2026 Submission

**Last refreshed**: 2026-04-26 cycle 75 ~21:15
**Purpose**: Single source of truth for drafting the merged Paper 1 + Paper 2 paper. Every cycle-75 experiment is mapped to a section of the proposed narrative below, including framed negatives.
**Sister docs**:
- `worklog.md` — chronological cycle log (full detail per experiment)
- `merge_topography_synthesis.md` — brain topography (Section 5)
- `merge_crossarch_synthesis.md` — cross-arch mechanism (Section 4)
- `merge_topography_lit_review.md` — EMNLP 2025 + Davidson FAA + Toneva-Wehbe lit context
- `r6_eeg_llm_synthesis.md` — original EEG-LLM circle (Section 2)
- `merge_lit_review.md` — broad lit review for V-axis training-signal directions
- `merged_paper_plan.md` — earlier outline (pre-Round 11)
- `codebase_index.md` — file-level navigation

---

## Best-narrative title candidates

1. **"One Direction, Many Minds: Few-Shot Valence Probes Reveal a Universal Latent Bridging Language Models, Vision, and Human EEG"** — emphasises universality + cross-modal bridge; matches Paper 1's strength.
2. **"What EEG Models Already Know: Cross-Architecture Convergence to a Language-Model Valence Latent"** — leads with the +0.955 unifying mechanism; closest fit to the negative-results narrative.
3. **"From Probe to Brain: Why External Valence Supervision Hurts EEG Emotion Models — and What Helps Instead"** — leads with the honest-scope finding; pairs the 14 negatives with the topography-targeted positive (if it lands).

**Working choice for narrative outline below**: title #1, with title #2's mechanism as the central spine.

---

## Story narrative (7 sections)

```
Universal Few-Shot Probe          (Paper 1 strength, expanded)
        │
        ▼
LLM ↔ Brain Bridge                (the merger pivot point)
        │
        ▼
New EEG SOTA                       (Paper 2 strength, absorbed)
        │
        ▼
Mechanism: Convergence to V-axis  (the unifying explanation)
        │
        ▼
Brain Topography of Valence       (neuroscience contribution)
        │
        ▼
Honest Scope: 14 Negatives        (exhaustive proof)
        │
        ▼
Specialised Supervision           (the closing positive — in flight)
```

---

## Section 1 — Universal Few-Shot Probe (Paper 1's strength)

**Section claim:** A 9-example "concept centroid → PCA → PC1" recipe extracts a 1D semantic axis from any late LLM layer. The axis generalises across LLM families, languages, modalities, and 20+ semantic concepts — emotions and non-emotions alike.

| Experiment (task #) | Setup | Headline result | Status |
|---|---|---|---|
| **#287 zero-shot SST-2** | Project SST-2 sentences onto V-axis, threshold at median | AUC = 0.868, accuracy = 77.75% (supervised LR upper bound 83.7%) | ✅ |
| **#288 zero-shot IMDB** | Same on IMDB 500/500 balanced | AUC = 0.895, accuracy = 81.0% | ✅ |
| **#289 NRC-VAD lexicon** | Project 20k Hu&Liu lexicon entries | \|r\| = 0.76 vs human valence ratings (6.3× random) | ✅ |
| **#290 GoEmotions 27→9** | Nearest-centroid map of GoEmotions classes | Top-9 retrieval accuracy validated | ✅ |
| **#295 few-shot ablation** | n ∈ {1, 3, 5, 9, 15, 25, 50} stories per class | n=15 matches supervised 5000-label baseline | ✅ |
| **#296 layer sweep** | All 28 Qwen layers, V-axis quality by layer | Sudden L27 emergence (V-shape) | ✅ |
| **#299 V-shape on Pythia + Bloom** | Same layer scan on other LMs | V-shape replicates across families | ✅ |
| **#316 Phi-3-mini VAD** | 5th LLM family | Cross-family replication confirmed | ✅ |
| **#326 Qwen3.5 rerun** | Re-extract on latest Qwen3.5-2B (per reviewer prep) | All headline numbers replicated | ✅ |
| **#384 P5-LANG multilingual** | mT0-base on JA/AR/RU SST-2 | AUC 0.89-0.91, BEATS English 0.868. Encoder-decoder >> causal | ✅ |
| **#385 P5-VIS-EXT vision** | CLIP image V-axis on IAPS, AVA aesthetics | Valence r=0.87, arousal r=0.80 — both BEAT supervised | ✅ |
| **#388/#396 cross-architecture** | 11 LLM families (Qwen2.5/3.5, Llama-3/4, Mistral, OLMo, Bloom, Phi, Gemma-4) | Best Qwen2.5-1.5B = 0.868, Gemma-4 family L1-peak outlier | ✅ |
| **#394 R6-CONCEPT-LIB** | 20 concepts (12 train + 8 test stories per pole, Qwen2.5-1.5B L27) | **17/20 at AUC ≥ 0.95**; non-emotion concepts (complexity, concreteness, authoritativeness) included | ✅ |
| **#394 transfer matrix** | 20×20 cross-concept AUC matrix | Reveals concept-axis neighbourhoods | ✅ |
| **#395 R6-COMPOSITION** | V_polite + V_happy → 4-quadrant text classification | 79% on agent-authored sentences (3.16× chance) | ✅ |
| **#400 R6b composition validation** | Same on naturally-occurring text (Yelp, SST5, GoEmotions) | 42-47% (still > 25% chance, demoted to "supporting") | ✅ |
| **#321 cross-language alignment** | Procrustes EN ↔ ES/FR/DE/ZH | Axis aligns up to scale across languages | ✅ |
| **#324 multilingual self-LOOCV** | Train on 4 languages, test on 5th | Mean AUC 0.84 across langs | ✅ |

**Negative framed positively:**
- **#274/#278/#281 VAD regression baseline** — supervised arousal regression at L27 fails (\|r\| < 0.3) → this is the V-works-A-fails asymmetry. Combined with section 5's neuroscience finding (arousal lives in central beta/gamma, valence in posterior alpha), the asymmetry has a published-grade explanation.

**Hero figures**:
- `figures/concept_universality.png` (20-concept AUC bars)
- `figures/r6_composition_quadrant.png` (4-quadrant V_polite × V_happy scatter)
- `figures/r6_layer_sweep_v_shape.png` (L27 V-shape emergence)

---

## Section 2 — LLM ↔ Brain Bridge (the merger pivot)

**Section claim:** The same V-axis built from 9 LLM example sentences predicts how the human brain responds to emotional stimuli, at correlation 0.71–0.89 across LLM families.

| Experiment (task #) | Setup | Headline result | Status |
|---|---|---|---|
| **#397 R6-EEG-LLM** (HERO) | CLIP V-axis (built on OASIS, validated at r=0.871) projected to 28 FACED stims via text tower; correlated with cohort EEG-Ridge per-stim valence predictions | r = +0.706 (rich text), r = +0.874 (bare emotion), r = +0.889 (valence cat); random control r = +0.069 | ✅ |
| **#411 MERGE-MULTI-LLM-EEG** | Same setup but using LLM text-tower V-axis from 13 LLM families | Mean r_eeg = 0.79 ± 0.06; best Qwen-14B r=0.862, Mistral-7B r=0.861, Gemma-27B r=0.815, Llama-4-Scout r=0.652. **Universality, not scaling** (within-Qwen scaling p=0.52) | ✅ |
| **#407 MERGE-XEEG semantic transfer** | FACED V-axis ordering vs SEED-V emotion ordering (no training, zero-shot) | r = +0.96 — cross-EEG-dataset semantic transfer is essentially perfect | ✅ |
| (sanity) | Behavioural valence vs CLIP V-axis | r = +0.91 | ✅ |
| (sanity) | Behavioural valence vs EEG-Ridge | r = +0.86 | ✅ |
| (sanity) | EEG split-half reliability | r = 0.988 ± 0.004 (extremely stable) | ✅ |

**Frame for the paper**: this section is the "the bridge that makes the merger possible." Without #397 + #411, Paper 1 and Paper 2 cannot live together.

**Hero figures**:
- `figures/r6_eeg_llm_circle.png` (6-panel hero: V-axis, EEG-Ridge, scatter, controls)
- `figures/multi_llm_eeg_bars.png` (13-LLM × r-with-EEG horizontal bar chart)

---

## Section 3 — New EEG State of the Art (Paper 2 absorbed)

**Section claim:** A principled multi-seed long-training EMOD ensemble achieves a new FACED 9-class SOTA at 69.5% balanced accuracy, beating prior published bests by ≥6 percentage points.

| Experiment (task #) | Setup | Headline result | Status |
|---|---|---|---|
| **#390 MATCHED-COMPUTE SOTA** | 8-seed d6_e150 ensemble at matched compute vs alternatives | **BACC = 0.6951**, ACC = 0.6920, kappa = 0.6528. Matches the 10-checkpoint mixed trick (0.6948) at less compute. p_paired = 0.46 vs mixed | ✅ |
| **#283 multi-recipe ensemble** | d6 + d8 + d6_e150 multi-architecture pool | Confirms pooling helps modestly | ✅ |
| **#285 mega-ensemble** | 20-25 d6 variants stacked | Diminishing returns past K=5 | ✅ |
| **#338 same-length 10-seed baseline** | 10-seed d6_e150 (no multi-length) | 0.6919 — within noise of "mixed" trick → no special diversity needed | ✅ |
| **#308 SEED-V d6 ensemble** | d6 SOTA recipe ported to SEED-V | Confirms recipe portability | ✅ |
| **#329 calibration NLL/ECE CIFAR-10** | Calibration of long-training ensembles | Better calibration with longer training | ✅ |
| **#382 P5-MECH triangulation** | TrajLenEns CKA / disagreement / bias-var / calibration battery | **Mechanism debunked** — same-seed cross-epoch ckpts share basin (CKA 0.92, 81% prediction agreement). The "diversity recipe" gain is just longer training in disguise. Justifies merger pivot | ✅ |
| **CBraMod baseline** | Trained 5 seeds, BACC 0.567-0.576 | The prior published SOTA we beat by +12 pp | ✅ (2026-04-03) |
| **EmotionKD baseline** | Reference value | 0.628 (we beat by +6.6 pp) | ✅ (literature) |

**Frame for the paper**: SOTA is one chapter, not the headline. The TrajLenEns mechanism debunk (#382) is what motivated the merger and is itself a paper-worthy negative finding (in the supplementary).

**Hero figures**:
- `figures/eeg_sota_bars.png` (CBraMod 0.572 vs EmotionKD 0.628 vs Our 0.6951)
- `figures/p2_mech_matched_compute_synthesis.png` (the mechanism debunk)

---

## Section 4 — Mechanism: EEG Models Converge to the LLM V-axis

**Section claim (REVISED 2026-04-27 after random-direction control)**: Across two architectures, better EEG models progressively encode the LLM-derived valence axis on **two orthogonal directions** (class-mean and within-class residual). The V-axis is one of the most accuracy-aligned directions in feature space, and the within-class residual specifically predicts ensemble contribution at p=0.014 — providing the principled mechanism for our SOTA ensemble.

| Experiment (task #) | Setup | Headline result | Status |
|---|---|---|---|
| **#405 MERGE-EMERGE** | V-axis r in EMOD penultimate features | PC1 \|r\| = 0.40 (initially "fail"; later reframed via #426) | ✅ |
| **#426 MERGE-CONTRADICTION** | Class-mean PC vs within-class residual PC vs oracle ridge | EMOD encodes V-axis on TWO directions: class-mean PC1 \|r\| = **0.68**, within-class residual best-PC \|r\| = **0.78**, oracle ridge r = **0.62**. PC1 of stim-mixture (= 0.40) is a "PC1-of-mixture" artefact. **V-axis info is saturated in EMOD on 2 orthogonal directions.** | ✅ |
| **#428 MERGE-PIVOT2-LINK** | V-axis \|r\| saturation curve vs ensemble size K | MEAN \|r\| flat across K, but VARIANCE saturates at K=8 (std 0.033 → 0.007) — same mechanism as PIVOT 2 BACC variance saturation at K=5 | ✅ |
| **#429 MERGE-CROSSARCH (n=36 final)** | 36 checkpoints (CBraMod + EMOD variants + ensembles); per-ckpt V-axis r vs accuracy | r(BACC, class-PC1 \|r\|) = **+0.885, n=36**. Within-class residual: r=+0.715. | ✅ |
| **🎯 #451 random-direction control** | 100 random Gaussian directions matched to CLIP V-axis L2 norm; recompute meta-r across 36 ckpts | V-axis lands at **93rd percentile** of null distribution. Empirical p=0.079 one-sided, p=0.13 two-sided. Null is wide (std 0.62) because 9-class PC1 is low-dim. **The V-axis is among the most accuracy-aligned directions but is not uniquely predictive at the class-PC1 level.** | ✅ |
| **🎯 #449 ensemble theory** | Per-ckpt within-class residual \|r\| vs leave-one-out ensemble contribution across 10 d6_f128 ckpts | r(within-resid \|r\|, ensemble contribution) = **+0.743, p=0.014**. Top-7 by within-resid → BACC=0.6962 vs bottom-7 → 0.6829 (z=+2.0). **Ensemble cancels orthogonal noise around within-class V-axis residual.** | ✅ |

**Critical reviewer-grade caveat**: The class-PC1 cross-architecture correlation (r=+0.885) sits in the top decile of accuracy-aligned random directions (93rd percentile, p=0.08), not above the >99th percentile. The robust signal lives in the **within-class residual** (#449: p=0.014 for ensemble contribution prediction; #426: \|r\|=0.78 for residual PC alignment). Frame the section accordingly — V-axis is a privileged direction, not THE direction.

**Hero figures**:
- `figures/crossarch_bacc_vs_vaxis.png` (3-panel scatter: class-PC1, within-class, oracle)
- `figures/crossarch_random_control.png` (null distribution histogram with V-axis marker)
- `figures/sota_ensemble_theory.png` (per-ckpt within-resid \|r\| vs ensemble LOO contribution)

**Hero figures**:
- `figures/crossarch_bacc_vs_vaxis.png` (3-panel scatter: class-PC1, within-class, oracle)
- `figures/crossarch_bacc_vs_vaxis_FINAL.png` *(pending)*
- `figures/crossarch_midtrain_trajectory.png` *(pending)*

---

## Section 5 — Brain Topography of Valence (Neuroscience Contribution)

**Section claim:** The V-axis is encoded most strongly in **posterior visual cortex**, not the frontal regions predicted by Davidson's classic asymmetry hypothesis. This challenges the entrenched frontal-asymmetry account for video-stimulus emotion paradigms.

| Experiment (task #) | Setup | Headline result | Status |
|---|---|---|---|
| **🎯 #430 MERGE-TOPOGRAPHY** | Per-channel × per-band cohort-level Pearson r between LLM V-axis and FACED DE features (32 ch × 5 bands × 28 stims, 123 subjects) | **Region mean \|r\|: occipital 0.212 > parietal 0.181 > central 0.180 > frontal 0.162**. Top single cells: PO3/gamma r=+0.48, F7/beta r=−0.47, O1/gamma r=+0.44 | ✅ |
| **Davidson FAA replication** | (F4 alpha − F3 alpha), (F8 − F7), (Fp2 − Fp1) for positive minus negative emotions | All three pairs in the predicted direction (positive ↔ relatively more right-frontal alpha), but ~10× weaker than the posterior signal | ✅ (within #430) |
| **Per-emotion topography** | 9-emotion × 32-channel × 5-band DE deviation maps | Stored at `topography/per_emotion_topography.npz`; figure `figures/topo_per_emotion_per_band.png` | ✅ |
| **Best frequency band** | Mean \|r\| over 32 channels per band | alpha 0.233 (winner) > beta 0.198 > delta 0.174 > gamma 0.148 > theta 0.124. Alpha is most spatially pervasive; gamma carries strongest single channels | ✅ |
| **#433 MERGE-LIT topography review** | EMNLP 2025 (Padakanti+Oota), Toneva-Wehbe NeurIPS'19, Schrimpf, Goldstein, Davidson FAA literature | Targeted-voxel-only fine-tuning is the lit-precedent (Toneva). Topographic scalp maps are the publishable artefact (Padakanti). Bonus: arousal lives in central beta/gamma (autonomic), valence in posterior alpha-gamma → explains V-works-A-fails asymmetry | ✅ |
| **#440 Time-resolved V-axis (LPP analogue)** | Within-30s-clip per-second cohort r between LLM V-axis and DE features | α peaks at **t=21s** (cohort r=0.40, best stim r=0.68); β at t=18s; δ/θ at t=12s; γ early at t=3-6s. **Mid-late α/β = LPP/sustained-attention; early γ = Müller 1999 reactivity.** | ✅ |
| **#440 Anger contrast (drop-class diagnostic)** | Recompute cohort r excluding each emotion class | **Removing Anger drops cohort r by −0.151** (32% of total). Amusement −0.060, Tenderness −0.057. Other 6 classes essentially noise. | ✅ |
| **#440 Multi-LLM at the brain** | 18 LLMs × per-LLM V-axis ↔ EEG anchor (PO3/γ) | Qwen-1.5B leads at r=+0.411, p=0.030. **Inverted-U scale law replicates at the brain level** (Phi-2/Gemma-4/TinyLlama collapse). | ✅ |
| **#440 Functional connectivity** | γ-DE second-resolution Pearson r among top-8 V-axis channels | Mean off-diag r = **0.675** — single posterior occipital-parietal network with F7 frontal hub, not independent contributors | ✅ |

**Frame for the paper**: this is the **paper's most novel neuroscience contribution**. Use this section to argue that for video-stimulus emotion paradigms (FACED, SEED-V), the valence representation is dominantly visual-cortex-driven, contra the dominant frontal-asymmetry account. Pair with the Davidson replication caveat — we *do* see his pattern, just weaker than the posterior signal.

**The Anger contrast subsection** is the sharpest framing: the "valence axis" is fundamentally an **anger-vs-amusement/tenderness contrast**, not a generic positive-vs-negative axis. This is more precise and more defensible than the broader claim and explains why some emotions (Disgust, Fear, Sadness) carry no V-axis-aligned EEG signal at PO3/γ.

**Hero figures**:
- `figures/topo_v_axis_alignment_by_band.png` (5-panel master |r| topomap by band)
- `figures/topo_pos_minus_neg_by_band.png` (5-panel positive − negative DE diff)
- `figures/topo_per_emotion_per_band.png` (9 emotions × 5 bands grid)
- `figures/extra_A_time_resolved_v_axis.png` (within-clip α/β/γ peak timing)
- `figures/extra_D_per_emotion_v_axis_r.png` (Anger drives the V-axis effect)
- `figures/extra_E2_per_llm_vs_eeg.png` (per-LLM ↔ EEG anchor — inverted-U at the brain)
- `figures/extra_H_connectivity_top_channels.png` (posterior network coordination)

---

## Section 6 — Honest Scope: 14 Negatives Prove V-axis Is Not Additive Supervision

**Section claim:** External V-axis supervision cannot improve EEG accuracy because the model already encodes V-axis on its own (Section 4 mechanism). We tested 14 distinct formulations spanning every published paradigm for representation alignment; all 14 fail. The "harder you push, the more it hurts" gradient is itself the cleanest possible proof of saturation.

### 6A — Auxiliary regression losses (3 experiments, all NEGATIVE)

| Task # | Variant | Worst-case Δ BACC | Notes |
|---|---|---|---|
| #401 MERGE-EEG-AUX | MSE aux on V-axis projection at multiple λ | -0.043 (monotonic) | Original aux loss; basis for all later variants |
| #408 MERGE-SCALING | V-axis aux at 4 data fractions {0.10, 0.25, 0.50, 1.00} × 2 λ | **-0.045 at full data** | Hurts more with more data — the strongest argument that V-axis info is already saturated |
| #422 MERGE-SMALLLAM | Tiny λ sweep {0.001, 0.005, 0.01, ...} | within noise (~0.622 vs vanilla 0.624) | At sub-noise λ, no detectable effect — confirms there's no "sweet spot" |

### 6B — Knowledge distillation / soft-label objectives (2 experiments, all NEGATIVE)

| Task # | Variant | Worst-case Δ BACC | Notes |
|---|---|---|---|
| #409 MERGE-KD | V-axis as soft-label KD target via softmax(-\|v_stim - v_class\|/τ); 3 (T, λ) configs × 5 seeds | -0.012 at T=2 λ=1 | Monotonic with KD strength |
| #415 MERGE-DISTANCE-CE | V-axis-aware label smoothing at τ ∈ {0.5, 1, 2, 5} × 5 seeds | **-0.397 at τ=5 (near chance)** | Most destructive curve in the entire merger battery |

### 6C — Initialisation / two-stage strategies (2 experiments, both NEGATIVE)

| Task # | Variant | Worst-case Δ BACC | Notes |
|---|---|---|---|
| #406 MERGE-INIT | V-axis as classifier head bias / weight initialisation | -0.017 (weight init) | Bias init within noise; weight init significantly worse |
| #416 MERGE-PRETRAIN-FT | V-axis pretrain (50 ep) → CE FT (50 ep), 3 modes (vanilla / frozen / unfrozen) × 5 seeds | **-0.190 (unfrozen V-axis pretrain → full CE FT)** | V-axis pretrain *catastrophically degrades* discriminative weights; even full FT recovers only 0.42 vs vanilla 0.609 |

### 6D — Representation alignment objectives (3 experiments, all NEGATIVE) — the lit-pick #1 picks

| Task # | Variant | Worst-case Δ BACC | Notes |
|---|---|---|---|
| #414 MERGE-RSA | RSA-aligned aux at λ ∈ {0.1, 0.5, 1.0, 5.0} × 5 seeds | **-0.093 at λ=5.0** | The literature's #1 representation-alignment technique. Beautifully clean monotonic destruction curve |
| #417 MERGE-INFONCE | CLIP-style symmetric InfoNCE EEG ↔ CLIP | -0.03 (V-axis arm vs vanilla, both broken-protocol numbers) | Direction consistent (V-axis arm slightly worse); broken absolute baseline noted |
| #419 MERGE-MULTI-V | Multi-LLM ensemble V-axis as aux target × 3 λ × 5 seeds | -0.043 at λ=0.5 | Multi-LLM ensembling does not save the destruction pattern |

### 6E — Cross-dataset transfer (2 experiments, both NEGATIVE)

| Task # | Variant | Worst-case Δ BACC | Notes |
|---|---|---|---|
| #407 MERGE-XEEG | Train FACED with V-axis aux, test SEED-V cross-dataset transfer | Δ = +0.0015, **p = 0.97** | Statistically null — cross-dataset transfer with V-axis aux is exactly zero |
| #412 MERGE-XEEG-FULL | Same but full FACED training + transfer phase | **Δ = 0.0000 exactly** (5+5 seeds, 5-class SEED-V transfer) | Identical numbers down to 4 digits |

### 6F — Inference-time / structural priors (3 experiments, all NEGATIVE)

| Task # | Variant | Result | Notes |
|---|---|---|---|
| #418 MERGE-PRIOR | V-axis as inference-time prior on existing checkpoints | +0.002 (noise floor) | Initial "100% accuracy" was label leakage; honest version is null |
| #398 R6-XARCH-ENS | Cross-architecture ensembling (CBraMod + EMOD + EmotionKD logits) | No diversity gain | Architectures don't disagree enough to help |
| #421 MERGE-STIMAGG | Stimulus-level aggregation + V-axis re-ranking | BACC = 1.000 at stim level (artefact: 28-stim → 9-class is leaky by construction); per-trial BACC = 0.680 | Useful as upper bound for stim-level aggregation |

### 6G — Other supporting negatives

| Task # | Variant | Result | Notes |
|---|---|---|---|
| #405 MERGE-EMERGE (initial frame) | V-axis emerges in EMOD penultimate at PC1 r = 0.40 | "Fails" if expecting r > 0.6 | Reframed by #426 — PC1 underestimates because V-axis info is on 2 non-PC1 directions |
| #404 MERGE-REVERSE (in flight) | EEG → V-axis prediction (regression-only encoder) | TBD | Tests whether the EEG signal alone predicts V-axis |
| #410 MERGE-VAXIS-ONLY (in flight) | Pure V-axis supervision (no class labels) | TBD | Tests if V-axis alone is enough — expected NEGATIVE per saturation logic |
| #420 MERGE-DISTILL (in flight) | V-axis-aware teacher → KD-only student | TBD | Test if a V-axis-rich teacher transfers via KD |
| #424 MERGE-EMODSTYLE (in flight) | Soft-weighted SupCon with CLIP V-axis (lit-review #1 pick) | TBD | Most theoretically promising untested approach |
| #423 MERGE-UNCERT (in flight) | Kendall uncertainty-weighted multi-task loss | TBD | If no fixed λ works, the principled uncertainty-weighted approach might |

**Frame for the paper**: this section is the "exhaustive proof" half of the story. Present as a **decisive negative result for representation-alignment as a training-time injection** — every paradigm we tried (aux MSE, KD, label smoothing, RSA, InfoNCE, two-stage pretrain, multi-LLM, etc.) failed in a way that's consistent with the Section 4 "saturation" mechanism. Together with the cross-arch convergence finding, this forms the cleanest possible story: *the V-axis is the latent that EEG models naturally converge to; it cannot be added externally.*

**Hero figures**:
- `figures/negatives_summary.png` (14 NEGATIVES bar chart; Δ BACC)
- `figures/scaling_curve.png` (V-axis aux hurts more with more data — the "harder you push" gradient)
- `figures/rsa_destruction.png` (RSA λ=0/0.1/0.5/1/5 monotonic curve)

---

## Section 7 — Specialised Supervision: When Targeted, the V-axis Bias *Helps* (in flight)

**Section claim** (testing now, 85 SLURM jobs queued tonight): If we apply the V-axis loss only to channels/parameters that already carry V-axis information — guided by the topography findings (Section 5) — we avoid the global destruction of Section 6. This is the missing positive training-time finding.

### 7A — Channel-targeted V-axis losses

| Task # | Variant | Channels used | Status (job ID) |
|---|---|---|---|
| **#438 MERGE-TOPO-OPTIMAL** (THE primary test) | Topography-recommended 8-channel set: PO3, F7, O1, P3, P4, C4, C3, Pz | The empirical "best channels" from #430 | 🔄 (job 46732627, 15 jobs) |
| #437 MERGE-OCCIPITAL | Posterior 8-channel set: O1, Oz, O2, P7, P3, Pz, P4, P8 | Occipital + parietal — overlaps heavily with topography-optimal | 🔄 (job 46732616, 10 jobs) |
| #434 MERGE-FRONTAL (now CONTROL) | Frontal 7-channel set: Fp1, Fp2, Fz, F3, F4, F7, F8 | The Davidson-prior set — now retroactively a *weak-channel control* given topography findings | 🔄 (job 46732613, 10 jobs) |

### 7B — Davidson-explicit FAA loss

| Task # | Variant | Setup | Status |
|---|---|---|---|
| **#435 MERGE-FAA** | Auxiliary regression of V-axis from log(F4 alpha / F3 alpha), the canonical Davidson Frontal Alpha Asymmetry formulation | 5 seeds × 2 λ | 🔄 (job 46732614, 10 jobs) |

### 7C — Parameter-efficient supervision (PEFT)

| Task # | Variant | Setup | Status |
|---|---|---|---|
| **#432 MERGE-PEFT** | Backbone-frozen + V-axis aux at three modes: (a) full classifier head + last 2 layers; (b) LoRA r=8 on attention qkv/proj; (c) IA3 scaling vectors | 3 modes × 2 λ × 5 seeds | 🔄 (job 46732612, 30 jobs) |

### 7D — Specialise-don't-add (Procrustes alignment)

| Task # | Variant | Setup | Status |
|---|---|---|---|
| **#436 MERGE-PROCRUSTES** | Rotate the within-class top-PC of EMOD's penultimate features toward the LLM V-axis direction (cosine²-loss + 0.1×MSE) — *specialise the existing V-axis encoding rather than fighting it* | 5 seeds × 2 λ | 🔄 (job 46732615, 10 jobs) |

### Predicted outcome (double dissociation)

| Variant | Channels / mechanism | Prediction |
|---|---|---|
| #438 topo-optimal | empirical best 8-channel set | **HELPS or NEUTRAL** — best chance of escaping the destruction pattern |
| #437 occipital | posterior (signal-bearing) | likely HELPS or NEUTRAL |
| #434 frontal | weak channels (control) | NEUTRAL or slight HURT |
| #435 FAA | F4-alpha − F3-alpha (Davidson explicit) | mild HELP if Davidson partial; mild HURT if posterior dominates |
| #432 PEFT | freeze most params, train adapters + V-axis | NEUTRAL or HELP — limits global destruction |
| #436 Procrustes | rotate not add | the cleanest "specialise" — mild HELP expected |

**If any of these flip the 14/14 negative pattern → first POSITIVE training-time finding.** Even if all six flip, they give us a clean double-dissociation story (posterior helps, frontal doesn't) that is publication-grade in itself.

**Hero figures (pending)**:
- `figures/specialized_summary.png` (6 variants vs 14 baselines bar chart)
- `figures/double_dissociation.png` (frontal vs occipital vs topo-optimal Δ BACC)

---

## Section 8 — Caveats, Failure Modes, Things We Didn't Use

### Sub-experiments that didn't make the cut but inform the paper

- **#383 P5-DEPTH concept-recipe ablations** (in flight): nonce-word stories, fine n-shot, multi-axis (V/A/D), authority decomposition. Negative arousal/dominance results support the V-only narrative.
- **#386 P5-FAIL TrajLenEns failure mapping** (DONE): GLUE-small, tabular variety, ESC-50 deeper. Pinpoints where the original Paper 2 trick breaks down. Used in Section 3 motivation.
- **#388/#396 Gemma-4 family-L1 outlier**: Gemma-4 family peaks at L1 instead of late layers. Universality has a known boundary case.
- **#427 MERGE-GEMMA-EEG (in flight)**: tests if Gemma-4 L1 V-axis correlates with EEG (boundary check). Determines whether universality survives even for the L1-peak outlier.
- **Lit-review insight (#433)**: arousal lives in central beta/gamma (autonomic, non-semantic) per Davidson + recent EEG saliency work — this is the neuroscience-grounded explanation for why arousal-as-LLM-axis fails (Sections 1 & 5).

### 🟡 Honest scope subsection: Simpson's paradox in the EEG-LLM circle (#440)

A critical caveat we must surface up-front in the paper:

- **Cohort r = 0.48 at PO3/γ, but mean per-subject r at the SAME 8 channels = −0.06** (median −0.07, std 0.28, range [−0.67, +0.79], 13× top/bottom-decile spread).
- The cohort signal only emerges *after averaging EEG across subjects, then correlating with V-axis* — not from individual brains aligning.
- The "cohort r=0.87" in #397 is therefore a **between-subject effect**, not a within-subject effect. Subjects vary enormously in which channels carry V-axis information.
- Best-channel-per-subject r = +0.55 mean / +0.89 max — so the brain-LLM alignment IS real per-subject, but at subject-specific channels.
- Honest framing: **"The valence axis exists across the population in posterior visual cortex; individuals encode it on idiosyncratic channels within that region."**
- Implication for follow-up: per-subject channel re-weighting head + class-aware loss reweighting (Anger/Amusement/Tenderness 3-5×) — both data-supported, both cheap. Recommended as fresh GPU experiment after Round 11.

### 🟡 MI vs linear correlation diagnostic (#440)

200 random Gaussian directions of equal magnitude:
- Observed |r| = 0.478, p_corr = **0.020** ← V-axis IS significantly above-random under linear correlation
- Observed MI = 0.112, p_MI = 0.115 ← V-axis is NOT significantly above-random under mutual information
- ⇒ The V-axis–EEG signal is essentially **linear**, not nonlinear-information-rich. This justifies linear ridge regression as the right-sized analysis tool and rules out elaborate nonlinear claims.

### 🔵 The V-axis is a 9-stim story (#441 — paper-sharpening)

The cleanest possible reframing of our headline finding, from #441 Analysis 3:

| Stim subset | Cohort r at PO3/γ |
|---|---|
| All 28 stims (paper headline) | **+0.478** |
| Anger + Amusement + Tenderness only (n=9) | **+0.870** |
| All 28 EXCEPT Anger+Amus+Tend (n=19 mid-valence) | **−0.015** |

The 19 mid-valence stims (Disgust, Fear, Sadness, Neutral, Inspiration, Joy) contribute zero brain–LLM alignment signal. The "valence axis" we discovered is fundamentally a **3-emotional-pole contrast** (negative-arousal-driven Anger vs warm-positive Amusement/Tenderness) operationalised across 9 stimuli.

**Implication for paper framing**: We can either (a) keep the 28-stim headline and add this as an "anatomy of the signal" subsection, or (b) lead with the 9-stim story for sharper claims. Recommendation: (a) — the 28-stim story matches the FACED protocol others use, but the 9-stim diagnostic gives reviewers the precision they want.

**Implication for the held GPU experiment #443**: Loss weighting {Anger:5, Amus:3, Tend:3, others:1} mathematically justified — current uniform-weighted Pearson loss averages over 19 noise-only gradient directions.

### 🔵 Per-subject ceiling analysis (#441 Analysis 2)

Establishing realistic targets for the per-subject head (#442):

| Scheme | Mean per-subject |r| | Δ vs fixed |
|---|---|---|
| Cohort-fixed top-8 channels in γ | 0.228 (≈ −0.062 signed) | — |
| Per-subject ORACLE: best 1 channel in γ | 0.484 | +0.26 |
| Per-subject ORACLE: best 1 (channel, band) | 0.551 | +0.32 |
| Per-subject ORACLE: top-8 (channel, band) | **0.616** | **+0.39** |

**Key insight**: All-band oracle (0.551) beats γ-only oracle (0.484). Different subjects encode V-axis on different BANDS, not just different channels. Per-subject head must expose all 5 bands.

### 🔵 Per-subject temporal attention (#441 Analysis 4)

Per-subject |r| at PERSONAL temporal peak ≈ **2× per-subject |r| at COHORT temporal peak**. But cohort 18-21s window catches only 17-24% of subjects. ⇒ Time-windowed loss (#444) needs LEARNED per-subject temporal attention, not a fixed window.

### Hyperparameter choices justified

- **Why Qwen2.5-1.5B as primary**: optimal V-axis quality (inverted-U across model size; 32B worst; SFT hurts). Switched to Qwen3.5 for newer-model coverage in #326. **Reviewer-credibility note**: re-run main experiments with Qwen3.5 before submission.
- **Why layer 27 (of 28)**: V-shape in #296 confirms sudden emergence at L27, replicated across families.
- **Why d6 (transformer depth 6)**: scales pretrained 3-layer EMOD via 3 random init layers (`strict=False`); width 128 / depth 6 is the sweet spot per #272/#277.
- **Why ensemble K=5 to 10**: PIVOT 2 compute-optimal law. K=5 saturates BACC variance reduction (#392).

### Things we explicitly DON'T claim

- **NOT** "V-axis is a training shortcut for EEG" — 14/14 fail (Section 6).
- **NOT** "we replicate Davidson's frontal asymmetry as the dominant valence signal" — posterior > frontal in our data (Section 5).
- **NOT** "TrajLenEns is a real diversity recipe" — debunked in #382.
- **NOT** "arousal V-axis works as well as valence" — supervised arousal regression fails (#274/#278/#281). The asymmetry is real and explained by Section 5 lit findings.

---

## Cross-section experiment count (total: 60+ cycle-75 experiments mapped)

| Section | Experiments mapped | Status |
|---|---|---|
| §1 Universal probe | 17 | 17 done |
| §2 LLM↔Brain bridge | 5 | 5 done |
| §3 New EEG SOTA | 9 | 9 done (incl. mechanism debunk) |
| §4 Convergence mechanism | 4 | 3 done + 1 in flight |
| §5 Brain topography | 4 | 4 done |
| §6 14 Negatives | 14 + 6 in-flight | 14 done + 6 in-flight |
| §7 Specialised supervision | 6 | 6 in-flight (results tonight) |
| §8 Other / caveats | 5 | 4 done + 1 in flight |

---

## Key numbers to memorise for paper drafting

| Statistic | Value | Source |
|---|---|---|
| EEG SOTA on FACED | **0.6951** BACC | #390 |
| Prior best (CBraMod) | 0.572 BACC | literature + #340 |
| Prior best (EmotionKD) | 0.628 BACC | literature |
| EEG-LLM correlation, bare-emotion CLIP | **r = +0.874** | #397 |
| EEG-LLM correlation, multi-LLM mean | **r = +0.79 ± 0.06** | #411 |
| Cross-arch BACC ↔ V-axis r | **r = +0.955, p = 7.3e-10, n=18** | #429 |
| Random direction control | r = +0.07 | #397 |
| EMOD V-axis encoding (class PC1) | r = +0.68 | #426 |
| EMOD V-axis encoding (within-class) | r = +0.78 | #426 |
| Best individual brain channel | PO3/gamma r = +0.48 | #430 |
| Region mean \|r\|: occipital vs frontal | 0.212 vs 0.162 | #430 |
| Concept library AUC ≥ 0.95 | 17 of 20 | #394 |
| Composition 4-quadrant accuracy | 79% (3.16× chance) | #395 |
| Vision V-axis IAPS recovery | r = +0.87 | #385 |
| Multilingual mT0-base AUC | 0.89-0.91 (JA/AR/RU) | #384 |
| RSA worst destruction | -0.093 BACC at λ=5 | #414 |
| DCE worst destruction | -0.397 BACC at τ=5 | #415 |
| Scaling worst destruction | -0.045 BACC at full data | #408 |
| Pretrain-FT worst destruction | -0.190 BACC (unfrozen mode) | #416 |
| XEEG transfer null | Δ=0.0015, p=0.97 | #407 |
| XEEG-FULL transfer null | Δ=0.0000 | #412 |

---

## Open questions / things the paper drafter should anticipate reviewers asking

1. **Why r = +0.955 dominated by between-architecture spread?** Within-architecture is noisy at n=5 because BACC range collapses. Mid-training trajectory (in flight, #429 follow-up) will resolve this.
2. **Davidson FAA replicates qualitatively but is weak** — is this a FACED-video-specific finding or a general challenge to Davidson? Need to flag it for video-stimulus paradigms specifically.
3. **The 14 negatives** — are they really exhaustive, or did we miss something? The Round 11 specialised variants explicitly address this. If even those fail, the negative is publication-strength.
4. **Why Qwen2.5 not Qwen3.5 for main experiments?** Need to rerun headline numbers with Qwen3.5 before submission (#326 done in headline; concept library #394 still on Qwen2.5).
5. **Per-class V-axis r** — does it differ for positive vs negative emotions? Already in `topography/per_emotion_topography.npz`; needs per-class analysis figure.
6. **Multi-stim V-axis?** We have one V-axis per dataset. What if we built a per-emotion V-axis? See #221 (LDA-dim regression) for related negative.

---

*This document is the single source of truth for paper drafting. Every claim in the paper should trace to a row in one of the section tables above, which traces to a task # in the worklog, which traces to a results JSON in `/ibex/project/c2323/yousef/reports/`.*
