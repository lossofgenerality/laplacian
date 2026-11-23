(* ::Package:: *)

(* Bakry–Émery Curvature *)
(* © 2026 Computational Classnotes · CC BY-NC-SA 4.0 *)

(* ::Title:: *)
(*Bakry–Émery Curvature*)

(* ::Text:: *)
(*The Bochner formula without derivatives: curvature from the Laplacian alone — Curvature from the Laplacian, notebook 9*)

(* ::Text:: *)
(*© 2026 Computational Classnotes · CC BY-NC-SA 4.0*)

(* ::Text:: *)
(*This notebook builds Bakry–Émery curvature from the Laplacian alone. It starts from Bochner’s formula on the round sphere, turns it into the Γ-calculus, defines the curvature-dimension condition CD(K, N) on graphs, works the smallest cases by hand, computes exact values on families of graphs, and checks the Lichnerowicz eigenvalue bound and the Lin–Yau dimension bound. Evaluate top to bottom; every section ends with a check. The write-up “Bakry–Émery Curvature” carries the same section numbers.*)

(* ::Section:: *)
(*1. Toolkit*)

(* ::Text:: *)
(*Δg[G, f] is the normalised graph Laplacian Δf(v) = mean over the neighbours w of f(w) − f(v). Γq is the carré du champ Γ(f, g) = ½(Δ(fg) − fΔg − gΔf), which on a graph is ½ mean (f(w) − f(v))(g(w) − g(v)). Γ2q is Γ₂(f) = ½ΔΓ(f) − Γ(f, Δf). At a vertex x both Γ(f)(x) and Γ₂(f)(x) are quadratic forms in the values of f on the 2-ball of x; beForms returns their matrices (with f(x) = 0, since constants drop out). KN[G, x, 1/N] is the exact largest K with Γ₂ − (Δf)²/N ≥ KΓ at x: the distance-2 values are eliminated by a Schur complement, then K is the smallest generalised eigenvalue against Γ. KBE is the N = ∞ case.*)

