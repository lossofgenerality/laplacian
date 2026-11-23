# Reference content for the Laplacian Curvature Lab programmer's manual.
# Examples: (input, output) — output filled from the kernel and verified; "IMG:key" = picture.
# setup: hidden code run before an example during verification (not shown).

TITLE = "Laplacian Curvature Lab"
SUBTITLE = "Wolfram Language reference for the CCN curvature code: Riemannian formulas, surfaces, mean values, spectra, meshes, graph curvatures and flows."
REPO = "https://github.com/lossofgenerality/laplacian"
SITE = "https://lossofgenerality.github.io/laplacian/"
LAB = "https://lossofgenerality.github.io/laplacian/lab/Laplacian_Curvature_Lab.html"

GUIDES = [
 ("riemannian", "Riemannian Toolkit", "Coordinate formulas for metrics: Christoffel symbols, the Laplace–Beltrami operator, gradients, covariant Hessians, Gauss curvature, and the rough Laplacian on 1-forms. Every other smooth computation in the code base is built on these.",
  ["christoffel", "laplaceBeltrami", "gradNorm2", "hessian", "hessNorm2", "gaussCurvature", "roughLaplacian1", "dS2", "star1"]),
 ("surfaces", "Surfaces and Curvature", "Gauss and mean curvature of parametrised surfaces in ℝ³, the conformal (Liouville) form of K, the mean-curvature vector ΔX = −2H n, and curvature-coloured surface plots.",
  ["surfaceCurvatures", "meanCurvatureVector", "Kconformal", "curvatureSurface", "κColour", "κLegend"]),
 ("means", "Mean Values and Volumes", "The curved mean-value expansion of Δ on the sphere: a test function, the ambient-coordinate sphere Laplacian, pole evaluation, the exact circle mean and the flat and curved approximations.",
  ["F0", "ΔS2amb", "atPole", "exactMean", "flat4", "curved4", "curved6"]),
 ("spectral", "Spectral Geometry", "Heat traces of the unit sphere and of a flat torus with the same area, and their ratio to Weyl’s leading term.",
  ["heatTrace", "torusTrace", "ratio"]),
 ("mesh", "Discrete Surfaces", "Triangle meshes: corner angles, torus vertex indexing, and the angle defect, vertex area and cotangent Laplacian of a mesh.",
  ["angle", "idx", "meshCurvature"]),
 ("graphs", "Graph Curvature", "Curvatures of graphs built from the graph Laplacian: Ollivier and Lin–Lu–Yau (optimal transport and the Münch–Wojciechowski linear program), Bakry–Émery, Forman, resistance, Steinerberger and Higuchi curvature, and the normalised spectrum.",
  ["nbr", "edges", "Δgraph", "μLazy", "W1", "κOllivier", "κLLY", "bakryEmery", "forman", "formanAug", "resistance", "pNode", "steinerberger", "higuchiVertex", "higuchiTotal", "normLap", "spec", "Lpc"]),
 ("graphviz", "Graph Visualization", "Graph drawings coloured by curvature, single-edge neighbourhood pictures for Ollivier curvature, and a row layout for families of graphs.",
  ["edgeCurvaturePlot", "vertexCurvaturePlot", "edgePicture", "row"]),
 ("flows", "Flows and Further Instances", "Ricci flow in conformal form on a flat torus, curve-shortening flow of a polygon, and Ollivier curvature of ε-balls on the sphere and the hyperbolic plane.",
  ["u0", "Kt", "maxK", "totalK", "lapCurve", "polyArea", "resample", "κS2", "κH2"]),
 ("snippets", "Lab Snippet Functions", "Short self-contained definitions used by the Wolfram cells of the Laplacian Curvature Lab page. Each is a compact twin of a notebook function.",
  ["Lap", "g2", "Hs", "rough", "star", "Δg"]),
]

G1 = 'gS2 = {{1, 0}, {0, Sin[θ]^2}}; 𝓍S2 = {θ, φ};'
TORUS = 'torusPos = {(2 + Cos[v]) Cos[u], (2 + Cos[v]) Sin[u], Sin[v]};'
POLE = 'ext = F0[{x, y, z}/Sqrt[x^2 + y^2 + z^2]]; L1 = ΔS2amb[ext]; L2 = ΔS2amb[L1]; L3 = ΔS2amb[L2]; {p0, d1, d2, d3} = atPole /@ {ext, L1, L2, L3};'
MESH = TORUS + ' {nu, nvv} = {40, 20}; PT = Flatten[Table[N[torusPos /. {u -> 2 π i/nu, v -> 2 π j/nvv}], {i, 0, nu - 1}, {j, 0, nvv - 1}], 1]; TT = Flatten[Table[{{idx[i, j], idx[i + 1, j], idx[i + 1, j + 1]}, {idx[i, j], idx[i + 1, j + 1], idx[i, j + 1]}}, {i, 0, nu - 1}, {j, 0, nvv - 1}], 2];'
RICCI = 'solR = Quiet@First@NDSolve[{D[w[t, x, y], t] == Exp[-2 w[t, x, y]] (D[w[t, x, y], {x, 2}] + D[w[t, x, y], {y, 2}]), w[0, x, y] == u0[x, y], w[t, 0, y] == w[t, 2 π, y], w[t, x, 0] == w[t, x, 2 π]}, w, {t, 0, 2}, {x, 0, 2 π}, {y, 0, 2 π}, Method -> {"MethodOfLines", "SpatialDiscretization" -> {"TensorProductGrid", "MinPoints" -> 31, "MaxPoints" -> 31}}];'
CURVE = 'nC = 160; Xc = Table[(1 + 0.35 Cos[3 θ] + 0.2 Sin[5 θ]) {Cos[θ], Sin[θ]}, {θ, 0., 2 π - 2 π/nC, 2 π/nC}];'

