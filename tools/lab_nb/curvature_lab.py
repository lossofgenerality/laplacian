"""Source of notebooks/lab/Laplacian_Curvature_Lab.nb (restructured 24 Nov 2026): mathematics in sections 1-11,
every comparison with the page's JavaScript under a final section, Production Notes.
Build: PYTHONPATH=tools/lab_nb python3 tools/series/build_series.py curvature_lab"""
import curvature_lab_v1 as O  # the first version (23 Nov 2026): its code and hand-work strings are reused here

FILE, DIR, TITLE, URL = O.FILE, O.DIR, O.TITLE, O.URL
snippet, page_data, _js, _wl = O.snippet, O.page_data, O._js, O._wl

def old(prefix, style=None):
    r = [t for s, t in O.CELLS if t.startswith(prefix) and (style is None or s == style)]
    assert len(r) == 1, (prefix, len(r)); return r[0]

def rep(text, *pairs):
    for a, b in pairs:
        assert a in text, a[:60]; text = text.replace(a, b)
    return text

GRAPH_EDGES = "graphEdges = " + _wl({g: v["edges"] for g, v in _js["graphs"].items()}) + ";"

TOOLKIT = r"""ClearAll["Global`*"];  (* start from a clean kernel *)
(* the colour scale used throughout: blue negative, near-white zero, CCN orange positive, saturating at ±s *)
kcol[k_?NumericQ, s_] := With[{w = Clip[k/s, {-1, 1}]}, Blend[{RGBColor[0.10, 0.27, 0.75], GrayLevel[0.97], RGBColor[0.96, 0.47, 0.02]}, (1 + Sign[w] Abs[w]^0.55)/2]];
kLegend[s_, label_] := BarLegend[{kcol[#, s] &, {-s, s}}, LegendLabel -> label];
orange = RGBColor[0.96, 0.47, 0.02]; blue = RGBColor[0.10, 0.27, 0.75];
(* a plain table: header row, then rows; numbers to seven figures *)
valGrid[head_, rows_] := Grid[Prepend[Map[If[NumericQ[#] && ! IntegerQ[#], NumberForm[N[#], 7], #] &, rows, {2}], Style[#, Bold] & /@ head],
   Frame -> All, Alignment -> Left, Background -> {None, {1 -> GrayLevel[0.93]}}, FrameStyle -> GrayLevel[0.75]];"""

PN_HELPERS = r"""(* page[...] holds the readouts the page computes in the browser; cmpGrid lays them beside the Wolfram values *)
cmpRow[label_, q_, p_, w_] := {label, q, p, w, Abs[p - w]};
cmpGrid[rows_] := valGrid[{"", "quantity", "page (JavaScript)", "Wolfram", "|difference|"}, rows];"""

H, S, SS, T, I, F, DF, IT = "Section", "Subsection", "Subsubsection", "Text", "Input", "Figure", "DisplayFormula", "Item"

def worked(sec, cells): return [(S, "%d.1 Worked by hand" % sec)] + cells
def checks(sec, cells): return [(S, "%d.2 Checks on the kernel" % sec)] + cells
def figs(sec, cells): return [(S, "%d.3 Figures and animator" % sec)] + cells
def labcell(text): return [(SS, "The Lab’s Wolfram cell"), (T, text)]

def old_section(n):
    """the 'Worked by hand' Text cells of old section n (they are kept verbatim)"""
    out, cur, on = [], None, False
    for s, t in O.CELLS:
        if s == "Section": cur = int(t.split(".")[0]); on = False
        elif s == "Subsection": on = (cur == n and "Worked by hand" in t)
        elif on and s == "Text": out.append((T, t))
    return out

def old_figs(n):
    """the figure, animator and caption cells of old section n (Subsection 'The plot(s)/picture(s) the page draws')"""
    out, cur, on = [], None, False
    for s, t in O.CELLS:
        if s == "Section": cur = int(t.split(".")[0]); on = False
        elif s == "Subsection": on = (cur == n and "the page draws" in t)
        elif on: out.append((s, t))
    return out

CELLS = [
(  "Title", TITLE.replace("the notebook behind the page", "the mathematics behind every section")),
("Subtitle", "Curvature from the Laplacian, section by section: statements, worked by hand, checked on the kernel, drawn and animated"),
(T, "© 2026 Computational Classnotes · CC BY-NC-SA 4.0"),
(T, "This notebook follows the Laplacian Curvature Lab (" + URL + ") section by section. Each section states the mathematics, works its main example by hand, checks every claim on the kernel, and redraws the section’s pictures with an animator for its interactive parts. How the page itself computes, and every comparison between the page’s numbers and Wolfram’s, is gathered at the end under Production Notes."),
(T, "Conventions. Δ is the Laplace–Beltrami operator, negative semidefinite (Δ = ∂²/∂x² + ∂²/∂y² in the plane). On a graph, Δf(v) is the mean of f over the neighbours of v minus f(v): the normalised Laplacian, with the same sign. Evaluate from the top; the first cell clears the session."),
(H, "0. Toolkit"),
(I, TOOLKIT),
]