ClearAll[nbr, Δg, Γq, Γ2q, beForms, KN, KBE, κColour, κLegend];
nbr[G_, v_] := AdjacencyList[G, v];
Δg[G_, f_][v_] := Mean[(f[#] - f[v]) & /@ nbr[G, v]];
Γq[G_, f_, g_][v_] := 1/2 Mean[(f[#] - f[v]) (g[#] - g[v]) & /@ nbr[G, v]];
Γ2q[G_, f_][x_] := 1/2 Δg[G, Association[# -> Γq[G, f, f][#] & /@ VertexList[G]]][x] -
   Γq[G, f, Association[# -> Δg[G, f][#] & /@ VertexList[G]]][x];
beForms[G_, x_] := Module[{S1 = nbr[G, x], S2, vars, F, f, q1, q2, qD},
  S2 = Complement[VertexList[NeighborhoodGraph[G, x, 2]], S1, {x}];
  vars = Array[F, Length[S1] + Length[S2]];
  f = Association[Join[Thread[VertexList[G] -> 0], Thread[Join[S1, S2] -> vars]]];
  q1 = Γq[G, f, f][x]; q2 = Γ2q[G, f][x]; qD = Δg[G, f][x]^2;
  Join[{Length[S1]}, (1/2 D[#, {vars, 2}]) & /@ {q1, q2, qD}]];
KN[G_, x_, Ninv_] := Module[{k, M1, M2, MD, A, a, B, C, S},
  {k, M1, M2, MD} = beForms[G, x]; A = M2 - Ninv MD;
  a = A[[;; k, ;; k]]; B = A[[;; k, k + 1 ;;]]; C = A[[k + 1 ;;, k + 1 ;;]];
  S = If[C === {}, a, a - B . Inverse[C] . Transpose[B]];
  Min[Eigenvalues[{S, M1[[;; k, ;; k]]}]]];
KBE[G_, x_] := KN[G, x, 0];
κColour[k_, s_] := With[{u = Clip[k/s, {-1, 1}]}, Blend[{RGBColor[0.10, 0.27, 0.75], GrayLevel[0.97], RGBColor[0.96, 0.47, 0.02]}, (1 + Sign[u] Abs[u]^0.55)/2]];
κLegend[s_, name_] := BarLegend[{κColour[#, s] &, {-s, s}}, LegendLabel -> Style[name, 13, Black], LabelStyle -> {12, Black}];
tree = KaryTree[15, 2];
dumbbell = Graph[UndirectedEdge @@@ Join[List @@@ EdgeList[CompleteGraph[5]], (List @@@ EdgeList[CompleteGraph[5]]) + 7, {{5, 6}, {6, 7}, {7, 8}}]];
fam = {{"tree", tree}, {"C₆", CycleGraph[6]}, {"Q₃", HypercubeGraph[3]}, {"K₅", CompleteGraph[5]}, {"Petersen", PetersenGraph[]}, {"grid 4×4", GridGraph[{4, 4}]}, {"dumbbell", dumbbell}};

(* ::Section:: *)
(*2. Bochner’s formula on the sphere*)

(* ::Text:: *)
(*On a Riemannian manifold, ½Δ|∇f|² = ⟨∇f, ∇Δf⟩ + |Hess f|² + Ric(∇f, ∇f). In Γ-notation, with Γ(f) = |∇f|² and Γ₂(f) = ½ΔΓ(f) − Γ(f, Δf), this reads Γ₂(f) = |Hess f|² + Ric(∇f, ∇f). On the unit sphere S², Ric = 1, so Γ₂ − Γ = |Hess f|². The check below proves it for an arbitrary function F(θ, φ).*)

ClearAll[Δs, Γs, Γ2s, hess, hn2];
Δs[f_] := 1/Sin[θ] D[Sin[θ] D[f, θ], θ] + 1/Sin[θ]^2 D[f, {φ, 2}];
Γs[f_, g_] := D[f, θ] D[g, θ] + 1/Sin[θ]^2 D[f, φ] D[g, φ];
Γ2s[f_] := 1/2 Δs[Γs[f, f]] - Γs[f, Δs[f]];
hess[f_] := {{D[f, {θ, 2}], D[f, θ, φ] - Cot[θ] D[f, φ]}, {D[f, θ, φ] - Cot[θ] D[f, φ], D[f, {φ, 2}] + Sin[θ] Cos[θ] D[f, θ]}};
hn2[f_] := With[{H = hess[f]}, H[[1, 1]]^2 + 2 H[[1, 2]]^2/Sin[θ]^2 + H[[2, 2]]^2/Sin[θ]^4];
Simplify[Γ2s[F[θ, φ]] - Γs[F[θ, φ], F[θ, φ]] - hn2[F[θ, φ]]]

(* ::Text:: *)
(*Since |Hess f|² ≥ (Δf)²/2 in dimension 2 (Cauchy–Schwarz on the trace), Γ₂ ≥ Γ + (Δf)²/2: the sphere satisfies CD(1, 2). Equality needs a pure-trace Hessian. The height function z = cos θ is the first eigenfunction (Δz = −2z) and attains it everywhere.*)

{Simplify[{Γ2s[Cos[θ]], Γs[Cos[θ], Cos[θ]], Δs[Cos[θ]]^2/2}], Simplify[Γ2s[Cos[θ]] - Γs[Cos[θ], Cos[θ]] - Δs[Cos[θ]]^2/2]}

(* ::Text:: *)
(*For g = z + (x² − y²) = cos θ + sin²θ cos 2φ, which mixes the first two eigenspaces, the slack Γ₂ − Γ − (Δg)²/2 is 8 − 8 sin²θ + sin⁴θ (1 + cos 4φ), so it vanishes only where sin θ = 1 and cos 4φ = −1: four points of the equator. Fig. 1 shows it.*)

gS = Cos[θ] + Sin[θ]^2 Cos[2 φ];
slack = FullSimplify[Γ2s[gS] - Γs[gS, gS] - Δs[gS]^2/2];
{slack, MinMax[Table[slack, {θ, 0.01, Pi - 0.01, Pi/60}, {φ, 0, 2 Pi, Pi/60}]], Simplify[slack /. θ -> Pi/2]}

slackCol[v_] := Blend[{GrayLevel[0.98], RGBColor[1., 0.62, 0.20], RGBColor[0.92, 0.38, 0.], RGBColor[0.50, 0.20, 0.]}, (v/8)^0.8];
pic = Show[SphericalPlot3D[1, {θ, 0, Pi}, {φ, 0, 2 Pi}, ColorFunction -> Function[{x, y, z, t, p, r}, slackCol[slack /. {θ -> t, φ -> p}]],
  ColorFunctionScaling -> False, Mesh -> None, PlotPoints -> 70, Lighting -> {{"Ambient", GrayLevel[0.82]}, {"Directional", GrayLevel[0.28], ImageScaled[{2, 2, 3}]}}],
 Graphics3D[{GrayLevel[0.25], Thickness[0.004], Line[Table[1.004 {Cos[p], Sin[p], 0}, {p, 0, 2 Pi, Pi/90}]], Black, PointSize[0.03], Point[Table[1.01 {Cos[p], Sin[p], 0}, {p, Pi/4, 7 Pi/4, Pi/2}]]}],
 Boxed -> False, Axes -> False, SphericalRegion -> True, ViewPoint -> {2.4, 1.0, 0.9}, ImageSize -> 340];
Row[{pic, BarLegend[{slackCol, {0, 8}}, LegendLabel -> Style["slack", 12, Black], LabelStyle -> {12, Black}]}]

(* ::Text:: *)
(*Fig. 1. The slack Γ₂ − Γ − (Δg)²/2 of CD(1, 2) on the unit sphere for g = z + (x² − y²): zero only at the four equator points marked in black, largest, 8, at the poles.*)

(* ::Text:: *)
(*Check: the identity Γ₂ − Γ − |Hess F|² simplifies to 0 for arbitrary F; for z the slack is exactly 0; for g the slack lies in [0, 8].*)

(* ::Section:: *)
(*3. Definition on graphs*)

(* ::Text:: *)
(*On a graph Γ and Γ₂ need only the Laplacian, so the Bochner inequality can be imposed directly. A vertex x satisfies CD(K, N) if Γ₂(f)(x) ≥ (1/N)(Δf(x))² + K Γ(f)(x) for every function f. The Bakry–Émery curvature \!\(\*SubscriptBox[\(K\), \(N\)]\)(x) is the largest such K; K∞(x) drops the dimension term. Γ(f)(x) depends on the 1-ball of x and Γ₂(f)(x) on the 2-ball, so \!\(\*SubscriptBox[\(K\), \(N\)]\)(x) is a finite eigenvalue problem.*)

Dataset@Association[Function[g, g[[1]] -> N@Min[KBE[g[[2]], #] & /@ VertexList[g[[2]]]]] /@ fam]

(* ::Text:: *)
(*Check (minimum over vertices): tree −1/3, C₆ 0, Q₃ 2/3, K₅ 7/8, Petersen −1/3, 4×4 grid 0.0876 (an algebraic number), dumbbell −0.383 = (2 − √34)/10.*)

(* ::Section:: *)
(*4. Worked by hand*)

(* ::Text:: *)
(*One edge K₂. Put f(x) = 0, f(y) = t. Then Δf(x) = t, Δf(y) = −t, and Γ(f) = t²/2 at both ends, so ΔΓ(f)(x) = 0. Γ(f, Δf)(x) = ½(t − 0)(−t − t) = −t², hence Γ₂(f)(x) = 0 − (−t²) = t². So Γ₂/Γ = 2: K∞ = 2. With the dimension term, t² − t²/N ≥ K t²/2 gives \!\(\*SubscriptBox[\(K\), \(N\)]\) = 2 − 2/N.*)

{KBE[CompleteGraph[2], 1], Table[KN[CompleteGraph[2], 1, 1/n], {n, {1, 2, 4, 10}}]}

(* ::Text:: *)
(*Long cycles are flat. On Cₙ with n ≥ 5, take f(v) = position along the path through x (values −2, −1, 0, 1, 2 on the 2-ball). Then Δf = 0 near x, and Γ(f) = ½ at every vertex, so ΔΓ = 0 and Γ₂(f)(x) = 0 while Γ(f)(x) = ½. Hence K∞ ≤ 0; the kernel gives exactly 0.*)

Table[KBE[CycleGraph[n], 1], {n, 3, 9}]

(* ::Text:: *)
(*Complete graphs. On Kₙ every other vertex is a neighbour, so there is no 2-ball part. The same calculation, with Δf(x) = mean of the neighbour values, gives K∞(Kₙ) = (n + 2)/(2(n − 1)): 2 for K₂, 5/4 for K₃, 7/8 for K₅, falling to ½ as n → ∞.*)

Table[{n, KBE[CompleteGraph[n], 1], (n + 2)/(2 (n - 1))}, {n, 2, 8}]

(* ::Text:: *)
(*Check: K₂ gives 2 and \!\(\*SubscriptBox[\(K\), \(N\)]\) = 2 − 2/N; C₃ = K₃ gives 5/4, C₄ = Q₂ gives 1, Cₙ (n ≥ 5) gives 0; Kₙ matches (n + 2)/(2(n − 1)) for n = 2 … 8.*)

(* ::Section:: *)
(*5. Families*)

(* ::Text:: *)
(*The hypercube \!\(\*SubscriptBox[\(Q\), \(d\)]\) has K∞ = 2/d at every vertex. A tree is negatively curved at the root and branch vertices and positive at the leaves (2/3). On the dumbbell the two bridge vertices are the most negative, (2 − √34)/10 ≈ −0.383; the vertex where a clique meets the bridge is just below zero, (35 − √1385)/80 ≈ −0.028.*)

{Table[{d, KBE[HypercubeGraph[d], 1]}, {d, 1, 5}], Table[KBE[tree, v], {v, {1, 2, 4, 8}}], Table[KBE[dumbbell, v], {v, {1, 5, 6, 7}}]}

(* ::Text:: *)
(*Fig. 2 colours every vertex of the seven example graphs by K∞, on the same blue–white–orange scale as the Ollivier gallery.*)

vertexPlot[G_, label_] := With[{ks = KBE[G, #] & /@ VertexList[G]},
  Graph[G, VertexStyle -> Thread[VertexList[G] -> (Directive[EdgeForm[{GrayLevel[0.1], Thickness[0.004]}], κColour[#, 1.25]] & /@ ks)],
   VertexSize -> If[VertexCount[G] > 12, 0.32, 0.22], EdgeStyle -> Directive[GrayLevel[0.35], Thickness[0.006]], ImageSize -> 190,
   PlotLabel -> Style[Row[{label, "  min ", With[{k = Min[ks]}, If[MatchQ[k, _Integer | _Rational], k, NumberForm[N[k], 3]]]}], 11, GrayLevel[0.1]], ImagePadding -> {{6, 6}, {6, 34}}]];
Legended[Grid[Partition[vertexPlot[#[[2]], #[[1]]] & /@ fam, 4, 4, {1, 1}, ""]], κLegend[1.25, Subscript["K", "∞"]]]

(* ::Text:: *)
(*Fig. 2. Seven graphs with every vertex coloured by its Bakry–Émery curvature K∞. Complete graphs and cubes are positive, long cycles flat; tree branch points and the dumbbell’s bridge are negative.*)

(* ::Text:: *)
(*Check: K∞(\!\(\*SubscriptBox[\(Q\), \(d\)]\)) = 2/d for d = 1 … 5; tree: root −1/3, second level −1/3, third level (5 − √33)/6 ≈ −0.124, leaf 2/3; dumbbell: clique vertex (93 − √793)/80 ≈ 0.81, attaching vertex ≈ −0.028, bridge vertices ≈ −0.383.*)

(* ::Section:: *)
(*6. Dimension: the curve \!\(\*SubscriptBox[\(K\), \(N\)]\)*)

(* ::Text:: *)
(*Adding the dimension term lowers the curvature: \!\(\*SubscriptBox[\(K\), \(N\)]\)(x) increases with N and tends to K∞(x). Fig. 3 plots N ↦ \!\(\*SubscriptBox[\(K\), \(N\)]\) for four vertex-transitive graphs (every vertex has the same value). On C₆ and Petersen \!\(\*SubscriptBox[\(K\), \(N\)]\) already equals K∞ at N = 2: the function that attains K∞ there has Δf(x) = 0, so the dimension term costs nothing. On K₅ and Q₃ \!\(\*SubscriptBox[\(K\), \(N\)]\) only approaches K∞. Lin and Yau proved that every graph satisfies CD(1/D − 1, 2), where D is the maximum degree; the check confirms K₂ ≥ 1/D − 1 at every vertex.*)

curves = Table[{g[[1]], Table[{n, KN[g[[2]], 1, 1/n]}, {n, 1, 30, 0.5}]},
   {g, {{"K₅", CompleteGraph[5]}, {"Q₃", HypercubeGraph[3]}, {"C₆", CycleGraph[6]}, {"Petersen", PetersenGraph[]}}}];
ListLinePlot[curves[[All, 2]], PlotLegends -> curves[[All, 1]], AxesLabel -> {"N", Subscript["K", "N"]},
 PlotStyle -> (Directive[#, AbsoluteThickness[3]] & /@ {RGBColor[0.90, 0.42, 0.], RGBColor[0.10, 0.27, 0.75], RGBColor[0., 0.50, 0.45], RGBColor[0.50, 0.20, 0.72]}),
 BaseStyle -> {FontSize -> 13, FontColor -> GrayLevel[0.1]}, AxesStyle -> Directive[GrayLevel[0.2], AbsoluteThickness[1.2]],
 Epilog -> {Dashing[{0.02, 0.012}], AbsoluteThickness[1.8], RGBColor[0.90, 0.42, 0.], Line[{{0, 7/8}, {30, 7/8}}], RGBColor[0.10, 0.27, 0.75], Line[{{0, 2/3}, {30, 2/3}}]},
 PlotRange -> {{0, 30}, {-1.4, 1}}, PlotLabel -> "Curvature with a dimension term rises to K∞ (dashed)", ImageSize -> 520, ImagePadding -> {{46, 30}, {34, 34}}, GridLines -> {None, {0}}]

(* ::Text:: *)
(*Fig. 3. \!\(\*SubscriptBox[\(K\), \(N\)]\) against N on K₅, Q₃, C₆ and Petersen. Each curve rises to its K∞ (7/8 and 2/3 dashed; 0 and −1/3 are reached at N = 2).*)

AllTrue[fam, Function[g, With[{D = Max[VertexDegree[g[[2]]]]}, AllTrue[VertexList[g[[2]]], KN[g[[2]], #, 1/2] >= 1/D - 1 &]]]]

(* ::Text:: *)
(*Check: the curves increase in N; K₂ ≥ 1/D − 1 holds at every vertex of all seven graphs (True).*)

(* ::Section:: *)
(*7. What a lower bound buys: Lichnerowicz and Bonnet–Myers*)

(* ::Text:: *)
(*If every vertex satisfies CD(K, N) with K > 0, the first non-zero eigenvalue of −Δ satisfies λ₁ ≥ NK/(N − 1); with N = ∞, λ₁ ≥ K. The table compares λ₁ with the best bound over N.*)

spec[G_] := With[{A = N[AdjacencyMatrix[G]], d = N[VertexDegree[G]]}, Sort[Eigenvalues[IdentityMatrix[Length[d]] - DiagonalMatrix[1/d] . A]][[2]]];
Dataset@Association[Function[g, g[[1]] -> With[{G = g[[2]]}, <|"λ₁" -> spec[G], "K∞" -> N@Min[KBE[G, #] & /@ VertexList[G]],
       "best NK/(N−1)" -> Max[Table[With[{k = Min[KN[G, #, 1/n] & /@ VertexList[G]]}, If[k > 0, N[n k/(n - 1)], 0]], {n, {2, 3, 4, 6, 10, 20, 50}}]]|>]] /@
   {{"K₅", CompleteGraph[5]}, {"Q₃", HypercubeGraph[3]}, {"K₃", CompleteGraph[3]}, {"Q₄", HypercubeGraph[4]}}]

(* ::Text:: *)
(*Check: λ₁ ≥ K∞ in every row, with equality on the cubes Q₃ (2/3) and Q₄ (1/2). On these graphs the N = ∞ bound is the strongest; the best finite-N bound is a little lower.*)

(* ::Text:: *)
(*Diameter. Liu, Münch and Peyerimhoff prove diam ≤ 2 \!\(\*SubscriptBox[\(Deg\), \(max\)]\)/K under CD(K, ∞) for the unnormalised Laplacian, sharp on hypercubes. For a d-regular graph the normalised Laplacian is 1/d times the unnormalised one, so K∞ scales by 1/d and the bound becomes diam ≤ 2/K∞.*)

Grid[Prepend[Function[g, With[{k = Min[KBE[g[[2]], #] & /@ VertexList[g[[2]]]]}, {g[[1]], GraphDiameter[g[[2]]], k, 2/k}]] /@
    {{"K₃", CompleteGraph[3]}, {"K₅", CompleteGraph[5]}, {"Q₂", HypercubeGraph[2]}, {"Q₃", HypercubeGraph[3]}, {"Q₄", HypercubeGraph[4]}},
   {"graph", "diam", Subscript["K", "∞"], "2/K∞"}], Frame -> All]

(* ::Text:: *)
(*Check: diam ≤ 2/K∞ on every row, with equality on the cubes Q₂, Q₃, Q₄ (diameter d = 2/(2/d)).*)

(* ::Section:: *)
(*8. Bakry–Émery and Ollivier side by side*)

(* ::Text:: *)
(*Both curvatures copy a property of Ricci curvature, Bakry–Émery the Bochner formula and Ollivier the transport of balls. They agree in sign on these examples but not in size. The Ollivier values are from notebook 7 (Lin–Lu–Yau curvature, minimum over edges).*)

Grid[Prepend[Function[g, {g[[1]], N@Min[KBE[g[[2]], #] & /@ VertexList[g[[2]]]], g[[3]]}] /@
    {{"K₅", CompleteGraph[5], "5/4"}, {"Q₃", HypercubeGraph[3], "2/3"}, {"C₆", CycleGraph[6], "0"}, {"Petersen", PetersenGraph[], "0"}, {"grid 4×4", GridGraph[{4, 4}], "0"}},
   {"graph", Subscript["K", "∞"], Row[{"min ", Subscript["κ", "LLY"]}]}], Frame -> All]

(* ::Text:: *)
(*Check: on Q₃ both give 2/3; on K₅ Ollivier is larger (5/4 against 7/8); on Petersen Bakry–Émery is negative (−1/3) while Lin–Lu–Yau is 0.*)

(* ::Section:: *)
(*9. Exercises*)

(* ::Text:: *)
(*1. Show by hand that K∞(K₃) = 5/4. 2. Show \!\(\*SubscriptBox[\(K\), \(N\)]\)(K₂) = 2 − 2/N from the K₂ calculation. 3. Find f on C₄ with Γ₂(f) = Γ(f) at a vertex, so K∞(C₄) ≤ 1. 4. Prove K∞(\!\(\*SubscriptBox[\(Q\), \(d\)]\)) ≤ 2/d with f = one coordinate. 5. On S², show that the slack of g is 8 − 8 sin²θ + sin⁴θ (1 + cos 4φ) and find its four zeros.*)

{KBE[CompleteGraph[3], 1], KBE[CycleGraph[4], 1], slack /. {θ -> Pi/2, φ -> Pi/4}}

(* ::Text:: *)
(*Check: 5/4, 1, 0.*)

(* ::Text:: *)
(*© 2026 Computational Classnotes · CC BY-NC-SA 4.0*)
