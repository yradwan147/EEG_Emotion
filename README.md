# ICLR 2027 — EEG Emotion

**The Saturation Regularity: When Concept-Aligned Supervision Stops Helping Converged EEG Classifiers**

`main.tex` is the LaTeX root. The default build uses the official ICLR 2027
anonymous submission style, author-year citations, Times text, and US Letter pages.
The author block stays in the source for later camera-ready use and is hidden in
submission mode. Leave `\iclrfinalcopy` disabled for review.

## Build

Use pdfLaTeX and BibTeX through latexmk (tested with TeX Live 2025):

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

For Overleaf, select `main.tex` as the main document and pdfLaTeX as the compiler.
The tracked `main.pdf` is the compiled submission draft.

## Layout

- `sections/`: main text, existing ethics/reproducibility statements, and appendix.
- `figures/`: original figure assets.
- `references.bib`: original bibliography data.
- `iclr2027_conference.sty`, `iclr2027_conference.bst`, `natbib.sty`, and
  `fancyhdr.sty`: unmodified files from the official ICLR 2027 style archive.
- `sections/checklist.tex`: historical NeurIPS checklist retained as source only;
  it is not included in the ICLR PDF.

See [ICLR2027_SUBMISSION.md](ICLR2027_SUBMISSION.md) for measured page counts,
validation, and outstanding author disclosures.
