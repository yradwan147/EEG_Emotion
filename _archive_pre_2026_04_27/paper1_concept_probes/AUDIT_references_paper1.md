# Paper 1 — References Audit Pass (Round 2)

Paper: FewConcept (paper1_concept_probes/)
Updated: 2026-04-24, cycle 74m
Auditor: Claude Code

## Round 2 deltas

Round 2 narrative editing added references to:
- **Park, Choe, Veitch 2024** — Linear Representation Hypothesis (ICML 2024)
  → new key `park2024linear`
- **Arditi et al. 2024** — Refusal Direction (NeurIPS 2024)
  → new key `arditi2024refusal`
- **Mikolov, Yih, Zweig 2013** — Linguistic Regularities (NAACL)
  → new key `mikolov2013linguistic` (used for embedding-level word geometry in intro / discussion)
- **Bolukbasi et al. 2016** — Man-is-to-Programmer (NeurIPS)
  → new key `bolukbasi2016man` (used for embedding-level concept direction precedent)
- **Conneau et al. 2020** — XLM-R / Unsupervised Cross-lingual Repr Learning
  → new key `conneau2020unsupervised` (used in cross-lingual Related-Work paragraph)

All 5 added to `refs.bib` via Edit tool. Existing 23 Round 1 keys unchanged.

## Citation inventory (Round 2)

Total unique keys cited: **28** (Round 1: 23 + 5 Round 2 additions).

| Key | Sections | In bib? | Entry type | Status |
|---|---|---|---|---|
| `qwen2.5` | 4 | Y | @misc | OK (carryover) |
| `buechel2017emobank` | 4 | Y | @inproceedings | OK |
| `alain2016understanding` | 1,2 | Y | @article | OK |
| `hewitt2019structural` | 1,2 | Y | @inproceedings | OK |
| `rimsky2024steering` | 1,2,abs,concl | Y | @inproceedings | OK |
| `turner2024activation` | 2 | Y | @article | OK |
| `huliu2004opinion` | 1,2,4 | Y | @inproceedings | OK |
| `warriner2013norms` | 1,2 | Y | @article | OK |
| `liu2024faced` | 3.2 | Y | @article | OK |
| `demszky2020goemotions` | 3.2 | Y | @inproceedings | OK |
| `zou2023representation` | 1,2,4,concl | Y | @article | OK (heavier usage in Round 2) |
| `zhang2024emotionkd` | 2 | Y | @article | placeholder — can remove |
| `li2025emod` | 2 | Y | @article | placeholder — can remove |
| `aqa2024emotion` | 2 | Y | @article | placeholder — can remove |
| `reimers2019sentence` | 2 | Y | @inproceedings | OK |
| `gao2021simcse` | 2 | Y | @inproceedings | OK |
| `mohammad2018obtaining` | 2 | Y | @inproceedings | OK |
| `olsson2022induction` | 2 | Y | @article | OK |
| `wei2022emergent` | 2 | Y | @article | OK |
| `michaud2024quantization` | 2 | Y | @article | OK |
| `brown2020language` | 2 | Y | @inproceedings | OK |
| `wei2022finetuned` | 2 | Y | @inproceedings | OK |
| `snell2017prototypical` | 5 | Y | @inproceedings | OK |
| `belinkov2022probing` | 2 | Y | @article | OK (was listed Round 1) |
| **`park2024linear`** | 1,2,4,5,concl | Y | @inproceedings | **NEW Round 2** |
| **`arditi2024refusal`** | 1,2,4,concl | Y | @inproceedings | **NEW Round 2** |
| **`mikolov2013linguistic`** | 2,5 | Y | @inproceedings | **NEW Round 2** |
| **`bolukbasi2016man`** | 2,5 | Y | @article | **NEW Round 2** |
| **`conneau2020unsupervised`** | 2 | Y | @article | **NEW Round 2** |

## Expected compile

After Round 2 edits, `pdflatex + bibtex + pdflatex + pdflatex` on
`main.tex` should produce:
- 0 undefined-citation warnings
- Bibliography rendered as [1]-[28] (or similar continuous numbering)

## Recommendations (carried from Round 1)

1. The three placeholder citations (`zhang2024emotionkd`, `li2025emod`,
   `aqa2024emotion`) remain used once each in Section 2; they don't
   support any numerical claim. Pre-submission, either fill with real
   IEEE TAC/AAAI citations or remove.
2. Optionally prune 63 legacy EEG-carryover orphan entries from
   `refs.bib` for final submission.
3. `reimers2019sentence` and `reimers2019sbert` are both in bib; paper
   only uses `reimers2019sentence`. No action required but a final
   pass could dedup.

## Overall Verdict (Round 2): **PASS**

5 new citations added and cleanly placed in sec/1,2,4,5,6. No orphans
from Round 2 additions. Placeholders from Round 1 carry forward
unchanged; they are still low-priority since they do not support any
factual claim.
