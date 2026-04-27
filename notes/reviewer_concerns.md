# Anticipated reviewer concerns + planned responses

Living document; add new concerns as they surface in internal review.

## Methodological

- **R1 (anonymous, expected): "Why are 9 story centroids enough?"**
  Pre-empt: data-efficiency curve in Sec 3 + Hu & Liu |r| = 0.76 control.

- **R2: "Cherry-picked layer (L27)?"**
  Pre-empt: V-shape figure spanning all layers; the claim is that L27 is
  *modal* across families, not the only working layer.

- **R3: "Are the EEG alignments above chance after multiple comparisons?"**
  Pre-empt: bootstrap CIs, permutation tests, nonce-token ablation,
  random-direction control already on the books.

## Significance

- **R4: "How is this different from existing concept-probe papers?"**
  Pre-empt: the brain bridge (Sec 4 + Sec 6) is novel — the same axis lines
  up with EEG topography. No prior work shows that.

- **R5: "FACED gain is small / could be longer training alone."**
  Acknowledge directly in Sec 8. Cite the Paper-2 mechanism debunk
  (cycle 75). Position the SOTA as a *demonstration* of the axis, not the
  selling point.

## Reproducibility

- **R6: "Seeds, splits, hardware?"**
  Appendix A + reproducibility checklist (already required by NeurIPS).

- **R7: "Will probes / centroids be released?"**
  Yes; commit to releasing the 9 centroids and the EEG alignment scripts.