# ------------------------------------------------------------------ 1
CELLS += [
(H, "1. Gauss and mean curvature on six surfaces"),
(T, "For a parametrised surface X(u, v) with first fundamental form E, F, G and second fundamental form L, M, N:"),
(DF, "K = (LN − M²)/(EG − F²),    H = (EN − 2FM + GL)/(2(EG − F²)),    dA = √(EG − F²) du dv."),
(T, "Gauss–Bonnet: on a closed surface ∬K dA = 2πχ, so 4π on the sphere and 0 on the torus. On the torus K is positive on the outer half, negative on the inner half and zero on the top and bottom circles."),
] + worked(1, old_section(1)) + checks(1, labcell("Gauss and mean curvature, and Gauss–Bonnet on the torus:") + [
(I, snippet("surfaces")),
(T, "Expected: K = cos v/(2 + cos v) and total 0."),
(SS, "All six surfaces"),
(T, "The six surfaces with their drawn parameter domains: K and H symbolically, their range on a 57 × 37 grid, and ∬K dA by NIntegrate. The sphere is drawn for 0.02 ≤ v ≤ π − 0.02, so its total there is 4π cos 0.02 = 12.5639; the saddle, catenoid and pseudosphere are open patches, whose totals depend on the patch."),
(I, rep(old("surf = <|"), (old("surf = <|")[old("surf = <|").index("surfRows[key_]"):], r"""surfData[key_] := Module[{X, U, V, c, g, Ks, Hs},
   {X, U, V} = surf[key]; c = surfaceCurvatures[X, {u, v}];
   g = N@Flatten[Table[{U[[1]] + (U[[2]] - U[[1]]) i/56, V[[1]] + (V[[2]] - V[[1]]) j/36}, {i, 0, 56}, {j, 0, 36}], 1];
   Ks = (c["K"] /. {u -> #[[1]], v -> #[[2]]}) & /@ g; Hs = (Abs[c["H"]] /. {u -> #[[1]], v -> #[[2]]}) & /@ g;
   <|"kmin" -> Min[Ks], "kmax" -> Max[Ks], "hmax" -> Max[Hs],
     "total" -> Chop[Quiet[NIntegrate[c["K"] c["dA"], {u, U[[1]], U[[2]]}, {v, V[[1]], V[[2]]}, PrecisionGoal -> 10, AccuracyGoal -> 12]], 10^-12]|>];
surfVals = AssociationMap[surfData, Keys[surf]];
valGrid[{"surface", "min K", "max K", "max |H|", "∬ K dA"}, KeyValueMap[{#1, #2["kmin"], #2["kmax"], #2["hmax"], #2["total"]} &, surfVals]]"""))),
(I, old("torusK = Simplify")),
(T, "K > 0 exactly where cos v > 0, and K = 0 on the circles v = π/2 and 3π/2."),
]) + figs(1, old_figs(1))

# ------------------------------------------------------------------ 2
CELLS += [
(H, "2. Ricci flow is a heat equation for the conformal factor"),
(T, "On a surface Ric = K g, so Ricci flow ∂g/∂t = −2 Ric becomes ∂g/∂t = −2K g. With g = e^{2u}(dx² + dy²) and Liouville’s formula for K:"),
(DF, "K = −e^{−2u} Δ₀u,        ∂u/∂t = −K = e^{−2u} Δ₀u."),
(T, "On the flat torus a bumpy metric is ironed out and ∬K dA stays 0. Ricci flow as a heat equation, with the maximum principle, energy and entropy, and reaction against diffusion, is the subject of its own notebook: Ricci Flow and the Curvature–Laplacian Relations (series notebook 14)."),
] + worked(2, old_section(2)) + checks(2, labcell("Liouville form of K, and the shrinking sphere:") + [
(I, "ClearAll[t];  (* t is a variable here *)"),
(I, snippet("ricci")),
(T, "Expected {1, −1, 0}: the stereographic sphere has K = 1, the half-plane K = −1, and (1 − 2t)g_{S²} solves ∂g/∂t = −2 Ric = −2g."),
(SS, "The conformal form of the flow"),
(I, old("(* the conformal form")),
(SS, "The flow on a 32 × 32 grid"),
(T, "A 32 × 32 periodic grid on [0, 2π)², initial u = a cos x + b sin 2y cos(x + y) with a = 0.3, b = 0.83a, the five-point Laplacian, and explicit steps dt = 0.2 h² e^{2 min u}, one at a time, until t ≥ 2."),
(I, rep(old("ricciRun[a_"), (old("ricciRun[a_")[old("ricciRun[a_").index("cmpGrid["):], 'valGrid[{"quantity", "value"}, {{"max |K| at t = 0", rr["maxK0"]}, {"t at the end", rr["t"]}, {"max |K| at the end", rr["maxK"]}, {"∬ K dA (−h² Σ Δ₀u)", rr["totalK"]}}]'))),
(T, "∬K dA = −h²ΣΔ₀u is 0 to round-off, because a periodic five-point Laplacian sums to zero exactly."),
]) + figs(2, old_figs(2))