P = {}
def page(name, guide, defined, usage, details, examples, see, setup="", kind="Function"):
    P[name] = dict(name=name, guide=guide, defined=defined, usage=usage, details=details, examples=examples, see=see, setup=setup, kind=kind)

# ------------------------------------------------------------------ Riemannian toolkit
page("christoffel", "riemannian", "Notebook §1",
 [("christoffel[g, 𝓍]", "gives the Christoffel symbols Γⁱⱼₖ of the metric matrix g in coordinates 𝓍, as a nested list indexed [[i, j, k]].")],
 ["Γⁱⱼₖ = ½ Σₗ gⁱˡ (∂ⱼ gₗₖ + ∂ₖ gₗⱼ − ∂ₗ gⱼₖ); the result is symmetric in j and k.",
  "g is an n×n symmetric matrix of expressions in the coordinate list 𝓍 of length n.",
  "The result is simplified with Simplify."],
 {"Basic Examples": [(G1 + "\nchristoffel[gS2, 𝓍S2]", None)],
  "Scope": [("christoffel[{{1, 0}, {0, r^2}}, {r, ϑ}]", None)],
  "Properties & Relations": [("With[{Γ = christoffel[gS2, 𝓍S2]}, Table[Γ[[i, j, k]] - Γ[[i, k, j]], {i, 2}, {j, 2}, {k, 2}]]", None)]},
 ["hessian", "gaussCurvature", "laplaceBeltrami", "roughLaplacian1"], setup=G1)
page("laplaceBeltrami", "riemannian", "Notebook §1",
 [("laplaceBeltrami[g, 𝓍][u]", "gives the Laplace–Beltrami operator Δu = (1/√det g) Σ ∂ᵢ(√det g gⁱʲ ∂ⱼu) of u for the metric g in coordinates 𝓍.")],
 ["laplaceBeltrami[g, 𝓍] is an operator: apply it to an expression, or map it over a list.",
  "The sign convention is the analyst’s: Δ = div grad, so Δ ≤ 0 on a closed manifold.",
  "The result is not simplified; wrap it in Simplify when needed."],
 {"Basic Examples": [(G1 + "\nSimplify[laplaceBeltrami[gS2, 𝓍S2][Cos[θ]]]", None)],
  "Scope": [("Simplify[laplaceBeltrami[{{1, 0}, {0, 1}}, {x, y}][x^2 y]]", None),
            (G1 + "\nSimplify[laplaceBeltrami[gS2, 𝓍S2][θ]]", None)],
  "Properties & Relations": [("Simplify[laplaceBeltrami[{{1, 0}, {0, 1}}, {x, y}][F[x, y]] == Laplacian[F[x, y], {x, y}]]", None)]},
 ["gradNorm2", "hessian", "meanCurvatureVector", "Lap"], setup=G1)
page("gradNorm2", "riemannian", "Notebook §1",
 [("gradNorm2[g, 𝓍][u]", "gives |∇u|² = Σ gⁱʲ ∂ᵢu ∂ⱼu for the metric g in coordinates 𝓍.")],
 ["Used in the Bochner formula ½Δ|∇f|² = |Hess f|² + ⟨∇f, ∇Δf⟩ + Ric(∇f, ∇f)."],
 {"Basic Examples": [(G1 + "\ngradNorm2[gS2, 𝓍S2][Sin[θ] Cos[φ]]", None)]},
 ["hessNorm2", "laplaceBeltrami", "g2"], setup=G1)
page("hessian", "riemannian", "Notebook §1",
 [("hessian[g, 𝓍][u]", "gives the covariant Hessian ∇ᵢ∇ⱼu = ∂ᵢ∂ⱼu − Σ Γᵏᵢⱼ ∂ₖu as a matrix.")],
 ["The trace with the inverse metric, Tr[g⁻¹·hessian], is the Laplace–Beltrami operator."],
 {"Basic Examples": [(G1 + "\nSimplify[hessian[gS2, 𝓍S2][Cos[θ]]]", None)],
  "Properties & Relations": [(G1 + "\nSimplify[Tr[Inverse[gS2] . hessian[gS2, 𝓍S2][F[θ, φ]]] - laplaceBeltrami[gS2, 𝓍S2][F[θ, φ]]]", None)]},
 ["christoffel", "hessNorm2", "laplaceBeltrami", "Hs"], setup=G1)
page("hessNorm2", "riemannian", "Notebook §1",
 [("hessNorm2[g, 𝓍][u]", "gives |Hess u|² = Tr[g⁻¹ H g⁻¹ H] with H the covariant Hessian of u.")],
 ["The squared Hessian term of the Bochner formula."],
 {"Basic Examples": [(G1 + "\nSimplify[hessNorm2[gS2, 𝓍S2][Cos[θ]]]", None)]},
 ["hessian", "gradNorm2"], setup=G1)
page("gaussCurvature", "riemannian", "Notebook §1",
 [("gaussCurvature[g, 𝓍]", "gives the Gauss curvature of a two-dimensional metric g in coordinates 𝓍, from the Riemann tensor: K = R₁₂₁₂ / det g.")],
 ["g must be 2×2. For embedded surfaces see surfaceCurvatures; for conformal metrics see Kconformal."],
 {"Basic Examples": [(G1 + "\ngaussCurvature[gS2, 𝓍S2]", None)],
  "Scope": [("gaussCurvature[{{1, 0}, {0, Sinh[r]^2}}, {r, φ}]", None),
            ("gaussCurvature[{{(2 + Cos[v])^2, 0}, {0, 1}}, {u, v}]", None)],
  "Properties & Relations": [("Simplify[Kconformal[w[x, y]] - gaussCurvature[Exp[2 w[x, y]] IdentityMatrix[2], {x, y}]]", None)]},
 ["Kconformal", "surfaceCurvatures", "christoffel"], setup=G1)
