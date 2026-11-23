"""Glossary of every technical term used on the Laplacian sites.

python3 tools/build_glossary.py  ->  docs/glossary.html  (then run tools/build_search.py)
Each entry: (term, aliases, definition HTML, [(link text, url), ...]).
Definitions follow the conventions of the write-ups (random-walk normalised graph Laplacian).
"""
import pathlib, re, html

W = 'laplacian-curvature.html'
O = 'series/07-ollivier.html'
B = 'series/09-bakry-emery.html'
LAB = 'https://lossofgenerality.github.io/laplacian/lab/Laplacian_Curvature_Lab.html'
PL = 'https://lossofgenerality.github.io/Laplacian-lab/'
MAN = 'https://lossofgenerality.github.io/laplacian/manual.html'

T = [
("Angle defect", "angular deficit",
 "At a vertex of a triangle mesh, δ = 2π − (sum of the corner angles of the triangles meeting there): how far the angles fall short of a flat 2π. Positive at cone-like points, negative at saddle-like points. A cube corner has δ = 2π − 3·π/2 = π/2. δ/A, with A the vertex area, approximates the Gauss curvature K.",
 [("Write-up §6", W + "#discrete-surfaces-the-cotangent-laplacian"), ("Lab: Meshes", LAB + "#mesh")]),
("Bakry–Émery curvature", "K_N, K∞, CD(K, N)",
 "The largest K such that Γ₂(f) ≥ (1/N)(Δf)² + KΓ(f) at a point for every function f: Bochner’s inequality imposed using the Laplacian alone. K∞ drops the dimension term. On graphs it is a small exact eigenvalue problem on the 2-ball of a vertex.",
 [("Write-up 09", B), ("Lab: Graph curvatures", LAB + "#graphs")]),
("Ball mean / sphere mean", "M_r f, mean value",
 "The average of f over a ball, or over a sphere, of radius r centred at a point. As r → 0 both differ from f(x₀) by a multiple of r²Δf: 2n(M_r f − f)/r² → Δf on the sphere and 2(n + 2)(M_r f − f)/r² → Δf on the ball.",
 [("Programmable Lab §1", PL + "#origin"), ("Write-up §3", W + "#mean-values-and-volumes-where-the-mean-value-origin-of-δ-meets-curvature")]),
("Bochner formula", "Bochner identity",
 "½Δ|∇f|² = ⟨∇f, ∇Δf⟩ + |Hess f|² + Ric(∇f, ∇f). In Γ-notation, Γ₂(f) = |Hess f|² + Ric(∇f, ∇f). A lower bound on Ricci curvature becomes Γ₂ ≥ KΓ + (Δf)²/n, the form that graph curvatures copy.",
 [("Write-up §5", W + "#bochner-formula-and-its-consequences"), ("Write-up 09 §2", B + "#the-carré-du-champ-and-bochners-formula-written-with-the-laplacian")]),
("Bonnet–Myers theorem", "diameter bound",
 "A positive lower bound on curvature bounds the diameter. On a manifold with Ric ≥ (n − 1)K > 0, diam ≤ π/√K. On graphs: diam ≤ 2/κ for Ollivier-type curvature κ > 0, and diam ≤ 2/K∞ for Bakry–Émery curvature on regular graphs (both attained on hypercubes).",
 [("Write-up 07 §7", O + "#what-a-lower-bound-on-κ-buys"), ("Write-up 09 §7", B + "#what-a-lower-bound-buys")]),
("Carré du champ", "Γ, square of the field",
 "French for “square of the field”. Γ(f, g) = ½(Δ(fg) − fΔg − gΔf): how far Δ is from obeying the product rule. On a manifold Γ(f) = |∇f|²; on a graph Γ(f)(v) = ½ mean over neighbours w of (f(w) − f(v))². For f = x² on the line, Γ(f) = 4x² = (f′)².",
 [("Write-up 09 §2", B + "#the-carré-du-champ-and-bochners-formula-written-with-the-laplacian")]),
("Iterated carré du champ", "Γ₂",
 "Γ₂(f) = ½ΔΓ(f) − Γ(f, Δf): the carré du champ construction repeated with Γ in place of the product. By Bochner’s formula Γ₂(f) = |Hess f|² + Ric(∇f, ∇f) on a manifold.",
 [("Write-up 09 §2", B + "#the-carré-du-champ-and-bochners-formula-written-with-the-laplacian")]),
("Conformal factor", "isothermal coordinates, e^(2u)",
 "In two dimensions every metric can be written g = e^(2u)(dx² + dy²) in suitable (isothermal) coordinates; e^(2u) is the conformal factor. Gauss curvature is then K = −e^(−2u)Δ₀u, with Δ₀ the flat Laplacian.",
 [("Write-up §1", W + "#gauss-curvature-is-a-laplacian"), ("Lab: Ricci flow", LAB + "#ricci")]),
("Cotangent Laplacian", "cotan Laplacian",
 "The standard Laplacian on a triangle mesh: (Δf)ᵢ = (1/2Aᵢ) Σⱼ (cot αᵢⱼ + cot βᵢⱼ)(fⱼ − fᵢ), where αᵢⱼ and βᵢⱼ are the two angles opposite edge ij and Aᵢ is the vertex area. Applied to the vertex positions it gives ΔX ≈ −2Hn.",
 [("Write-up §6", W + "#discrete-surfaces-the-cotangent-laplacian"), ("Lab: Meshes", LAB + "#mesh")]),
("Curvature-dimension condition", "CD(K, N)",
 "Γ₂(f) ≥ (1/N)(Δf)² + KΓ(f) for all f: “Ricci curvature at least K and dimension at most N”, stated with the Laplacian only. The unit sphere S² satisfies CD(1, 2).",
 [("Write-up 09 §3", B + "#definition-on-graphs"), ("Write-up 09 §6", B + "#dimension-the-curve-k_n")]),
("Euler characteristic", "χ",
 "χ = V − E + F for a surface built from V vertices, E edges and F faces. A sphere has χ = 2, a torus χ = 0. Gauss–Bonnet ties it to curvature: ∬K dA = 2πχ.",
 [("Write-up §6", W + "#discrete-surfaces-the-cotangent-laplacian")]),
("Forman curvature", "Forman–Ricci",
 "An edge curvature from the Weitzenböck splitting of the 1-form Hodge Laplacian. For an unweighted edge xy: 4 − d_x − d_y + 3·(number of triangles containing xy).",
 [("Write-up §7", W + "#graph-curvatures-and-the-graph-laplacian"), ("Lab: Graph curvatures", LAB + "#graphs")]),
("Gauss curvature", "K",
 "The product of the two principal curvatures of a surface; intrinsic (Gauss’s Theorema Egregium). K = 1 on the unit sphere, 0 on the plane and cylinder, −1 on the hyperbolic plane. In isothermal coordinates K = −e^(−2u)Δ₀u.",
 [("Write-up §1", W + "#gauss-curvature-is-a-laplacian"), ("Lab: Surfaces", LAB + "#surfaces")]),
("Gauss–Bonnet theorem", "",
 "For a closed surface, ∬K dA = 2πχ. Its discrete form: the angle defects of a closed mesh add to exactly 2πχ. Resistance curvature and Higuchi’s combinatorial curvature satisfy graph versions.",
 [("Write-up §6", W + "#discrete-surfaces-the-cotangent-laplacian"), ("Write-up §7", W + "#graph-curvatures-and-the-graph-laplacian")]),
("Graph Laplacian (random-walk normalisation)", "Δf(v), normalised Laplacian",
 "Δf(v) = (mean of f over the neighbours of v) − f(v), the convention used throughout these sites. It equals −(I − D⁻¹A) with A the adjacency and D the degree matrix; its eigenvalues are those of the symmetric normalised Laplacian I − D^(−1/2)AD^(−1/2).",
 [("Write-up 07 Scope", O + "#scope-and-conventions"), ("Write-up §7", W + "#graph-curvatures-and-the-graph-laplacian"), ("Programmable Lab §7", PL + "#graph")]),
("Harmonic function", "",
 "A function with Δf = 0: it equals its own sphere and ball means. In ℝ³, 1/r is harmonic away from the origin; 1/r² is not (Δ(1/r²) = 2/r⁴).",
 [("Programmable Lab §6", PL + "#radial")]),
("Heat trace", "Weyl’s law, Minakshisundaram–Pleijel",
 "Z(t) = Σ e^(−λₖt) over the Laplacian eigenvalues. For a surface, Z(t) = (A/4πt)(1 + Kt/3 + …) as t → 0 (for constant K): the area is heard first, curvature at the next order, which is why curvature is “audible”.",
 [("Write-up §4", W + "#heat-kernel-and-spectrum-curvature-is-audible"), ("Lab: Heat trace", LAB + "#heat")]),
("Hessian", "Hess f",
 "The matrix of second covariant derivatives of f. Its trace is Δf; on a 2-dimensional space |Hess f|² ≥ (Δf)²/2, with equality when the Hessian is a multiple of the metric.",
 [("Write-up 09 §2", B + "#the-carré-du-champ-and-bochners-formula-written-with-the-laplacian")]),
("Higuchi curvature", "combinatorial curvature",
 "For a vertex of a planar graph or polyhedron: 1 − d/2 + Σ 1/(size of each face at the vertex). The values add to χ (Gauss–Bonnet); every vertex of a Platonic solid has the same positive value.",
 [("Write-up §7", W + "#graph-curvatures-and-the-graph-laplacian")]),
("Idleness, lazy random walk", "α-lazy walk, μ_α",
 "A random walk that stays put with probability α and otherwise moves to a uniformly chosen neighbour. Ollivier curvature κ_α of the α-lazy walk is concave and piecewise linear in α; the Lin–Lu–Yau curvature is the limit of κ_α/(1 − α).",
 [("Write-up 07 §5", O + "#laziness-and-the-linluyau-curvature")]),
("Laplace–Beltrami operator", "Δ on a manifold",
 "The Laplacian of a Riemannian manifold, Δf = div(grad f), in coordinates (1/√det g) ∂ᵢ(√det g gⁱʲ ∂ⱼ f). On the unit sphere, Δf = (1/sin θ)∂θ(sin θ ∂θ f) + (1/sin²θ)∂φ² f.",
 [("Manual: Riemannian toolkit", MAN + "#/guide/riemannian"), ("Write-up 09 §2", B + "#the-carré-du-champ-and-bochners-formula-written-with-the-laplacian")]),
("Lichnerowicz bound", "spectral gap",
 "A positive lower curvature bound forces a gap in the spectrum. On an n-manifold with Ric ≥ (n − 1)k > 0, λ₁ ≥ nk. On graphs, λ₁ ≥ κ for Ollivier curvature and λ₁ ≥ NK/(N − 1) under CD(K, N); equality holds on hypercubes.",
 [("Write-up §5", W + "#bochner-formula-and-its-consequences"), ("Write-up 09 §7", B + "#what-a-lower-bound-buys")]),
("Lin–Lu–Yau curvature", "κ_LLY",
 "The Ollivier curvature of a lazy random walk, in the limit of full laziness: κ_LLY = lim κ_α/(1 − α) as α → 1. It equals 2κ_(1/2) on every graph tested here; Münch–Wojciechowski give a limit-free formula.",
 [("Write-up 07 §5", O + "#laziness-and-the-linluyau-curvature"), ("Lab: Graph curvatures", LAB + "#graphs")]),
("Liouville’s equation", "",
 "Δ₀u + Ke^(2u) = 0 with K constant: the equation for a conformal factor of constant Gauss curvature K.",
 [("Write-up §1", W + "#gauss-curvature-is-a-laplacian")]),
("Mean curvature", "H",
 "The average of the two principal curvatures of a surface in space; H = 1 on the unit sphere, 0 on minimal surfaces such as the catenoid and helicoid. The Laplacian of the position vector is ΔX = −2Hn, with n the unit normal.",
 [("Write-up §2", W + "#mean-curvature-is-a-laplacian"), ("Lab: Surfaces", LAB + "#surfaces")]),
("Mean-curvature flow, curve shortening", "",
 "Moving a surface by ∂X/∂t = ΔX = −2Hn. A sphere of radius R₀ shrinks as R² = R₀² − 4t. For plane curves it is curve shortening: any embedded curve becomes round, and the enclosed area falls at exactly 2π per unit time.",
 [("Write-up §10", W + "#flows-and-further-identities-worked-out-notebook-10"), ("Lab: Curve shortening", LAB + "#flows")]),
("Ollivier curvature", "coarse Ricci curvature, κ(x, y)",
 "κ(x, y) = 1 − W₁(m_x, m_y)/d(x, y): how much closer two averaging measures are than their centres. On a graph m_x is the random walk at x; on a manifold with ε-ball averages κ ≈ Kε²/8 on a surface.",
 [("Write-up 07", O), ("Lab: Ollivier on manifolds", LAB + "#ollivier")]),
("Orthonormal mandate", "Theorem 7.4",
 "An average of f over stencil points ±hu, ±hv gives h²∇ᵀ(uuᵀ + vvᵀ)∇f to second order, which is h²Δf only when u, v are orthonormal. Skewed axes add a cross term 2M₁₂ ∂ₓ∂ᵧf. This is why the Laplacian looks the same in every orthonormal frame.",
 [("Programmable Lab §5", PL + "#discrete"), ("Write-up §6", W + "#discrete-surfaces-the-cotangent-laplacian")]),
("Resistance curvature", "Devriendt–Lambiotte",
 "A vertex curvature from effective resistances ω (computed from the pseudoinverse L⁺ of the Laplacian): pᵢ = 1 − ½ Σⱼ∼ᵢ ωᵢⱼ. By Foster’s theorem the values add to exactly 1 on every connected graph, a discrete Gauss–Bonnet.",
 [("Write-up §7", W + "#graph-curvatures-and-the-graph-laplacian")]),
("Ricci curvature", "Ric",
 "The trace of the Riemann curvature tensor: Ric(v, v) measures how volumes of small balls in direction v deviate from flat ones. On a surface Ric = K·g. Every graph curvature on these sites copies one property of a Ricci lower bound.",
 [("Write-up §5", W + "#bochner-formula-and-its-consequences"), ("Write-up 07 §2", O + "#positive-curvature-brings-averages-together")]),
("Ricci flow", "",
 "∂g/∂t = −2Ric (Hamilton 1982): directions of positive Ricci curvature shrink, negative ones stretch. Ricci curvature is minus a Laplacian of the metric (Ric_ij = −½Δg_ij + lower order in harmonic coordinates), so the flow is a heat equation for the metric. In two dimensions with g = e^(2u)(dx² + dy²) it is the nonlinear heat equation ∂u/∂t = e^(−2u)Δ₀u = −K; the round sphere shrinks as (1 − 2t)g₀ and a bumpy flat torus flattens.",
 [("Write-up §10", W + "#flows-and-further-identities-worked-out-notebook-10"), ("Lab: Ricci flow", LAB + "#ricci"), ("Notebook 14", "https://github.com/lossofgenerality/laplacian/blob/main/notebooks/series/14-Ricci-Flow.nb")]),
("Riemannian metric", "g, metric tensor",
 "An inner product on the tangent vectors at each point of a space, varying smoothly from point to point. Lengths, angles, areas, geodesics and every curvature are computed from it; Ricci flow moves it. Not the same as a distance function, though it determines one.",
 [("Lab: Ricci flow", LAB + "#ricci"), ("Notebook 14 §1", "https://github.com/lossofgenerality/laplacian/blob/main/notebooks/series/14-Ricci-Flow.nb")]),
("Sectional curvature", "K(X, Y)",
 "The curvature of the plane spanned by tangent vectors X and Y. A small geodesic triangle with legs εX and εY has third side L(ε) = ε‖X − Y‖(1 − K(X, Y)(1 + ⟨X, Y⟩)ε²/12 + …): shorter than flat when K > 0, longer when K < 0. On a surface it is the Gauss curvature; Ricci curvature averages it.",
 [("Lab: Ricci flow", LAB + "#ricci"), ("Notebook 14 §1", "https://github.com/lossofgenerality/laplacian/blob/main/notebooks/series/14-Ricci-Flow.nb")]),
("Maximum principle", "",
 "At an interior maximum the Hessian is negative semidefinite, so the Laplacian is ≤ 0; under a heat-type equation u_t = Δu + … the maximum therefore cannot rise (and the minimum cannot fall) unless the extra terms push it. Under 2-D Ricci flow max u falls, min u rises, and min K never decreases because K_t = Δ_g K + 2K².",
 [("Lab: Ricci flow", LAB + "#ricci"), ("Notebook 14 §3", "https://github.com/lossofgenerality/laplacian/blob/main/notebooks/series/14-Ricci-Flow.nb")]),
("Energy (heat equation)", "E = ∫u², Dirichlet energy",
 "For u_t = Δu on a closed space, E = ∫u² decreases: E′ = −2∫|∇u|². For the Lab’s Ricci flow the analogue D = ∬|∇₀u|² of the conformal factor decreases at the rate 2∬K² dA.",
 [("Lab: Ricci flow", LAB + "#ricci"), ("Notebook 14 §4", "https://github.com/lossofgenerality/laplacian/blob/main/notebooks/series/14-Ricci-Flow.nb")]),
("Entropy (heat equation)", "S = −∫u ln u",
 "For a positive solution of u_t = Δu, S = −∫u ln u increases: S′ = ∫|∇u|²/u, the Fisher information. For the Lab’s Ricci flow the entropy of the area density ρ = e^(2u)/A increases at the rate 4D/A and is largest, ln 4π², for the flat metric.",
 [("Lab: Ricci flow", LAB + "#ricci"), ("Notebook 14 §4", "https://github.com/lossofgenerality/laplacian/blob/main/notebooks/series/14-Ricci-Flow.nb")]),
("Fisher information", "",
 "∫|∇u|²/u for a positive density u: the rate at which the entropy of a heat flow increases. Perelman’s monotone quantity for Ricci flow is closer to a Fisher information than to an entropy.",
 [("Notebook 14 §4", "https://github.com/lossofgenerality/laplacian/blob/main/notebooks/series/14-Ricci-Flow.nb")]),
("Reaction–diffusion equation", "u_t = Δu + u²",
 "A diffusion term that spreads plus a reaction term that concentrates. With u² the reaction can win: constant data u₀ > 0 blow up at t = 1/u₀. Curvature under Ricci flow obeys such an equation (on a surface K_t = Δ_g K + 2K²); the shrinking round sphere is its blow-up.",
 [("Lab: Ricci flow", LAB + "#ricci"), ("Notebook 14 §5", "https://github.com/lossofgenerality/laplacian/blob/main/notebooks/series/14-Ricci-Flow.nb")]),
("Stencil", "5-point, 7-point stencil",
 "A finite-difference formula for Δ: Σᵢ[f(x₀ + heᵢ) + f(x₀ − heᵢ)] − 2d·f(x₀), divided by h², equals Δf + O(h²). In 2D this is the 5-point stencil, in 3D the 7-point stencil.",
 [("Programmable Lab §5", PL + "#discrete")]),
("Steinerberger curvature", "",
 "A vertex curvature K solving D·K = n·1, where D is the graph distance matrix and n the number of vertices; it gives Bonnet–Myers-type bounds on the mean distance.",
 [("Write-up §7", W + "#graph-curvatures-and-the-graph-laplacian")]),
("Wasserstein distance W₁", "earth mover’s distance, optimal transport",
 "The least average distance mass must travel to turn one probability distribution into another. By Kantorovich duality it also equals the largest difference of averages of a 1-Lipschitz test function.",
 [("Write-up 07 §3", O + "#definition"), ("Write-up 07 §4", O + "#worked-by-hand")]),
("Weitzenböck formula", "Bochner–Weitzenböck",
 "On 1-forms the Hodge Laplacian splits as Δ_Hodge = ∇*∇ + Ric: a rough Laplacian plus curvature. With Ric > 0 there are no harmonic 1-forms. Forman curvature is the graph version of this splitting.",
 [("Write-up §10", W + "#flows-and-further-identities-worked-out-notebook-10")]),
]