# ------------------------------------------------------------------ 3
CELLS += [
(H, "3. The mean-value origin of Δ, on a curved surface"),
(T, "On a surface of constant curvature K the mean of f over the geodesic circle of radius r is"),
(DF, "M_r f = f + (r²/4)Δf + r⁴(Δ²f/64 + KΔf/96) + r⁶(Δ³f/2304 + KΔ²f/1152 + K²Δf/1440) + O(r⁸)."),
(T, "For f = eˣ(1 + z)² + yz³ on the unit sphere, at the north pole f = 4, Δf = −4, Δ²f = −20, Δ³f = 500. The errors of the flat formula, of the formula with KΔf/96, and of the formula with the r⁶ terms fall like r⁴, r⁶ and r⁸. The area of a geodesic disc is"),
(DF, "A(r)/πr² = 1 − Kr²/12 + K²r⁴/360 − …"),
] + worked(3, old_section(3)) + checks(3, labcell("The pole values, and the r⁶ expansion checked exactly (the last entry must be 0):") + [
(I, snippet("means")),
(SS, "The error slopes"),
(T, "The exact circle mean (NIntegrate at 30 digits) on r = 2^{−k/4}, k = 4 … 24, with log–log slopes fitted on 0.04 < r < 0.16:"),
(I, rep(old("F0[{x_, y_, z_}] := Exp[x] (1 + z)^2 + y z^3; pole"), ('cmpGrid[MapThread[cmpRow[#1, "log–log slope", #2, #3] &, {{"flat formula", "+ KΔf/96 at r^4", "+ r^6 terms"}, page["means", "slopes"], slopes}]]',
   'valGrid[{"approximation", "log–log slope"}, Transpose[{{"flat formula", "+ KΔf/96 at r^4", "+ r^6 terms"}, slopes}]]'))),
(T, "Slopes near 4, 6 and 8; not exactly integers, because each error still carries its next-order term on this window."),
(SS, "The disc area"),
(I, old("(* disc area on a surface")),
]) + figs(3, old_figs(3))

# ------------------------------------------------------------------ 4
CELLS += [
(H, "4. Curvature is the first correction to Weyl’s law"),
(T, "The heat trace has the small-t expansion (McKean–Singer)"),
(DF, "Tr e^{tΔ} ~ (4πt)^{−n/2}(Vol + (t/6)∫S dV + …)."),
(T, "For the unit sphere (eigenvalues l(l + 1), multiplicity 2l + 1, area 4π) the ratio to Weyl’s Area/(4πt), which is t·Tr e^{tΔ}, is 1 + t/3 + t²/15 + …; for a flat torus of the same area it is 1 up to exponentially small terms."),
] + worked(4, old_section(4)) + checks(4, labcell("The heat trace of the unit sphere against 1 + t/3 + t²/15:") + [
(I, snippet("heat")),
(SS, "Sphere and flat torus"),
(I, rep(old("sph[t_]"), (old("sph[t_]")[old("sph[t_]").index("cmpGrid["):], 'valGrid[{"t", "sphere t·Tr", "1 + t/3 + t²/15", "flat torus t·Tr"}, Table[{t, sph[t], 1 + t/3 + t^2/15, tor[t]}, {t, {0.01, 0.05, 0.1}}]]'))),
(I, old("(* why the torus line is flat")),
(T, "The torus ratio is θ₃(0, e^{−π/t})² = 1 + 4e^{−π/t} + …: 1 to machine precision for t ≤ 0.1, and 1.0016 at t = 0.4."),
]) + figs(4, old_figs(4))

# ------------------------------------------------------------------ 5
CELLS += [
(H, "5. Bochner’s formula, and what a curvature bound controls"),
(DF, "½Δ|∇f|² = |Hess f|² + ⟨∇f, ∇Δf⟩ + Ric(∇f, ∇f)."),
(T, "Integrated, it gives Lichnerowicz’s bound λ₁ ≥ nk when Ric ≥ (n − 1)k; along geodesics it gives the comparison Δr ≤ (n − 1)√k cot(√k r). The carré du champ Γ(f) = ½(Δ(f²) − 2fΔf) = |∇f|² and Γ₂(f) = ½ΔΓ(f) − Γ(f, Δf) carry the formula to spaces without derivatives. On a surface of curvature K > 0: λ₁ ≥ 2K, equality for the round sphere; diameter ≤ π/√K (Bonnet–Myers); Δr changes sign at r = π/(2√K). For K ≤ 0, Δr → √|K|."),
] + worked(5, old_section(5)) + checks(5, labcell("Bochner on S² for an arbitrary function (must return 0):") + [
(I, snippet("bochner")),
(SS, "Comparison, Lichnerowicz and the carré du champ"),
(I, old("(* on a surface of constant curvature K in geodesic polar")),
(I, old("(* round sphere of curvature K")),
(I, old("X = {θ, φ}; g = {{1, 0}, {0, Sin[θ]^2}}; Lap[w_]")),
]) + figs(5, old_figs(5))

