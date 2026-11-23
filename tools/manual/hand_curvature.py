# "Worked by Hand" sections for the Laplacian Curvature Lab manual.
# Each entry: list of steps (plain text, X_{sub} for subscripts). The last step names the Out it reproduces.

HAND = {
"christoffel": [
 "On the unit sphere g = diag(1, sin²θ), so the only non-constant entry is g_{φφ} = sin²θ, with ∂_{θ} g_{φφ} = 2 sin θ cos θ.",
 "Γ^θ_{φφ} = ½ g^{θθ}(−∂_{θ} g_{φφ}) = −sin θ cos θ.",
 "Γ^φ_{θφ} = Γ^φ_{φθ} = ½ g^{φφ} ∂_{θ} g_{φφ} = ½ · (1/sin²θ) · 2 sin θ cos θ = cot θ.",
 "Every other symbol contains a derivative of a constant entry, so it is 0.",
 "Result: Γ^θ = {{0, 0}, {0, −sin θ cos θ}} and Γ^φ = {{0, cot θ}, {cot θ, 0}} — Out[1]."],
"laplaceBeltrami": [
 "On the unit sphere √det g = sin θ and g^{θθ} = 1, g^{φφ} = 1/sin²θ, so Δu = (1/sin θ) ∂_{θ}(sin θ ∂_{θ}u) + (1/sin²θ) ∂²_{φ}u.",
 "For u = cos θ: ∂_{θ}u = −sin θ, so sin θ ∂_{θ}u = −sin²θ.",
 "∂_{θ}(−sin²θ) = −2 sin θ cos θ; divide by sin θ: −2 cos θ. The φ-term is 0.",
 "Δ cos θ = −2 cos θ: cos θ is a degree-1 spherical harmonic, eigenvalue −l(l + 1) = −2 — Out[1]."],
"gradNorm2": [
 "|∇u|² = (∂_{θ}u)² + (∂_{φ}u)²/sin²θ on the unit sphere.",
 "For u = sin θ cos φ: ∂_{θ}u = cos θ cos φ and ∂_{φ}u = −sin θ sin φ.",
 "|∇u|² = cos²θ cos²φ + sin²θ sin²φ/sin²θ = cos²θ cos²φ + sin²φ — Out[1]."],
"hessian": [
 "∇_{i}∇_{j}u = ∂_{i}∂_{j}u − Γ^k_{ij} ∂_{k}u, with the sphere’s symbols from christoffel.",
 "u = cos θ: ∂_{θ}u = −sin θ, ∂_{φ}u = 0, ∂²_{θ}u = −cos θ.",
 "H_{θθ} = −cos θ (Γ^k_{θθ} = 0). H_{θφ} = −Γ^φ_{θφ} ∂_{φ}u = 0.",
 "H_{φφ} = 0 − Γ^θ_{φφ} ∂_{θ}u = −(−sin θ cos θ)(−sin θ) = −sin²θ cos θ.",
 "Hess cos θ = {{−cos θ, 0}, {0, −cos θ sin²θ}} — Out[1]; its trace with g⁻¹ is −2 cos θ = Δ cos θ."],
"hessNorm2": [
 "With H from hessian, |H|² = Tr[g⁻¹ H g⁻¹ H] = (H_{θθ})² + (H_{φφ})²/sin⁴θ.",
 "= cos²θ + (cos θ sin²θ)²/sin⁴θ = cos²θ + cos²θ.",
 "|Hess cos θ|² = 2 cos²θ — Out[1]."],
"gaussCurvature": [
 "For a metric dθ² + G(θ) dφ², the Gauss curvature is K = −(√G)″/√G.",
 "Sphere: √G = sin θ, (sin θ)″ = −sin θ, so K = 1 — Out[1].",
 "Hyperbolic plane: √G = sinh r, (sinh r)″ = sinh r, so K = −1 — Out[2].",
 "Torus (coordinates u, v; the roles swap): g = (2 + cos v)² du² + dv², √E = 2 + cos v, K = −(√E)_{vv}/√E = cos v/(2 + cos v) — Out[3]."],
"roughLaplacian1": [
 "ω = sin²θ dφ is ⋆d(−cos θ): d(−cos θ) = sin θ dθ and ⋆dθ = sin θ dφ.",
 "−cos θ is an l = 1 harmonic, so the Hodge Laplacian (positive convention) gives Δ_{H}ω = l(l + 1) ω = 2ω.",
 "Weitzenböck on S² (Ric = 1): Δ_{H}ω = ∇*∇ω + ω, so ∇*∇ω = 2ω − ω = ω.",
 "∇*∇ (sin²θ dφ) = sin²θ dφ, i.e. {0, sin²θ} — Out[1]."],
"dS2": [
 "dh = ∂_{θ}h dθ + ∂_{φ}h dφ.",
 "h = sin θ cos φ: ∂_{θ}h = cos θ cos φ, ∂_{φ}h = −sin θ sin φ.",
 "dh = {cos θ cos φ, −sin θ sin φ} — Out[1]."],
"star1": [
 "The area form of the unit sphere is sin θ dθ ∧ dφ, and ⋆ rotates a covector by 90° in the metric.",
 "⋆dθ = sin θ dφ and ⋆dφ = −dθ/sin θ, so ⋆(a dθ + b dφ) = −(b/sin θ) dθ + a sin θ dφ.",
 "a = 1, b = 0 gives {0, sin θ} — Out[1]; applying ⋆ again gives {−1, 0} = −dθ, so ⋆⋆ = −1."],
"surfaceCurvatures": [
 "Torus X = ((2 + cos v) cos u, (2 + cos v) sin u, sin v): X_{u} has length 2 + cos v, X_{v} length 1, X_{u}·X_{v} = 0, so E = (2 + cos v)², F = 0, G = 1 and dA = 2 + cos v.",
 "With n = X_{u} × X_{v}/|…|, the second form is L = −cos v (2 + cos v), M = 0, N = −1.",
 "K = (LN − M²)/(EG − F²) = cos v (2 + cos v)/(2 + cos v)² = cos v/(2 + cos v).",
 "H = (EN + GL)/(2EG) = −((2 + cos v)² + cos v (2 + cos v))/(2(2 + cos v)²) = −(1 + cos v)/(2 + cos v) — Out[1] (the sign follows n)."],
"meanCurvatureVector": [
 "Catenoid X = (cosh v cos u, cosh v sin u, v): E = G = cosh²v, F = 0, a conformal metric.",
 "So ΔX = (X_{uu} + X_{vv})/cosh²v.",
 "X_{uu} = (−cosh v cos u, −cosh v sin u, 0) and X_{vv} = (cosh v cos u, cosh v sin u, 0): they cancel.",
 "ΔX = 0, hence H = 0: the catenoid is minimal — Out[1]."],
"Kconformal": [
 "u = log 2 − log(1 + r²) with r² = x² + y².",
 "Δ₀ log(1 + r²) = 4/(1 + r²)², so Δ₀u = −4/(1 + r²)².",
 "e^{−2u} = (1 + r²)²/4.",
 "K = −e^{−2u} Δ₀u = 1: the stereographic metric is the round sphere — Out[1]."],
"curvatureSurface": [
 "The colour is κColour[K, 1] with K = cos v/(2 + cos v) from surfaceCurvatures.",
 "Outer equator v = 0: K = 1/3, light orange. Inner equator v = π: K = −1, full blue.",
 "Top and bottom circles v = ±π/2: K = 0, near-white — Out[1]."],
"κColour": [
 "The blend parameter is (1 + clip(k/s, −1, 1))/2.",
 "k = 1, s = 1: parameter 1, the last colour, CCN orange RGBColor[0.98, 0.56, 0.17] — Out[1].",
 "k = 0: parameter ½, the middle colour GrayLevel[0.96] — Out[2]. k = 5 is clipped to 1, so it equals Out[1] — the Possible Issues example."],
"κLegend": [
 "The legend samples κColour[t, s] for t from −s to s.",
 "s = 1: bottom −1 blue, middle 0 near-white, top +1 orange, labelled K — Out[1]."],
"F0": [
 "F0(x, y, z) = eˣ(1 + z)² + y z³.",
 "At the north pole (0, 0, 1): e⁰ · 2² + 0 = 4 — Out[1]."],
"ΔS2amb": [
 "On the sphere z/|X| restricts to cos θ, a degree-1 harmonic: Δ cos θ = −2 cos θ.",
 "At the pole cos θ = 1, so the value is −2 — Out[1]."],
"atPole": [
 "Substitute x = 0, y = 0, z = 1 into eˣ(1 + z)² + y z³.",
 "1 · 4 + 0 = 4 — Out[1]."],
"exactMean": [
 "The curved expansion gives mean ≈ f + r²Δf/4 + r⁴(Δ²f/64 + KΔf/96) with f = 4, Δf = −4, Δ²f = −20, K = 1.",
 "r = 1/10: 4 − 0.01 − (5/16 + 1/24) · 10⁻⁴ = 4 − 0.01 − 0.0000354 = 3.9899646.",
 "The r⁶ term adds 63/320 · 10⁻⁶ ≈ 2 × 10⁻⁷: 3.9899648 — Out[1] (3.98996478…)."],
"flat4": [
 "f + r²Δf/4 + r⁴Δ²f/64 with f = 4, Δf = −4, Δ²f = −20.",
 "= 4 − r² − 20r⁴/64 = 4 − r² − 5r⁴/16 — Out[1]."],
"curved4": [
 "Add the curvature term r⁴ K Δf/96 = r⁴ · (−4)/96 = −r⁴/24 to flat4.",
 "−5/16 − 1/24 = −15/48 − 2/48 = −17/48: 4 − r² − 17r⁴/48 — Out[1]."],
"curved6": [
 "r⁶ coefficient: Δ³f/2304 + KΔ²f/1152 + K²Δf/1440 with Δ³f = 500, Δ²f = −20, Δf = −4.",
 "Over 11520: 2500 − 200 − 32 = 2268, and 2268/11520 = 63/320.",
 "4 − r² − 17r⁴/48 + 63r⁶/320 — Out[1]."],
"heatTrace": [
 "McKean–Singer on the unit sphere (area 4π, K = 1): t · Tr e^{tΔ} = 1 + t/3 + t²/15 + O(t³).",
 "t = 0.01: 1 + 0.0033333 + 0.0000067 = 1.0033400 — Out[1] (1.00334001…)."],
"torusTrace": [
 "A flat square torus of side L₀ = 2√π has area 4π, the same as the unit sphere, and K = 0.",
 "So Weyl’s term is exact to all orders: Tr e^{tΔ} ≈ Area/(4πt) = 1/t = 100 at t = 0.01.",
 "0.01 · 100/π = 1/π = 0.31831 — Out[1]."],
"ratio": [
 "Sphere: ratio = t · Tr e^{tΔ} ≈ 1 + t/3 + t²/15; at t = 0.1 this is 1 + 0.03333 + 0.00067 = 1.0340.",
 "Flat torus: no curvature correction, ratio 1.0000.",
 "{1.0340, 1.0000} — Out[1]."],
"angle": [
 "At vertex 1 = (0, 0, 0) the edges go to (1, 0, 0) and (0, 1, 0).",
 "Their dot product is 0, so the angle is π/2 — Out[1]."],
"idx": [
 "idx[i, j] = (i mod nu) · nvv + (j mod nvv) + 1 with nu = 40, nvv = 20.",
 "idx[0, 0] = 1; idx[1, 0] = 20 + 1 = 21; idx[40, 21] wraps to (0, 1) and gives 2 — Out[1]."],
"meshCurvature": [
 "Discrete Gauss–Bonnet: the angle defects of a closed mesh add up to exactly 2πχ.",
 "A torus has χ = V − E + F = 0, so Σ defect = 0 — Out[1].",
 "On the outer equator the smooth K is 1/3; defect/area there is 0.335 — Out[2]."],
"nbr": ["In CycleGraph[6] vertex 1 is joined to 2 and 6 — Out[1]."],
"edges": ["CycleGraph[4] has the four edges 1–2, 1–4, 2–3, 3–4 — Out[1]."],
"Δgraph": [
 "Δf(1) = mean of f over the neighbours of 1, minus f(1). In C₄ the neighbours of 1 are 2 and 4.",
 "f(v) = v²: (4 + 16)/2 − 1 = 9 — Out[1]."],
"μLazy": [
 "α = ½ stays at vertex 1; the other ½ is split evenly over its two neighbours 2 and 6.",
 "<|1 → ½, 2 → ¼, 6 → ¼|> — Out[1]."],
"W1": [
 "Two point masses: the only plan moves all the mass from 1 to 4.",
 "In C₆ the distance from 1 to 4 is 3, so W₁ = 3 — Out[1]."],
"κOllivier": [
 "In K₅ the walks at 1 and 2 share three common neighbours with mass ¼ each; only the ¼ on 2 must move to 1, a distance 1.",
 "The test function f = 1 at 2, 0 elsewhere shows W₁ ≥ ¼, so W₁ = ¼.",
 "κ₀ = 1 − ¼ = 3/4 — Out[1]."],
"κLLY": [
 "Use κ_{LLY} = 2κ_{1/2} on an edge xy of Q₃: the ½-lazy walk puts ½ at home and ⅙ on each neighbour.",
 "m_{x} has ½ on x, ⅙ on y; m_{y} has ⅙ on x, ½ on y: move ⅓ from x to y (cost ⅓).",
 "The other two neighbours of x each sit next to one of the other neighbours of y (the cube’s squares): move ⅙ + ⅙ a distance 1 (cost ⅓).",
 "W₁ = 2/3, κ_{1/2} = 1/3, κ_{LLY} = 2/3 — Out[1]."],
"bakryEmery": [
 "Bakry–Émery asks for the largest K with Γ₂(f) ≥ K Γ(f) at x for every f. A single test function gives an upper bound.",
 "On C₆ take f(v) = v near x (a straight line). Then Δf = 0 at x and its neighbours, and Γ(f) = ½ on the 2-ball.",
 "Γ₂(f)(x) = ½ ΔΓ(f)(x) − Γ(f, Δf)(x) = 0 − 0 = 0 while Γ(f)(x) = ½, so K ≤ 0.",
 "The kernel’s bisection shows K = 0 is attained: bakryEmery[CycleGraph[6], 1] = 0 — the first value of Out[2]."],
"forman": [
 "Forman’s edge curvature is 4 − deg x − deg y.",
 "In K₅ both endpoints have degree 4: 4 − 4 − 4 = −4 — Out[1]."],
"formanAug": [
 "Each edge of K₅ lies in 3 triangles (one for each other vertex).",
 "4 − 4 − 4 + 3 · 3 = 5 — Out[1]."],
"resistance": [
 "In C₄ two adjacent vertices are joined by a path of resistance 1 and a parallel path of resistance 3: 1 · 3/(1 + 3) = 3/4.",
 "Opposite vertices: two parallel paths of resistance 2: 2 · 2/4 = 1.",
 "Rows {0, 0.75, 1, 0.75}, … — Out[1]."],
"pNode": [
 "In C₆ each edge has resistance 1 · 5/6 = 5/6 (the edge in parallel with the other 5).",
 "p = 1 − ½ (5/6 + 5/6) = 1/6 = 0.167 at every vertex — Out[1]; six of them sum to 1."],
"steinerberger": [
 "In K₅ the distance matrix is D = J − I (J all ones), and by symmetry K is constant, K = c·1.",
 "(D·K)_{i} = 4c must equal n = 5, so c = 5/4 = 1.25 — Out[1]."],
"higuchiVertex": [
 "Higuchi: κ(v) = 1 − d/2 + Σ 1/|face| over the faces at v.",
 "Dodecahedron: d = 3, three pentagons: 1 − 3/2 + 3/5 = 1/10 — Out[1]."],
"higuchiTotal": [
 "Tetrahedron: 4 vertices, each 1 − 3/2 + 3/3 = ½: total 2.",
 "Cube: 8 vertices, each 1 − 3/2 + 3/4 = ¼: total 2.",
 "Truncated icosahedron: 60 vertices, each 1 − 3/2 + 1/5 + 2/6 = 1/30: total 2 — Out[1]."],
"normLap": [
 "C₃: D = 2I, so I − D^{−1/2} A D^{−1/2} = I − A/2.",
 "Diagonal 1, off-diagonal −½ — Out[1]."],
"spec": [
 "C₆ is 2-regular, so the normalised Laplacian is I − A/2 with eigenvalues 1 − cos(2πk/6), k = 0…5.",
 "1 − {1, ½, −½, −1, −½, ½} = {0, ½, 3/2, 2, 3/2, ½}; sorted {0, ½, ½, 3/2, 3/2, 2} — Out[1]."],
"Lpc": [
 "Belkin–Niyogi: the heat-kernel average approximates f + tΔf, so (mean − f)/t → Δf.",
 "f = z on S² is an l = 1 harmonic: Δz = −2z = −2 at the north pole.",
 "The point cloud gives −2.05, within the sampling error — Out[1]."],
"edgeCurvaturePlot": [
 "In the dumbbell the bridge edge 5–6 joins degree 5 to degree 2 with no shared neighbour; the tree formula gives κ_{LLY} = 2/5 + 2/2 − 2 = −3/5 (blue).",
 "The middle edge 6–7 joins two degree-2 vertices: 2/2 + 2/2 − 2 = 0 (white).",
 "Inside each K₅ clique the edges are positive (orange) — Out[1]."],
"vertexCurvaturePlot": [
 "On a tree every edge has resistance 1, so p(v) = 1 − deg(v)/2.",
 "Root (degree 2): 0, white. The 6 inner vertices (degree 3): −½, blue. The 8 leaves: +½, orange.",
 "Total 0 − 3 + 4 = 1, as resistance curvature always sums to 1 — Out[1]."],
"edgePicture": [
 "For the edge 1–2 of K₅ the three other vertices are neighbours of both ends: all shared (purple).",
 "κ_{LLY} = 5/4 and κ₀ = 3/4 (see κOllivier), the values in the label — Out[1]."],
"row": [
 "row only lays plots side by side; nothing is computed.",
 "C₅ and K₄ appear in one row 1100 points wide — Out[1]."],
"u0": [
 "u₀(0, 0) = 0.3 cos 0 + 0.25 sin 0 · cos 0 = 0.3 — Out[1]."],
"Kt": [
 "At t = 0, w = u₀. At the origin u₀ = 0.3, and Δ₀u₀ = −0.3 (the second term has Δ₀ = 0 there because it contains sin 2y).",
 "K = −e^{−2u}Δ₀u = −e^{−0.6}(−0.3) = 0.1646 — Out[1]."],
"maxK": [
 "Ricci flow on the torus converges to the flat metric, the only metric with constant K and ∬K dA = 0.",
 "So max |K| must decay: 4.827 at t = 0, 0.147 at t = 1, 0.059 at t = 2 — Out[1]."],
"totalK": [
 "∬K dA = ∬ −e^{−2w}Δ₀w · e^{2w} dx dy = −∬Δ₀w dx dy.",
 "The integral of a Laplacian over a closed torus is 0 (divergence theorem with no boundary).",
 "{0, 0, 0} at every time — Out[1]; this is Gauss–Bonnet with χ = 0."],
"lapCurve": [
 "On a circle of radius 1 sampled at spacing h, the second difference (X_{k−1} − 2X_{k} + X_{k+1})/h² points to the centre with length 1/r.",
 "r = 1, so the length is 1 — Out[1]: the curvature of the circle."],
"polyArea": [
 "Shoelace: A = ½ |Σ (x_{k} y_{k+1} − x_{k+1} y_{k})|.",
 "Unit square: ½ |0 + 1 + 1 + 0| = 1 — Out[1]."],
"resample": [
 "The square with side 2 has perimeter 8; 4 points evenly spaced by arc length are 2 apart.",
 "Starting at (0, 0) they land on the four corners — Out[1]."],
"κS2": [
 "The sliding-coupling series on the unit sphere is κ = ε²/8 − ε⁴/64 + …",
 "κ/ε² = 1/8 − ε²/64 = 0.125 − 0.0025/64 = 0.12496 at ε = 0.05 — Out[1]."],
"κH2": [
 "On the hyperbolic plane K = −1: κ = −ε²/8 − ε⁴/64 + …",
 "κ/ε² = −0.125 − 0.000039 = −0.12504 at ε = 0.05 — Out[1]."],
"Lap": [
 "Lap is laplaceBeltrami on the unit sphere: Δu = (1/sin θ)∂_{θ}(sin θ ∂_{θ}u) + ∂²_{φ}u/sin²θ.",
 "u = cos θ: (1/sin θ)∂_{θ}(−sin²θ) = −2 cos θ — Out[1]."],
"g2": [
 "|∇u|² = (∂_{θ}u)² + (∂_{φ}u)²/sin²θ.",
 "u = sin θ cos φ: cos²θ cos²φ + sin²φ — Out[1]."],
"Hs": [
 "Same computation as hessian: H_{θθ} = −cos θ, H_{φφ} = −Γ^θ_{φφ} ∂_{θ} cos θ = −sin²θ cos θ, H_{θφ} = 0.",
 "{{−cos θ, 0}, {0, −cos θ sin²θ}} — Out[1]."],
"rough": [
 "ω = sin²θ dφ = ⋆d(−cos θ) has Hodge Laplacian 2ω, and Ric = 1 on S².",
 "∇*∇ω = 2ω − ω = ω = {0, sin²θ} — Out[1]."],
"star": [
 "⋆(a dθ + b dφ) = −(b/sin θ) dθ + a sin θ dφ.",
 "a = 1, b = 0: {0, sin θ} — Out[1]."],
"Δg": [
 "In C₄ the neighbours of 1 are 2 and 4; f(v) = v².",
 "(4 + 16)/2 − 1 = 9 — Out[1]."],
}