slug = lambda s: re.sub(r'[^a-z0-9]+', '-', s.lower().replace('–', '-')).strip('-')
items = sorted(T, key=lambda t: t[0].lower())
toc = ' · '.join('<a href="#%s">%s</a>' % (slug(t[0]), html.escape(t[0])) for t in items)
def sub(t):
    t = html.escape(t)
    t = re.sub(r'([A-Za-zκμλΓαβθδω])_\(([^)]+)\)', r'\1<sub>\2</sub>', t)
    return re.sub(r'([A-Za-zκμλΓΔαβθδω])_([A-Za-z0-9∞α]+)', r'\1<sub>\2</sub>', t)


rows = []
for term, alias, d, links in items:
    lk = ' '.join('<a class="go" href="%s">%s</a>' % (html.escape(u), html.escape(t)) for t, u in links)
    rows.append('<section class="g" id="%s"><h2>%s%s</h2><p>%s</p><div class="lk">%s</div></section>' % (
        slug(term), sub(term), (' <span class="al">' + sub(alias) + '</span>') if alias else '', sub(d), lk))
page = '''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Glossary — Laplacian Labs · Computational Classnotes</title>
<link rel="stylesheet" href="../brand/ccn-tokens.css">
<style>
*{box-sizing:border-box} body{margin:0;background:var(--ccn-page);color:var(--ccn-ink);font:16px/1.55 var(--ccn-f-body)}
.top{display:flex;flex-wrap:wrap;gap:6px 18px;align-items:baseline;max-width:920px;margin:0 auto;padding:16px 20px;border-bottom:1px solid var(--ccn-line)}
.wm{font:700 20px/1.1 var(--ccn-f-display);letter-spacing:-.01em;white-space:nowrap;color:inherit;text-decoration:none} .wm b{color:var(--ccn-orange-ink)}
.top a.l{color:var(--ccn-soft);font-size:14px} .top a.l:first-of-type{margin-left:auto}
main{max-width:920px;margin:0 auto;padding:22px 20px 40px}
h1{font:700 clamp(24px,2.4vw,28px)/1.15 var(--ccn-f-display);margin:0 0 6px} .lede{color:var(--ccn-soft);font-size:15px;margin:0 0 14px}
.toc{font-size:14px;line-height:1.9;background:var(--ccn-panel);border:1px solid var(--ccn-line);border-radius:10px;padding:10px 14px;margin-bottom:18px}
.toc a{color:var(--ccn-orange-ink)}
.g{background:var(--ccn-panel);border:1px solid var(--ccn-line);border-radius:10px;padding:12px 16px;margin-bottom:10px;scroll-margin-top:12px}
.g:target{border-color:var(--ccn-orange);box-shadow:0 0 0 3px var(--ccn-orange-tint)}
.g h2{font:700 18px/1.3 var(--ccn-f-display);margin:0 0 4px} .g .al{font:400 13.5px var(--ccn-f-body);color:var(--ccn-soft)}
.g p{margin:0 0 8px;max-width:78ch} .lk{display:flex;flex-wrap:wrap;gap:6px 14px;font-size:14px} .lk a{color:var(--ccn-orange-ink)}
footer{max-width:920px;margin:0 auto;padding:16px 20px 40px;color:var(--ccn-soft);font-size:13.5px;border-top:1px solid var(--ccn-line)} footer a{color:inherit}
</style></head><body>
<div class="top"><a class="wm" href="../lab/Laplacian_Curvature_Lab.html">Laplacian <b>Curvature</b> Lab</a><a class="l" href="../manual.html">Manual</a><a class="l" href="series/">Write-ups</a><a class="l" href="../search.html">Search</a><a class="l" href="https://lossofgenerality.github.io/Laplacian-lab/">Laplacian Programmable Lab</a></div>
<main><h1>Glossary</h1>
<p class="lede">Every technical term used across both Labs, both manuals and the write-ups: a short definition in the sites’ conventions, and links to where it is worked out. Link to a term with <code>glossary.html#term-name</code>.</p>
<div class="toc">%s</div>
%s
</main>
<footer>%d terms. Built by <code>tools/build_glossary.py</code>. Part of <a href="https://github.com/lossofgenerality/laplacian">lossofgenerality/laplacian</a>.<br>© Computational Classnotes · CC BY-NC-SA 4.0</footer>
</body></html>
''' % (toc, '\n'.join(rows), len(items))
out = pathlib.Path(__file__).resolve().parent.parent / 'docs/glossary.html'
out.write_text(page, encoding='utf-8')
print(out, len(items), 'terms')