# ------------------------------------------------------------------ 6
CELLS += [
(H, "6. On a mesh, angle defect is curvature and the cotangent Laplacian is −2Hn"),
(DF, "(Δf)_i = (1/2A_i) Σ_j (cot α_ij + cot β_ij)(f_j − f_i),        δ_i = 2π − Σ θ_i,        K_i ≈ δ_i/A_i."),
(T, "Here θ_i are the corner angles at vertex i, α_ij and β_ij the angles opposite edge ij, and A_i the barycentric area (one third of each incident triangle). The defects of a closed mesh add to exactly 2πχ: a cube corner has δ = 2π − 3·π/2 = π/2, and eight of them give 4π. The corner angle at vertex i of triangle ijk is ang[i, j, k] = VectorAngle[P[[j]] − P[[i]], P[[k]] − P[[i]]]."),
] + worked(6, old_section(6)) + checks(6, [
(SS, "ang on triangles, fans, a pyramid and a saddle"),
(I, old("SeedRandom[7]; angSum")),
(I, old("defectAt[apex_")),
(T, "The square-pyramid apex with unit edges has four equilateral corners: 2π − 4π/3 = 2π/3. The saddle ring alternates up and down, so its corner angles add to more than 2π: −0.8054."),
(SS, "The five regular polyhedra"),
(I, old("polyDefects[name_]")),
] + labcell("Angle defect on a 40 × 20 torus mesh (must return 0):") + [
(I, snippet("mesh")),
(SS, "The torus mesh at four resolutions"),
(T, "Vertices, total defect and the largest error of defect/area against the smooth K = cos v/(2 + cos v):"),
(I, rep(old("meshCurvature[P_"), (old("meshCurvature[P_")[old("meshCurvature[P_").index("meshRows[m_]"):], r"""meshData[{nu_, nv_}] := Module[{P, T, M, Km, Ks},
   {P, T} = torusMesh[nu, nv]; M = meshCurvature[P, T]; Km = M["defect"]/M["area"];
   Ks = Flatten[Table[N[Cos[2 π j/nv]/(2 + Cos[2 π j/nv])], {i, 0, nu - 1}, {j, 0, nv - 1}]];
   <|"nu" -> nu, "nv" -> nv, "vertices" -> Length[P], "defect" -> Total[M["defect"]], "err" -> Max[Abs[Km - Ks]], "Kouter" -> Km[[1]]|>];
meshVals = meshData /@ {{12, 6}, {24, 12}, {40, 20}, {64, 32}};
valGrid[{"mesh", "vertices", "Σ defect", "max |Kmesh − K|", "Kmesh at the outer equator (K = 1/3)"},
 {ToString[#["nu"]] <> " × " <> ToString[#["nv"]], #["vertices"], #["defect"], #["err"], #["Kouter"]} & /@ meshVals]"""))),
(T, "The total defect is 0 = 2πχ(torus) at every resolution, to round-off; the pointwise error falls by about 2.6 for each 1.6-fold refinement, like h²."),
]) + figs(6, [(s, rep(t, ('page["mesh"]', 'meshVals')) if s == I and t.startswith("ListLogLogPlot") else t) for s, t in old_figs(6)])

# ------------------------------------------------------------------ 7
G7 = rep(old("curvs = <|"),
  ('graphOf[g_] := Graph[Range[page["graphs", g, "n"]], UndirectedEdge @@@ page["graphs", g, "edges"]];', 'graphOf[g_] := Graph[Range[Max[graphEdges[g]]], UndirectedEdge @@@ graphEdges[g]];'),
  ('c[[3]][G, #] & /@ page["graphs", g, "edges"]', 'c[[3]][G, #] & /@ graphEdges[g]'))
