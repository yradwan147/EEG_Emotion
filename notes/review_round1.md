# Round 1 Paper Review — issues, fixes, follow-ups

## Critical numerical conflations

**A1. Abstract conflates two distinct r-values.** Lines 19-23 currently say
"accuracy correlates with V-axis encoding strength at r=+0.74 (p=0.014) in
the within-class residual subspace." But:
  - BACC ↔ within-class residual r = +0.715 (no significance reported)
  - Within-class residual r ↔ ensemble contribution Δ_k = +0.743, p=0.014
The +0.74 with p=0.014 is the second correlation, not the first.
**Fix**: split sentence cleanly — "BACC correlates with V-axis encoding
strength at r=+0.715 (within-class residual); per-checkpoint within-residual
|r| predicts ensemble contribution at r=+0.74, p=0.014."

**A2. Introduction line 53**: "cohort signal of r=0.48 at the fixed best
channel hides a per-subject mean of -0.06". §6 reports cohort r=+0.021 at
fixed top-8 channels and per-subject mean -0.062. The "0.48" refers to
the single best (channel, band) cell, not to the fixed-top-8 cohort. The
juxtaposition is misleading. **Fix**: change to "cohort top-8 fixed channels
gives r=+0.02 vs. per-subject mean r=-0.06" or be explicit that the 0.48
is the cohort best-cell while the -0.06 is per-subject at fixed channels.

**A3. Introduction line 64-65**: "$r=+0.715$ in the within-class residual"
But the abstract says +0.74 with p=0.014. The +0.715 is BACC↔within-residual;
the +0.74 is within-residual ↔ LOO contribution. Need consistent framing.

## Reference issues

- 40 missing bibtex keys (citation agent dispatched). Once that returns,
  re-run pdflatex for clean build.
- Likely duplicates between `vandenoord2018cpc` and `oord2018representation`
  (both Van den Oord 2018 CPC paper). Consolidate to one key.

## LaTeX / build issues

- Em-dash unicode: replaced with `---`. Done.
- Müller umlaut: replaced with `M\"uller`. Done.
- ↔ unicode in §02 line 73: replaced with `$\leftrightarrow$`. Done.

## Section-level coherence issues

**B1. §4 (in_brain) and §6 (topography) overlap heavily** on:
  - 9-stim contrast table (both have it)
  - 18-LLM brain ranking (only in §4)
  - Random-direction control (in §4)
  - Time-locked dynamics (in §4 brief, §6 detailed)
  - Davidson FAA (§6 only)
**Decision**: §4 should be the high-level claim ("V-axis predicts EEG"),
§6 the dissection (where, how, per-subject). Move the 9-stim table out
of §4 and reference §6's table; tighten §4 to 1.5 pages as planned.

**B2. §5 within-class mechanism intro implies the random-direction null
softens the cross-arch claim** but the section then leads with the
saturated class-PC1 r=+0.885. Reorder so the within-class residual is
the headline, class-PC1 is supporting/null-noted.

**B3. §7 saturation lists 25 interventions but the table has 13 + 12 = 25**
verified. Caption says "Statistically significant negative interventions
(13 / 25 cases)". Correct.

**B4. §9 discussion mentions "arousal extraction yields per-LLM
directions with comparable text-domain quality but substantially lower
brain alignment (r ∈ [0.18, 0.41])"** — need to verify these arousal
numbers are in the worklog. If not, soften or cite.

## Tone consistency

- Abstract is confident throughout. ✓
- Introduction: "without being asked" and "find the LLM valence axis on
  their own" are good rhetorical anchors. ✓
- §7 uses "Twenty-five interventions, one verdict" subtitle which is
  strong. ✓
- §9 limitations section is honest without being self-deprecating. ✓

## Missing pieces

- No "Figures" referenced in any section yet (figures \ref{fig:...}).
  Need to add after landmark figures land.
- §6 references `\citep{sani2024crosssubject}` but this entry may be
  hallucinated; agent #466 will verify.
- §1 contributions list could end with a one-line summary "We thus unify
  three previously separate phenomena under a single principle." That
  sentence currently ends the abstract; consider repeating or rotating.

## Style nits

- §1 line 91: "raises EMOD beyond the published baseline (0.6287)" — but
  we should be more precise: V-axis raises CBraMod 0.572 → 0.578 (single
  seed only) and EMOD-d3 vanilla 0.624 → 0.626-0.630 (n.s. positives).
  The current phrasing implies a stronger effect than we have. **Fix**:
  "V-axis loss does not significantly hurt EMOD-vanilla (Δ ≈ 0,
  $p > 0.2$) but significantly hurts the strong recipe (Δ ≈ -0.02,
  $p < 0.05$)."

- §3 line 38: parenthetical "(Qwen2.5 0.5B--72B, ...)" should not break
  out of the sentence; consider grouping into a footnote.

- §6 has "documents an important Simpson's-paradox dynamic: the cohort
  signal of r=0.48 at the best fixed channel hides a per-subject mean
  of -0.06" — same issue as A2, the comparison apples and oranges.

## Round 1 verdict

The paper draft is structurally complete. All 11 sections present (00-10),
1865 lines total. Builds cleanly modulo missing bibtex (in flight) and
the abstract/§1 r-value conflation noted above. Round 1 passes on
narrative integrity; Round 2 will tighten the numerical conflations.
