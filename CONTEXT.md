# CONTEXT — Laplacian Lab

Working context for anyone (person or assistant) picking up the Laplacian Lab project. It records what exists, how the pieces fit, the decisions already made, and what is still open.

© 2026 Computational Classnotes · CC BY-NC-SA 4.0
Last updated: 23 November 2026

---

## 1. What the project is

Laplacian Lab is an interactive teaching assistant for the Laplacian operator "in all its forms". It is built on the Computational Classnotes notebook:

> *Where did Laplacian come from? Laplacian things… Computational conception of Laplacian Operator (fully coded) β1.0*, Dara O Shayda, Computational Classnotes. DOI 10.13140/RG.2.2.33742.01600.
> Live notebook: https://www.wolframcloud.com/obj/ccn2/Published/Laplacian_things.nb

The wider goal: compute lesser-known properties of the Laplacian, provide a software lab for experimenting with it, and grow into a Symbolic Teaching Assistant for researchers and students.

The page has three layers:

1. **Live demonstrations** in plain JavaScript (no server): sphere and ball means, Taylor moments, coefficient tables, Δⁿ expansions, stencils, 1/rⁿ fields, graph Laplacian with spectrum, a reference sheet and a quiz.
2. **Wolfram Language cells**, one per section plus a free cell, evaluated on a Wolfram kernel.
3. **Ask the TA**, a chat teaching assistant that knows the notebook and the current state of the section the student came from.

---

## 2. Deliverables and where they are

### Published artifacts (claude.ai, private to the owner)

| Name | URL id | State |
|---|---|---|
| **Laplacian Lab** | `PwLafg8VqNGeKbXfigbhq6` | Version 5. The original. Uses the Wolfram connector (`mcp`) and Claude (`sample`) capabilities. User asked for it to be left unchanged. |
| **Laplacian Lab_version2** | `VWTpah5hC6ACLpoDg454Yc` | Version 1. Exact copy of the original with "_version2" in the title and heading. **None of the standalone version2 changes are in it.** |
| **The Laplacian and Curvature — Instances and Relationships** (doc) | `8C2j3466b5YuTWRwX2oAkE` | Claude Docs write-up, see §2a. |

### Files

| File | What it is |
|---|---|
| `laplacian-ta.html` | Source of the **Laplacian Lab** artifact (publish this path to update it). |
| `laplacian-lab-version2.html` | Source of the **Laplacian Lab_version2** artifact. |
| `Laplacian_Lab.html` | Standalone file, version 1. Settings block holds `API_KEY`, `MODEL`, `WOLFRAM_URL`, `WOLFRAM_KEY`. The Section 12 Setup box and "Two things to know" note were removed at the user's request. |
| `Laplacian_Lab_version2.html` | Standalone file, version 2. **No keys in the file.** Masked **CCN-KEY** field in Section 12; TA chat routed through LaplacianLabKernel. Settings block holds only `MODEL` and `WOLFRAM_URL`. |
| `LaplacianLabKernel.wl` | The Wolfram Cloud API both standalone files call. Current version has the chat proxy. |
| `laplacianSteps.wl` | Staged, self-checking derivation of Δ from the sphere or ball mean. |
| `Laplacian_Lab_Tutorial.md` / `.pdf` | User tutorial for the standalone .html (16 pages, A4). Reworded for CCN Cloud; contains no references to Claude, Anthropic, or the key variable names. |

The Lab files above were made in a temporary session scratchpad; the user holds the delivered copies. They are **not** in the GitHub repo yet.

### 2a. Laplacian and curvature companion (23 Nov 2026)

A literature survey plus a verified write-up and notebook on every Laplacian–curvature relationship, smooth, mesh and graph.

- **GitHub:** https://github.com/lossofgenerality/laplacian (branch `main`; commits authored as Noor Hoshino <noor@compclassnotes.com>, no Claude attribution).
  - `CONTEXT.md`: this file.
  - `STYLE.md`: house style for math documents (doc, notebook, md/pdf, diagram, git).
  - `README.md`.
  - `docs/laplacian-curvature.md`: markdown copy of the write-up (GitHub `$$` maths).
  - `docs/relationship-map.png`: diagram of six smooth identities and their discrete twins.
  - `notebooks/LaplacianCurvature.nb`: Wolfram notebook, no outputs saved; evaluate top to bottom.
  - `notebooks/LaplacianCurvature.wl`: same code as a script.
  - `tools/cells.py`: the notebook's cell content. This is the source of truth: edit it, not the `.nb`.
  - `tools/build.py`: `python3 tools/build.py notebooks` regenerates `.nb` and `.wl` (and `chunks.json`, the Input cells grouped by section, for testing).