G7 = G7[:G7.index("graphTable[g_]")] + r"""graphSummary[g_] := With[{sp = normSpec[graphOf[g]]}, Join[Table[With[{w = N[wlValues[g, k]]}, {If[k == "lly", g, ""], curvs[k][[1]], Min[w], Max[w], If[k == "res", Total[w], Mean[w]]}], {k, Keys[curvs]}],
   {{"", "λ₁ · λmax (normalised)", sp[[2]], sp[[-1]], ""}}]];
valGrid[{"graph", "curvature", "min", "max", "mean (sum for p)"}, graphSummary["dumbbell"]]"""
CELLS += [
(H, "7. Seven graph curvatures, each built from the graph Laplacian"),
(T, "Seven graphs: the binary tree on 15 vertices, the cycle C₆, the cube Q₃, the complete graph K₅, the Petersen graph, the 5 × 5 grid, and the dumbbell (two K₅ joined by a path of three edges). Seven curvatures:"),
(IT, "Lin–Lu–Yau κ_LLY on edges: the limit of Ollivier curvature as the walk becomes idle (κ_LLY = 2κ_{1/2})."),
(IT, "Ollivier κ₀ on edges, with the non-lazy walk."),
(IT, "Bakry–Émery K_∞ on vertices: the largest K with Γ₂ ≥ KΓ."),
(IT, "Forman F = 4 − d_x − d_y on edges, and Forman with triangles F + 3·#triangles."),
(IT, "Resistance curvature p_i = 1 − ½Σ_{j∼i} ω_ij on vertices, with ω the effective resistance."),
(IT, "Steinerberger curvature w on vertices, solving Dw = n·1 with D the distance matrix."),
(T, "The discrete Lichnerowicz bounds λ₁ ≥ min κ_LLY and λ₁ ≥ min K_∞ hold for the normalised Laplacian."),
] + worked(7, old_section(7)) + checks(7, [
(SS, "The seven graphs"),
(T, "Edge lists, vertices numbered from 1 (the tree: i joined to 2i and 2i + 1):"),
(I, GRAPH_EDGES),
] + labcell("Lin–Lu–Yau by the Münch–Wojciechowski linear programme, and λ₁ on Q₃:") + [
(I, snippet("graphs")),
(T, "Expected {{2/3}, 2/3}."),
(SS, "All seven curvatures"),
(T, "κ_LLY and κ₀ by optimal transport between the neighbourhood measures (LinearOptimization); K_∞ as the largest K with Γ₂ − KΓ ⪰ 0 on functions on the ball of radius 2, the quadratic forms built symbolically from Δ and the bound found by bisection on the least eigenvalue; resistance and Steinerberger curvature from pseudoinverses."),
(I, old("W1[G_, m1_, m2_]")),
(I, G7),
(I, 'Column[{Style[#, Bold], valGrid[{"graph", "curvature", "min", "max", "mean (sum for p)"}, graphSummary[#]]}, Spacings -> 1] & /@ {"tree", "cycle", "cube", "complete", "petersen", "grid"} // Column'),
(SS, "The facts stated for each graph"),
(I, rep(old("val[g_, k_]"), ('edgeIdx[g_, pred_] := Position[page["graphs", g, "edges"]', 'edgeIdx[g_, pred_] := Position[graphEdges[g]'), ('Sort[deg[[#]]] & /@ page["graphs", "grid", "edges"]', 'Sort[deg[[#]]] & /@ graphEdges["grid"]'))),
(T, "On the tree the interior edges have κ_LLY = −2/3 except the two at the root, whose end has degree 2 (−1/3), and the leaf edges +2/3. On a tree effective resistance equals distance, and Steinerberger curvature is exactly 2n/(n − 1) = 15/7 times resistance curvature: the inverse distance matrix of a tree is −½L + ττᵀ/(2(n − 1)) with τ = 2 − degree (Graham–Lovász), so D⁻¹1 = τ/(n − 1) and p = τ/2. C₆ is flat for all three. Q₃ has κ_LLY = K_∞ = λ₁ = 2/3 and K₅ has κ_LLY = λ₁ = 5/4: equality cases of λ₁ ≥ κ. Petersen has κ_LLY = 0, κ₀ = −1/3, K_∞ = −1/3, λ₁ = 2/3. On the grid κ_LLY is 0 on interior edges and along the sides, +1/6 on edges from a side inward and +1/3 at the corners. On the dumbbell the two edges joining a clique to the path have κ_LLY = −3/5, the middle edge 0."),
(I, rep(old("(* the two discrete"), ("(* the two discrete Lichnerowicz bounds the page ticks, on every graph *)", "(* the two discrete Lichnerowicz bounds and Foster's theorem, on every graph *)"), ('{g, Keys[page["graphs"]]}', '{g, Keys[graphEdges]}'))),
]) + figs(7, [(s, t.replace('page["graphs", g, "edges"]', 'graphEdges[g]').replace('Keys[page["graphs"]]', 'Keys[graphEdges]').replace("The seven graphs of the page", "The seven graphs").replace(", as on the page", "").replace(" (the page’s default curvature)", "")) for s, t in old_figs(7)])

# ------------------------------------------------------------------ 8
F8 = old("curveInit[kind_")
F8 = F8[:F8.index("cmpGrid[")] + 'valGrid[{"start", "mean dA/dt", "t when area < 8%", "vertices at the end"}, {#, runs[#, "rate"], runs[#, "t"], runs[#, "vertices"]} & /@ Keys[runs]]'
CELLS += [
(H, "8. Mean-curvature flow: a curve rounds itself off"),
(DF, "∂X/∂t = ΔX = κN."),
(T, "In the plane any embedded closed curve becomes convex, then round, and shrinks to a point (Gage–Hamilton–Grayson). The area falls at exactly 2π per unit time, because ∮κ ds = 2π. A polygon is moved by the cycle-graph Laplacian weighted by arc length: vertex i moves by k(t_f − t_b) with k = 2/(ℓ_f + ℓ_b), ℓ the lengths and t the unit directions of the edges out of and into it."),
] + worked(8, old_section(8)) + checks(8, labcell("Exact flows: the round sphere under Ricci flow, and a sphere of radius √(R₀² − 4t) under mean-curvature flow (both residuals 0):") + [
(I, "ClearAll[t];  (* t is a variable here *)"),
(I, snippet("flows")),
(SS, "The polygon flow on four starting curves"),
(T, "Explicit steps of at most 0.2 × (shortest edge)², the stability limit of an explicit heat step; every 20 steps the polygon is resampled by arc length when 160 × (perimeter/initial perimeter) vertices (at least 24) is under 85% of the current count, or when the longest edge exceeds three times the shortest. Run until the area is below 8% of its start; the mean dA/dt should be −2π = −6.2832."),
(I, F8),
(T, "All four rates are within about 0.5% of −2π. The small excess is the area lost at each resampling (it cuts corners); between resamplings the polygon’s rate is −Σ 2 sin(θ_i/2) over its turning angles θ_i, just under 2π."),
(I, old("Row[Table[Graphics[{RGBColor[0.98")),
(F, "The last frame of curve shortening for the four starting curves: smooth near-circles."),
]) + figs(8, old_figs(8))

