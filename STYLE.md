# STYLE — Computational Classnotes math documents

House style for every math document made for Computational Classnotes. The reference example is `docs/laplacian-curvature.md` / `.pdf` and its Claude Doc, "The Laplacian and Curvature — Instances and Relationships".

© 2026 Computational Classnotes · CC BY-NC-SA 4.0

---

## 1. The document (Claude Doc)

1. **Title**, then a byline line: date · Computational Classnotes · project name.
2. **Lead paragraph** that states the result, not "this document outlines". Then one sentence on how the document and its notebook fit together.
3. **Scope and conventions**: a short bullet list covering sign conventions, normalisations, the notebook ↔ document section map and the repository.
4. **At a glance**: one diagram near the top showing how the parts relate. Its title states the finding, and one sentence of reading goes under it.
5. **Numbered sections**, one relationship or idea each:
   - A heading that makes a claim ("Mean curvature is a Laplacian").
   - One or two sentences of statement.
   - The key formula as a display formula (LaTeX block, never inline).
   - A sentence or two on consequences and connections, citing other sections as §n.
   - A closing bold **Checked (notebook §n):** line with the values the Wolfram kernel actually returned.
6. **Verified results table**: one row per test case, units or meaning in the headers, and a sentence under it on totals and equality cases.
7. **References**, grouped by area. Every item is linked to a page that was actually opened; standard texts that weren't opened are marked as such.
8. **Copyright line** at the end: © Computational Classnotes · CC BY-NC-SA 4.0.

Writing: short plain sentences (under 25 words), paragraphs of three sentences or fewer, specific numbers over adjectives. In the user's writing, use "conversational-construct", never "LLM".

## 2. The companion Wolfram notebook

- One notebook section per document section. A shared toolkit goes in §1, so the notebook is document §n ↔ notebook §n+1.
- Each section has a Text cell restating the claim, then Input cells, ending in a check that returns True, 0, or the number quoted in the document.
- **Geometric graphics and worked examples for every instance.** Each notion is drawn, not only verified: surfaces coloured by the curvature (blue negative, near-white zero, CCN orange positive, with a legend); comparison plots across K = 1, 0, −1; log–log error plots showing the order at which a correction enters; and for graph notions a family of example graphs (tree, cycle, cube, complete, Petersen, grid, dumbbell) with edges or vertices coloured by the value. Each picture has a Text cell saying what to see in it.
- In plots, use `Row[{…}]` rather than `GraphicsRow` when the panels carry legends, and plain `r^4` rather than superscript ⁴/⁶ in plot labels (the plot font lacks them).
- Never nest `#…&` inside `#…&`; use `Function[{name, G}, …]` for the outer function.
- Every check is run on a Wolfram kernel before the document quotes it.
- Visible code uses Greek letters, ∈ and script symbols (θ, φ, 𝓍, 𝒻) rather than long names.
- The notebook's source is `tools/cells.py`; `python3 tools/build.py notebooks` writes the `.nb` and `.wl`. Edit the source, not the `.nb`.
- Title, subtitle and copyright cells come first, and the copyright cell is repeated at the end.

## 3. Files: markdown and PDF

- **Markdown**: `docs/<name>.md`, with maths in `$$…$$` (rendered by GitHub) and the diagram as `docs/<name>-map.png` or similar.
- **PDF**: A4, built with
  `pandoc docs/<name>.md -s --mathml --css tools/pdf-style.css -o <name>.html`
  then `google-chrome --headless=new --no-pdf-header-footer --print-to-pdf=<name>.pdf <name>.html`.
  - DejaVu Sans body, 10.5 pt; Latin Modern Math for maths.
  - h2 headings with a 2 px rule in Computational Classnotes orange, RGB(250, 143, 43).
  - Light grey bordered tables with a tinted header row.
  - The diagram fits on page 1 (max height 105 mm).
  - Footer on every page: © 2026 Computational Classnotes · CC BY-NC-SA 4.0.
  - Remove pandoc's title block, because the markdown carries its own `#` title.
- Look at the rendered pages before pushing.

## 4. Diagram

- Two columns or a flow, quiet boxes with one accented row for the key thread, and connectors in the gaps.
- Title = the finding. Each box has a name line and one formula or body line, plus the § it maps to.
- Colour tokens only, so light and dark themes both work; export a PNG for the repo.

## 5. Git

- Commits authored and committed as Noor Hoshino <noor@compclassnotes.com>, with no Co-Authored-By or Claude-Session lines.
- `CONTEXT.md` (project state) and `STYLE.md` (this file) live at the repo root.

## 6. Rules added 23 November 2026 (from the user)

- **Worked by hand, everywhere.** Every programmer’s-manual page has a **Worked by Hand** section: a short derivation, done as one would on paper, of at least one example on that page, ending at the same value as its Out[n]. Every write-up section on a definition also works its examples by hand before computing them (as in `docs/series/07-ollivier.md` §4). The user called this section “excellent” and “most beautiful”; never omit it.
- **Index every figure.** Every figure carries a number and a caption: **Fig. n.** in write-ups (md, PDF, HTML) and in notebooks (a bold “Fig. n.” caption cell after the figure; series notebooks use explicit `("Figure", caption)` cells). Text refers to figures by number.
- **No A_B pseudo-subscripts.** Never write κ_LLY, K_BE, μ_x and so on as plain text. Use real subscripts: LaTeX `$\kappa_{\mathrm{LLY}}$` in markdown, `<sub>` in HTML, inline `SubscriptBox` cells in notebook Text cells (the builders convert X_Y and X_{Y} automatically), and `Subscript["κ", "LLY"]` in Wolfram code (plot labels, legends, table headers). Underscores are Wolfram pattern syntax and must not appear in names.
- **HTML counterpart with real 3D.** Each write-up also has an HTML version; every 3D figure in it is genuinely 3D (rotatable), not a static picture.
