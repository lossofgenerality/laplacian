# Ollivier curvature — a worked notebook in the "Curvature from the Laplacian" series.
# Cells: (style, text). Styles: Title, Subtitle, Section, Subsection, Text, Input.

NAME = "Ollivier"
FILE = "07-Ollivier"
TITLE = "Ollivier Curvature"
SUBTITLE = "Comparing two averages: coarse Ricci curvature on graphs and on manifolds — Curvature from the Laplacian, notebook 7"

CELLS = [
("Title", TITLE),
("Subtitle", SUBTITLE),
("Text", "© 2026 Computational Classnotes · CC BY-NC-SA 4.0"),
("Text", "This notebook defines Ollivier’s curvature, works it out by hand on small graphs, computes it on a family of graphs, "
         "follows it through laziness to the Lin–Lu–Yau curvature, proves its main consequences on examples, and returns to smooth surfaces, "
         "where it recovers the Gauss curvature as κ ≈ Kε²/8. Evaluate top to bottom; every section ends with a check. "
         "The write-up “Ollivier Curvature” carries the same section numbers."),

# ------------------------------------------------------------------ 1
("Section", "1. Toolkit"),
("Text", "Graph functions used throughout. μ[G, x, α] is the lazy random walk at x: mass α stays at x and 1 − α is spread evenly over the neighbours. "
         "W1 is the Wasserstein-1 (earth mover’s) distance for the graph metric, solved as a linear program; plan returns the optimal transport plan. "
         "κ[G, {x, y}, α] = 1 − W1(μx, μy)/d(x, y) is Ollivier’s curvature for any pair of vertices."),
("Input",
"""ClearAll[nbr, μ, W1, plan, W1dual, κ, κLLY, κColour, κLegend];
nbr[G_, v_] := AdjacencyList[G, v];
μ[G_, x_, α_] := Merge[{<|x -> α|>, AssociationThread[nbr[G, x] -> (1 - α)/Length[nbr[G, x]]]}, Total];
plan[G_, m_, n_] := Module[{A = Keys[m], B = Keys[n], p, vars, sol},
  vars = Flatten@Table[p[a, b], {a, A}, {b, B}];
  sol = LinearOptimization[Sum[GraphDistance[G, a, b] p[a, b], {a, A}, {b, B}],
    Join[Table[Sum[p[a, b], {b, B}] == m[a], {a, A}], Table[Sum[p[a, b], {a, A}] == n[b], {b, B}], Thread[vars >= 0]], vars];
  Select[Association@Flatten@Table[{a, b} -> (p[a, b] /. sol), {a, A}, {b, B}], # > 0 &]];
W1[G_, m_, n_] := Total@KeyValueMap[GraphDistance[G, #1[[1]], #1[[2]]] #2 &, plan[G, m, n]];
W1dual[G_, m_, n_] := Module[{S = Union[Keys[m], Keys[n]], f},
  -LinearOptimization[-(Sum[m[a] f[a], {a, Keys[m]}] - Sum[n[b] f[b], {b, Keys[n]}]),
    Flatten@Table[f[S[[i]]] - f[S[[j]]] <= GraphDistance[G, S[[i]], S[[j]]], {i, Length[S]}, {j, Length[S]}], f /@ S, "PrimalMinimumValue"]];
κ[G_, {x_, y_}, α_] := 1 - W1[G, μ[G, x, α], μ[G, y, α]]/GraphDistance[G, x, y];
κLLY[G_, {x_, y_}] := Module[{S, vars, f, cons}, S = Union[{x, y}, nbr[G, x], nbr[G, y]];
  vars = Table[Unique["f"], {Length[S]}]; f = AssociationThread[S -> vars];
  cons = Flatten[{f[y] - f[x] == 1, f[x] == 0, Table[With[{d = GraphDistance[G, S[[i]], S[[j]]]},
      {f[S[[i]]] - f[S[[j]]] <= d, f[S[[j]]] - f[S[[i]]] <= d}], {i, Length[S]}, {j, i + 1, Length[S]}]}];
  LinearOptimization[(Mean[f /@ nbr[G, x]] - f[x]) - (Mean[f /@ nbr[G, y]] - f[y]), cons, vars, "PrimalMinimumValue"]];
κColour[k_, s_] := Blend[{RGBColor[0.18, 0.36, 0.78], GrayLevel[0.96], RGBColor[0.98, 0.56, 0.17]}, (1 + Clip[k/s, {-1, 1}])/2];
κLegend[s_, name_] := BarLegend[{κColour[#, s] &, {-s, s}}, LegendLabel -> name];
tree = KaryTree[15, 2];
dumbbell = Graph[UndirectedEdge @@@ Join[List @@@ EdgeList[CompleteGraph[5]], (List @@@ EdgeList[CompleteGraph[5]]) + 7, {{5, 6}, {6, 7}, {7, 8}}]];
{μ[CycleGraph[6], 1, 0], μ[CycleGraph[6], 1, 1/2]}"""),
("Text", "Check: the walk on the 6-cycle puts ½ on each neighbour and 0 at home; the ½-lazy walk keeps ½ at home and ¼ on each neighbour."),

# ------------------------------------------------------------------ 2
("Section", "2. The idea: positive curvature brings averages together"),
("Text", "On a round sphere, two geodesics that leave nearby points in parallel bend towards each other. So a small ball around x, slid along the geodesic to a nearby point y, "
         "lands on the ball around y with every point travelling less than the distance d(x, y) between the centres. On a flat plane every point travels exactly d(x, y); "
         "on a saddle-shaped surface points off the geodesic travel more. Ollivier (2009) turned this into a definition that needs only distances and averaging: "
         "curvature is how much closer the two averaging measures are than their centres."),
("Text", "Fig. 1: on the unit sphere, points of the ε-ball around x (left) are carried by a rotation onto the ε-ball around y. "
         "A point at distance λ from the equator moves along a circle of radius cos λ, so it travels δ cos λ < δ. Arrow colour shows the ratio travelled/δ = cos λ: orange 1 (on the geodesic), blue the smallest."),
("Input",
"""With[{δ = 0.7, ε = 0.42, R = RotationTransform[0.7, {0, 0, 1}]},
 Module[{ball, pts, arrows},
  ball = Select[SpherePoints[2600], VectorAngle[#, {1, 0, 0}] < ε &];
  pts = ball[[;; ;; 7]];
  arrows = {Blend[{RGBColor[0.18, 0.36, 0.78], RGBColor[0.98, 0.56, 0.17]}, (Sqrt[1 - #[[3]]^2] - Cos[ε])/(1 - Cos[ε])], Arrowheads[0.012], Arrow[Table[1.01 RotationTransform[t, {0, 0, 1}][#], {t, 0, δ, δ/12}]]} & /@ pts;
  Graphics3D[{{Opacity[0.25], GrayLevel[0.85], Sphere[]},
    {GrayLevel[0.3], Thick, Line[Table[1.005 {Cos[t], Sin[t], 0}, {t, -0.3, δ + 0.3, 0.02}]]},
    {GrayLevel[0.2], Thickness[0.004], Line[Table[1.012 {Cos[ε], Sin[ε] Cos[t], Sin[ε] Sin[t]}, {t, 0, 2 π, π/60}]],
      Line[Table[1.012 R[{Cos[ε], Sin[ε] Cos[t], Sin[ε] Sin[t]}], {t, 0, 2 π, π/60}]]}, arrows,
    {Black, PointSize[0.016], Point[{1.02 {1, 0, 0}, 1.02 R[{1, 0, 0}]}]},
    Text[Style["x", 14, Bold], 1.18 {1, 0, 0}], Text[Style["y", 14, Bold], 1.18 R[{1, 0, 0}]]},
   ViewPoint -> {3, 1.3, 1.1}, Boxed -> False, ImageSize -> 420, Lighting -> "Neutral",
   PlotLabel -> Style["ε-ball at x slid onto the ε-ball at y: every point moves less than δ", 11]]]]"""),
("Figure", "The ε-ball at x on the unit sphere slid by a rotation onto the ε-ball at y; arrow colour is the distance travelled divided by δ."),
("Text", "What to see: points on the equator (the geodesic) travel the full δ; points nearer the poles of the ball travel less. The average distance travelled is below δ, so κ > 0."),

# ------------------------------------------------------------------ 3
("Section", "3. Definition"),
("Text", "Let (X, d) be a metric space with, for each point x, a probability measure mₓ (an averaging rule, or one step of a random walk). "
         "The Wasserstein-1 distance between two probability measures is the least average distance needed to move one onto the other:"),
("Text", "W₁(m, m′) = min over couplings π of Σ π(a, b) d(a, b),   where π ≥ 0 has row sums m(a) and column sums m′(b)."),
("Text", "Ollivier’s curvature of the pair x ≠ y is"),
("Text", "κ(x, y) = 1 − W₁(mₓ, m_y) / d(x, y)."),
("Text", "On a graph, d is the shortest-path distance and mₓ = μ[G, x, α] is the α-lazy simple random walk. Write κ_α for the resulting curvature; κ₀ is the non-lazy one. "
         "Kantorovich–Rubinstein duality gives a second formula, a maximum over 1-Lipschitz test functions:"),
("Text", "W₁(m, m′) = max over f with |f(a) − f(b)| ≤ d(a, b) of  Σ f(a) m(a) − Σ f(b) m′(b)."),
("Text", "So an explicit transport plan bounds W₁ above (κ below), an explicit 1-Lipschitz function bounds W₁ below (κ above), and when the two meet the value is proved. "
         "The check computes W₁ both ways, as the primal and the dual linear program."),
("Input",
"""With[{cases = {{CycleGraph[6], {1, 2}}, {CompleteGraph[5], {1, 2}}, {tree, {2, 4}}, {PetersenGraph[], {1, 3}}, {HypercubeGraph[3], {1, 2}}}},
 Table[With[{G = c[[1]], x = c[[2, 1]], y = c[[2, 2]]},
   {W1[G, μ[G, x, 0], μ[G, y, 0]], W1dual[G, μ[G, x, 0], μ[G, y, 0]]}], {c, cases}]]"""),
("Text", "Check: each pair is equal — {1, 1}, {1/4, 1/4}, {5/3, 5/3}, {4/3, 4/3}, {1, 1} — so the transport plans found are optimal."),

# ------------------------------------------------------------------ 4
("Section", "4. Worked by hand"),
("Subsection", "4.1 Complete graph Kₙ, non-lazy walk"),
("Text", "Take adjacent x, y in Kₙ. The walk at x puts 1/(n − 1) on y and on each of the n − 2 common neighbours; the walk at y puts 1/(n − 1) on x and on the same n − 2 common neighbours. "
         "The common masses already match, so leave them. Only the mass 1/(n − 1) sitting on y has to move to x, a distance 1. Hence W₁ ≤ 1/(n − 1). "
         "The test function f = 1 at y, 0 elsewhere is 1-Lipschitz and gives Σ f mₓ − Σ f m_y = 1/(n − 1), so W₁ = 1/(n − 1) exactly and"),
("Text", "κ₀(x, y) = 1 − 1/(n − 1) = (n − 2)/(n − 1)."),
("Input", """Table[{n, κ[CompleteGraph[n], {1, 2}, 0], (n - 2)/(n - 1)}, {n, 3, 7}]"""),
("Subsection", "4.2 Cycle Cₙ, n ≥ 4"),
("Text", "Number the cycle so x = 1, y = 2. Then mₓ puts ½ on 0 and ½ on 2, and m_y puts ½ on 1 and ½ on 3. Move 0 → 1 and 2 → 3, each a distance 1 carrying ½: W₁ ≤ 1. "
         "The function f = 1 on 0 and 2, f = 0 elsewhere, is 1-Lipschitz and gives ½ + ½ − 0 = 1. So W₁ = 1 and κ₀ = 0: long cycles are flat. "
         "For n = 3 the cycle is K₃ and κ₀ = ½."),
("Input", """Table[{n, κ[CycleGraph[n], {1, 2}, 0]}, {n, 3, 8}]"""),
("Subsection", "4.3 An interior edge of the binary tree"),
("Text", "In the binary tree with 15 vertices take the edge x = 2, y = 4 (both of degree 3). Each walk puts ⅓ on the other endpoint and ⅓ on each of two further neighbours. "
         "The neighbours of x other than y lie at distance 3 from the neighbours of y other than x. One optimal plan moves the mass ⅓ on y to a neighbour of y (distance 1), "
         "the mass ⅓ on the far neighbour of x to x (distance 1), and the last ⅓ across, distance 3: W₁ = ⅓ + ⅓ + 1 = 5/3, so κ₀ = −2/3. Trees spread out: negative curvature."),
("Input", """{κ[tree, {2, 4}, 0], plan[tree, μ[tree, 2, 0], μ[tree, 4, 0]]}"""),
("Text", "The plan lists (from, to) → mass. Fig. 2 shows the optimal plans for one edge of K₅, C₆ and the tree: the edge in black, mass moved as orange arrows labelled by the amount."),
("Input",
"""planPicture[G_, {x_, y_}, label_] := Module[{pl = plan[G, μ[G, x, 0], μ[G, y, 0]], pos, moves},
  pos = AssociationThread[VertexList[G] -> GraphEmbedding[G]];
  moves = Select[Normal[pl], #[[1, 1]] =!= #[[1, 2]] &];
  Show[Graph[G, VertexSize -> 0.12, VertexStyle -> GrayLevel[0.85], EdgeStyle -> GrayLevel[0.8],
     VertexLabels -> None, ImageSize -> If[VertexCount[G] > 10, 360, 230]],
   Graphics[{{Black, Thickness[0.012], Line[{pos[x], pos[y]}]},
     Table[With[{a = m[[1, 1]], b = m[[1, 2]], w = m[[2]]},
       {RGBColor[0.98, 0.56, 0.17], Thickness[0.006], Arrowheads[0.06],
        Arrow[{pos[a], pos[b]}, 0.08], Black, Text[Style[w, 10, Background -> White], (pos[a] + pos[b])/2]}], {m, moves}]}],
   PlotLabel -> Style[Row[{label, ":  W₁ = ", W1[G, μ[G, x, 0], μ[G, y, 0]], ",  κ₀ = ", κ[G, {x, y}, 0]}], 10]]];
Row[{planPicture[CompleteGraph[5], {1, 2}, "K₅"], planPicture[CycleGraph[6], {1, 2}, "C₆"], planPicture[tree, {2, 4}, "binary tree"]}, "  "]"""),
("Figure", "Optimal transport plans for one edge of K₅, C₆ and the binary tree; the edge is black, moved mass is orange."),
("Text", "What to see: in K₅ one arrow of mass ¼; in C₆ two arrows of mass ½; in the tree some mass has to cross the edge and travel 3."),

# ------------------------------------------------------------------ 5
("Section", "5. Laziness and the Lin–Lu–Yau curvature"),
("Text", "Bipartite graphs show a defect of the non-lazy walk: on the cube Q₃ the walk at x lives on the odd vertices and the walk at y on the even ones, so every unit of mass must move and κ₀ = 0, "
         "although the lazy walk below shows the cube is positively curved. Laziness repairs this. The idleness function α ↦ κ_α(x, y) is concave and piecewise linear, "
         "and on [1/(d + 1), 1], with d = max(deg x, deg y), it is linear and vanishes at α = 1 (Bourne, Cushing, Liu, Münch and Peyerimhoff 2018). "
         "Lin, Lu and Yau (2011) defined κ_LLY = lim κ_α/(1 − α) as α → 1. Linearity gives, for every α in that interval,"),
("Text", "κ_LLY(x, y) = κ_α(x, y)/(1 − α),   in particular κ_LLY = 2 κ_{1/2}."),
("Text", "Münch and Wojciechowski (2019) showed κ_LLY(x, y) = min{ ∇ₓᵧ Δf : f 1-Lipschitz, f(y) − f(x) = 1 }, a formula in the graph Laplacian Δf(v) = mean of f over neighbours − f(v). "
         "This is how κLLY is computed in the toolkit, independently of any transport problem. The check compares the two routes on seven edges."),
("Input",
"""cases = {{"K₅", CompleteGraph[5], {1, 2}}, {"C₆", CycleGraph[6], {1, 2}}, {"Q₃", HypercubeGraph[3], {1, 2}}, {"Petersen", PetersenGraph[], {1, 3}},
   {"tree", tree, {2, 4}}, {"dumbbell bridge", dumbbell, {5, 6}}, {"star", StarGraph[5], {1, 2}}};
as = {0, 1/8, 1/6, 1/5, 1/4, 1/3, 1/2, 2/3, 3/4, 9/10};
idle = Table[With[{G = c[[2]], e = c[[3]]}, {c[[1]], Max[VertexDegree[G, #] & /@ e], κ[G, e, #] & /@ as, κLLY[G, e]}], {c, cases}];
Grid[Prepend[{#[[1]], #[[2]], Union[Select[Transpose[{as, #[[3]]}], Function[p, p[[1]] >= 1/(#[[2]] + 1)]] /. {a_, k_} :> k/(1 - a)], #[[4]]} & /@ idle,
  {"edge", "d", Row[{Subscript["κ", "α"], "/(1 − α) for α ≥ 1/(d+1)"}], Row[{Subscript["κ", "LLY"], " (Laplacian LP)"}]}], Frame -> All, Background -> {None, {LightGray}}]"""),
("Text", "Check: in every row the third column is a single value equal to the fourth — K₅ 5/4, C₆ 0, Q₃ 2/3, Petersen 0, tree −2/3, dumbbell bridge −3/5, star 1/2."),
("Text", "The idleness functions themselves (Fig. 3): each is linear from α = 1/(d + 1) down to 0 at α = 1; the dot marks α = 1/(d + 1). K₅ peaks at κ = 1 exactly there."),
("Input",
"""ListLinePlot[Table[Append[Transpose[{as, t[[3]]}], {1, 0}], {t, idle}], PlotMarkers -> Automatic, PlotLegends -> idle[[All, 1]],
 Epilog -> {Black, PointSize[0.018], Table[Point[{1/(t[[2]] + 1), κ[cases[[i, 2]], cases[[i, 3]], 1/(t[[2]] + 1)]}], {i, Length[idle]}, {t, {idle[[i]]}}]},
 AxesLabel -> {"α", Subscript["κ", "α"]}, PlotLabel -> "Idleness functions: linear on [1/(d+1), 1]", ImageSize -> 520, GridLines -> {{1/2}, {0}}]"""),

("Figure", "Idleness functions α ↦ κ_α on seven edges; black dots mark α = 1/(d + 1)."),

# ------------------------------------------------------------------ 6
("Section", "6. A gallery of graphs"),
("Text", "Fig. 4 colours every edge by κ_LLY (= 2κ_{1/2}) on the CCN scale: blue negative, near-white zero, orange positive. "
         "Complete graphs and cubes are positive, cycles and grids are flat in the interior, trees and bridges are negative."),
("Input",
"""edgePlot[G_, label_] := With[{ks = κLLY[G, List @@ #] & /@ EdgeList[G]},
  Graph[G, EdgeStyle -> Thread[EdgeList[G] -> (Directive[κColour[#, 1.25], Thickness[0.012]] & /@ ks)],
   VertexSize -> 0.15, VertexStyle -> GrayLevel[0.35], ImageSize -> 175,
   PlotLabel -> Style[Row[{label, "  min ", Min[ks]}], 9]]];
fam = {{"tree", tree}, {"C₆", CycleGraph[6]}, {"Q₃", HypercubeGraph[3]}, {"K₅", CompleteGraph[5]}, {"Petersen", PetersenGraph[]}, {"grid 4×4", GridGraph[{4, 4}]}, {"dumbbell", dumbbell}};
Legended[Grid[Partition[edgePlot[#[[2]], #[[1]]] & /@ fam, 4, 4, {1, 1}, ""]], κLegend[1.25, Subscript["κ", "LLY"]]]"""),
("Figure", "Seven graphs with every edge coloured by κ_LLY."),
("Text", "What to see: the grid’s boundary edges are positive and its interior edges zero; the dumbbell’s bridge path is the most negative part of the graph."),

# ------------------------------------------------------------------ 7
("Section", "7. What a lower bound on κ buys"),
("Subsection", "7.1 Local to global"),
("Text", "Ollivier proved that on a graph (more generally a geodesic space) it is enough to bound κ on edges: if κ(x, y) ≥ k for every edge then κ(x, y) ≥ k for every pair, because W₁ is a metric "
         "and the triangle inequality adds up along a geodesic. On Q₃ with the ½-lazy walk, every edge has κ = 1/3; pairs at distance 2 and 3 have at least that."),
("Input", """With[{G = HypercubeGraph[3]}, {κ[G, {1, 2}, 1/2], κ[G, {1, 4}, 1/2], κ[G, {1, 8}, 1/2], GraphDistance[G, 1, 4], GraphDistance[G, 1, 8]}]"""),
("Subsection", "7.2 Bonnet–Myers: positive curvature bounds the diameter"),
("Text", "On a Riemannian manifold Ric ≥ (n − 1)k > 0 forces diam ≤ π/√k. For graphs Lin, Lu and Yau proved: if κ_LLY ≥ k > 0 on every edge then diam(G) ≤ 2/k. "
         "The cube Q₃ attains it with equality: k = 2/3 and diam = 3."),
("Input",
"""Table[With[{G = g[[2]], k = Min[κLLY[g[[2]], List @@ #] & /@ EdgeList[g[[2]]]]}, {g[[1]], k, GraphDiameter[G], 2/k}],
 {g, {{"K₅", CompleteGraph[5]}, {"Q₃", HypercubeGraph[3]}, {"star", StarGraph[5]}, {"K₃,₃", CompleteGraph[{3, 3}]}}}]"""),
("Subsection", "7.3 Lichnerowicz: positive curvature opens a spectral gap"),
("Text", "Ollivier proved that the first non-zero eigenvalue λ₁ of the normalised Laplacian I − D⁻¹A is at least κ₀ whenever κ₀ ≥ k on all edges (and Lin–Lu–Yau the same with κ_LLY). "
         "The check lists min κ₀, min κ_LLY and λ₁; the bound is informative only when the curvature is positive."),
("Input",
"""Table[With[{G = c[[2]]}, {c[[1]], Min[κ[G, List @@ #, 0] & /@ EdgeList[G]], Min[κLLY[G, List @@ #] & /@ EdgeList[G]],
   Round[Sort[Eigenvalues[N[IdentityMatrix[VertexCount[G]] - Inverse[DiagonalMatrix[VertexDegree[G]]] . AdjacencyMatrix[G]]]][[2]], 0.0001]}], {c, cases}]"""),
("Text", "Check: K₅ has λ₁ = 5/4 = κ_LLY and Q₃ has λ₁ = 2/3 = κ_LLY (both equality); the star has λ₁ = 1 ≥ 1/2; on the other graphs the curvature is ≤ 0 and the bound says nothing."),

# ------------------------------------------------------------------ 8
("Section", "8. Back on a surface: κ ≈ Kε²/8"),
("Text", "Let mₓ be the uniform measure on the geodesic ε-ball around x in a surface of constant curvature K, and let y be at a small distance δ along a geodesic. "
         "Slide the ball along the geodesic (parallel transport). A point at signed distance λ from the geodesic follows a curve at constant distance λ, and the Jacobi equation J″ + KJ = 0 "
         "gives its displacement δ cos(√K λ) + o(δ). Averaging over the ball,"),
("Text", "W₁(mₓ, m_y) ≤ δ · E[cos(√K λ)] + o(δ),   so   κ(x, y) ≥ 1 − E[cos(√K λ)] = (K/2) E[λ²] + O(ε⁴)."),
("Text", "In the flat disc of radius ε, E[λ²] = ε²/4 (λ = ρ sin α in polar coordinates), so κ ≈ Kε²/8. Ollivier showed the sliding coupling is optimal at this order, and in dimension N the same "
         "computation gives κ = ε² Ric(v, v)/(2(N + 2)) + O(ε³). The first check computes E[λ²] exactly."),
("Input", """Integrate[(ρ Sin[α])^2 ρ, {α, 0, 2 π}, {ρ, 0, ε}]/(π ε^2)"""),
("Text", "Exact geometry of the ball: in polar coordinates (ρ, α) at x, spherical trigonometry gives sin(√K λ) = sin(√K ρ) sin α and the area element is sin(√K ρ)/√K dρ dα. "
         "The sliding-coupling curvature is then a plain integral. Its series in ε, for any K:"),
("Input",
"""kappaSliding[K_, n_] := Module[{e, ρ, α, sn = Sin[Sqrt[K] #]/Sqrt[K] &},
  Normal@Series[Integrate[Normal@Series[(1 - Sqrt[1 - Sin[Sqrt[K] ρ]^2 Sin[α]^2]) sn[ρ], {ρ, 0, n + 1}], {α, 0, 2 π}, {ρ, 0, e}]/
     (2 π Integrate[Normal@Series[sn[ρ], {ρ, 0, n + 1}], {ρ, 0, e}]), {e, 0, n}] /. e -> ε];
kappaSliding[K, 6] // Expand"""),
("Text", "Check: K ε²/8 − K² ε⁴/64 + 11 K³ ε⁶/46080. The leading term is K/8 for the sphere (K = 1), 0 for the plane and −1/8 for the hyperbolic plane (K = −1). "
         "The ε⁴ and higher terms belong to this particular coupling: they bound κ from below but are not claimed to be the exact W₁."),
("Text", "Dimension 3: on the unit 3-sphere (Ric = 2) the same sliding computation over a 3-ball gives ε² · 2/(2 · 5) = ε²/5."),
("Input",
"""Module[{e, ρ, ψ}, Normal@Series[Integrate[Normal@Series[(1 - Sqrt[1 - Sin[ρ]^2 Sin[ψ]^2]) Sin[ρ]^2, {ρ, 0, 7}] Sin[ψ], {ψ, 0, π}, {ρ, 0, e}]/
     (2 Integrate[Normal@Series[Sin[ρ]^2, {ρ, 0, 7}], {ρ, 0, e}]), {e, 0, 4}] /. e -> ε]"""),
("Text", "Check: ε²/5 − 2ε⁴/75, whose leading term is Ollivier’s ε² Ric/(2(N + 2)) with Ric = 2, N = 3."),
("Text", "Fig. 5 compares κ/ε² from exact quadrature (written cancellation-free as s²/(1 + √(1 − s²)) with s = sin(√K ρ) sin α) with its limit K/8, for K = 1, 0, −1."),
("Input",
"""κS2[ε_?NumericQ] := NIntegrate[With[{s = Sin[ρ] Sin[α]}, s^2/(1 + Sqrt[1 - s^2])] Sin[ρ], {ρ, 0, ε}, {α, 0, 2 π}]/(2 π (1 - Cos[ε]));
κH2[ε_?NumericQ] := -NIntegrate[With[{s = Sinh[ρ] Sin[α]}, s^2/(1 + Sqrt[1 + s^2])] Sinh[ρ], {ρ, 0, ε}, {α, 0, 2 π}]/(2 π (Cosh[ε] - 1));
Plot[{κS2[e]/e^2, 0, κH2[e]/e^2, 1/8, -1/8}, {e, 0.02, 1.2}, PlotStyle -> {RGBColor[0.98, 0.56, 0.17], GrayLevel[0.4], RGBColor[0.18, 0.36, 0.78], Dashed, Dashed},
 PlotLegends -> {"sphere K = 1", "plane K = 0", "hyperbolic K = −1", "K/8"}, AxesLabel -> {"ε", "κ/ε²"}, PlotRange -> {-0.2, 0.2},
 PlotLabel -> "Ollivier curvature of ε-balls tends to K/8", ImageSize -> 480]"""),
("Figure", "κ/ε² against ε for the sphere, the plane and the hyperbolic plane, with the limits ±1/8."),
("Input", """{κS2[0.05]/0.05^2, κH2[0.05]/0.05^2, N[kappaSliding[1, 6]/ε^2 /. ε -> 0.3] - κS2[0.3]/0.09}"""),
("Text", "Check: 0.12496 and −0.12504 at ε = 0.05; the series and the quadrature agree at ε = 0.3 to 3 × 10⁻⁸."),

# ------------------------------------------------------------------ 9
("Section", "9. Exercises"),
("Text", "1. Show by a transport plan and a test function that κ₀ = 0 on every edge of the complete bipartite graph K₃,₃."),
("Text", "2. Compute κ_{1/2} on an edge of C₄ and of C₅ by hand. (Answers: 1/2 and 1/4.)"),
("Text", "3. A tree edge with endpoint degrees dₓ and d_y has κ_LLY = 2/dₓ + 2/d_y − 2. Check it on the star K₁,₄ and on the two kinds of edge of the binary tree."),
("Text", "4. Show that κ_LLY = 2/n on every edge of the hypercube Qₙ, so the diameter bound 2/κ = n is attained for every n."),
("Text", "5. Prove E[λ²] = ε²/4 for the uniform measure on a flat disc, and deduce the K/8."),
("Text", "Answers, computed:"),
("Input",
"""{κ[CompleteGraph[{3, 3}], {1, 4}, 0], {κ[CycleGraph[4], {1, 2}, 1/2], κ[CycleGraph[5], {1, 2}, 1/2]},
 {κLLY[StarGraph[5], {1, 2}], 2/4 + 2/1 - 2, κLLY[tree, {2, 4}], 2/3 + 2/3 - 2, κLLY[tree, {4, 8}], 2/3 + 2/1 - 2},
 Table[{n, κLLY[HypercubeGraph[n], {1, 2}], GraphDiameter[HypercubeGraph[n]]}, {n, 2, 5}]}"""),

# ------------------------------------------------------------------ 10
("Section", "10. Summary"),
("Text", "κ(x, y) = 1 − W₁(mₓ, m_y)/d(x, y) needs only a distance and an averaging rule. On graphs it is computed by a transport linear program (or its 1-Lipschitz dual); "
         "laziness makes it linear in α and yields the Lin–Lu–Yau curvature, itself a Laplacian formula. Positive lower bounds bound the diameter (Q₃: equality) and open a spectral gap (K₅, Q₃: equality). "
         "On a surface with ε-balls it recovers the Gauss curvature: κ = Kε²/8 + O(ε⁴); in dimension N, ε² Ric/(2(N + 2))."),
("Text", "© 2026 Computational Classnotes · CC BY-NC-SA 4.0"),
]