# ------------------------------------------------------------------ 9
K9 = old("κball[K_").replace("κball[K_, ε_?NumericQ] := Which[", "κball[K_, ε_?NumericQ] := κball[K, ε] = Which[")  # remembered: the Production Notes reuse the values
K9 = K9[:K9.index("cmpGrid[")] + r"""emax[K_] := If[K == 0, 1.2, Min[1.2, 0.9 π/Sqrt[Abs[K]]/2]];
valGrid[{"K", "κ/ε² at ε = 0.05", "K/8", "largest ε drawn", "κ/ε² there"}, Table[{K, κball[K, 0.05]/0.05^2, K/8, emax[K], κball[K, emax[K]]/emax[K]^2}, {K, {-2, -1, 0, 1, 2}}]]"""
CELLS += [
(H, "9. Comparing two ball averages measures Ricci curvature"),
(DF, "κ(x, y) = 1 − W₁(μ_x, μ_y)/d(x, y),        κ ≈ ε² Ric(v, v)/(2(n + 2)) = ε²K/8 on a surface,"),
(T, "with μ uniform on ε-balls (Ollivier). Sliding the surface along the geodesic carries one ball onto the other, and a point at distance λ from the geodesic moves δ cos(√K λ), so κ is a plain integral over the ball."),
] + worked(9, old_section(9)) + checks(9, labcell("κ/ε² → K/8 on S² and H²:") + [
(I, snippet("ollivier")),
(SS, "κ/ε² for five curvatures"),
(I, K9),
]) + figs(9, old_figs(9))

# ------------------------------------------------------------------ 10, 11
CELLS += [
(H, "10. Every Laplacian–curvature relationship on one sheet"),
(T, "The sheet restates formulas checked in the sections above and in the write-up notebook (LaplacianCurvature.nb §2–§10). Two further Wolfram cells of the Lab, and the ball-volume line of the sheet:"),
(SS, "Yamabe: u⁴ times the flat metric of ℝ³ is the round S³, scalar curvature 6"),
(I, snippet("yamabe")),
(SS, "Weitzenböck on S²: Δ_Hodge ω − ∇*∇ω = Ric(ω) = ω for every 1-form df + ⋆dh (must return {0, 0})"),
(I, snippet("weitzenbock")),
(SS, "Ball volume"),
(I, old("(* the ball-volume line")),
(H, "11. Self-check: the answers"),
(I, rep(old("tK = Simplify"), ('Keys[page["graphs"]]', 'Keys[graphEdges]'))),
(T, "Question 4 (Bakry–Émery copies Bochner, Γ₂ ≥ KΓ) and question 5 (the dumbbell’s bridge is negative because its two neighbourhoods barely overlap) are checked in §5 and §7."),
]

