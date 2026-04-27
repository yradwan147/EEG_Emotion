# Writing Audit — 2026-04-27 (Round 2)

**Auditor**: writing-audit subagent
**Goal**: ensure every 🟢 paper-grade finding from `all_findings_catalog.md` is
either present in the paper or justifiably omitted; tighten narrative
seams; judge whether SOTA framing reads cleanly.
**Build state at end**: 35 pages, 0 errors, 0 undefined references, bibtex clean.

---

## Executive summary

The paper was already structurally complete (11 sections, 1983 LOC). Round 2
audit applied targeted polish edits to surface several 🟢-tier findings that
were missing or underweighted, tightened §4↔§6 overlap on the 9-stim contrast,
and consolidated the duplicate CPC citation key. The SOTA framing was
**preserved** rather than reframed — current §8 already opens with "The
saturation theorem of Section~\ref{sec:saturation} is not just a negative
result. It implies a positive prescription," which positions SOTA as the
direct corollary the user wanted.

---

## SOTA framing decision and rationale

**Decision**: Keep the +21.5%-over-CBraMod / +10.6%-over-EmotionKD framing
intact.

**Rationale**: The current §1 / §8 / abstract narrative already does the work
the user worried about. Specifically:

1. The contributions list orders things as `Universality → Convergence →
   Topography → Saturation → SOTA`, with SOTA labeled "Principled ensembling
   around the universal latent." That phrasing is already a corollary frame.
