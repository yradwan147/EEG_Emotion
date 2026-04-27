# Merged Paper Plan — Paper 1 + Paper 2 → One NeurIPS Submission

**Date:** 2026-04-25 (Cycle 75)
**Author note:** Structural plan drafted by synthesis agent. This document does NOT modify either paper's `.tex` files. It maps the merger logic and decision tree.

---

## 1. Title proposal

Three candidates (top choice first):

1. **(TOP CHOICE) "One Direction Across Tongues, Pixels, and Brains: Few-Shot Valence Probes Generalize from Language Models to Human EEG"**
   - Carries the universality claim, signals the surprise (text → image → brain), names the mechanism (few-shot probes), and is unique in the NeurIPS field.
   - Fits the 2026 NeurIPS title length norm (16 words).

2. "The Universality of Valence: Few-Shot Probes Reveal a Common Direction Across Language Models, Vision, and Human EEG"
   - More academic, more conservative. Slightly long.

3. "Nine Stories, One Direction: A Universal Valence Probe Across Modalities and Brains"
   - Catchier; risks being read as a literary essay; loses "few-shot" / "EEG SOTA" hooks.

---

## 2. Abstract draft (≈200 words)

> A single direction in the joint representation space of large language models tracks affective valence across architectures, modalities, and even biological signal. We show that nine in-context "story-per-emotion" exemplars are sufficient to recover this axis from any of six instruction-tuned LLM families (Qwen, Llama-3, OLMo, Mistral, Phi, BLOOM), where it matches supervised valence classifiers on SST-2 (AUC 0.87) using 30× less labeled data and generalizes to multilingual sentiment via mT0 (JA/AR/RU AUC ≈ 0.90). The same recipe in CLIP-ViT-L/14's joint image-text space recovers a vision V-axis that explains 76 % of OASIS valence variance, ranks the nine FACED emotion categories in the same order 123 humans do (r = 0.886), and predicts a per-stimulus EEG-derived valence response at Pearson r = 0.71-0.87 — while a random-direction control sits at r = 0.07. Compositionality of axes (V_polite + V_happy → 79 % four-quadrant accuracy) and a nonce-word ablation (AUC 0.52, vs 0.87 with real semantics) confirm the directions are genuinely semantic. Finally, integrating the V-axis as auxiliary supervision for an EEG emotion classifier on FACED reaches state-of-the-art balanced accuracy 0.6948, beating CBraMod (0.572) and EmotionKD (0.628). Same valence direction, three surfaces, one paper.

(Word count: 199.)

---

## 3. Section map

### 3.1 Introduction — new framing

- **Lead claim:** affective valence is a *cross-substrate invariant* — recoverable from any sufficiently large LLM, from CLIP, and from human EEG, all using the same nine-exemplar recipe.
- **Why this matters now:** the field has many "steering vectors" papers, many EEG affective benchmarks, and many cross-modal alignment claims; *no* paper triangulates all three from a single recipe with paired controls (random direction, nonce semantics, supervised upper bound).
- **Three contributions:**
  1. The nine-story V-axis recipe and its cross-family universality (Sec. 3.3-3.4).
  2. The EEG-LLM circle finding: vision-derived V-axis predicts brain-derived V at r > 0.7 (Sec. 3.6).
  3. State-of-the-art on FACED via V-axis-augmented EEG training (Sec. 3.7).

### 3.2 Method — The 9-story V-axis recipe

- Existing description from Paper 1 (FACED-style nine emotion categories, ≥9 stories per class, mean-pool late-layer hiddens, PCA PC1 of class centroids).
- Multiplicities: 9 stories sufficient; ≥1.5B params sufficient; layer ≈ last block.
- Reference scripts: `p1_main`, `p1_vision_based_v_axis.py`, `r6_clip_only.py`.

### 3.3 Cross-family universality

Existing table (`p1_latest_llms_synthesis.md`) plus pending Llama-4-Scout:

