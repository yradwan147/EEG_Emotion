# NeurIPS 2026 Style — Source Documentation

**Date set up:** 2026-04-27

## Style file in use

`neurips_2026.sty` (437 lines) — copied from
`/ibex/project/c2323/yousef/EEG_Emotion/neurips_2026.sty`.

Header of the .sty confirms it is the genuine NeurIPS 2026 submission package:

> partial rewrite of the LaTeX2e package for submissions to the
> Conference on Neural Information Processing Systems (NeurIPS) ...
> last revision: January 2026

This is the same file already used (and successfully compiled) by both
`EEG_Emotion/paper1_concept_probes/` and `EEG_Emotion/paper2_ensemble_trick/`
during cycle 75, so it is known-good for our environment.

## Submission mode

Default is anonymous submission (`\usepackage{neurips_2026}`).
Available switches inside `main.tex` (commented out by default):

- `\usepackage[preprint]{neurips_2026}` — for arXiv preprint
- `\usepackage[final]{neurips_2026}` — camera-ready (de-anonymized)

## Bibliography style

The .sty auto-loads `natbib`. We use:

```
\bibliographystyle{plainnat}
\bibliography{references}
```

`neurips_2026` is a *package*, not a `.bst` file, so it must not be passed to
`\bibliographystyle`. `plainnat` is the convention used by the existing
NeurIPS-2026 paper drafts in `EEG_Emotion/paper1_concept_probes/`.

## Compilation

LaTeX is provided by the Ibex `texlive/2022` module (no system pdflatex on
PATH by default):

```
module load texlive/2022
pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex
```

## Provenance check

If a fresher official 2026 sty is later released by neurips.cc, drop it in
place of `neurips_2026.sty` here — no other changes should be needed since the
sec scaffolding only uses standard LaTeX.