page("roughLaplacian1", "riemannian", "Notebook §10.1",
 [("roughLaplacian1[g, 𝓍][ω]", "gives the rough (connection) Laplacian ∇*∇ω = −gʲᵏ ∇ₖ∇ⱼ ω of the 1-form ω, given as its list of components.")],
 ["Second covariant derivatives are built from christoffel.",
  "With the Hodge Laplacian it verifies the Weitzenböck identity Δ_{Hodge} = ∇*∇ + Ric."],
 {"Basic Examples": [(G1 + "\nSimplify[roughLaplacian1[gS2, 𝓍S2][{0, Sin[θ]^2}]]", None)],
  "Properties & Relations": [(G1 + "\nWith[{ΔS2 = laplaceBeltrami[gS2, 𝓍S2]}, Simplify[dS2[-ΔS2[F[θ, φ]]] + star1[dS2[-ΔS2[H[θ, φ]]]] - (roughLaplacian1[gS2, 𝓍S2][dS2[F[θ, φ]] + star1[dS2[H[θ, φ]]]] + dS2[F[θ, φ]] + star1[dS2[H[θ, φ]]])]]", None)]},
 ["dS2", "star1", "christoffel", "rough"], setup=G1)
page("dS2", "riemannian", "Notebook §10.1",
 [("dS2[h]", "gives the differential dh of a function h(θ, φ) on S² as its covector {∂θh, ∂φh}.")],
 ["Defined for the coordinates θ, φ of the unit sphere."],
 {"Basic Examples": [("dS2[Sin[θ] Cos[φ]]", None)]},
 ["star1", "roughLaplacian1"])
page("star1", "riemannian", "Notebook §10.1",
 [("star1[{a, b}]", "gives the Hodge star of the 1-form a dθ + b dφ on the unit sphere: {−b/sin θ, a sin θ}.")],
 ["Every 1-form on S² is df + ⋆dh, because S² has no harmonic 1-forms.",
  "Applying star1 twice gives −1, as for any 1-form in two dimensions."],
 {"Basic Examples": [("star1[{1, 0}]", None)],
  "Properties & Relations": [("Simplify[star1[star1[{a, b}]]]", None)]},
 ["dS2", "roughLaplacian1", "star"])

# ------------------------------------------------------------------ surfaces
page("surfaceCurvatures", "surfaces", "Notebook §1.1",
 [("surfaceCurvatures[pos, 𝓍]", "gives an Association with the Gauss curvature \"K\", mean curvature \"H\" and area element \"dA\" of the surface pos(u, v) ⊂ ℝ³ in parameters 𝓍.")],
 ["Uses the first fundamental form E, F, G and the second L, M, N: K = (LN − M²)/(EG − F²), H = (EN − 2FM + GL)/(2(EG − F²)).",
  "The sign of H follows the normal Xᵤ × Xᵥ; the sign of K does not depend on it."],
 {"Basic Examples": [(TORUS + "\nsurfaceCurvatures[torusPos, {u, v}]", None)],
  "Scope": [("surfaceCurvatures[{Sech[v] Cos[u], Sech[v] Sin[u], v - Tanh[v]}, {u, v}][\"K\"]", None),
            ("surfaceCurvatures[{u, v, u^2 - v^2}, {u, v}][\"K\"]", None)],
  "Properties & Relations": [(TORUS + "\nWith[{t = surfaceCurvatures[torusPos, {u, v}]}, Integrate[Simplify[t[\"K\"] t[\"dA\"], 0 < v < 2 π], {u, 0, 2 π}, {v, 0, 2 π}]]", None)]},
 ["meanCurvatureVector", "gaussCurvature", "curvatureSurface"])
page("meanCurvatureVector", "surfaces", "Notebook §3",
 [("meanCurvatureVector[pos, 𝓍]", "gives the mean curvature \"H\" from ΔX = −2H n and the \"tangential part\" of ΔX, which is zero."),
  ("meanCurvatureVector[pos, 𝓍, assum]", "simplifies under the extra assumptions assum.")],
 ["ΔX is the Laplace–Beltrami operator of the induced metric applied to each coordinate of pos.",
  "A surface is minimal exactly when its coordinate functions are harmonic."],
 {"Basic Examples": [("meanCurvatureVector[{Cosh[v] Cos[u], Cosh[v] Sin[u], v}, {u, v}]", None)],
  "Scope": [("meanCurvatureVector[3 {Sin[θ] Cos[φ], Sin[θ] Sin[φ], Cos[θ]}, {θ, φ}, 0 < θ < π]", None),
            ("meanCurvatureVector[{(2 + Cos[v]) Cos[u], (2 + Cos[v]) Sin[u], Sin[v]}, {u, v}]", None)]},
 ["surfaceCurvatures", "laplaceBeltrami"])
page("Kconformal", "surfaces", "Notebook §2",
 [("Kconformal[u]", "gives the Gauss curvature K = −e^{−2u} Δ₀u of the conformal metric e^{2u}(dx² + dy²), with u an expression in x and y.")],
 ["Δ₀ is the flat Laplacian in x, y. For constant K this is Liouville’s equation.",
  "The same identity makes 2-D Ricci flow the heat equation ∂u/∂t = e^{−2u}Δ₀u = −K."],
 {"Basic Examples": [("Kconformal[Log[2/(1 + x^2 + y^2)]]", None)],
  "Scope": [("Kconformal[Log[1/y]]", None), ("Kconformal[Log[2/(1 - x^2 - y^2)]]", None)]},
 ["gaussCurvature", "Kt"])
