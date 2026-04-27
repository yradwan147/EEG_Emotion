# Oral-Target Checklist — V-Axis Paper

*Author: research-agent pass, 2026-04-27. Reviewed N=6 confirmed orals from NeurIPS 2024 / ICLR 2024 / ICLR 2025 / ICML 2024 / ICML 2025. Companion to `comparative_review_2026_04_27.md` (which scored us against three spotlights).*

## Executive summary

Current oral-confidence is **~25-30%**. The paper is solidly spotlight-grade but two specific oral-signature traits are *missing*, not partial: (a) a single-sentence headline claim that the program committee can paraphrase from memory after one talk, and (b) a controlled causal intervention that closes the loop on the central correlational claim. Spotlights survive without these; orals do not. With the seven items in the ranked fix list addressed, oral-confidence rises to **~55-65%** — the residual gap is the single-EEG-dataset ceiling and the absence of a formal theorem corresponding to the "saturation theorem" name. The single most-leveraged fix is **reframing the headline from "we extend Platonic to a third modality" to "we discover and quantify a saturation principle that bounds when concept supervision can help"** — the saturation result is the part of our paper that is unique, talk-shaped, and unmatched by any oral we read; the V-axis-as-substrate is supporting evidence rather than the lead. The second-most-leveraged is the causal ablation of the V-axis subspace inside an EEG model at inference time, mirroring Arditi's ablate-and-add, which converts our $r{=}0.74$ ensemble-contribution prediction into a causal claim.

---

## Step 1 — Six confirmed orals reviewed (status verified)

I verified each via the conference virtual site or `papers.cool` filter. Spotlights and posters were rejected from the sample even when topically perfect (notably Arditi 2024 = poster, Brain-JEPA = spotlight, MindAligner = poster).

**O1. The Platonic Representation Hypothesis** (Huh, Cheung, Wang, Isola — ICML 2024 oral, position-paper track). Argues that representations across vision and language are converging to a "shared statistical model of reality." The talk-slide is the kernel-alignment colour grid. Rationale for oral: position-paper that crystallises a generalisation already half-believed in the field, with a coined name that survives the talk. <https://icml.cc/virtual/2024/oral/35559>

**O2. Predictive auxiliary objectives in deep RL mimic learning in the brain** (Fang, Stachenfeld — ICLR 2024 oral). Quote: *"representational changes in this RL system bear a striking resemblance to changes in neural activity observed in the brain across various experiments... predictive objectives improve and stabilize learning particularly in resource-limited architectures."* Rationale for oral: a cross-domain "ANN matches brain" claim done with experimental discipline (auxiliary-objective ablation at multiple horizons) and a clean theory-of-mechanism (predictive horizon → representation transfer). <https://iclr.cc/virtual/2024/oral/19748>

**O3. Generalization in diffusion models arises from geometry-adaptive harmonic representations** (Kadkhodaie, Guth, Simoncelli, Mallat — ICLR 2024 oral). Headline: *"two DNNs trained on non-overlapping subsets of a dataset learn nearly the same score function, and thus the same density, when the number of training images is large enough."* Rationale for oral: it is a *convergence* result with a sharp identification of the inductive bias (geometry-adaptive harmonic basis) — the kind of paper where the headline result is one sentence and the mechanism is a named mathematical object. <https://arxiv.org/abs/2310.02557>

**O4. Trading Place for Space: Increasing Location Resolution Reduces Contextual Capacity in Hippocampal Codes** (Rooke, Wang, Di Tullio, Balasubramanian — NeurIPS 2024 oral). Quote: *"a fundamental trade-off between high resolution encoding of position and the number of storable contexts is identified. This trade-off is tuned by place cell width, which might explain the change in firing field scale along the dorsal-ventral axis of the hippocampus."* Rationale for oral: identifies a quantitative trade-off (capacity exponent vs. resolution), explains a known anatomical gradient (dorsal-ventral) as a consequence. The oral is built around one inequality. <https://neurips.cc/virtual/2024/oral/97978>

**O5. Interpreting CLIP's Image Representation via Text-Based Decomposition** (Gandelsman, Efros, Steinhardt — ICLR 2024 oral). Decomposes CLIP into per-head, per-patch components and labels them via text projections, finding that *"property-specific roles for many heads"* emerge along with spatial localisation. Rationale for oral: a structural decomposition of a widely-used model that anyone can reproduce in an afternoon, with concrete causal interventions (zero-out a head, behaviour changes predictably). <https://arxiv.org/abs/2310.05916>

