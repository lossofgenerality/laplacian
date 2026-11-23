# Cell content for "The Laplacian and Curvature" notebook.
# Each entry: (style, text). Styles: Title, Subtitle, Section, Subsection, Text, Input.

CELLS = [
("Title", "The Laplacian and Curvature"),
("Subtitle", "Instances and relationships, computed — a Laplacian Lab companion notebook"),
("Text", "© 2026 Computational Classnotes · CC BY-NC-SA 4.0"),
("Text", "Each section below matches a section of the write-up “The Laplacian and Curvature — Instances and Relationships”. "
         "Evaluate the notebook top to bottom: Sections 2\u20136 use the toolkit of Section 1 and Section 9 uses the functions of Section 8. Each section ends with a check that should return True, 0, or a number "
         "close to the value stated in the write-up. Conventions: Δ is the analyst’s Laplacian (Δ = div grad, negative semidefinite on closed manifolds); "
         "on graphs Δf(x) = mean of f over the neighbours of x minus f(x) (random-walk normalisation) unless stated otherwise."),

# ---------------------------------------------------------------- 1
("Section", "1. Riemannian toolkit (used in Sections 2–5)"),
("Text", "Laplace–Beltrami operator, Christoffel symbols, covariant Hessian, Riemann tensor and Gauss curvature for a metric g in coordinates \U0001D4CD."),
("Input",
"""ClearAll[christoffel, laplaceBeltrami, gradNorm2, hessian, hessNorm2, gaussCurvature];
christoffel[g_, \U0001D4CD_] := Module[{gi = Inverse[g], n = Length[\U0001D4CD]},
  Table[1/2 Sum[gi[[i, l]] (D[g[[l, j]], \U0001D4CD[[k]]] + D[g[[l, k]], \U0001D4CD[[j]]] - D[g[[j, k]], \U0001D4CD[[l]]]), {l, n}],
   {i, n}, {j, n}, {k, n}] // Simplify];
laplaceBeltrami[g_, \U0001D4CD_][u_] := Module[{gi = Inverse[g], s = Sqrt[Det[g]], n = Length[\U0001D4CD]},
  1/s Sum[D[s gi[[i, j]] D[u, \U0001D4CD[[j]]], \U0001D4CD[[i]]], {i, n}, {j, n}]];
gradNorm2[g_, \U0001D4CD_][u_] := With[{gi = Inverse[g]}, Sum[gi[[i, j]] D[u, \U0001D4CD[[i]]] D[u, \U0001D4CD[[j]]], {i, Length[\U0001D4CD]}, {j, Length[\U0001D4CD]}]];
hessian[g_, \U0001D4CD_][u_] := With[{Γ = christoffel[g, \U0001D4CD], n = Length[\U0001D4CD]},
  Table[D[u, \U0001D4CD[[i]], \U0001D4CD[[j]]] - Sum[Γ[[k, i, j]] D[u, \U0001D4CD[[k]]], {k, n}], {i, n}, {j, n}]];
hessNorm2[g_, \U0001D4CD_][u_] := With[{gi = Inverse[g], H = hessian[g, \U0001D4CD][u]}, Tr[gi . H . gi . H]];
gaussCurvature[g_, \U0001D4CD_] := Module[{Γ = christoffel[g, \U0001D4CD], R},
  R[i_, j_, k_, l_] := D[Γ[[i, j, l]], \U0001D4CD[[k]]] - D[Γ[[i, j, k]], \U0001D4CD[[l]]] +
     Sum[Γ[[i, k, m]] Γ[[m, j, l]] - Γ[[i, l, m]] Γ[[m, j, k]], {m, 2}];
  Simplify[Sum[g[[1, i]] R[i, 2, 1, 2], {i, 2}]/Det[g]]];
gS2 = {{1, 0}, {0, Sin[θ]^2}}; \U0001D4CDS2 = {θ, φ};
gaussCurvature[gS2, \U0001D4CDS2]"""),

# ---------------------------------------------------------------- 2
("Section", "2. Gauss curvature is a Laplacian: conformal metrics and Liouville’s equation"),
("Text", "For g = e^{2u}(dx² + dy²) the Gauss curvature is K = −e^{−2u} Δ₀u, where Δ₀ is the flat Laplacian. "
         "Equivalently Δ₀u = −K e^{2u} (Liouville’s equation when K is constant). Checks: the round sphere through stereographic projection gives K = 1, the Poincaré half-plane gives K = −1, and the formula agrees with the Riemann-tensor computation for a generic u."),
("Input",
"""Kconformal[u_] := Simplify[-Exp[-2 u] (D[u, {x, 2}] + D[u, {y, 2}])];
{Kconformal[Log[2/(1 + x^2 + y^2)]],          (* unit sphere, stereographic *)
 Kconformal[Log[1/y]],                         (* hyperbolic half-plane *)
 Kconformal[Log[2/(1 - x^2 - y^2)]],           (* Poincaré disc *)
 Simplify[Kconformal[w[x, y]] - gaussCurvature[Exp[2 w[x, y]] IdentityMatrix[2], {x, y}]]}"""),

# ---------------------------------------------------------------- 3
("Section", "3. Mean curvature is a Laplacian: ΔX = −2H\U0001D427"),
("Text", "For a surface X : U → ℝ³ with induced metric, the Laplace–Beltrami operator applied to each coordinate of the position vector gives the mean-curvature vector: ΔX = −2H\U0001D427 (H the mean of the principal curvatures, \U0001D427 the unit normal; the sign depends on orientation). "
         "Consequence: a surface is minimal exactly when its coordinate functions are harmonic. Checks: sphere (H = 1/a), torus, and the catenoid (H = 0)."),
("Input",
"""meanCurvatureVector[pos_, \U0001D4CD_, assum_ : True] := Module[{g, n, ΔX},
  g = Simplify[Table[D[pos, \U0001D4CD[[i]]] . D[pos, \U0001D4CD[[j]]], {i, 2}, {j, 2}]];
  ΔX = Simplify[laplaceBeltrami[g, \U0001D4CD] /@ pos];
  n = Simplify[Normalize[Cross[D[pos, \U0001D4CD[[1]]], D[pos, \U0001D4CD[[2]]]]], \U0001D4CD ∈ Reals && assum];
  <|"H" -> Simplify[-ΔX . n/2, \U0001D4CD ∈ Reals && assum],
    "tangential part" -> Simplify[{ΔX . D[pos, \U0001D4CD[[1]]], ΔX . D[pos, \U0001D4CD[[2]]]}]|>];
{meanCurvatureVector[3 {Sin[θ] Cos[φ], Sin[θ] Sin[φ], Cos[θ]}, {θ, φ}, 0 < θ < π],
 meanCurvatureVector[{(2 + Cos[v]) Cos[u], (2 + Cos[v]) Sin[u], Sin[v]}, {u, v}],
 meanCurvatureVector[{Cosh[v] Cos[u], Cosh[v] Sin[u], v}, {u, v}]}"""),

# ---------------------------------------------------------------- 4
("Section", "4. Mean values and volumes: curvature in the mean-value expansion of Δ"),
("Text", "Laplacian Lab Section 1 derives Δ from the sphere mean in flat space: M_r f = f + r²/(2n) Δf + …. On a curved manifold the same expansion picks up curvature (Gray–Willmore 1982). "
         "On a surface of constant curvature K the geodesic-circle mean is"),
("Text", "  M_r f(p) = f + (r²/4) Δf + r⁴ (Δ²f/64 + K Δf/96) + r⁶ (Δ³f/2304 + K Δ²f/1152 + K² Δf/1440) + O(r⁸)."),
("Text", "Derivation on the unit sphere: the circle-mean operator acts on a degree-l spherical harmonic as the Legendre polynomial P_l(cos r), and Δ acts as λ = −l(l+1). Matching the series of P_l(cos r) in powers of λ gives the coefficients; scaling the sphere restores K."),
("Input",
"""λ = -l (l + 1);
ser = Expand@Normal@Series[LegendreP[l, Cos[r]], {r, 0, 6}];
{Factor@Coefficient[ser, r, 2],
 SolveAlways[Coefficient[ser, r, 4] == a λ^2 + b λ, l],
 SolveAlways[Coefficient[ser, r, 6] == a3 λ^3 + b3 λ^2 + c3 λ, l]}"""),
("Text", "Direct check on S² with a non-symmetric test function. Write it in ambient coordinates and extend it as a degree-0 function F(X/|X|); then |X|²·Δ_ℝ³ of it is again degree 0 and equals Δ_S² F. Average F over the geodesic circle of colatitude r about the north pole and compare with the formula evaluated at the pole."),
("Input",
"""F0[{x_, y_, z_}] := Exp[z] (1 + x)^2 + y z^3;
ext = F0[{x, y, z}/Sqrt[x^2 + y^2 + z^2]];
ΔS2amb[h_] := Simplify[(x^2 + y^2 + z^2) Laplacian[h, {x, y, z}]];
L1 = ΔS2amb[ext]; L2 = ΔS2amb[L1]; L3 = ΔS2amb[L2];
atPole[h_] := h /. {x -> 0, y -> 0, z -> 1};
circleMean = Integrate[Normal@Series[F0[{Sin[r] Cos[φ], Sin[r] Sin[φ], Cos[r]}], {r, 0, 6}], {φ, 0, 2 π}]/(2 π);
formula = atPole[ext] + r^2/4 atPole[L1] + r^4 (atPole[L2]/64 + atPole[L1]/96) +
   r^6 (atPole[L3]/2304 + atPole[L2]/1152 + atPole[L1]/1440);
Simplify[Expand[circleMean - formula]]"""),
("Text", "Volumes. Area of a geodesic disc on a surface of curvature K: A(r) = πr²(1 − K r²/12 + K²r⁴/360 − …) (Bertrand–Diguet–Puiseux). In dimension n: Vol B_r = ω_n rⁿ (1 − S r²/(6(n+2)) + O(r⁴)), S the scalar curvature. Check on S³ (S = 6)."),
("Input",
"""areaK = 2 π Integrate[Sin[Sqrt[K] ρ]/Sqrt[K], {ρ, 0, r}];
volS3 = 4 π Integrate[Sin[ρ]^2, {ρ, 0, r}];
{Series[areaK/(π r^2), {r, 0, 4}], Series[volS3/(4/3 π r^3), {r, 0, 2}], 1 - 6 r^2/(6 (3 + 2))}"""),

# ---------------------------------------------------------------- 5
("Section", "5. Heat kernel and spectrum: curvature is audible"),
("Text", "Minakshisundaram–Pleijel / McKean–Singer: Tr e^{tΔ} ~ (4plan)^{−n/2} (Vol + (t/6)∫S + O(t²)). On the unit S² (area 4π, S = 2) the spectrum is l(l+1) with multiplicity 2l+1, so t·Tr e^{tΔ} → 1 + t/3 + t²/15 + …. For a surface the t⁰ coefficient is (1/12π)∫K = χ/6, so the Euler characteristic can be heard."),
("Input",
"""heatTrace[t_?NumericQ] := Sum[(2 j + 1) Exp[-j (j + 1) t], {j, 0, 2000}];
TableForm[Table[{t, t heatTrace[t], 1 + t/3 + t^2/15}, {t, {0.1, 0.03, 0.01}}],
 TableHeadings -> {None, {"t", "t·Tr e^{tΔ}", "1 + t/3 + t²/15"}}]"""),

# ---------------------------------------------------------------- 6
("Section", "6. Bochner formula, Lichnerowicz bound and Laplacian comparison"),
("Text", "Bochner: ½Δ|∇f|² = |Hess f|² + ⟨∇f, ∇Δf⟩ + Ric(∇f, ∇f). This is the identity every “Bakry–Émery” curvature (Section 8) copies. Verified for an arbitrary f on S² (Ric = g)."),
("Input",
"""ΔS2 = laplaceBeltrami[gS2, \U0001D4CDS2];
F = \U0001D4BB[θ, φ];
Simplify[1/2 ΔS2[gradNorm2[gS2, \U0001D4CDS2][F]] - (hessNorm2[gS2, \U0001D4CDS2][F] +
     Sum[Inverse[gS2][[i, j]] D[F, \U0001D4CDS2[[i]]] D[ΔS2[F], \U0001D4CDS2[[j]]], {i, 2}, {j, 2}] + gradNorm2[gS2, \U0001D4CDS2][F])]"""),
("Text", "Lichnerowicz: Ric ≥ (n−1)k > 0 implies λ₁ ≥ nk. On the unit S² (n = 2, k = 1) the first eigenvalue is exactly 2: equality (Obata). Laplacian comparison: Ric ≥ 0 gives Δr ≤ (n−1)/r; on S² the distance from the pole has Δr = cot r ≤ 1/r."),
("Input",
"""{Simplify[ΔS2[SphericalHarmonicY[1, 0, θ, φ]]/SphericalHarmonicY[1, 0, θ, φ]],
 Simplify[ΔS2[θ]],
 And @@ Table[Cot[r] <= 1/r, {r, 0.01, 3.13, 0.01}]}"""),

# ---------------------------------------------------------------- 7
("Section", "7. Discrete surfaces: cotangent Laplacian, angle defect, discrete Gauss–Bonnet"),
("Text", "On a triangle mesh, the cotangent Laplacian (L f)_i = ½ Σ_j (cot α_ij + cot β_ij)(f_j − f_i), divided by the vertex area A_i, approximates Δ. Applied to the vertex positions it gives the discrete mean-curvature normal (Meyer–Desbrun–Schröder–Barr). "
         "The angle defect 2π − Σθ at a vertex is the discrete Gauss curvature; it sums to exactly 2πχ. Test: 400-point mesh of the unit sphere (H = 1, K = 1, χ = 2)."),
("Input",
"""mesh = ConvexHullMesh[SpherePoints[400]];
P = MeshCoordinates[mesh]; T = MeshCells[mesh, 2][[All, 1]]; nv = Length[P];
angle[i_, j_, k_] := VectorAngle[P[[j]] - P[[i]], P[[k]] - P[[i]]];
defect = ConstantArray[2. π, nv]; W = SparseArray[{}, {nv, nv}, 0.]; A = ConstantArray[0., nv];
Do[Module[{a, b, c}, {a, b, c} = tri;
  defect[[a]] -= angle[a, b, c]; defect[[b]] -= angle[b, c, a]; defect[[c]] -= angle[c, a, b];
  W[[b, c]] += Cot[angle[a, b, c]]/2; W[[c, b]] += Cot[angle[a, b, c]]/2;
  W[[c, a]] += Cot[angle[b, c, a]]/2; W[[a, c]] += Cot[angle[b, c, a]]/2;
  W[[a, b]] += Cot[angle[c, a, b]]/2; W[[b, a]] += Cot[angle[c, a, b]]/2;
  A[[{a, b, c}]] += Norm[Cross[P[[b]] - P[[a]], P[[c]] - P[[a]]]]/6], {tri, T}];
Lcot = W - DiagonalMatrix[Total[W]];
ΔX = (Lcot . P)/A;
<|"Σ angle defect / 2π (= χ)" -> Total[defect]/(2 π),
  "mean K = defect/area" -> Mean[defect/A],
  "mean |ΔX|/2 (= H)" -> Mean[Norm /@ ΔX]/2,
  "mean ΔX·n" -> Mean[MapThread[Dot, {ΔX, P}]]|>"""),
("Input",
"""Graphics3D[{EdgeForm[GrayLevel[.6]], MapThread[{ColorData["SunsetColors"][Rescale[#2, MinMax[defect/A]]], Polygon[P[[#1]]]} &,
   {T, Mean[(defect/A)[[#]]] & /@ T}]}, Boxed -> False, PlotLabel -> "Angle defect / vertex area ≈ K = 1"]"""),

# ---------------------------------------------------------------- 8
("Section", "8. Graph curvatures built from the graph Laplacian"),
("Text", "Every notion below is defined from the graph Laplacian Δ, from the random walk it generates, or from its pseudoinverse. "
         "Test graphs: cycle C₆, complete K₅, cube Q₃, Petersen graph, 4×4 grid."),
("Subsection", "8.1 Ollivier / Lin–Lu–Yau curvature"),
("Text", "Ollivier: κ_α(x,y) = 1 − W₁(μ_x^α, μ_y^α)/d(x,y), with μ_x^α the lazy random walk (stay with probability α). It compares averages over two small balls — the discrete twin of Section 4. "
         "Lin–Lu–Yau: κ = lim_{α→1} κ_α/(1−α); it equals 2κ_{1/2} for every edge. "
         "Münch–Wojciechowski limit-free formula: κ(x,y) = inf { ∇_{xy}Δf : f 1-Lipschitz, ∇_{yx}f = 1 }, a linear program in which the Laplacian appears explicitly. "
         "Both routes are computed and must agree."),
("Input",
"""nbr[G_, v_] := AdjacencyList[G, v];
Δgraph[G_, f_][v_] := Mean[f /@ nbr[G, v]] - f[v];

κLLY[G_, {x_, y_}] := Module[{S, vars, f, cons, obj},
  S = Union[{x, y}, nbr[G, x], nbr[G, y]];
  vars = Table[Unique["f"], {Length[S]}]; f = AssociationThread[S -> vars];
  cons = Flatten[{f[y] - f[x] == 1, f[x] == 0,
     Table[With[{d = GraphDistance[G, S[[i]], S[[j]]]}, {f[S[[i]]] - f[S[[j]]] <= d, f[S[[j]]] - f[S[[i]]] <= d}],
      {i, Length[S]}, {j, i + 1, Length[S]}]}];
  obj = Δgraph[G, f][x] - Δgraph[G, f][y];
  LinearOptimization[obj, cons, vars, "PrimalMinimumValue"]];

W1[G_, μ_Association, ν_Association] := Module[{A = Keys[μ], B = Keys[ν], plan, vars},
  vars = Flatten@Table[plan[a, b], {a, A}, {b, B}];
  LinearOptimization[Sum[GraphDistance[G, a, b] plan[a, b], {a, A}, {b, B}],
   Join[Table[Sum[plan[a, b], {b, B}] == μ[a], {a, A}], Table[Sum[plan[a, b], {a, A}] == ν[b], {b, B}], Thread[vars >= 0]],
   vars, "PrimalMinimumValue"]];
μLazy[G_, x_, α_] := Merge[{<|x -> α|>, AssociationThread[nbr[G, x] -> (1 - α)/Length[nbr[G, x]]]}, Total];
κOllivier[G_, {x_, y_}, α_] := 1 - W1[G, μLazy[G, x, α], μLazy[G, y, α]];

graphs = <|"C6" -> CycleGraph[6], "K5" -> CompleteGraph[5], "Q3" -> HypercubeGraph[3],
   "Petersen" -> PetersenGraph[], "Grid4x4" -> GridGraph[{4, 4}]|>;
edges[G_] := List @@@ EdgeList[G];
Dataset@Map[Function[G, <|"min κ_LLY (LP)" -> Min[κLLY[G, #] & /@ edges[G]],
     "min 2κ_1/2 (transport)" -> Min[2 κOllivier[G, #, 1/2] & /@ edges[G]],
     "min κ_0" -> Min[κOllivier[G, #, 0] & /@ edges[G]]|>], graphs]"""),
("Subsection", "8.2 Bakry–Émery curvature (the discrete Bochner formula)"),
("Text", "Γ(f) = ½(Δf² − 2fΔf), Γ₂(f) = ½(ΔΓ(f) − 2Γ(f, Δf)). The curvature-dimension condition CD(K, ∞) at x is Γ₂(f)(x) ≥ K Γ(f)(x) for all f. "
         "Both sides are quadratic forms in the values of f on the 2-ball of x, so the best K is the largest K with Γ₂ − KΓ positive semidefinite (found by bisection)."),
("Input",
"""bakryEmery[G_, x_] := Module[{B2, F, ff, Γv, q1, q2, M1, M2, lo = -10., hi = 10., mid},
  B2 = VertexList[NeighborhoodGraph[G, x, 2]];
  F = Array[\U0001D4BB, Length[B2]]; ff = AssociationThread[B2 -> F];
  Γv[v_] := 1/2 Mean[(ff[#] - ff[v])^2 & /@ nbr[G, v]];
  q1 = Γv[x];
  q2 = 1/2 (Mean[Γv /@ nbr[G, x]] - Γv[x]) -
    1/2 Mean[(ff[#] - ff[x]) (Δgraph[G, ff][#] - Δgraph[G, ff][x]) & /@ nbr[G, x]];
  M1 = D[q1, {F, 2}]/2; M2 = D[q2, {F, 2}]/2;
  Do[mid = (lo + hi)/2; If[Min[Eigenvalues[N[M2 - mid M1]]] >= -10^-9, lo = mid, hi = mid], {60}];
  N[Floor[lo 10^6]/10^6]];   (* rounded down, so theorem checks stay safe *)
Dataset@Map[Function[G, Min[bakryEmery[G, #] & /@ VertexList[G]]], graphs]"""),
("Subsection", "8.3 Forman curvature (the discrete Bochner–Weitzenböck splitting)"),
("Text", "Forman splits the combinatorial Hodge Laplacian on 1-cells as □ = B + F; the diagonal part F is the curvature. For an unweighted graph, F(e) = 4 − d_x − d_y; counting triangles as 2-cells gives the augmented version 4 − d_x − d_y + 3·#triangles(e)."),
("Input",
"""forman[G_, {x_, y_}] := 4 - VertexDegree[G, x] - VertexDegree[G, y];
formanAug[G_, {x_, y_}] := forman[G, {x, y}] + 3 Length[Intersection[nbr[G, x], nbr[G, y]]];
Dataset@Map[Function[G, <|"min Forman" -> Min[forman[G, #] & /@ edges[G]],
     "min augmented" -> Min[formanAug[G, #] & /@ edges[G]]|>], graphs]"""),
("Subsection", "8.4 Resistance curvature (from the pseudoinverse of the Laplacian)"),
("Text", "Effective resistance ω_ij = (L⁺)_ii + (L⁺)_jj − 2(L⁺)_ij with L the Kirchhoff matrix. Node curvature p_i = 1 − ½ Σ_{j~i} ω_ij (Devriendt–Lambiotte). "
         "Foster’s theorem Σ_edges ω = n − 1 makes Σ p_i = 1 for every connected graph: a discrete Gauss–Bonnet theorem. Edge curvature κ_ij = 2(p_i + p_j)/ω_ij."),
("Input",
"""resistance[G_] := Module[{Lp = PseudoInverse[N@KirchhoffMatrix[G]], n = VertexCount[G]},
  Table[Lp[[i, i]] + Lp[[j, j]] - 2 Lp[[i, j]], {i, n}, {j, n}]];
pNode[G_] := With[{Ω = resistance[G], V = VertexList[G]},
  Table[1 - 1/2 Sum[Ω[[i, VertexIndex[G, j]]], {j, nbr[G, V[[i]]]}], {i, Length[V]}]];
Dataset@Map[<|"Σ p (=1)" -> Chop@Total[pNode[#]], "min p" -> Min[pNode[#]], "max p" -> Max[pNode[#]]|> &, graphs]"""),
("Subsection", "8.5 Steinerberger curvature and combinatorial (Higuchi) curvature"),
("Text", "Steinerberger: solve D·K = n·1 with D the distance matrix (least squares if singular). Higuchi’s combinatorial curvature for a polyhedral surface: κ(v) = 1 − d_v/2 + Σ_faces∋v 1/|face|; by Euler’s formula it sums to χ = 2 on every convex polyhedron."),
("Input",
"""steinerberger[G_] := LeastSquares[N@GraphDistanceMatrix[G], ConstantArray[N@VertexCount[G], VertexCount[G]]];
higuchiTotal[name_] := Module[{F = PolyhedronData[name, "FaceIndices"], nv = Length[PolyhedronData[name, "VertexCoordinates"]]},
  Total@Table[1 - Count[F, _?(MemberQ[#, v] &)]/2 + Total[1/Length[#] & /@ Select[F, MemberQ[#, v] &]], {v, nv}]];
{Dataset@Map[<|"min K" -> Min[steinerberger[#]], "max K" -> Max[steinerberger[#]]|> &, graphs],
 AssociationMap[higuchiTotal, {"Tetrahedron", "Cube", "Dodecahedron", "Icosahedron", "TruncatedIcosahedron"}]}"""),

# ---------------------------------------------------------------- 9
("Section", "9. Spectral consequences on graphs, and the graph-to-manifold limit"),
("Text", "Discrete Lichnerowicz theorems for the normalised Laplacian I − D^{−1/2}AD^{−1/2}: Ollivier curvature ≥ κ > 0 gives λ₁ ≥ κ (Ollivier; Lin–Lu–Yau); CD(K,∞) gives λ₁ ≥ K (Bakry–Émery; Lin–Yau); and λ_max ≤ 2 − κ₀ (Ollivier, Bauer–Jost–Liu)."),
("Input",
"""normLap[G_] := Module[{A = N@AdjacencyMatrix[G], d}, d = Total[A];
   IdentityMatrix[Length[d]] - DiagonalMatrix[d^(-1/2)] . A . DiagonalMatrix[d^(-1/2)]];
spec[G_] := Sort[Eigenvalues[normLap[G]]];
Dataset@Map[Function[G, With[{s = spec[G], kL = Min[κLLY[G, #] & /@ edges[G]], kB = Min[bakryEmery[G, #] & /@ VertexList[G]],
      k0 = Min[κOllivier[G, #, 0] & /@ edges[G]]},
     <|"λ1" -> s[[2]], "λmax" -> Last[s], "λ1 ≥ κ_LLY" -> s[[2]] >= kL - 10^-9,
       "λ1 ≥ K_BE" -> s[[2]] >= kB - 10^-6, "λmax ≤ 2 − κ0" -> Last[s] <= 2 - k0 + 10^-9|>]], graphs]"""),
("Text", "Belkin–Niyogi: on points sampled from a manifold, the heat-kernel graph Laplacian (weighted mean − value)/t converges to Δ. "
         "Check on 20 000 points of S² with f = z, for which Δf = −2f: the fitted ratio should be close to 1."),
("Input",
"""pts = SpherePoints[20000]; t = 0.002; nf = Nearest[pts];
Lpc[p_] := Module[{q = nf[p, {All, 6 Sqrt[t]}], w}, w = Exp[-SquaredEuclideanDistance[p, #]/(4 t)] & /@ q;
   (w . q[[All, 3]]/Total[w] - p[[3]])/t];
s = pts[[;; ;; 200]]; lhs = Lpc /@ s; rhs = -2 s[[All, 3]];
<|"fitted ratio" -> (lhs . rhs)/(rhs . rhs), "correlation" -> Correlation[lhs, rhs]|>"""),

# ---------------------------------------------------------------- 10
("Section", "10. Further instances (statements only)"),
("Text", "• Weitzenböck on 1-forms: Δ_Hodge ω = ∇*∇ω + Ric(ω); Bochner’s theorem (Ric > 0 ⇒ b₁ = 0) follows. "
         "• Ricci flow ∂g/∂t = −2Ric: in dimension 2 with g = e^{2u}g₀ it reads ∂u/∂t = e^{−2u}Δ₀u = −K, a nonlinear heat equation. "
         "• Mean curvature flow ∂X/∂t = ΔX = −2H\U0001D427: the heat equation for the embedding. "
         "• Ollivier curvature on a manifold: for nearby x, y along v, κ ≈ ε² Ric(v,v)/(2(n+2)) for balls of radius ε — Ricci curvature measured by comparing ball means. "
         "• Yamabe / prescribed scalar curvature: for g̃ = u^{4/(n−2)}g, −(4(n−1)/(n−2))Δu + Su = S̃u^{(n+2)/(n−2)}."),
("Text", "© 2026 Computational Classnotes · CC BY-NC-SA 4.0"),
]