page("curvatureSurface", "surfaces", "Notebook §1.1",
 [("curvatureSurface[pos, {u, u0, u1}, {v, v0, v1}, κ, s, label]", "plots the surface pos coloured by the curvature expression κ on the scale ±s, titled label."),
  ("curvatureSurface[…, opts]", "passes options opts to ParametricPlot3D.")],
 ["Colours come from κColour: blue negative, near-white zero, CCN orange positive.",
  "κ is an expression in the same parameters u, v as pos."],
 {"Basic Examples": [(TORUS + "\ncurvatureSurface[torusPos, {u, 0, 2 π}, {v, 0, 2 π}, Cos[v]/(2 + Cos[v]), 1, \"Torus: K\"]", "IMG:curvsurf")]},
 ["κColour", "κLegend", "surfaceCurvatures"])
page("κColour", "surfaces", "Notebook §1.1",
 [("κColour[k, s]", "gives the curvature colour of the value k on the symmetric scale ±s.")],
 ["Values are clipped to [−s, s]: −s is blue RGBColor[0.18, 0.36, 0.78], 0 is GrayLevel[0.96], +s is CCN orange RGBColor[0.98, 0.56, 0.17]."],
 {"Basic Examples": [("κColour[1, 1]", None), ("κColour[0, 1]", None)],
  "Possible Issues": [("κColour[5, 1] === κColour[1, 1]", None)]},
 ["κLegend", "curvatureSurface", "edgeCurvaturePlot"])
page("κLegend", "surfaces", "Notebook §1.1",
 [("κLegend[s, name]", "gives a BarLegend for the κColour scale from −s to s, labelled name.")],
 ["Use with Legended to attach the scale to a plot."],
 {"Basic Examples": [("κLegend[1, \"K\"]", "IMG:legend")]},
 ["κColour", "curvatureSurface"])

# ------------------------------------------------------------------ mean values
page("F0", "means", "Notebook §4",
 [("F0[{x, y, z}]", "gives the test function eˣ(1 + z)² + y z³ used for the curved mean-value checks on S².")],
 ["At the north pole f = 4, Δf = −4, Δ²f = −20 and Δ³f = 500. Δf ≠ 0 there, so the curvature term KΔf/96 is visible."],
 {"Basic Examples": [("F0[{0, 0, 1}]", None)]},
 ["ΔS2amb", "atPole", "exactMean"])
page("ΔS2amb", "means", "Notebook §4",
 [("ΔS2amb[h]", "gives the Laplacian on the unit sphere of a degree-0 homogeneous function h of x, y, z, as |X|² Δ_ℝ³ h.")],
 ["Extend a function on S² by h(X/|X|); the result is again homogeneous of degree 0, so ΔS2amb can be iterated."],
 {"Basic Examples": [("ΔS2amb[z/Sqrt[x^2 + y^2 + z^2]] /. {x -> 0, y -> 0, z -> 1}", None)],
  "Properties & Relations": [("atPole /@ NestList[ΔS2amb, F0[{x, y, z}/Sqrt[x^2 + y^2 + z^2]], 3]", None)]},
 ["atPole", "F0", "laplaceBeltrami"])
page("atPole", "means", "Notebook §4",
 [("atPole[h]", "evaluates h at the north pole x = 0, y = 0, z = 1.")], [],
 {"Basic Examples": [("atPole[Exp[x] (1 + z)^2 + y z^3]", None)]},
 ["ΔS2amb", "F0"])
page("exactMean", "means", "Notebook §4.1",
 [("exactMean[r]", "gives the mean of F0 over the geodesic circle of colatitude r about the north pole, by numerical integration at 40-digit precision.")],
 ["Used to measure the error of flat4, curved4 and curved6; their errors fall like r⁴, r⁶ and r⁸."],
 {"Basic Examples": [("N[exactMean[1/10], 20]", None)],
  "Properties & Relations": [("N[Abs[exactMean[1/20] - {flat4[1/20], curved4[1/20], curved6[1/20]}], 3]", None)]},
 ["flat4", "curved4", "curved6", "F0"], setup=POLE)
page("flat4", "means", "Notebook §4.1",
 [("flat4[r]", "gives the flat-space circle-mean approximation f + r²Δf/4 + r⁴Δ²f/64 at the pole, with the pole values p0, d1, d2.")],
 ["Missing the curvature term, its error is of order r⁴."],
 {"Basic Examples": [("flat4[r]", None)]},
 ["curved4", "curved6", "exactMean"], setup=POLE)
page("curved4", "means", "Notebook §4.1",
 [("curved4[r]", "gives flat4[r] plus the curvature term r⁴KΔf/96 (K = 1 on the unit sphere).")],
 ["Its error is of order r⁶."],
 {"Basic Examples": [("curved4[r]", None)]},
 ["flat4", "curved6"], setup=POLE)
page("curved6", "means", "Notebook §4.1",
 [("curved6[r]", "gives curved4[r] plus the r⁶ terms Δ³f/2304 + KΔ²f/1152 + K²Δf/1440.")],
 ["Its error is of order r⁸. The coefficients are verified exactly against the Legendre series of P_l(cos r)."],
 {"Basic Examples": [("curved6[r]", None)]},
 ["curved4", "exactMean"], setup=POLE)

# ------------------------------------------------------------------ spectral
page("heatTrace", "spectral", "Notebook §5",
 [("heatTrace[t]", "gives the heat trace Σ (2l + 1) e^{−l(l+1)t} of the unit sphere, summed to l = 2000.")],
 ["t must be numeric. t·heatTrace[t] → 1 + t/3 + t²/15 as t → 0 (McKean–Singer)."],
 {"Basic Examples": [("0.01 heatTrace[0.01]", None)],
  "Properties & Relations": [("{0.01 heatTrace[0.01], 1 + 0.01/3 + 0.01^2/15}", None)]},
 ["torusTrace", "ratio"])