2. §8 opens by deriving SOTA from saturation theorem ("the only remaining
   lever is within-class V-axis variance, which is exactly what averaging
   seeds exploits").
3. The two-tier theory (Section 5 within-class residual r=+0.74 ↔ ensemble
   contribution) and §8's mega-ensemble null mechanically tie SOTA gain to
   the V-axis story.
4. The vanilla-EMOD 0.629 vs vanilla-CBraMod 0.572 framing the user
   mentioned IS already present — the cascade table walks from CBraMod 0.572
   to ensemble SOTA via single-component steps; vanilla EMOD-d3 at 0.6194 is
   row 1 of the cascade.

If a reviewer reads §1+§8 only, they get: "V-axis is universal; models
converge to it; aligning to it as supervision fails (saturation); ensembling
around the residual is the right mechanism, and that gives a new SOTA." The
SOTA is not a parallel headline; it is the engineering payoff of the
mechanism.

If we ever did reframe, the cleanest dial would be a single line in the
abstract retitling the SOTA paragraph as "We turn this *into* a new SOTA"
(currently "We *turn* this principle into a new state-of-the-art on FACED
9-class emotion classification") — already in place.

---

## Edits applied

### §3 (`03_v_axis_in_llms.tex`)

**Edit 1**: Expanded the compositionality subsection into
"Compositionality and concept-library generality." Added the 17/20 concepts
at AUC≥0.95 finding (catalog row 3.26) and the toxicity AUC=0.59 caveat
(catalog row 3.28). _Why_: the concept-library result was a 🟢 row that
substantiates the "this is a generic recipe, not a hand-tuned valence
trick" claim.

**Edit 2**: Added a new `\subsection{Specificity controls}` with two pieces:
- Nonce-word ablation (catalog row 3.35): real-words 0.868 → nonce 0.524
  chance. _Why_: this is an essential sanity-check that distinguishes
  semantic content from prompt-template artefacts; was missing.
- Arousal asymmetry (catalog row 3.10 + 3.42): valence transfers, arousal
  collapses on text/brain (despite vision success). _Why_: 🟢 caveat that
  recurs in §9 limitations; needed to be foreshadowed in §3 as scope of
  claim, not parked only in discussion.

**Edit 3**: Updated section summary to add (vi) "generic — same recipe
recovers 17 of 20 concepts" and reference the nonce control.

### §4 (`04_v_axis_in_brain.tex`)

**Edit 1**: Added a "Reliability and granularity" paragraph reporting
- per-stim split-half $r=0.988$ (catalog 4.7, was missing)
- trial-level $r=0.17{-}0.21$ at $n=3{,}444$ (catalog 4.5, was missing)
- class-level $r=+0.886$ vs. behavioural valence (catalog 4.6, was missing)

_Why_: review_round1 didn't flag these but they're 🟡 anchors that ground
the cohort $r=0.87$ headline in measurement at every aggregation level.
Reviewers will ask "is this real at the trial level?" — now it's preempted.

**Edit 2**: Compressed the §4 9-stim drop-class paragraph from a verbatim
table preview to a single sharper paragraph that forward-references §6's
full table. _Why_: review_round1 issue B1 — §4 and §6 had overlapping 9-stim
content; now §4 has the claim, §6 owns the dissection.

### §5 (`05_cross_arch_convergence.tex`)

**Edit 1**: Added per-architecture class-PC1 mean breakdown (CBraMod 0.21,
EMOD-d6 0.67, EMOD-d6-e150 0.69) to the "Both metrics correlate" subsection.
_Why_: catalog rows 5.6–5.8 are 🟡 supporting; useful one-line clarification
that the linear band is real and stratified by architecture, not just noise.

### §6 (`06_brain_topography.tex`)

**Edit 1**: Added "Analytical ceiling" paragraph quantifying the 9-stim
weighting → r=0.714 ceiling. _Why_: catalog 6.9 is 🟡 but it is the bridge
to §7's anger-paradox subsection. Without it, §7's "the analytical ceiling
goes from 0.478 to 0.714" appears with no setup. Now §6 establishes the
analytical-ceiling concept; §7 invokes it.

### §1 (`01_introduction.tex`)

**Edit 1**: Consolidated `oord2018representation` → `vandenoord2018cpc`
(review_round1 noted likely duplicate). Single canonical key now used
across §1 and §7.

---

## 🟢 finding audit table

Status legend: `IN` (already in paper before round 2) · `ADDED` (added in
this audit) · `OMITTED` (intentionally not in paper, with reason).

### §3 (V-axis in LLMs)

| Finding | Status | Notes |
|---|---|---|
| 3.0 9-emotion centroid PCA protocol | IN | §3.1 (Extraction protocol) |
| 3.1 SST-2 AUC=0.868 zero-shot | IN | §3 table |
| 3.7 Hu&Liu \|r\|=0.76 | IN | §3 prose |
| 3.8 NRC \|r\|=0.79 (small lex) | IN (rounded to 0.79) | §1, §3 |
| 3.9 Warriner \|r\|=0.66 | IN | §3 prose |
| 3.10 Arousal axis fails text | ADDED | §3 specificity controls |
| 3.11 18-LLM r=0.654 mean off-diag | IN | §3 universality |
| 3.12 Inverted-U Qwen-1.5B optimal | IN | §3 universality |
| 3.13 6 LLM families confirmed | IN | §3 universality |
| 3.14 Gemma-4 L1 outlier | IN | §3 V-shape |
| 3.17 V-shape L27 emergence | IN | §3 V-shape |
| 3.18 V-shape replicates cross-family | IN | §3 V-shape |
| 3.19 Latent-space metrics (PCA-var, eff-rank) | OMITTED | catalog 🟢 but appendix-quality detail; would dilute §3 |
| 3.20 n=1 already works (data efficiency) | IN | §3 protocol mentions n=1 0.74 |
| 3.21 Few-label curve / supervised LR @ N=80 | OMITTED | the AUC 0.868 > LR @ 5k 0.837 statement IS the headline; the @N=80 micro-detail belongs to appendix |
| 3.23 V_polite + V_happy 79% | IN | §3 compositionality |
| 3.26 17/20 concepts AUC≥0.95 | ADDED | §3 compositionality+concept-library |
| 3.28 Toxicity fails AUC 0.59 | ADDED | §3 (and §9 future-work in spirit) |
| 3.31 mT0 multilingual closes asymmetry | IN | §3 multilingual |
| 3.35 Nonce-word ablation chance | ADDED | §3 specificity |
| 3.39 OASIS V-axis beats supervised | IN | §3 cross-modal |

### §4 (V-axis in brain)

| Finding | Status | Notes |
|---|---|---|
| 4.1 Cohort r=0.87, p<10⁻⁹ | IN | §4 cohort alignment |
| 4.4 Random-direction r=0.07 null | IN | §4 random control |
| 4.5 Trial-level r=0.17–0.21 | ADDED | §4 reliability |
| 4.6 Class-level r=+0.886 vs behavioural | ADDED | §4 reliability |
| 4.7 Per-stim split-half r=0.988 | ADDED | §4 reliability |
| 4.8 18-LLM brain prediction | IN | §4 18-LLM table |
| 4.11 Gemma-4 boundary check L17 r=0.819 | IN | §4 Gemma boundary |
| 4.13 FACED→SEED-V transfer r=+0.96 | IN | §4 cross-EEG |

### §5 (Cross-arch convergence)

| Finding | Status | Notes |
|---|---|---|
| 5.1 Class-PC1 r=+0.885 | IN | §5 main claim |
| 5.2 Within-resid r=+0.715 | IN | §5 main claim |
| 5.3 Per-ckpt within-resid ↔ LOO r=+0.743 p=0.014 | IN | §5 within-class mechanism |
| 5.4 Top-7 0.6962 vs bottom-7 0.6829 | IN | §5 within-class mechanism |
| 5.5 Random-direction null at 93rd %ile | IN | §5 honest scope |
| 5.6–5.8 Per-arch class-PC1 r breakdown | ADDED | §5 prose |

### §6 (Brain topography)

| Finding | Status | Notes |
|---|---|---|
| 6.1 occipital 0.21 > frontal 0.16 | IN | §6 region-mean |
| 6.2 PO3/γ +0.48, F7/β -0.47, O1/γ +0.44 | IN | §6 top channels |
| 6.4 Davidson F4-F3 α=+0.006 (10× weaker) | IN | §6 FAA |
| 6.6 Removing Anger drops r by -0.151 | IN | §6 9-stim |
| 6.7 9-stim Anger+Amus+Tend r=+0.870 | IN | §6 9-stim |
| 6.8 Excluding 9-stim r=-0.015 | IN | §6 9-stim |
| 6.9 Anger-weighted analytical ceiling r=0.714 | ADDED | §6 analytical ceiling |
| 6.10 Cohort r=0.48 vs per-subj -0.06 (Simpson) | IN | §6 simpson |
| 6.11 Per-subject oracle \|r\|=0.616 | IN | §6 simpson |
| 6.14–6.16 Time-resolved peaks (α=21s, β=18s, γ=3s) | IN | §6 time-resolved |
| 6.17 Func conn r=0.675 | IN | §6 connectivity |
| 6.18 PAC null p=0.667 | IN | §6 theta-gamma |
| 6.19 MI not sig p=0.115 | IN | §6 MI section |

### §7 (Saturation theorem)

| Finding | Status | Notes |
|---|---|---|
| 7.1–7.7 13 sig-negative interventions | IN | §7 negatives table + appendix |
| 7.16–7.20 Monotonic destruction (5 families) | IN | §7 monotonic table |
| Anger-weighted hurts despite analytical ceiling (mechanism check) | IN | §7 anger-paradox |
| Mechanism check: V-axis training raises class-PC1 +0.01 to +0.36, residual ~10⁻⁸ | IN | §7 mechanism check |
| Saturation transition (CBraMod / EMOD-d3 / strong-recipe) | IN | §7 transition table |
| Path B: V-axis ckpts hurt vanilla 10-ckpt ensemble | IN | §7 Path B |

### §8 (SOTA + ensembling)

| Finding | Status | Notes |
|---|---|---|
| 8.1–8.13 Recipe cascade CBraMod 0.572 → ensemble 0.6948 | IN | §8 cascade table |
| 8.13 Single-checkpoint val-selected 0.6755 | IN | §8 best single |
| 8.14 val→test rank Spearman 0.825 | IN | §8 best single prose |
| 8.15 Mega-ensemble null | IN | §8 mega-ensemble |
| 8.17 Two-tier theory | IN | §8 two-tier subsection |
| 8.18 100ep vs 150ep tied means, diversity gain only | IN | §8 cascade table footnote |
| 8.19 Cross-group disagreement +10.3pp | IN | §8 two-tier |
| 8.22–8.25 SEED-V / CIFAR-10 / MNIST generality | IN | §8 generality subsection |
| 8.29–8.31 Compute-optimal law (workshop tier) | OMITTED | catalog labels these 🟡 (workshop / appendix); we keep them out of main paper to stay focused |

### §9 (Discussion)

| Finding | Status | Notes |
|---|---|---|
| Cross-arch null at 93rd %ile (honest) | IN | §9 honest negatives |
| Arousal asymmetry (image vs brain) | IN | §9 honest negatives |
| MI not significant | IN | §9 honest negatives |
| CFC null (theta-gamma) | IN | §9 honest negatives |

### §10 (Appendix)

| Finding | Status | Notes |
|---|---|---|
| A.1 Full 25-row intervention table | IN | §10 (currently 27 rows incl. SOTA-recipe variants) |
| A.4 Confusion matrices | IN | §10 (figure shell, awaits figure file) |
| A.5 Reproducibility manifest | PARTIAL | §10 has SLURM/seed list, full manifest is owned by repro agent |

---

## Narrative-level changes

**§3 → §4 transition**: Now reads "with this universal axis in hand, we turn
to its presence in the human brain" → "we now show that the V-axis ...
predicts human EEG responses." Smooth.

**§4 → §5 transition**: §4 ends "the next section establishes that the brain
encodes this axis predominantly in posterior visual cortex" but the next
section is actually §5 (cross-arch convergence). Looking at this more
carefully: the *reading* order is §4 (brain) → §5 (cross-arch) → §6
(topography) → §7 (saturation) → §8 (SOTA). So §4's closing should bridge
to §5, not §6.

Caught this issue but **deferred fix** because it requires re-reading the
intended section ordering with the parent agent. Current §4 closing line
points to §6's content, which in the reader's flow comes one section later.
Will flag in followup section.

**§5 → §6 → §7 → §8 transitions**: §5 closes with "The next two sections
make the picture mechanistic — where in cortex the V-axis lives (§6), and
what happens when we try to inject it as supervision into already-converged
models (§7)." This is correct and clean. §6 closes by handing off to §7.
§7 closes by handing off to §8 ("The next section operationalises this
theory into our SOTA ensemble result"). §8 closes with "We close the paper
by situating these findings in the broader representation-alignment
literature." Bridges good.

**Repetition between §4 and §6**: Cleaned up. §4 now states the 9-stim
claim in 1 paragraph and forward-references §6's table; §6 owns the table
+ analytical ceiling + Simpson dissection.

**Repetition between §5 and §8**: §5 establishes the within-class residual
mechanism; §8 invokes it as "Section~\ref{sec:within-class-mechanism}
established that 10 vanilla d=6 checkpoints share..." This is appropriate
re-statement, not redundant exposition. Kept as is.

**Voice consistency**: Active throughout, confident without
self-deprecation. Hedge balance preserved (only the cross-arch null at
93rd-percentile and the MI null appear as honest hedges). Good.

**Paragraph rhythm**: Most paragraphs are 4–8 lines. No walls of text. No
single-sentence stub paragraphs.

---

## Followup items / not blockers

1. **§4 closing line** points to topography content (correct topically but
   the *next* section in reading order is §5 cross-arch). Either: (a) reorder
   to put §6 directly after §4 (currently §6 is _after_ §5), or (b) update
   §4's closing line to bridge to §5 cross-arch convergence first. Suggest
   option (b) since the §5 cross-arch story is a natural continuation of
   "brain alignment" → "models that learn this brain alignment." Single
   1-sentence edit when parent agent confirms section order is locked.

2. **Figures**: The figure shells and `\IfFileExists{...}` fallbacks are
   in place. When landmark figures land, no edits needed in .tex; pdflatex
   will pick them up automatically.

3. **Compute-optimal law (catalog 8.29–8.31)** intentionally omitted from
   main paper per catalog 🟡 marking; if the parent agent wants a workshop
   submission, that material is appendix-ready in `headline_numbers.md`.

4. **Class-level vs stim-level contradiction (catalog 5.10)** is implicit
   in §5's discussion of class-PC1 vs within-class residual; could be
   surfaced explicitly with one paragraph if reviewers ask "why are
   stim-level and class-level r values different?" — currently not in main
   text.

5. **Long-tail catalog rows 7.21–7.42**: Most live in the appendix table
   (full 25-row + 2 SOTA-recipe rows). Not all 35 rows are individually
   broken out in the appendix table; the main `tab:full-vaxis` covers the
   25 headline rows + 2 cliff rows. If a reviewer counts "you said 25 but
   the appendix shows 27," the answer is: the 25 are the recipe-internal
   sweep; the 2 cliff rows are the SOTA-recipe replications confirming the
   transition. Caption already says "Below the line are the SOTA-recipe
   replications confirming the saturation cliff."

---

## Build verification

Final state:
- `pdflatex main.tex` clean, no errors
- `bibtex main` clean (0 warnings, 0 missing keys)
- 35 pages, 1.37MB PDF
- All cross-references resolve
- Bibliography clean (consolidation of `oord2018representation` →
  `vandenoord2018cpc` complete)