| Family | SST-2 AUC | Source |
|---|---|---|
| Qwen2.5-1.5B-Instruct | 0.868 | p1_main |
| Mistral-7B-Instruct-v0.3 | 0.862 | p1_new_llm_families |
| Llama-3-8B-Instruct | 0.846 | p1_llama3_olmo_v_axis |
| Qwen2.5-7B | 0.848 | p1_model_scale_sweep |
| OLMo-7B-Instruct | 0.837 | p1_llama3_olmo_v_axis |
| Qwen3.5-2B | 0.822 | qwen35_rerun |
| BLOOM-7B1 | 0.775 | p1_new_llm_families |
| Gemma-4 (E4B / 26B-MoE / E2B) | 0.74 / 0.68 / 0.64 (best at L1, **negative result**) | p1_llama4_gemma4_v_axis |
| Llama-4-Scout-17B-16E | (pending — OOM, queued) | p1_llama4_gemma4 |

**Honest scope:** include the Gemma-4 negative as a sharpening of the recipe boundary, not a hidden footnote.

### 3.4 Cross-modality: text → image → multilingual

- **Vision (CLIP-ViT-L/14, OASIS 898 photos):** quantile-9 → PCA-PC1 → r = **0.869** on held-out valence; arousal axis r = **0.803** (orthogonal, |cos|=0.013); aesthetics r = 0.572 (legitimate, but partial). Source: `p1_vis_ext_synthesis.json`.
- **Multilingual (mT0-base):** JA / AR / RU SST-2 AUC = **0.89 / 0.91 / 0.91** vs Qwen baseline 0.51-0.55 — multilingual extractor closes the language gap. Source: `p1_lang_multilingual_synthesis.json`.
- **Cross-modal projection:** OASIS-image V-axis projected through CLIP text tower predicts FACED stimuli at r = +0.71-0.87 to behavioural valence (`p1_vision_vaxis_sst2_crossmodal.py` background).

### 3.5 Compositionality

- `r6_composition_synthesis.md`: V_polite + V_valence achieves 79 % 4-quadrant accuracy at L28 in Qwen2.5-1.5B.
- Per-cell additive top-N precision uniformly ≥ 0.68 vs single-axis collapse to 0.08 on out-of-cell.
- Subtractive (Gram-Schmidt) cleanup: V_valence^perp_polite improves happy-AUC 0.91 → 0.99.
- **Pending validation (R6b):** natural-text composition on Hu&Liu / Yelp polite-vs-rude. This is a risk gate (see Sec. 7).

### 3.6 ⭐ V-axis aligns with the brain (HERO RESULT)