page("torusTrace", "spectral", "Notebook §5.1",
 [("torusTrace[t]", "gives the heat trace of the flat square torus of side L0 = 2√π (area 4π), as θ₃(0, e^{−(2π/L0)² t})².")],
 ["Same area as the unit sphere, zero curvature: its ratio to Weyl’s term stays 1."],
 {"Basic Examples": [("0.01 torusTrace[0.01]/π", None)]},
 ["heatTrace", "ratio"], setup="L0 = 2 Sqrt[π];")
page("ratio", "spectral", "Notebook §5.1",
 [("ratio[tr, t]", "gives the heat trace tr[t] divided by Weyl’s leading term Area/(4πt) for area 4π.")], [],
 {"Basic Examples": [("{ratio[heatTrace, 0.1], ratio[torusTrace, 0.1]}", None)]},
 ["heatTrace", "torusTrace"], setup="L0 = 2 Sqrt[π];")

# ------------------------------------------------------------------ mesh
page("angle", "mesh", "Notebook §7",
 [("angle[i, j, k]", "gives the angle at vertex i of the triangle (i, j, k) of the global vertex list P.")],
 ["Defined for the sphere mesh of Section 7; meshCurvature has its own local version."],
 {"Basic Examples": [("P = {{0, 0, 0}, {1, 0, 0}, {0, 1, 0}}; angle[1, 2, 3]", None)]},
 ["meshCurvature"])
page("idx", "mesh", "Notebook §7.1",
 [("idx[i, j]", "gives the 1-based vertex number of grid point (i, j) of the nu × nvv torus mesh, with wrap-around.")], [],
 {"Basic Examples": [("{nu, nvv} = {40, 20}; {idx[0, 0], idx[1, 0], idx[40, 21]}", None)]},
 ["meshCurvature"])
page("meshCurvature", "mesh", "Notebook §7.1",
 [("meshCurvature[P, T]", "gives an Association with the angle \"defect\", the vertex \"area\" and the cotangent Laplacian \"ΔX\" of the positions, for vertices P and triangles T.")],
 ["The angle defect of vertex i is 2π − (sum of the corner angles of the triangles meeting at i): how far the angles fall short of a flat 2π. A cube corner has defect 2π − 3·π/2 = π/2.",
  "defect/area approximates the Gauss curvature K; the defects of a closed mesh sum to exactly 2πχ, where χ = V − E + F is the Euler characteristic.",
  "\"ΔX\" approximates −2H n (Meyer–Desbrun–Schröder–Barr)."],
 {"Basic Examples": [("mt = meshCurvature[PT, TT]; Chop[Total[mt[\"defect\"]], 10^-9]", None)],
  "Scope": [("mt = meshCurvature[PT, TT]; Round[(mt[\"defect\"]/mt[\"area\"])[[{1, 6, 11}]], 0.001]", None)]},
 ["angle", "idx", "surfaceCurvatures"], setup=MESH)

# ------------------------------------------------------------------ graphs
GR = 'dumbbell = Graph[UndirectedEdge @@@ Join[List @@@ EdgeList[CompleteGraph[5]], (List @@@ EdgeList[CompleteGraph[5]]) + 7, {{5, 6}, {6, 7}, {7, 8}}]];'
page("nbr", "graphs", "Notebook §8.1",
 [("nbr[G, v]", "gives the neighbours of vertex v in the graph G.")], [],
 {"Basic Examples": [("nbr[CycleGraph[6], 1]", None)]}, ["edges", "Δgraph"])
page("edges", "graphs", "Notebook §8.1",
 [("edges[G]", "gives the edges of G as pairs {a, b}.")], [],
 {"Basic Examples": [("edges[CycleGraph[4]]", None)]}, ["nbr", "κLLY"])
page("Δgraph", "graphs", "Notebook §8.1",
 [("Δgraph[G, f][v]", "gives the random-walk Laplacian Δf(v) = mean of f over the neighbours of v − f(v).")],
 ["f is any function or Association of vertex values.",
  "This is the Laplacian used by κLLY and bakryEmery; its eigenvalues are minus those of normLap."],
 {"Basic Examples": [("Δgraph[CycleGraph[4], #^2 &][1]", None)]}, ["κLLY", "bakryEmery", "Δg"])
page("μLazy", "graphs", "Notebook §8.1",
 [("μLazy[G, x, α]", "gives the lazy random-walk measure at x: mass α at x and (1 − α)/deg x on each neighbour.")], [],
 {"Basic Examples": [("μLazy[CycleGraph[6], 1, 1/2]", None)]}, ["W1", "κOllivier"])
page("W1", "graphs", "Notebook §8.1",
 [("W1[G, μ, ν]", "gives the Wasserstein-1 distance between the measures μ and ν (Associations vertex → mass) on G, by linear programming.")],
 ["The ground metric is the graph distance."],
 {"Basic Examples": [("W1[CycleGraph[6], <|1 -> 1|>, <|4 -> 1|>]", None)]}, ["μLazy", "κOllivier"])
page("κOllivier", "graphs", "Notebook §8.1",
 [("κOllivier[G, {x, y}, α]", "gives Ollivier’s curvature 1 − W₁(μₓ^α, μᵧ^α)/d(x, y) with laziness α.")],
 ["α = 0 is the non-lazy curvature κ₀; 2κ_{1/2} equals the Lin–Lu–Yau curvature on every edge."],
 {"Basic Examples": [("κOllivier[CompleteGraph[5], {1, 2}, 0]", None)],
  "Properties & Relations": [("With[{G = PetersenGraph[]}, {2 κOllivier[G, {1, 3}, 1/2], κLLY[G, {1, 3}]}]", None)]},
 ["κLLY", "W1", "μLazy"])
