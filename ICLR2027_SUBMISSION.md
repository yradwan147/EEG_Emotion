# ICLR 2027 submission status

Updated September 16, 2026: **format and page-limit checks pass**. The author-approved AI use statement is included. The separate scientific/editorial review findings remain unaddressed at the author's direction; this status is not scientific validation.

## Verified PDF and build

- Main paper: **9 pages**, including all main-text figures and tables.
- AI use statement: **page 10**, excluded from the main-text limit. Ethics and reproducibility statements also fit on page 10.
- Total PDF: **36 pages**. References start on page 11.
- Root/compiler: `main.tex`, pdfLaTeX with BibTeX. In Overleaf, sync GitHub and recompile from scratch.
- Local build: `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex`.
- Official ICLR 2027 style/dependency files remain unmodified; anonymous review mode, US Letter, Times and author-year citations are preserved.
- Fresh builds pass with no undefined citations/references, LaTeX errors or overfull boxes. Changed main-text pages and AI-statement pages were rendered and visually inspected. PDF author metadata is empty.
- Figure assets, tables, displayed equations and bibliography data are unchanged. No figure or table was moved into the appendix and no layout compression was introduced.

## Authorized changes

No main-text trimming was needed. Scientific manuscript text is unchanged; only the approved AI disclosure was added.

The paper-specific disclosure is in `ai_use_statement.tex`, included before the references. It records author-reported literature/idea assistance, implementation and interpretation, drafting, figures based on verified data, and human review at key stages. Story generation is disclosed only in Vaxis and EEG; CMKL and PrimeKG do not claim it. Use the same account for the OpenReview AI-use response.

## OpenReview author requirements

Before submitting, confirm the following against the [ICLR 2027 author guidelines](https://iclr.cc/Conferences/2027/AuthorGuidelines):

- Register the genuine abstract and complete author list by **September 18, 2026, 23:59 AoE**. Submit the full paper by **September 25, 2026, 23:59 AoE**. Authors cannot be added or removed after the abstract deadline.
- Keep all authors' OpenReview profiles and conflicts current. Authors on at least three papers must review at least six papers unless exempt. Each submission normally needs an eligible author registered to review at least three; when no coauthor is eligible, the exemption allows at most one such submission per author. NeurIPS 2026 acceptance alone is too late for eligibility at the abstract deadline.
- Confirm the NeurIPS paper is no longer under review or accepted before making the full ICLR submission. Abstract registration while awaiting NeurIPS decisions is permitted.
- Complete the AI disclosure in both the manuscript and submission form, confirm supplementary/code anonymity, and acknowledge the Code of Ethics.

Policy check: September 16, 2026. In Overleaf, use `main.tex` with pdfLaTeX and recompile from scratch after syncing GitHub.

## Anonymity recheck (September 16, 2026)

Full-PDF text and OCR checks found no identifying affiliation, personal email, cluster path or author declaration. PDF author metadata is empty; no embedded files or comment annotations are present. Normal published references are retained. All papers remain at nine main pages.

Raw working repositories, source exports and Git history must not be treated as anonymized supplements: historical/internal material can identify authors. Submit the checked PDF; prepare and audit a separate package if supplying source/code. OpenReview eligibility, reviewer registration, final author lists, conflicts, related-submission overlap and duplicate-submission status still require author confirmation.

Hidden real author blocks and unused named comment macros were removed from the LaTeX source; rebuilt PDF pages are pixel-identical to the previous version.