# ------------------------------------------------------------------ Production Notes
PN = [
(H, "Production Notes"),
(T, "How the Lab page computes, and every number it prints set beside Wolfram’s. The page computes in the browser with JavaScript (lab/core.js, driven by lab/app.js). The association page below holds its readouts at the default settings and for every choice of every selector; it is produced by running lab/core.js under Node exactly as the browser runs it (tools/lab_nb/js_readouts.js). Each table gives the page value, the Wolfram value from the sections above, and their difference. Evaluate the sections above first."),
(I, page_data()),
(I, PN_HELPERS),
(S, "PN 1. Surfaces"),
(T, "The page takes K and H by central finite differences with step 10⁻³ on a 57 × 37 grid, and ∬K dA by a 160 × 160 midpoint rule."),
(I, 'cmpGrid[Join @@ Table[{cmpRow[key, "min K", page["surfaces", key, "kmin"], surfVals[key, "kmin"]], cmpRow["", "max K", page["surfaces", key, "kmax"], surfVals[key, "kmax"]],\n    cmpRow["", "max |H|", page["surfaces", key, "hmax"], surfVals[key, "hmax"]], cmpRow["", "∬ K dA", page["surfaces", key, "total"], surfVals[key, "total"]]}, {key, Keys[surf]}]]'),
(T, "The finite differences agree with the exact values to about 5 × 10⁻⁷ (the O(h²) error of step 10⁻³), except max |H| on the pseudosphere (3 × 10⁻⁴), which is reached at the edge of the patch where H grows fastest; the totals agree to the accuracy of the midpoint rule (2 × 10⁻⁴ at most, on the sphere)."),
(S, "PN 2. Ricci flow"),
(T, "The page runs the scheme of §2 exactly, one explicit step per animation frame; the readings agree to round-off. The page’s check line once quoted the write-up notebook §10.2 (NDSolve on a 31 × 31 grid: max|K| 4.83 → 0.059), a different bump and grid; it now quotes this run, 4.63 → 0.059 by t = 2.00. On 23 Nov 2026 the page’s colours were made to follow max|K| (with a fixed ±1.5 option), because on a fixed scale the end of the run looked blank."),
(I, 'cmpGrid[{cmpRow["bump 0.3", "max |K| at t = 0", page["ricci", "maxK0"], rr["maxK0"]], cmpRow["", "t at the end", page["ricci", "t"], rr["t"]],\n  cmpRow["", "max |K| at the end", page["ricci", "maxK"], rr["maxK"]], cmpRow["", "∬ K dA", page["ricci", "totalK"], rr["totalK"]]}]'),
(S, "PN 3. Curved mean values"),
(T, "The page’s circle mean is a 720-point rule in double precision, fitted on the same window. The last slope differs in the third decimal (8.005 on the page, 8.000 here) because those errors are near 10⁻¹³, where double precision shows; here the circle mean is computed to 25 digits."),
(I, 'cmpGrid[MapThread[cmpRow[#1, "log–log slope", #2, #3] &, {{"flat formula", "+ KΔf/96 at r^4", "+ r^6 terms"}, page["means", "slopes"], slopes}]]'),
(S, "PN 4. Heat trace"),
(T, "The page sums the sphere’s eigenvalues and the torus’s theta function in double precision, at the slider value (default t = 0.05)."),
(I, 'cmpGrid[Join @@ Table[With[{t = h["t"]}, {cmpRow["t = " <> ToString[t], "sphere t·Tr", h["sphere"], sph[t]],\n     cmpRow["", "1 + t/3 + t²/15", h["series"], 1 + t/3 + t^2/15], cmpRow["", "flat torus t·Tr", h["torus"], tor[t]]}], {h, page["heat"]}]]'),
(S, "PN 5. Meshes"),
(T, "The page’s mesh, barycentric area and corner angles are those of §6, in JavaScript."),
(I, 'cmpGrid[Join @@ MapThread[{cmpRow[ToString[#2["nu"]] <> " × " <> ToString[#2["nv"]], "vertices", #1["vertices"], #2["vertices"]], cmpRow["", "Σ defect", #1["defect"], #2["defect"]],\n     cmpRow["", "max |Kmesh − K|", #1["err"], #2["err"]], cmpRow["", "Kmesh at the outer equator", #1["Kouter"], #2["Kouter"]]} &, {page["mesh"], meshVals}]]'),
(S, "PN 6. Graph curvatures"),
(T, "The page computes κ_LLY and κ₀ by its own transport solver, K_∞ by bisection rounded down to 10⁻⁶ (hence differences below 10⁻⁶), and the rest by matrix pseudoinverses. Its notes under each graph were corrected on 23 Nov 2026 from §7: the tree’s two root edges are −1/3, not −2/3; on the grid only the corner edges (+1/3) and the edges from a side inward (+1/6) are positive, not the whole boundary; on the dumbbell the middle edge of the bridge is 0, not −3/5. The note that Steinerberger and resistance curvature are proportional on the tree was right (the factor is 15/7)."),
(I, r"""graphTable[g_] := Module[{sp = normSpec[graphOf[g]]},
   Join[Join @@ Table[With[{w = N[wlValues[g, k]], p = page["graphs", g, k]},
       {{If[k == "lly", g, ""], curvs[k][[1]] <> ": min", Min[p], Min[w], Abs[Min[p] - Min[w]]},
        {"", "   max", Max[p], Max[w], Abs[Max[p] - Max[w]]},
        {"", "   largest |page − Wolfram| over all " <> If[curvs[k][[2]] == "e", "edges", "vertices"], "", "", Max[Abs[p - w]]}}], {k, Keys[curvs]}],
    {cmpRow["", "λ₁ (normalised)", page["graphs", g, "lambda1"], sp[[2]]], cmpRow["", "λmax", page["graphs", g, "lambdaMax"], sp[[-1]]]}]];
{page["graphs", #, "edges"] == graphEdges[#] & /@ Keys[graphEdges], Column[{Style[#, Bold], cmpGrid[graphTable[#]]}, Spacings -> 1] & /@ Keys[graphEdges] // Column}"""),
(S, "PN 7. Curve shortening"),
(T, "The page advances the flow of §8 in animation frames of 3 × 10⁻³ and stops at the end of the first frame below 8%, so its t is a little later than Wolfram’s, which stops at the first step. Before 23 Nov 2026 the page used a fixed step 2 × 10⁻⁴: as the curve shrank its edges fell below the stability limit, the polygon broke into a zig-zag at the end, and the mean dA/dt read about −5.6 instead of −2π."),
(I, 'cmpGrid[Flatten[Table[{cmpRow[k, "mean dA/dt", page["flows", k, "rate"], runs[k, "rate"]], cmpRow["", "t when area < 8%", page["flows", k, "t"], runs[k, "t"]]}, {k, Keys[runs]}], 1]]'),
(S, "PN 8. Ollivier on manifolds"),
(T, "The page integrates over the ball with a 160 × 160 midpoint rule (80 × 80 at the largest ε). Its check line quotes κ/ε² = 0.12496 (sphere), 0 (plane) and −0.12504 (hyperbolic plane) at ε = 0.05 from notebook 07-Ollivier §8; the converged values of §9 agree to five figures."),
(I, 'cmpGrid[Flatten[Table[{cmpRow["K = " <> ToString[o["K"]], "κ/ε² at ε = 0.05", o["at005"], κball[o["K"], 0.05]/0.05^2],\n     cmpRow["", "κ/ε² at ε = " <> ToString[NumberForm[o["emax"], 3]], o["atmax"], κball[o["K"], o["emax"]]/o["emax"]^2]}, {o, page["ollivier"]}], 1]]'),
(S, "PN 9. The Lab’s Wolfram cells"),
(T, "The snippets in §§1–10 are the Lab’s Wolfram cells exactly as the page offers them (lab/app.js, SNIP), with script letters written as named characters. On the page they run on the CCN Wolfram Cloud kernel after the reader enters a CCN-KEY."),
(T, "© 2026 Computational Classnotes · CC BY-NC-SA 4.0"),
]
CELLS += PN