page("κLLY", "graphs", "Notebook §8.1",
 [("κLLY[G, {x, y}]", "gives the Lin–Lu–Yau curvature of the edge xy by the Münch–Wojciechowski formula κ = inf {∇ₓᵧΔf : f 1-Lipschitz, f(y) − f(x) = 1}.")],
 ["A linear program over f on the union of the two neighbourhoods, with the graph distance as Lipschitz constraint.",
  "κ ≥ k > 0 on every edge implies λ₁ ≥ k for the normalised Laplacian."],
 {"Basic Examples": [("κLLY[HypercubeGraph[3], {1, 2}]", None)],
  "Scope": [("κLLY[KaryTree[15, 2], #] & /@ {{2, 4}, {4, 8}}", None),
            (GR + "\nκLLY[dumbbell, {6, 7}]", None)],
  "Properties & Relations": [("With[{G = CompleteGraph[5]}, {κLLY[G, {1, 2}], spec[G][[2]]}]", None)]},
 ["κOllivier", "bakryEmery", "spec"])
page("bakryEmery", "graphs", "Notebook §8.2",
 [("bakryEmery[G, x]", "gives the Bakry–Émery curvature K∞ at vertex x: the largest K with Γ₂(f)(x) ≥ K Γ(f)(x) for all f, rounded down to 6 digits.")],
 ["Γ is the carré du champ (“square of the field”), Γ(f) = ½(Δ(f²) − 2fΔf), which on a graph is ½ mean (f(y) − f(x))² over the neighbours y; Γ₂(f) = ½ΔΓ(f) − Γ(f, Δf) is the iterated carré du champ.",
  "Γ and Γ₂ are built from Δgraph on the 2-ball of x; K is found by bisection on the smallest eigenvalue of Γ₂ − KΓ.",
  "CD(K, ∞) implies λ₁ ≥ K."],
 {"Basic Examples": [("bakryEmery[CompleteGraph[5], 1]", None)],
  "Scope": [("bakryEmery[#, 1] & /@ {CycleGraph[6], HypercubeGraph[3], PetersenGraph[]}", None)]},
 ["κLLY", "Δgraph", "spec"])
page("forman", "graphs", "Notebook §8.3",
 [("forman[G, {x, y}]", "gives the Forman curvature 4 − deg x − deg y of the edge xy.")], [],
 {"Basic Examples": [("forman[CompleteGraph[5], {1, 2}]", None)]}, ["formanAug"])
page("formanAug", "graphs", "Notebook §8.3",
 [("formanAug[G, {x, y}]", "gives the augmented Forman curvature 4 − deg x − deg y + 3·#triangles(xy).")], [],
 {"Basic Examples": [("formanAug[CompleteGraph[5], {1, 2}]", None)]}, ["forman"])
page("resistance", "graphs", "Notebook §8.4",
 [("resistance[G]", "gives the matrix of effective resistances ωᵢⱼ = L⁺ᵢᵢ + L⁺ⱼⱼ − 2L⁺ᵢⱼ, with L the Kirchhoff matrix.")],
 ["Foster’s theorem: the resistances of the edges sum to n − 1."],
 {"Basic Examples": [("Round[resistance[CycleGraph[4]], 0.001]", None)],
  "Properties & Relations": [("With[{G = PetersenGraph[]}, Chop[Total[resistance[G][[#1, #2]] & @@@ edges[G]]]]", None)]},
 ["pNode", "steinerberger"])
page("pNode", "graphs", "Notebook §8.4",
 [("pNode[G]", "gives the resistance node curvatures pᵢ = 1 − ½ Σⱼ∼ᵢ ωᵢⱼ.")],
 ["They always sum to 1: a discrete Gauss–Bonnet theorem."],
 {"Basic Examples": [("Round[pNode[CycleGraph[6]], 0.001]", None)],
  "Properties & Relations": [(GR + "\nChop[Total[pNode[dumbbell]]]", None)]},
 ["resistance", "steinerberger"])
page("steinerberger", "graphs", "Notebook §8.5",
 [("steinerberger[G]", "gives Steinerberger’s vertex curvatures K solving D·K = n·1, with D the distance matrix (least squares).")],
 ["On a tree, distance equals resistance, so steinerberger and pNode are proportional."],
 {"Basic Examples": [("Round[steinerberger[CompleteGraph[5]], 0.001]", None)],
  "Properties & Relations": [("Correlation[steinerberger[KaryTree[15, 2]], pNode[KaryTree[15, 2]]]", None)]},
 ["pNode", "resistance"])
page("higuchiVertex", "graphs", "Notebook §8.6",
 [("higuchiVertex[name]", "gives Higuchi’s combinatorial curvature 1 − d/2 + Σ 1/|face| at each vertex of the polyhedron name.")], [],
 {"Basic Examples": [("Union[higuchiVertex[\"Dodecahedron\"]]", None)]}, ["higuchiTotal"])
page("higuchiTotal", "graphs", "Notebook §8.5",
 [("higuchiTotal[name]", "gives the total Higuchi curvature of the polyhedron name, which is χ = 2 for convex polyhedra.")], [],
 {"Basic Examples": [("higuchiTotal /@ {\"Tetrahedron\", \"Cube\", \"TruncatedIcosahedron\"}", None)]}, ["higuchiVertex"])
page("normLap", "graphs", "Notebook §9",
 [("normLap[G]", "gives the normalised Laplacian I − D^{−1/2} A D^{−1/2} of G as a numerical matrix.")],
 ["Its eigenvalues lie in [0, 2]."], {"Basic Examples": [("normLap[CycleGraph[3]]", None)]}, ["spec"])