**O6. Interpreting Emergent Planning in Model-Free Reinforcement Learning** (Bush, Chung, Anwar, Garriga-Alonso, Krueger — ICLR 2025 oral). Quote: *"the first mechanistic evidence that model-free reinforcement learning agents can learn to plan."* Methodology: probes for planning-relevant concepts, investigates plan formation in internal representations, then *causally verifies* effect of plans on behaviour by intervening on the discovered representations. Rationale for oral: a first-of-kind claim ("model-free RL learns to plan") backed by the trio probe → mechanism → causal intervention. <https://iclr.cc/virtual/2025/oral/31895>

(Adjacent confirmed orals not pursued: ICML 2025 oral on universal-loss-curve scaling laws (collapse onto a single curve under normalisation); ICML 2025 oral on intermediate-layer representations beating final layers — both are "single sentence summarises everything" papers but less topically close.)

---

## Step 2 — Synthesised oral signature (8 traits)

Confirmed against the six orals above. Examples cited.

**T1. One-sentence steal-able headline.** Each oral can be paraphrased in 12 words: O1 *"representations are converging across modalities."* O2 *"predictive aux losses in RL change reps to look like brain reps."* O3 *"diffusion models converge to the same score on disjoint splits."* O4 *"hippocampal place-cell width trades resolution for storable contexts."* O5 *"CLIP heads have interpretable property-specific roles."* O6 *"model-free RL agents learn to plan."* Spotlights typically need three-sentence summaries.

**T2. First-of-kind framing on a question the audience didn't know to ask.** O6 explicitly says "first mechanistic evidence." O3 phrases the diffusion result as resolving an open generalisation-vs-memorisation tension. O1 names the phenomenon (Platonic). Orals create vocabulary; spotlights extend it.

**T3. Probe → mechanism → causal-intervention triad.** O6 makes this explicit: probe for plans, study formation, intervene to alter behaviour. O5 does the same for CLIP heads (probe → label → ablate). O2 does it via auxiliary-objective ablations at varying predictive horizons. Orals close the causal loop; spotlights stop at correlation.

**T4. A formally-stated quantitative law / inequality / trade-off.** O4 is a capacity exponent vs. resolution inequality. O3 is a kernel-distance-equals-zero claim under "enough data." Even O1 (a position paper) coins the kernel-alignment metric as a measurable proxy. Orals contain at least one *named, quantitative, repeat-able* statement that survives the talk slide.

**T5. ≥2 modalities or ≥2 architectures (often the headline).** O1 (vision + language). O2 (RL + brain). O5 (CLIP image side + text side as decoder). O3 (diffusion + image-density). O6 (Sokoban model-free + concept probes from interpretability, two methodologies fused). Single-modality orals exist (O4) but compensate with theoretical universality.

**T6. The talk slide pre-exists the paper.** Each oral has one figure that, printed on a slide, conveys the entire claim: O1 = kernel-alignment grid; O3 = side-by-side score-functions of disjoint-split models; O4 = capacity-vs-width curve; O5 = head-decomposition heatmap; O6 = plan-overlay on Sokoban grid. The figure is the program-committee bait.

**T7. Statistical rigor visible in the abstract.** Orals quote effect sizes, p-values, or sample counts in their abstracts ("13 popular open-source chat models", "two DNNs on non-overlapping subsets", "across various experiments"). Reviewers see the rigor before they open the PDF.

**T8. Sharp limitations that name what the result is *not*.** O3 explicitly says the result holds "when the number of training images is large enough" — does not generalise to memorisation regime. O6 calls out that planning was demonstrated in Sokoban specifically, not as a universal claim. Orals draw their own bounding box; spotlights leave it implicit.

(Refuted candidate trait: "≥2 datasets is required". O4 used one neural model, O5 used one CLIP variant. The bar is universality of *claim*, not breadth of dataset. We over-estimated dataset breadth as a hard requirement.)

---

## Step 3 — Audit table (our paper vs the signature)