- **Doc ↔ notebook numbering:** write-up Section n ↔ notebook Section n+1 (notebook §1 is the Riemannian toolkit; §9 uses the graph functions of §8).
- **Write-up sections:** 1 Gauss curvature (Liouville), 2 ΔX = −2Hn, 3 curved mean values and volumes (Gray–Willmore; link to Lab Section 1), 4 heat trace (McKean–Singer), 5 Bochner / Lichnerowicz / Weitzenböck, 6 cotangent Laplacian and angle defect, 7 graph curvatures table (Ollivier, Lin–Lu–Yau, Bakry–Émery, CDE, Forman, entropic, resistance, Steinerberger, Higuchi), 8 graph spectral bounds and Belkin–Niyogi, 9 verified graph results, references.
- **Key verified results:**
  - Constant-curvature circle mean M_r f = f + r²Δf/4 + r⁴(Δ²f/64 + KΔf/96) + r⁶(Δ³f/2304 + KΔ²f/1152 + K²Δf/1440); exact to r⁶ on S² for a non-symmetric function.
  - Bochner holds symbolically on S² for arbitrary f.
  - The 400-vertex sphere mesh gives Σ defect = 4π, K ≈ 1.014 and H ≈ 1.006.
  - Lin–Lu–Yau by the Münch–Wojciechowski LP equals 2κ_{1/2} by transport on C₆, K₅, Q₃, Petersen and the 4×4 grid.
  - Bakry–Émery K∞ = 0, 7/8, 2/3, −1/3, 0.088 on those graphs.
  - The discrete Lichnerowicz bounds hold on all five.
  - Σ resistance curvature = 1, and Higuchi totals = 2.
  - The point-cloud Laplacian on 20 000 points of S² gives ratio 0.9997.
- **Fix (23 Nov):** the notebook §8.2 summary line nested two `&` functions (`bakryEmery[#, v] & /@ VertexList[#]`), which passed a vertex as the graph. Now `Function[G, Min[bakryEmery[G, #] & /@ VertexList[G]]]`.

---

## 3. Page structure (all versions)

Hash-routed, one section visible at a time, previous/next pagers.

| # | `#hash` | Section | Notebook § |
|---|---|---|---|
| 1 | `origin` | Mean-value origin | §2–3 |
| 2 | `taylor` | Taylor terms on a sphere | §1, §4 |
| 3 | `series` | Mean = sum of Δ powers | §2.2–2.3, §5.4, §6 |
| 4 | `powers` | Δⁿ and the multinomial | §5.1–5.3 |
| 5 | `discrete` | Stencils and the orthonormal mandate | §7–7.4 |
| 6 | `radial` | 1/rⁿ fields and harmonic functions | §7.5, §8 |
| 7 | `graph` | Graph and mesh Laplacian | §9, Coda |
| 8 | `forms` | All the forms (14 cards + physics table) | reference |
| 9 | `notes` | Notes on the notebook | review |
| 10 | `quiz` | Self-check (8 questions) | all |
| 11 | `ask` | Ask the TA | all |
| 12 | `wolfram` | Wolfram Language (free cell, snippets, Δ notation table) | all |

Design tokens: cool paper/ink palette with the Computational Classnotes orange (RGB 0.98, 0.56, 0.17) as accent; Bricolage Grotesque / IBM Plex Sans / JetBrains Mono; light and dark themes. Maths rendered by MathJax 3.2.2 (tex-svg) from cdnjs.

---

## 4. How the Wolfram cells and the TA connect

### Inside Claude (the artifacts)
- Wolfram cells call the **Wolfram connector** (`WolframLanguageEvaluator`) through the `mcp` capability.
- The TA uses the `sample` capability, and can call Wolfram itself through a `run_wolfram` tool; code it ran is shown under its answer.
- Artifacts cannot call `wolframcloud.com` directly (the frame blocks other hosts), so the CCN-KEY/LaplacianLabKernel route cannot work in an artifact.

### Standalone version 1 (`Laplacian_Lab.html`)
- Wolfram cells POST `code` + `key` to `WOLFRAM_URL`.
- The TA calls the chat service directly from the browser with `API_KEY` from the settings block.