page("spec", "graphs", "Notebook §9",
 [("spec[G]", "gives the sorted eigenvalues of normLap[G].")],
 ["spec[G][[2]] is λ₁, the spectral gap compared with κLLY and bakryEmery."],
 {"Basic Examples": [("Chop[spec[CycleGraph[6]]]", None)]}, ["normLap", "κLLY", "bakryEmery"])
page("Lpc", "graphs", "Notebook §9",
 [("Lpc[p]", "gives the heat-kernel point-cloud Laplacian of f = z at the point p: (weighted mean of z − z(p))/tPC over the global point set pts, with Gaussian weights of width tPC.")],
 ["Belkin–Niyogi: as the points fill the manifold and t → 0 this converges to Δz = −2z on S²."],
 {"Basic Examples": [("Lpc[{0, 0, 1.}]", None)]}, ["spec"],
 setup='pts = SpherePoints[20000]; tPC = 0.002; nf = Nearest[pts];')

# ------------------------------------------------------------------ graph visualization
FAM = GR + ' family = <|"Binary tree" -> KaryTree[15, 2], "Cycle C6" -> CycleGraph[6], "Cube Q3" -> HypercubeGraph[3], "Complete K5" -> CompleteGraph[5], "Petersen" -> PetersenGraph[], "Grid 5×5" -> GridGraph[{5, 5}], "Dumbbell" -> dumbbell|>;'
page("edgeCurvaturePlot", "graphviz", "Notebook §8.6",
 [("edgeCurvaturePlot[G, κf, s, label]", "draws G with each edge coloured by κf[G, edge] on the κColour scale ±s.")], [],
 {"Basic Examples": [(GR + "\nedgeCurvaturePlot[dumbbell, κLLY, 1.25, Row[{\"Dumbbell: \", Subscript[\"κ\", \"LLY\"]}]]", "IMG:edgeplot")]},
 ["vertexCurvaturePlot", "κLLY", "κColour"])
page("vertexCurvaturePlot", "graphviz", "Notebook §8.6",
 [("vertexCurvaturePlot[G, kv, s, label]", "draws G with vertex i coloured by kv[[i]] on the κColour scale ±s.")], [],
 {"Basic Examples": [("vertexCurvaturePlot[KaryTree[15, 2], pNode[KaryTree[15, 2]], 0.3, \"Tree: resistance p\"]", "IMG:vertexplot")]},
 ["edgeCurvaturePlot", "pNode", "bakryEmery"])
page("edgePicture", "graphviz", "Notebook §8.6",
 [("edgePicture[G, {x, y}, label]", "draws G with the edge xy in black, the union of the two neighbourhoods in orange and the shared neighbours in purple, labelled with κLLY and κ₀.")], [],
 {"Basic Examples": [("edgePicture[CompleteGraph[5], {1, 2}, \"K5\"]", "IMG:edgepic")]}, ["κLLY", "κOllivier"])
page("row", "graphviz", "Notebook §8.6",
 [("row[plots]", "lays out a list of graph plots in one row, 1100 points wide.")], [],
 {"Basic Examples": [("row[{CycleGraph[5], CompleteGraph[4]}]", "IMG:row")]}, ["edgeCurvaturePlot"])

# ------------------------------------------------------------------ flows
page("u0", "flows", "Notebook §10.2",
 [("u0[x, y]", "gives the initial conformal factor 0.3 cos x + 0.25 sin 2y cos(x + y) of the Ricci-flow example on the flat torus.")], [],
 {"Basic Examples": [("u0[0, 0]", None)]}, ["Kt", "Kconformal"])
page("Kt", "flows", "Notebook §10.2",
 [("Kt[t, x, y]", "gives the Gauss curvature −e^{−2w}Δ₀w of the Ricci-flow solution w = solR at time t.")],
 ["solR is the NDSolve solution of ∂w/∂t = e^{−2w}Δ₀w with w(0) = u0, periodic on [0, 2π]²."],
 {"Basic Examples": [("Kt[0, 0., 0.]", None)]}, ["maxK", "totalK", "u0"], setup=RICCI)
page("maxK", "flows", "Notebook §10.2",
 [("maxK[t]", "gives max |K| over a 21 × 21 grid at time t of the Ricci flow.")], [],
 {"Basic Examples": [("Round[maxK /@ {0, 1, 2}, 0.001]", None)]}, ["Kt", "totalK"], setup=RICCI)
page("totalK", "flows", "Notebook §10.2",
 [("totalK[t]", "gives ∬K dA = −∬Δ₀w dx dy at time t; it stays 0 (Gauss–Bonnet, χ = 0).")], [],
 {"Basic Examples": [("Chop[totalK /@ {0, 1, 2}, 10^-4]", None)]}, ["Kt", "maxK"], setup=RICCI)
page("lapCurve", "flows", "Notebook §10.3",
 [("lapCurve[X]", "gives ∂²X/∂s² of the closed polygon X: the arc-length-weighted Laplacian of the cycle graph on its vertices.")],
 ["One Euler step X + dt lapCurve[X] is curve-shortening flow; on a circle it points inwards with length 1/r."],
 {"Basic Examples": [("With[{X = Table[{Cos[s], Sin[s]}, {s, 0., 2 π - π/50, π/50}]}, Norm[lapCurve[X][[1]]]]", None)]}, ["polyArea", "resample"])
page("polyArea", "flows", "Notebook §10.3",
 [("polyArea[X]", "gives the area enclosed by the closed polygon X (shoelace formula).")], [],
 {"Basic Examples": [("polyArea[{{0, 0}, {1, 0}, {1, 1}, {0, 1}}]", None)]}, ["lapCurve", "resample"])
