# ICLR 2027 submission status

The scientific conversion is limited to formatting. No scientific prose, claims, numerical
results, figure assets, table entries, or bibliography records were removed,
rewritten, or moved between the main paper and appendix.

## Build and format

- Root: `main.tex`; compiler: pdfLaTeX with BibTeX, via `latexmk -pdf`.
- Tested with TeX Live 2025 / pdfTeX 1.40.27.
- Official unmodified ICLR 2027 style, bibliography style, `natbib.sty`, and
  `fancyhdr.sty`, copied from `iclr-2027-style-files.zip`.
- Anonymous submission mode; 10-point Times body text; US Letter pages;
  official line numbers and author-year citations.
- Normal bibliography font restored; appendix list spacing restored; one table
  minipage widened slightly to eliminate an overfull box without changing data.
- Main text, statements, references, and appendices separated with `\clearpage`,
  which flushes pending floats without discarding them. Historical NeurIPS
  checklist source remains unmodified and excluded from the PDF.

## Verified PDF

- Main scientific text: **9 pages**, within the 9-page initial submission limit.
- Existing ethics and reproducibility statements: page 10.
- References: pages 11–14.
- Appendices: pages 15–36. Total: **36 pages**.
- Successful latexmk build; no undefined citations/references or overfull boxes.
  Remaining log notices are underfull boxes and automatic `h` to `ht` float
  placement adjustments.
- All 36 rendered pages visually reviewed, including the final main-text page.
  The author block and affiliations are absent from the rendered paper, and PDF
  author metadata is empty.
- Bibliography and figure assets are unchanged. Section differences are limited
  to list spacing, the width of a table minipage, and the author-confirmed code-release timing; all scientific content is preserved.

## Outstanding author input

1. The mandatory **AI use statement** is pending the authors' disclosure. No
   claim about AI use or author verification has been invented or inserted.
   Supply the statement before final submission; it is excluded from the page
   limit and must be at most one page.
The authors confirmed that code will be released upon acceptance. The ethics
and reproducibility statements have been updated to match the existing appendix
release plan; this is the only author-requested wording correction.

Official guidance: https://iclr.cc/Conferences/2027/AuthorGuidelines

## OpenReview author requirements

Before submitting, confirm the following against the [ICLR 2027 author guidelines](https://iclr.cc/Conferences/2027/AuthorGuidelines):

- Register the genuine abstract and complete author list by **September 18, 2026, 23:59 AoE**. Submit the full paper by **September 25, 2026, 23:59 AoE**. Authors cannot be added or removed after the abstract deadline.
- Keep all authors' OpenReview profiles and conflicts current. Authors on at least three papers must review at least six papers unless exempt. Each submission normally needs an eligible author registered to review at least three; when no coauthor is eligible, the exemption allows at most one such submission per author. NeurIPS 2026 acceptance alone is too late for eligibility at the abstract deadline.
- Confirm the NeurIPS paper is no longer under review or accepted before making the full ICLR submission. Abstract registration while awaiting NeurIPS decisions is permitted.
- Complete the AI disclosure in both the manuscript and submission form, confirm supplementary/code anonymity, and acknowledge the Code of Ethics.

Policy check: September 16, 2026. In Overleaf, use `main.tex` with pdfLaTeX and recompile from scratch after syncing GitHub.