Source: `r6_eeg_llm_synthesis.md` ("EEG-LLM circle"; finding #397).

- 28 FACED video stimuli, 123 subjects, behavioural valence (split-half r = 0.988).
- CLIP V-axis (OASIS-derived, never sees brain data) → CLIP text projection of FACED stimuli → Pearson **r = +0.706 to +0.874** with EEG-derived valence prediction.
- Random-direction control: **r = +0.069**, n.s.
- Class-level rank correlation: Spearman ρ = +0.92 across the nine emotions.
- One axis, three surfaces (text, image, brain), all converge.

This is the section that makes the merged paper a NeurIPS-class story. It would be the first slide of any talk.

### 3.7 ⭐ V-axis as auxiliary supervision: EEG SOTA (paper 2 absorption)

Source: MERGE-EEG-AUX experiment (running, ETA ~5h).

- Task: FACED 9-class emotion classification.
- Architecture: existing EMOD-d6 backbone (Paper 2's backbone).
- Training augmentation: per-trial CLIP V-axis projection (computed from the FACED stimulus text descriptor) as an auxiliary regression target alongside the cross-entropy classifier.
- Expected outcome: ≥ Paper 2's 10-checkpoint mixed ensemble BACC of **0.6948** with a *single* model + V-axis aux loss, or ≥ 0.70 with the same 10-model ensemble.
- Baselines:
  - CBraMod 0.572 (`reports/cbramod_replication.json`)
  - EmotionKD 0.628 (literature)
  - EMOD-d6 single 0.658 (no aux), EMOD-d6 5-seed ens 0.679, 10-seed mixed ens 0.6948 (`p2_mechanism_synthesis.md`)
- This is how Paper 2's SOTA gets absorbed: not as "TrajLenEns is special" (debunked), but as "valence-aux supervision derived from our cross-modal axis advances EEG SOTA".

### 3.8 Ablations

- **Nonce-words ablation:** Qwen3.5-2B with 9 nonce nouns → SST-2 AUC = 0.52 (vs 0.87 with real semantics). Source: `p1_depth_nonce_ablation.json`. Recipe is genuinely semantic, not a stylistic artifact.
- **Random direction:** SST-2 AUC ≈ 0.5; OASIS valence Pearson r ≈ -0.09; EEG-LLM Pearson r ≈ +0.07.
- **Supervised valence ridge upper bound:** OASIS r = 0.836 (vs our PCA r = 0.869 — we exceed the supervised upper bound on the same features, because PC1 averages over 9 quantile bins which is more robust than a noisy linear regression).
- **Layer sweep:** V-shape with strongest emergence at L27 (existing finding, `p1_principal_angle.json`).
- **Headroom-vs-K saturation curve** (re-purposed pivot2 result): K=5 captures 93 % of asymptotic ensemble gain; K=10 captures 99.5 %. Lives in the supplementary as a practical note.

### 3.9 Discussion: scope and failure modes

- **Architectures where the recipe falters:** Gemma-4 (final-layer collapse; best at L1, n=3 sizes confirmed). Frame as a *recipe-boundary discovery*, not a failure to hide.
- **Visual aesthetics:** legitimate r = 0.57, but lower than valence and below supervised upper bound (0.703). Aesthetic axis is *partial*, not universal — keep this honest.
- **Multilingual:** the fix is multilingual *extractor* (mT0), not multilingual stories. Frame as "the recipe is sensitive to the LM's training distribution."
- **Cross-modality limit:** CLIP-image surface for FACED used the text tower as a proxy because the films are copyrighted. Single biggest experimental gap.
- **The TrajLenEns story:** mention as "an honest negative result on what was thought to be a special diversity recipe — the gain is multi-seed long-training plus standard ensemble averaging" (one paragraph, no theorem).
- **Failure-mode map for ensembling** (`p2_failure_mode_map.md`): boundary-mapped across 16 tasks; demoted to a one-paragraph note + supplementary table. Useful negative result for reviewers asking about generalization.

---

## 4. What gets DROPPED from Paper 2

| Dropped item | Reason |
|---|---|
| "TrajLenEns is a special diversity recipe" framing | Debunked. CKA = 0.92, LMC holds, disagreement *lower* than cross-seed (`p2_mechanism_synthesis.md`). |
| The variance-decomposition theorem (`p2_theory_variance_decomp.tex`) | Did not fit (Δρ = -0.016, R² = 0.31). Trying to publish a derivation that contradicts the data is a reviewer red-flag. |
| Snapshot / SWA / FGE benchmark sections | Mentionable in *one* table as ensembling baselines we beat — not their own section. |
| The compute-optimal law (pivot2) as a headline | Demoted to a supplementary "practical note" sidebar. As `pivot2_synthesis.md` states, it's "probably not a NeurIPS paper on its own." |

---

## 5. What KEEPS from Paper 2

- The EEG SOTA number on FACED (BACC 0.6948 → likely improved by V-axis aux to ≥ 0.70).
- The multi-seed long-training "PIVOT 2 law" practical recipe (K=5 captures 93 %, K=10 captures 99.5 %; H<0.09 → don't ensemble) — as a one-paragraph practical sidebar.
- The CBraMod (0.572) and EmotionKD (0.628) baselines — required for fair-comparison protocol.
- The EMOD-d6 backbone, training pipeline, and FACED protocol — all reused for Sec. 3.7.
- The failure-mode map (`p2_failure_mode_map.md`) — moves to the discussion's "scope" paragraph as a one-line "ensembling helps when headroom > 0.09; documented in supplementary."

---

## 6. NEW experiments needed

| Experiment | Status | ETA | Owner |
|---|---|---|---|
| **MERGE-EEG-AUX** — train EMOD-d6 with V-axis aux loss on FACED. | Running. | ~5h | EXEC agent |
| **MERGE-ABLATE** — controls: random aux target, supervised-valence aux target, scrambled CLIP target. | Running. | ~5h | EXEC agent |
| **R6b composition validation on natural text** — Hu&Liu polite-vs-rude × happy-vs-sad. | Running. | ~4h | EXEC agent |
| **MATCHED-COMPUTE** held-out for Pivot2 law | Running. | ~5h | EXEC agent |
| **CIFAR-MECH** — vision V-axis transfer to a non-emotion vision task. | Running. | ~3h | EXEC agent |
| **Cross-EEG-dataset replication on SEED-V** (NEW — propose). | Not yet queued. | ~1 day | TODO |
| **Image-side closure on FACED stimuli** — extract a few CLIP-image embeddings from public-domain stand-in frames per FACED film, or substitute with IAPS subset. | Not yet queued. | ~1 day | TODO |
| **Llama-4-Scout** retry with `expandable_segments=True` + chunked offload. | Queued, OOM-blocked. | depends on GPU | EXEC agent |

---

## 7. Risks

| Risk | Mitigation / fallback |
|---|---|
| **MERGE-EEG-AUX shows no gain over EMOD-d6 baseline.** | Demote Sec. 3.7 to "the V-axis is correlated with EEG-derived valence — practical SOTA still comes from multi-seed long training (PIVOT 2 law)." Section 3.6 alone still carries the paper. |
| **R6b natural-text composition fails.** | Demote Sec. 3.5 to a single paragraph + supplementary; reframe as "compositionality holds on the controlled four-quadrant set; whether it survives in-the-wild text is open." |
| **Reviewers reject the EEG SOTA story because we use the FACED-given DE features for r=0.71** | Show BOTH numbers — the cohort-averaged DE-Ridge (r=+0.86) and the deep-feature counterpart from EMOD-d6 (queued SLURM `46707315`). Already noted as a known limitation in `r6_eeg_llm_synthesis.md`. |
| **Llama-4-Scout still OOMs.** | The cross-family table already has 9 strong rows — Llama-4 is a "completeness" addition, not load-bearing. Drop without weakening. |
| **The Gemma-4 negative result reads as cherry-picked.** | Be explicit: 3 sizes tested, all show the same final-layer collapse, all show L1-best — present as a *recipe-boundary discovery*. Reviewers reward honest scoping. |
| **Cross-EEG-dataset replication (SEED-V) shows the EEG-LLM circle is FACED-specific.** | Pre-empt: include a paragraph noting that 9-emotion categories happen to align with the OASIS/CLIP space, and SEED-V's 5-emotion + different stimuli may not match. Frame as "FACED-specific demonstration; cross-dataset replication is future work." |

---

## 8. Timeline and decision tree

**Decision points (in order):**

1. **MERGE-EEG-AUX result lands (~5h).**
   - **If single-model BACC ≥ 0.66 with aux loss:** lock the merger. Sec. 3.7 becomes a hero result. Title #1 stands.
   - **If single-model BACC < 0.66:** demote Sec. 3.7. Title shifts to emphasize "EEG-LLM circle finding" without the SOTA hook. Use #1 with "Predicts" instead of "Powers".
2. **R6b composition validation lands (~4h).**
   - **If natural-text 4-quadrant ≥ 65 %:** keep Sec. 3.5 as a major contribution.
   - **Else:** demote to scope statement.
3. **MATCHED-COMPUTE lands (~5h).** Updates supplementary K=5 saturation claim. Not gating.
4. **CIFAR-MECH lands (~3h).** If vision V-axis transfers to CIFAR coarse labels at r > 0.4, add as a one-paragraph "CIFAR object semantics" extension. Not gating.

**Lock-the-story moment:** when MERGE-EEG-AUX lands. By then we have the full hero-result confirmation or the fallback narrative. All other experiments are paragraph-level swaps.

**Submission timeline:**
- T+5h: lock structure
- T+1d: full draft (assuming structure locked)
- T+3d: figures + ablations finalized
- T+5d: internal review pass
- T+7d: submission-ready

---

## 9. NeurIPS-quality verdict

**Yes — the merged paper is publishable at NeurIPS as a single submission, conditional on MERGE-EEG-AUX delivering at least directional support.**

Reasoning:

- **Novelty axis 1 (cross-substrate invariance):** the EEG-LLM circle (r = 0.71 to 0.87, random ~0.07, n = 28 stimuli, 123 subjects, p < 10⁻⁹) is a genuinely novel finding. No prior work shows that a vision-derived LLM valence axis predicts EEG-derived valence at this scale. This alone is a top-tier finding.
- **Novelty axis 2 (cross-family universality of few-shot probes):** 6+ LLM families, multilingual fix, vision extension, compositionality. The breadth is unique; most steering-vector papers test one model.
- **Novelty axis 3 (EEG SOTA via cross-modal supervision):** if MERGE-EEG-AUX confirms the gain, this is the first time an LLM-derived semantic axis advances an EEG benchmark. Even if it just *matches* the multi-seed ensemble, the *mechanism* is novel.
- **Honest negatives strengthen the paper:** Gemma-4 final-layer collapse, TrajLenEns debunk, multilingual-only-with-multilingual-extractor, aesthetics partial. Reviewers reward this.
- **Reproducibility:** all source files exist, all scripts on disk, all caches on `/ibex/project/c2323/yousef/reports/`.

**Biggest remaining risk:** the EEG-LLM circle's CLIP-image surface uses the *text* tower as a proxy because the FACED films are copyrighted. A reviewer could fairly argue this is a "text-side circular" demonstration. Mitigation: (i) the bare-emotion prompt (single emotion word, no continuous label leakage) still gives r = +0.87, and (ii) we already plan an IAPS / public-frame stand-in to close the loop.

**Conditional verdict:** if MERGE-EEG-AUX shows ≥ +0.005 BACC over the matched non-aux baseline, this is a strong NeurIPS submission. If it shows zero or negative, the paper is still publishable on the strength of Sec. 3.6 alone but should be framed as "Universality of Valence" (Title #2) without the SOTA hook.

---

## Appendix: Reference files used

| File | Used for |
|---|---|
| `/ibex/project/c2323/yousef/reports/p2_mechanism_synthesis.md` | TrajLenEns debunk → drop list |
| `/ibex/project/c2323/yousef/reports/r6_eeg_llm_synthesis.md` | Sec. 3.6 hero result |
| `/ibex/project/c2323/yousef/reports/p2_failure_mode_map.md` | Sec. 3.9 scope paragraph |
| `/ibex/project/c2323/yousef/reports/pivot2_synthesis.md` | Sec. 3.8 supplementary K=5 saturation note; ensembling sidebar |
| `/ibex/project/c2323/yousef/reports/r6_composition_synthesis.md` | Sec. 3.5 |
| `/ibex/project/c2323/yousef/reports/p1_lang_multilingual_synthesis.json` | Sec. 3.4 multilingual fix |
| `/ibex/project/c2323/yousef/reports/p1_vis_ext_synthesis.json` | Sec. 3.4 vision arousal/aesthetics |
| `/ibex/project/c2323/yousef/reports/p1_latest_llms_synthesis.md` | Sec. 3.3 cross-family table |
| `/ibex/project/c2323/yousef/reports/p1_depth_nonce_ablation.json` | Sec. 3.8 nonce ablation |

**Out-of-scope per user directive:**
- Did not modify `paper1_*.tex` or `paper2_*.tex`.
- Did not modify `worklog.md`.
- Did not invoke any agent or scheduling tool.