page("resample", "flows", "Notebook §10.3",
 [("resample[X]", "redistributes the nC vertices of the closed polygon X evenly by arc length.")], [],
 {"Basic Examples": [("nC = 4; resample[{{0, 0}, {2, 0}, {2, 2}, {0, 2}}]", None)]}, ["lapCurve", "polyArea"])
page("κS2", "flows", "Notebook §10.4",
 [("κS2[ε]", "gives the Ollivier curvature of ε-balls on the unit sphere, in the limit δ → 0, from the sliding (rotation) coupling.")],
 ["κS2[ε]/ε² → 1/8 = Ric/(2(n + 2)) as ε → 0. The integrand is written as s²/(1 + √(1 − s²)) to avoid cancellation."],
 {"Basic Examples": [("κS2[0.05]/0.05^2", None)]}, ["κH2", "κLLY"])
page("κH2", "flows", "Notebook §10.4",
 [("κH2[ε]", "gives the Ollivier curvature of ε-balls on the hyperbolic plane (K = −1), in the limit δ → 0.")],
 ["κH2[ε]/ε² → −1/8 as ε → 0."], {"Basic Examples": [("κH2[0.05]/0.05^2", None)]}, ["κS2"])

# ------------------------------------------------------------------ lab snippets
SN_G = 'X = {θ, φ}; g = {{1, 0}, {0, Sin[θ]^2}}; gi = Inverse[g]; Γ = Table[1/2 Sum[gi[[i, l]] (D[g[[l, j]], X[[k]]] + D[g[[l, k]], X[[j]]] - D[g[[j, k]], X[[l]]]), {l, 2}], {i, 2}, {j, 2}, {k, 2}];'
page("Lap", "snippets", "Lab Wolfram cells: Bochner and Weitzenböck snippets",
 [("Lap[w]", "gives the Laplace–Beltrami operator of w(θ, φ) on the unit sphere, using the snippet globals g, gi and X.")],
 ["Twin of laplaceBeltrami[gS2, 𝓍S2]. The Weitzenböck snippet defines it directly as (1/sin θ)(∂θ(sin θ ∂θw) + ∂φ²w/sin θ)."],
 {"Basic Examples": [("Simplify[Lap[Cos[θ]]]", None)]}, ["laplaceBeltrami"], setup=SN_G, kind="Snippet function")
page("g2", "snippets", "Lab Wolfram cell: Bochner snippet",
 [("g2[w]", "gives |∇w|² on the unit sphere.")], ["Twin of gradNorm2[gS2, 𝓍S2]."],
 {"Basic Examples": [("g2[Sin[θ] Cos[φ]]", None)]}, ["gradNorm2"], setup=SN_G, kind="Snippet function")
page("Hs", "snippets", "Lab Wolfram cell: Bochner snippet",
 [("Hs[w]", "gives the covariant Hessian of w on the unit sphere.")], ["Twin of hessian[gS2, 𝓍S2]."],
 {"Basic Examples": [("Simplify[Hs[Cos[θ]]]", None)]}, ["hessian"], setup=SN_G, kind="Snippet function")
page("rough", "snippets", "Lab Wolfram cell: Weitzenböck snippet",
 [("rough[ω]", "gives the rough Laplacian ∇*∇ω of a 1-form on the unit sphere.")], ["Twin of roughLaplacian1[gS2, 𝓍S2]."],
 {"Basic Examples": [("Simplify[rough[{0, Sin[θ]^2}]]", None)]}, ["roughLaplacian1"], setup=SN_G, kind="Snippet function")
page("star", "snippets", "Lab Wolfram cell: Weitzenböck snippet",
 [("star[{a, b}]", "gives the Hodge star {−b/sin θ, a sin θ} of a 1-form on the unit sphere.")], ["Twin of star1."],
 {"Basic Examples": [("star[{1, 0}]", None)]}, ["star1"], kind="Snippet function")
page("Δg", "snippets", "Lab Wolfram cell: Lin–Lu–Yau snippet",
 [("Δg[G, f][v]", "gives the random-walk Laplacian of f at v.")], ["Twin of Δgraph."],
 {"Basic Examples": [("Δg[CycleGraph[4], #^2 &][1]", None)]}, ["Δgraph", "κLLY"], kind="Snippet function")

SNIPPET_SOURCES = {
 "Lap": "Lap[w_] := 1/Sqrt[Det[g]] Sum[D[Sqrt[Det[g]] gi[[i, j]] D[w, X[[j]]], X[[i]]], {i, 2}, {j, 2}];\n(* Weitzenböck snippet form: *)\nLap[w_] := 1/Sin[θ] (D[Sin[θ] D[w, θ], θ] + D[w, φ, φ]/Sin[θ]);",
 "g2": "g2[w_] := Sum[gi[[i, j]] D[w, X[[i]]] D[w, X[[j]]], {i, 2}, {j, 2}];",
 "Hs": "Hs[w_] := Table[D[w, X[[i]], X[[j]]] - Sum[Γ[[k, i, j]] D[w, X[[k]]], {k, 2}], {i, 2}, {j, 2}];",
 "rough": "rough[ω_] := Module[{T, TT}, T = Table[D[ω[[i]], X[[j]]] - Sum[Γ[[k, i, j]] ω[[k]], {k, 2}], {i, 2}, {j, 2}];\n  TT = Table[D[T[[i, j]], X[[k]]] - Sum[Γ[[m, k, i]] T[[m, j]] + Γ[[m, k, j]] T[[i, m]], {m, 2}], {i, 2}, {j, 2}, {k, 2}];\n  Table[-Sum[gi[[j, k]] TT[[i, j, k]], {j, 2}, {k, 2}], {i, 2}]];",
 "star": "star[{a_, b_}] := {-b/Sin[θ], a Sin[θ]};",
 "Δg": "Δg[G_, f_][v_] := Mean[f /@ nbr[G, v]] - f[v];",
}