| # | Trait | Status | Evidence in our paper | Fix |
|---|---|---|---|---|
| T1 | One-sentence headline | **MISSING** | Abstract names 5 contributions (universality + brain + convergence + saturation + SOTA) in 6 sentences. Reviewer can't paraphrase the paper from memory. | Pick ONE: "Saturated concept directions are unhelpful supervision targets." Lead abstract with this; everything else is evidence. |
| T2 | First-of-kind framing | **PARTIAL** | Cross-modal triangle (LLM↔brain↔EEG-model) is genuinely first-of-kind, but the abstract opens with "we answer affirmatively for valence" — refinement framing. | Rename and reframe. The saturation theorem is also first-of-kind ("late-layer concept directions are not free real estate") and is more talk-shaped. |
| T3 | Probe → mechanism → causal triad | **PARTIAL** | We have probe (V-axis extraction §3) + mechanism (within-class residual prediction at $r=0.74, p=0.014$, §5) + interventional *attempts* (the 25 saturation interventions). But intervention is *additive* (add V-axis loss), not *ablative* (zero out V-axis subspace at inference). Arditi-style ablation is missing. | Run V-axis ablation on a trained EMOD checkpoint: zero out the within-class residual subspace at inference, measure BACC drop. Should drop by the analytically-predicted amount. ~3 days of compute. |
| T4 | Formal quantitative law | **PARTIAL** | We *call* it "saturation theorem" and identify a transition window in $[0.62, 0.66]$ BACC, but no formal statement. Reviewer 2 will catch this. The within-class-residual-r predicts ensemble-contribution at $r=0.74, p=0.014$ — that *is* a quantitative law, just not labelled as one. | (a) Restate the saturation result as a formal proposition: "for any concept direction $v$ already encoded by the converged network at $\|H v\|/\|v\| > \tau^*$, adding $v$-projection auxiliary loss with weight $\lambda > 0$ yields $\Delta\text{BACC} \le 0$ in expectation." Then say "we show $\tau^*$ empirically falls in $[0.62, 0.66]$ for FACED-9." (b) Coin the within-class-residual-predicts-ensemble-contribution claim as a named quantitative law — "Residual Contribution Law." |
| T5 | ≥2 modalities/architectures | **PRESENT** | LLM + brain + EEG-model is three modalities. Two architectures (CBraMod, EMOD). 18 LLMs. We are *over*-stocked here. | Don't dilute. But foreground the *triangle*, not the count. |
| T6 | Pre-existing talk slide | **PARTIAL** | F1 (universal V-axis hero), F4 (brain topography), F8 (two-tier scatter) are 3 candidates. None is unambiguously *the* slide. Compare to Huh's kernel-alignment grid which is unambiguous. | Build one new figure: the saturation-cliff figure (Δ-BACC from V-axis supervision plotted against base-recipe BACC across 25 interventions, with the transition in $[0.62, 0.66]$ shaded). This is `lf6_saturation_cliff.pdf` already — make it the F1 hero, demote universality to F2. |
| T7 | Stats visible in abstract | **PRESENT** | $r{=}0.87$, $p<10^{-9}$, $r{=}0.885$, $r{=}0.74, p{=}0.014$, $0.6948$ BACC, +21.5% relative — all in abstract. | Keep. Possibly cut to 3-4 numbers to make room for the headline (T1 fix). |
| T8 | Sharp limitations | **PRESENT** | §9.5/9.6: single dataset, cohort-only, threshold dataset-specific, negative-results-need-strong-baseline. Strong. | Keep, but elevate to a numbered "what this result is not" paragraph in the introduction, mirroring O3 and O6. Reviewers reward this in the front of the paper. |

Net: **3 PRESENT, 4 PARTIAL, 1 MISSING.** The MISSING is the single most-fixable item.

---

## Step 4 — Ranked fix list

**1. [HIGH IMPACT, LOW EFFORT — 4 hours of writing] Reframe headline around saturation, not V-axis.** New abstract opening: *"Late-layer concept directions are not free real estate. We show that once a network has absorbed a concept (here the valence axis of human emotion) from task supervision alone, adding that same concept as an auxiliary loss is at best a no-op and at worst harmful. We locate the saturation threshold empirically..."* The V-axis is then the *substrate* on which we discover saturation, not the headline.

