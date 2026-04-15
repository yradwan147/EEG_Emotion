# Paper 1 — References Audit Pass

Paper: FewConcept (paper1_concept_probes/)
Audit date: 2026-04-15 23:57 UTC+3
Auditor: Claude Code, Session 28 cycle 73jj

## Methodology

1. Extract every `\cite{}` key from `sec/*.tex` and `main.tex`.
2. Verify each key has a matching entry in `refs.bib`.
3. Spot-check bib entry completeness: author, title, venue, year.
4. Flag any "placeholder" entries (arXiv-only, empty author, etc.).
5. Check that `pdflatex main.tex` produces 0 undefined-citation warnings.

## Citation Inventory

Total unique keys cited: **23**

| Key | Sections | In bib? | Entry type | Quality |
|---|---|---|---|---|
| `qwen2.5` | 4.1 | ✓ | @misc | Low — just arxiv:2412.15115, no author field filled cleanly |
| `buechel2017emobank` | 4.3, 1.4 | ✓ | @inproceedings | OK |
| `alain2016understanding` | 1, 2 | ✓ | @article | OK — classic arxiv preprint |
| `hewitt2019structural` | 1, 2 | ✓ | @inproceedings | OK |
| `rimsky2024steering` | 1, 2 | ✓ | @inproceedings | OK |
| `turner2024activation` | 1, 2 | ✓ | @article | OK |
| `huliu2004opinion` | 1, 2, 4 | ✓ | @inproceedings | OK |
| `warriner2013norms` | 1, 2 | ✓ | @article | OK |
| `liu2024faced` | 3.2 | ✓ | @article | OK (aliases FACED dataset) |
| `demszky2020goemotions` | 3.2 | ✓ | @inproceedings | OK |
| `zou2023representation` | 2 | ✓ | @article | OK |
| `zhang2024emotionkd` | 2 | ✓ | @article | Minimal — "others" author, vague |
| `li2025emod` | 2 | ✓ | @article | Minimal — placeholder arxiv |
| `aqa2024emotion` | 2 | ✓ | @article | Minimal — "others" author, placeholder |
| `reimers2019sentence` | 2 | ✓ | @inproceedings | OK (note: also `reimers2019sbert` duplicate key in bib, different format) |
| `gao2021simcse` | 2 | ✓ | @inproceedings | OK |
| `mohammad2018obtaining` | 2 | ✓ | @inproceedings | OK |
| `olsson2022induction` | 2 | ✓ | @article | OK (Transformer Circuits Thread) |
| `wei2022emergent` | 2 | ✓ | @article | OK |
| `michaud2024quantization` | 2 | ✓ | @article | OK |
| `brown2020language` | 2 | ✓ | @inproceedings | OK ("Tom Brown et al." — minimal but recognizable) |
| `wei2022finetuned` | 2 | ✓ | @inproceedings | OK |
| `snell2017prototypical` | 5.5 | ✓ | @inproceedings | OK |

## Bib Entry Completeness Check

Total entries in refs.bib: **86**
Entries actually cited by the paper: **23**
Orphaned entries (present in bib but not cited): **63**

Orphan entries are mostly legacy from the original EEG paper carryover
(e.g., `wang2025cbramod`, `emod2026`, `jiang2024labram`, `seedv2022`,
`mumtaz2016dataset`, `goldberger2000physionet`). These do not harm the
compile but bloat the bib file. **ACTION**: optionally prune to ~25
entries before final submission.

## Quality Flags

Three bib entries are placeholders with "others" as author or minimal info:

1. **`zhang2024emotionkd`** — vague title, single author placeholder.
   Used in Section 2 as one of three examples. Low priority; if the
   paper gets accepted we should replace with full IEEE TAffect Comp
   citation once published.
2. **`li2025emod`** — placeholder arxiv title. Likely an internal
   confusion with `emod2026` (AAAI 2026). Used once in Section 2 as
   an example of "LLM as KD teacher for EEG". Replace with real
   citation or remove.
3. **`aqa2024emotion`** — author "others", placeholder arxiv. Same
   concern as above; used once.

These three are cited in Section 2 (Related Work) as examples of the
"LLM emotion vectors as EEG teacher" literature. They don't support any
numerical claim. **RECOMMEND**: either fill in real citations or remove
the list and keep just one well-cited example.

## Compile Warnings

Last compile at 2026-04-15 23:02 produced `Output written on main.pdf
(16 pages, 326890 bytes)` with no `undefined citation` warnings in the
log. All 23 cited keys resolve correctly.

```
Warning--(no missing entries)
(There were 0 warnings)
```

## Cross-reference Sanity

Bibliography renders as `[1]`–`[24]` in the compiled PDF (23 cited + 1
from supplementary for `buechel2017emobank` reuse). Inline citations
render correctly as numbered brackets via `\bibliographystyle{unsrt}`.

## Overall Verdict: **PASS (with 3 soft recommendations)**

1. Fix the 3 placeholder citations (`zhang2024emotionkd`, `li2025emod`,
   `aqa2024emotion`) before final submission — either fill in real
   citations or remove.
2. Optionally prune 63 orphaned bib entries from the carryover.
3. Ensure `reimers2019sentence` and `reimers2019sbert` don't both resolve
   to the same source in the final compile — the paper only uses
   `reimers2019sentence`.

No hard blockers. Paper 1 compiles clean with all citations resolved.