### Standalone version 2 (`Laplacian_Lab_version2.html`)
- The user types **CCN-KEY** into the masked field and presses **Connect** (optional "Remember on this device" in localStorage).
- Connect sends `$VersionNumber`; the kernel replies with `chat_ready: True/False`. The chat key is never sent to the page.
- Wolfram cells POST `code` and `code_b64`; results come back as `text_b64` (+ `image` PNG for graphics).
- TA questions POST `mode=chat` with `payload_b64` (JSON: model, max_tokens, system, messages). The kernel calls the chat service with the key from a **private** Wolfram Cloud object and returns `text_b64` + `stop_reason`, or `error` + `status`.
- In code the key variable is `WL_KEY` and the field id is `wl-key`; only the visible English text says "CCN-KEY".

### LaplacianLabKernel deployment
1. `CloudPut["<chat key>", "LaplacianLab/apikey", Permissions -> "Private"]` (once, or when the key changes).
2. `CloudDeploy[APIFunction[…], "LaplacianLabKernel", Permissions -> "Public"]` wrapped in `With[{keyObj = CloudObject["LaplacianLab/apikey"], secret = "…"}]`. Same name keeps the URL.
- Backward compatible: plain `code` is still accepted, so version 1 pages keep working with the new kernel.
- Must be deployed from a **signed-in** Mathematica or Wolfram Cloud notebook; the Claude Wolfram connector kernel cannot deploy.

---

## 5. The Δ notation (notebook's delta system)

Rebuilt with built-ins because the notebook's package does not load (see §7). With the "Δ notation" checkbox on, a prelude is prepended to each cell and shorthand is rewritten before sending:

| Typed | Sent / meaning |
|---|---|
| `Δf`, `∇²f` | `Δ[1]@f` — Laplacian of f[x,y,z] |
| `Δ²f`, `Δ^2 f`, `Δ2f`, `Δ(2)f` | `Δ[2]@f` |
| `Δ[n][expr]`, `Δ[n]@expr` | nth power on any expression |
| `𝜟⊗f`, `𝜟⊗𝜟⊗f` | §5.3 operator, applied repeatedly |
| `\[ScriptA]\[ScriptR]\[ScriptG]\[ScriptS] = {x,y,z,t};` | change variables / dimension |
| `𝒹`, `𝒞enter`, `ℋelp` | dimension, centre point, symbol list |

Output: `Derivative[a,b,c][f]` is displayed as `f^(a,b,c)`. Verified on the kernel: Δ²f has 6 terms, Δ⁵f has 21, `Δ[3]@f − 𝜟⊗𝜟⊗𝜟⊗f = 0`, 4D switch works.

The prelude, kernel and `laplacianSteps` code are also saved verbatim in the user's memory note **laplacian-lab-wolfram**.

---

## 6. Conventions and user preferences

- Every deliverable carries "© Computational Classnotes · CC BY-NC-SA 4.0" (dated where requested).
- The user's own copy of the notebook is credited in the page footer with its DOI.
- Prefer Greek letters and ∈ over long names in visible Wolfram code (`φ`, `θ`, `∈` replaced `\[Phi]`, `\[Theta]`, `\[Element]`).
- Each new standalone .html ships with **empty settings**; the user copies `WOLFRAM_URL` (and in version 1 the keys) across.
- Don't change an artifact unless asked; the user has said "leave the artifact unchanged" more than once.
- In the tutorial, readers use "CCN Cloud and CCN's Wolfram Cloud kernel"; no key or deployment advice for readers.
- Avoid the term "LLM" in the user's writing; use "conversational-construct" where such a term is needed.
- Git commits for the user: author/committer Noor Hoshino <noor@compclassnotes.com>; no Co-Authored-By or Claude-Session lines.
- **Math document house style:** see `STYLE.md` at the repo root (Claude Doc + numbered sections + "Checked (notebook §n)" lines + verified table + references; companion notebook; md + A4 PDF). The reference example is the Laplacian and curvature write-up.

---

## 7. Technical lessons (do not relearn these)

