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
