# NeurIPS 2026 — Universal Valence Axis paper

Working title: **Universal Valence Axis: From Language Models to Human EEG**

This is the active, single-source-of-truth paper directory created on
2026-04-27. All earlier paper drafts live in `_archive_pre_2026_04_27/`.

## Layout

```
paper_neurips26_final/
├── _archive_pre_2026_04_27/   # All pre-2026-04-27 paper work, untouched
├── neurips_2026.sty           # Style file (see STYLE_INFO.md)
├── STYLE_INFO.md              # Provenance of the style file
├── main.tex                   # Top-level shell, \input{sections/...}
├── sections/                  # 00_abstract.tex ... 10_appendix.tex
├── figures/                   # Figure files land here
├── references.bib             # Empty; populate from audited list
├── notes/
│   ├── narrative.md           # Story spine
│   ├── headline_numbers.md    # Verified numbers + source artefacts
│   ├── reviewer_concerns.md   # Anticipated reviews + responses
│   └── abstract_draft.md      # Working abstract drafts
└── README.md                  # this file
```

## Build instructions

LaTeX is provided via the Ibex `texlive/2022` module:

```
module load texlive/2022
cd /ibex/project/c2323/yousef/paper_neurips26_final
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

The current `main.tex` is a placeholder shell. Section bodies are stubs;
fill them in incrementally.

## Source of truth

- **Numbers** — `notes/headline_numbers.md` (every claim traceable to a JSON
  artefact under `/ibex/project/c2323/yousef/reports/`).
- **References** — populate `references.bib` only from
  `_archive_pre_2026_04_27/reports_paper_md/PAPER_REFERENCES_AUDITED.md`.
  Per the cycle-75 audit, drop these hallucinated entries entirely:
  `li2025emod`, `aqa2024emotion`, `gemma4_2026`.

## Conventions

- One section per file under `sections/`, numbered `NN_name.tex`.
- All figures go in `figures/` (auto-found via `\graphicspath{{figures/}}`).
- No edits to worklog or memory from this directory.
- Do NOT run paper edits during overnight experiment cycles
  (per `feedback_no_paper_updates_overnight.md`).