- The Claude Wolfram connector kernel is **stateless** and **not signed in** to Wolfram Cloud: `CloudGet["https://wolfr.am/1ItEvTTUn"]`, `ℒ𝒜𝒫init[]`, `seriesDerv`, `exponentsToDervs` and `CloudDeploy` do not work there.
- The notebook's variables symbol is `𝒶𝓇ℊ𝓈` — the script g is **ℊ (U+210A)**. A three-letter `𝒶𝓇𝓈` is a different, undefined symbol.
- Named slots cannot contain underscores: `#payload_b64` parses as `#payload` `_b64`. Use `#["payload_b64"]`.
- `ImportString[s, "RawJSON"]` fails on non-ASCII; use `ImportByteArray[StringToByteArray[s], "RawJSON"]`.
- APIFunction `"JSON"` output garbles Unicode; send and return text as base64 of UTF-8. JS (`TextEncoder`+`btoa`, `atob`+`TextDecoder`) and Wolfram (`BaseEncode[StringToByteArray[…]]`) produce byte-identical base64.
- Optional typed arguments: `d : (_Integer?Positive) : 3`, not `d_Integer?Positive : 3`.
- Deployed APIFunctions run as the owner, so a private CloudObject keeps a secret server-side.
- Page CSS: grid children need `min-width: 0`; add `[hidden]{display:none!important}` when sections use `display:flex`.
- Pandoc + Chromium for the PDF: link the stylesheet with a path relative to the HTML file; use `--mathml` (MathJax cannot load offline).
- Writing a `.nb` by script: `Cell["code", "Input"]` with non-ASCII escaped as `\:XXXX` (BMP) and `\|XXXXXX` (astral, e.g. 𝓍 = `\|01d4cd`) parses correctly (checked with `ImportString[…, "NB"]`).
- `NormalizedGraphLaplacian` is not a built-in; use I − D^(−1/2) A D^(−1/2). `d^-1/2` parses as (d^-1)/2 — write `d^(-1/2)`.
- `LinearOptimization[…, "PrimalMinimumValue"]` returns a number, not a list.
- Point-cloud (Belkin–Niyogi) checks need quasi-uniform points (`SpherePoints`) and a `Nearest` radius cut-off; random points at small t are too noisy.
- Never nest `#…&` inside `#…&`: the inner `#` captures the slot. Use `Function[G, …]` for the outer one. Test summary lines exactly as they appear in the notebook, not a rewritten form.

---

## 8. Open issues

1. **𝒶𝓇𝓈 bug (all versions, both artifacts).** The Insert button, the Section 12 Δ notation table and the "Δ notation" snippet comment use the three-letter `𝒶𝓇𝓈`, which Wolfram doesn't recognise. Fix: insert `𝒶𝓇ℊ𝓈` and have `deltaPre` map `𝒶𝓇𝓈` → `\[ScriptA]\[ScriptR]\[ScriptG]\[ScriptS]`.
2. **Section 9 claim about §3.2** ("`series2` is never defined") is unverified and may be wrong.
3. **Notebook section numbers** cited from reading (e.g. "Factorial2 form (§4.6)", "Factorial form (§4.5)") not checked against the notebook.
4. **Tutorial §5.6** lists results for the Section 4 cell (Δ³f vs (x+y+z)³) and the Section 12 Plot3D cell that were not run as those exact cells.
5. **Laplacian Lab_version2 artifact** has none of the standalone version2 changes (by design for the key flow; the 𝒶𝓇𝓈 fix could still go in).
6. **LaplacianLabKernel deployed form** untested end to end: the `With[…]`/`CloudDeploy` wrapper, reading the private key object, URL staying the same, and a real chat answer (only an invalid-key 401 was tested). The file ends with `URLExecute` checks.
7. **Cloud API time limit.** Version 2 chat waits for the whole answer (no streaming). Long answers may hit the Wolfram Cloud plan's API timeout; lower `max_tokens` in the page if so.
8. **LaplacianLabKernel.wl comments** still say WOLFRAM_KEY; the page now says CCN-KEY.
9. **Remaining trade-off (version 2):** anyone with the CCN-KEY can use the TA chat at the owner's cost through the kernel, though they cannot read the chat key.
10. **Curvature notebook** has not been run whole in a desktop front end; cells were tested one by one on the connector kernel, and one summary line (§8.2) was wrong until the 23 Nov fix. CDE/CDE′ and entropic curvature are described, not computed. The general (non-constant-curvature) Gray–Willmore r⁴ coefficient is not stated.
11. **Lab source files** (`Laplacian_Lab*.html`, `LaplacianLabKernel.wl`, `laplacianSteps.wl`, tutorial) are not in the GitHub repo; add them from the user's copies if wanted.

---

## 9. Suggested next steps

- Fix open issue 1 in both standalone files and both artifacts (ask before touching the original artifact).
- Deploy the new LaplacianLabKernel and run the three `URLExecute` checks.
- Bring the tutorial in line with version 2 (CCN-KEY field, Connect button, chat through the kernel).
- Add a "show the steps" mode to Wolfram cells using `laplacianSteps` (staged evaluation, one checkable Out per step).
- Start the Symbolic Teaching Assistant on top of version 2.
- Add a curved-space section to Laplacian Lab (geodesic-circle mean on S² with the K terms, plus a graph-curvature panel for Section 7) drawing on the curvature notebook.