# ---- wording: no page or JavaScript talk above Production Notes
import re as _re
_FIX = [
 (" (The sign of H follows the outward normal; the page shows |H|.)", " (The sign of H follows the outward normal.)"),
 ("These are exactly the page’s max K = 0.3333, min K = −1.0000 and max |H| = 0.6667 for the torus.", "These are the torus’s max K = 0.3333, min K = −1.0000 and max |H| = 0.6667 in the table of §1.2."),
 ("The table in §1 is these formulas evaluated on the page’s grid.", "The table in §1.2 is these formulas evaluated on the grid."),
 ("The six surfaces of the page coloured by Gauss curvature K on the page’s scale:", "The six surfaces coloured by Gauss curvature K:"),
 (", as on the page.", "."),
 (" (the page’s chart), and the curvature field at t = 0, 0.5 and the end, on the page’s colour scale (saturating at |K| = 1.5).", ", and the curvature field at t = 0, 0.5 and the end (colours saturate at |K| = 1.5)."),
 ("Ricci flow as a heat equation (the maximum principle, energy and entropy, reaction against diffusion), shown on the page under this animation, has its own notebook", "Ricci flow as a heat equation (the maximum principle, energy and entropy, reaction against diffusion) has its own notebook"),
 (" (the page’s chart). The lines have slopes 4, 6 and 8. With the circle mean at 30 digits the blue line keeps falling below 10⁻¹³, where the page’s double precision flattens it.", ". The lines have slopes 4, 6 and 8; with the circle mean at 30 digits the blue line keeps falling below 10⁻¹³."),
 (" (the page’s disc-area chart).", "."),
 (" (the page’s chart; the grey line is the default t = 0.05).", " (the grey line marks t = 0.05)."),
 ("The animator: slide t, as on the page;", "The animator: slide t;"),
 (" (the page’s chart): positive", ": positive"),
 (": the page’s two pictures.", "."),
 (", as the page reads.", "."),
 (" and the spectral bounds the page ticks.", " and the spectral bounds."),
 (" (the page’s chart); the dashed line is K/8.", "; the dashed line is K/8."),
 ("Why ∬K dA stays 0 on the page.", "Why ∬K dA stays 0 on the grid."),
 ("so the page reads 0 to round-off, about 10⁻¹⁵", "so the grid total is 0 to round-off, about 10⁻¹⁵"),
 ("(the page reads 3.97 × 10⁻⁶; the r⁶ terms account for the rest)", "(the r⁶ terms change it a little)"),
 ("At the default t = 0.05 the page reads 1.016835 for the sphere and 1.000000 for the torus, and 1 + t/3 + t²/15 = 1.016833.", "At t = 0.05 the sphere gives 1.016835, the torus 1.000000, and 1 + t/3 + t²/15 = 1.016833."),
 ("For curvature K the page’s readout:", "For curvature K:"),
 ("1 − Kr²/12 + K²r⁴/360, the formula on the page.", "1 − Kr²/12 + K²r⁴/360, the formula stated above."),
 ("The page’s κ/ε² at ε = 0.05 is 0.12496 = 1/8 − 0.000039;", "At ε = 0.05, κ/ε² = 0.12496 = 1/8 − 0.000039 (table in §9.2);"),
 ("and the page’s ratio defect/area at that vertex is 0.3352 against the smooth 1/3", "and the ratio defect/area at that vertex is 0.3352 against the smooth 1/3 (table in §6.2)"),
]
_pn = [i for i, (s, t) in enumerate(CELLS) if t == "Production Notes"][0]
_used = set()
for _i in range(_pn):
    _s, _t = CELLS[_i]
    if _s == "Input": continue
    for _a, _b in _FIX:
        if _a in _t: _t = _t.replace(_a, _b); _used.add(_a)
    CELLS[_i] = (_s, _t)
_miss = [a for a, b in _FIX if a not in _used]
assert not _miss, _miss