**2. [HIGH IMPACT, MEDIUM EFFORT — 3 days compute, 1 day analysis] Causal ablation: zero out the V-axis residual subspace at inference, measure BACC drop.** Pick our SOTA single-checkpoint (vanilla_e150_s789, BACC 0.6755). Project penultimate features onto the orthogonal complement of the within-class V-axis residual; re-run logits; measure new BACC. Predicted drop matches the within-class residual contribution to ensemble gain. This is the Arditi-equivalent intervention. Closes T3.

**3. [HIGH IMPACT, MEDIUM EFFORT — 1 day writing] Formalise the saturation statement as a proposition.** Section 7.1 already has the empirical content; add 3 sentences of formal statement at the top of §7. Stop using "theorem" colloquially; either upgrade to a proposition with a proof sketch (~half page) or downgrade to "Saturation Principle" / "Saturation Regularity" (already recommended in `comparative_review_2026_04_27.md` fix #4). Closes T4.

**4. [MEDIUM IMPACT, LOW EFFORT — 4 hours] Build the canonical talk slide: saturation-cliff hero.** Promote `lf6_saturation_cliff.pdf` to F1. Side-by-side with a "naïve intuition vs. our finding" inset. Closes T6.

**5. [MEDIUM IMPACT, MEDIUM EFFORT — 1-2 weeks compute] Second-EEG-dataset replication of the saturation cliff (DEAP or SEED-IV).** Even partial — 5 interventions on 1 alternate dataset showing the same monotonic destruction — would convert the saturation claim from FACED-internal to a cross-dataset regularity. This is the same fix `comparative_review_2026_04_27.md` ranked #1; we agree, but rank it lower for orals because spotlights *also* need it, and the items above (T1, T3, T4, T6) discriminate oral from spotlight more directly.

**6. [MEDIUM IMPACT, LOW EFFORT — 1 hour] Coin a name for the residual-r ↔ ensemble-contribution law.** "Residual Contribution Law: for a saturated network with within-class residual encoding of axis $v$ at $|r| = \rho$, ensemble-gain contribution scales linearly with $\rho$, $\hat\beta = 0.74 \pm 0.16$ on FACED ($p = 0.014, n=10$)." This is a quantitative law (T4) and ours alone — Arditi has nothing analogous. Closes the "we are 'Arditi-for-emotion'" critique by giving us a named result Arditi doesn't have.

**7. [LOW IMPACT, LOW EFFORT — 30 minutes] Add a "What this result is not" boxed paragraph to the introduction.** Three sentences. Mirrors O3's training-image-count caveat and O6's Sokoban-specific scope. Closes T8 by elevating it.

---

## Anti-spotlight risks (residual after fixes)

Even with all 7 fixes, three things may push reviewers from oral to spotlight:

1. **Saturation theorem will not become a *formal* theorem in 30 days.** A real proof would require either (a) a tractable model where saturation is provable analytically (1-D logistic with a known feature direction, possibly), or (b) a scaling-law fit across multiple dataset sizes and capacities. Neither is feasible at our deadline. The honest framing of fix #3 is to call it "Saturation Principle" with a formal *empirical* statement, not a *mathematical* theorem. A reviewer on the AC committee who insists on theorem-level rigor will downgrade us, and we cannot fully neutralise this without compute time.

2. **One emotion-EEG dataset.** Even with DEAP/SEED-IV (fix #5), we will have at most two emotion datasets, where LaBraM (a *spotlight*) covered ~20 in pretraining. Orals are sometimes single-dataset (O4, O5) but compensate with theoretical universality; we lean on empirical universality, which means dataset count matters more for us than for them. Hard ceiling.

3. **Davidson reframe is conservative, not exciting.** The "10× weaker frontal" claim was the most arresting brain-side result in the original draft; the conservative reframe (paradigm difference, not refutation) loses some of that punch. There is no fix that simultaneously calibrates the claim *and* keeps its excitement. We accept the trade.

---

## What the talk slide would be

**Top half:** The saturation cliff — Δ-BACC from V-axis supervision plotted against base-recipe BACC across the 25 interventions, with each intervention as a labelled point. Above the line: zero or marginal gain at weak baselines (CBraMod, EMOD-vanilla). Below the line: monotonic decrement at strong recipes. Transition window $[0.62, 0.66]$ shaded. Single arrow in the centre: "Saturation."

**Bottom half:** The probe → mechanism → causal-intervention triad as 3 mini-panels. Panel A: V-axis is the latent (one $r=0.87$ dot, one random-null cloud at $r=0.07$). Panel B: residual r predicts ensemble contribution ($r=0.74, p=0.014$ scatter, 10 dots). Panel C: causal ablation — zero out residual subspace, BACC drops as predicted (a single before/after bar from fix #2).

**Where we are now:** F1 (universal V-axis hero) + F6 (saturation cliff) exist separately. F8 (two-tier scatter) covers panel B. Panel C is the missing experiment from fix #2. Two of three triad panels are already there; the slide is one experiment and one figure-merge away.

---

## Three orals to specifically aspire to in writing style

**O3 (Kadkhodaie, Generalization in diffusion models).** Rationale: identifies a sharp universality result ("two DNNs trained on non-overlapping subsets learn nearly the same score function") and pairs it with a named mechanism (geometry-adaptive harmonic representations). Our V-axis-is-found-by-everyone result has the same structure; our mechanism (within-class residual / saturation) needs the same crisp naming.

**O6 (Bush, Interpreting Emergent Planning).** Rationale: explicit probe→mechanism→causal triad on a single model. Their methodology section reads like a checklist; reviewers love that. Our §5 (cross-arch convergence) should read this way — we should structure it as "(1) we probe, (2) we identify the residual mechanism, (3) we causally verify by ablation."

**O4 (Rooke, Trading Place for Space).** Rationale: a quantitative trade-off (capacity exponent vs. resolution) becomes the title and the punchline. Our saturation cliff is a similar-shaped finding: a transition between two regimes characterised by a single empirical scalar. Our paper's title should signal this; consider "Saturated Representations: The Limits of Concept Supervision in Emotion-Aware Models" or similar.

---

## Reviewer-resistant changes (anticipated objections + the sentence that pre-empts each)

**Objection R-A: "This is Arditi-for-emotion."**
Pre-empt sentence (place in §1 paragraph 2): *"Unlike prior work that documented single concept directions in chat models (Arditi et al., 2024), our central finding is not the existence of the V-axis but the* saturation *of its supervisory value: once present, it cannot be re-injected as a learning signal — a quantitative regularity tested across 25 interventions."*

**Objection R-B: "Single direction extracted from 9 stories is over-fit / brittle."**
Pre-empt sentence (already partially there in §3): explicit data-efficiency curve plus the existing Hu&Liu lexicon $|r|=0.76$ external-validity number. Recommend: add a 9-story leave-one-out variant to show the V-axis is stable to story choice. ~1 day compute.

**Objection R-C: "The Davidson 10× claim is a between/within-subject confound."**
Pre-empt: §6.1 already has the conservative reframe ("paradigm-level finding for video-evoked emotion … not a refutation of within-subject FAA effects"); ensure the abstract and §1 also use this language. Currently §1 still says "challenging the classical frontal-asymmetry account."

**Objection R-D: "FACED-only — does this generalise?"**
Pre-empt: the SEED-V cross-dataset class-ranking $r=0.96$ should be quoted in the abstract or §1, not buried in §4. Combined with fix #5 (partial DEAP/SEED-IV saturation sweep) this becomes a "two-dataset regularity" claim.

**Objection R-E: "$r=0.885$ class-PC1 cross-arch result is at 93rd percentile of nulls but the within-class $p=0.014$ is the only statistically robust signal."**
Pre-empt: §5.3 already discloses this honestly. Recommend: lead with the within-class residual result as the *primary* convergence claim, demote class-PC1 to supporting evidence. Currently the abstract foregrounds the higher-$r$ but less-robust class-PC1 number. Numerical re-ordering, not new content.

**Objection R-F: "'Saturation theorem' is empirical, calling it a theorem is overreach."**
Pre-empt: fix #3. Replace "theorem" → "principle" (already recommended) or upgrade to a formally-stated proposition (better for orals).

**Objection R-G: "25 interventions failed because they were all wrong, not because saturation is real."**
Pre-empt: §7.2 monotonic-destruction tables (RSA $\lambda$-sweep, Distance-CE $\tau$-sweep, etc.) already address this. Surface this in the abstract: *"Five intervention families exhibit monotonic accuracy destruction with increasing intervention strength — not a hyperparameter problem but a structural one."*

---

*~2,200 words. End of checklist.*
