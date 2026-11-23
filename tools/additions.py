# Geometric graphics and worked examples, inserted into CELLS by build.py.
# ADD[n] = cells appended at the end of notebook Section n (before Section n+1).

ADD = {}

# ---------------------------------------------------------------- 1: toolkit extras
ADD[1] = [
("Subsection", "1.1 Curvatures of an embedded surface, and a colour scale"),
("Text", "For a parametrised surface X(u, v) in ℝ³: first fundamental form E, F, G, second fundamental form L, M, N, "
         "K = (LN − M²)/(EG − F²), H = (EN − 2FM + GL)/(2(EG − F²)). "
         "Colours below: blue = negative curvature, near-white = zero, orange = positive."),
("Input",
"""surfaceCurvatures[pos_, \U0001D4CD_] := Module[{Xu, Xv, nn, E1, F1, G1, L1, M1, N1},
  Xu = D[pos, \U0001D4CD[[1]]]; Xv = D[pos, \U0001D4CD[[2]]];
  nn = Cross[Xu, Xv]/Sqrt[Cross[Xu, Xv] . Cross[Xu, Xv]];
  {E1, F1, G1} = {Xu . Xu, Xu . Xv, Xv . Xv};
  {L1, M1, N1} = {D[pos, \U0001D4CD[[1]], \U0001D4CD[[1]]] . nn, D[pos, \U0001D4CD[[1]], \U0001D4CD[[2]]] . nn, D[pos, \U0001D4CD[[2]], \U0001D4CD[[2]]] . nn};
  <|"K" -> Simplify[(L1 N1 - M1^2)/(E1 G1 - F1^2)],
    "H" -> Simplify[(E1 N1 - 2 F1 M1 + G1 L1)/(2 (E1 G1 - F1^2))],
    "dA" -> Simplify[Sqrt[E1 G1 - F1^2]]|>];
κColour[k_, s_] := Blend[{RGBColor[0.18, 0.36, 0.78], GrayLevel[0.96], RGBColor[0.98, 0.56, 0.17]}, (1 + Clip[k/s, {-1, 1}])/2];
curvatureSurface[pos_, {u_, u0_, u1_}, {v_, v0_, v1_}, κ_, s_, label_, opts___] :=
  ParametricPlot3D[pos, {u, u0, u1}, {v, v0, v1},
   ColorFunction -> Function[{x, y, z, uu, vv}, κColour[κ /. {u -> uu, v -> vv}, s]], ColorFunctionScaling -> False,
   Mesh -> 12, MeshStyle -> GrayLevel[0.5, 0.35], Lighting -> "Neutral", Boxed -> False, Axes -> False,
   PlotPoints -> 40, PlotLabel -> Style[label, 11], opts];
κLegend[s_, name_] := BarLegend[{κColour[#, s] &, {-s, s}}, LegendLabel -> name];
surfaceCurvatures[{(2 + Cos[v]) Cos[u], (2 + Cos[v]) Sin[u], Sin[v]}, {u, v}]"""),
]

# ---------------------------------------------------------------- 2: Gauss curvature examples
ADD[2] = [
("Subsection", "2.1 Worked examples: positive, zero and negative Gauss curvature"),
("Text", "Six classical surfaces, each coloured by its Gauss curvature K. The sphere is K = 1 everywhere; the cylinder is K = 0 (it unrolls flat); "
         "the torus is positive on the outside, negative on the inside and zero on the top and bottom circles; the saddle, catenoid and pseudosphere are negatively curved, the pseudosphere with K = −1 everywhere."),
("Input",
"""surfaces = {
   {"Sphere", {Sin[v] Cos[u], Sin[v] Sin[u], Cos[v]}, {0, 2 π}, {0.01, π - 0.01}},
   {"Cylinder", {Cos[u], Sin[u], v}, {0, 2 π}, {-1, 1}},
   {"Torus (R = 2, r = 1)", {(2 + Cos[v]) Cos[u], (2 + Cos[v]) Sin[u], Sin[v]}, {0, 2 π}, {0, 2 π}},
   {"Saddle z = x² − y²", {u, v, u^2 - v^2}, {-1, 1}, {-1, 1}},
   {"Catenoid", {Cosh[v] Cos[u], Cosh[v] Sin[u], v}, {0, 2 π}, {-1.2, 1.2}},
   {"Pseudosphere", {Sech[v] Cos[u], Sech[v] Sin[u], v - Tanh[v]}, {0, 2 π}, {0.05, 3}}};
Kformulas = Table[{s[[1]], surfaceCurvatures[s[[2]], {u, v}]["K"]}, {s, surfaces}];
TableForm[Kformulas, TableHeadings -> {None, {"surface", "K(u, v)"}}]"""),
("Input",
"""Legended[GraphicsGrid[Partition[Table[With[{s = surfaces[[i]], K = Kformulas[[i, 2]]},
     curvatureSurface[s[[2]], {u, s[[3, 1]], s[[3, 2]]}, {v, s[[4, 1]], s[[4, 2]]}, K, 1, s[[1]]]], {i, 6}], 3],
   ImageSize -> 760, Spacings -> {10, 10}], κLegend[1, "K"]]"""),
("Text", "Gauss–Bonnet on the examples: ∬K dA = 2πχ. The torus (χ = 0) integrates to 0, the sphere (χ = 2) to 4π. The Liouville form of Section 2 reproduces the sphere’s K from the stereographic conformal factor."),
("Input",
"""With[{t = surfaceCurvatures[{(2 + Cos[v]) Cos[u], (2 + Cos[v]) Sin[u], Sin[v]}, {u, v}],
   s = surfaceCurvatures[{Sin[v] Cos[u], Sin[v] Sin[u], Cos[v]}, {u, v}]},
 {"torus ∬K dA" -> Integrate[Simplify[t["K"] t["dA"], 0 < v < 2 π], {u, 0, 2 π}, {v, 0, 2 π}],
  "sphere ∬K dA" -> Integrate[Simplify[s["K"] s["dA"], 0 < v < π], {u, 0, 2 π}, {v, 0, π}]}]"""),
]

# ---------------------------------------------------------------- 3: mean curvature examples
ADD[3] = [
("Subsection", "3.1 Worked examples: the mean-curvature vector drawn"),
("Text", "Left: the torus coloured by H, with −ΔX drawn as arrows (ΔX itself points into the tube). The arrows are normal to the surface, longest on the outer equator where H = 2/3, and vanish on the inner equator where H = 0. "
         "Right: the catenoid and the helicoid are minimal surfaces (H = 0): their coordinate functions are harmonic, so ΔX vanishes and no arrows appear."),
("Input",
"""torusPos = {(2 + Cos[v]) Cos[u], (2 + Cos[v]) Sin[u], Sin[v]};
gT = Simplify[Table[D[torusPos, {u, v}[[i]]] . D[torusPos, {u, v}[[j]]], {i, 2}, {j, 2}]];
ΔXtorus = Simplify[laplaceBeltrami[gT, {u, v}] /@ torusPos];
Htorus = Simplify[-surfaceCurvatures[torusPos, {u, v}]["H"], v ∈ Reals];   (* outward normal *)
arrows = Table[With[{p = torusPos /. {u -> a, v -> b}, w = ΔXtorus /. {u -> a, v -> b}}, Arrow[{p, p - 0.3 w}]],
   {a, 0, 2 π - 0.01, 2 π/16}, {b, 0, 2 π - 0.01, 2 π/8}];
torusPlot = Show[curvatureSurface[torusPos, {u, 0, 2 π}, {v, 0, 2 π}, Htorus, 0.7, "Torus: colour = H, arrows = −ΔX = 2H n"],
   Graphics3D[{Darker[Gray], Arrowheads[0.012], Flatten[arrows]}]];
minimal = {curvatureSurface[{Cosh[v] Cos[u], Cosh[v] Sin[u], v}, {u, 0, 2 π}, {v, -1.2, 1.2},
    surfaceCurvatures[{Cosh[v] Cos[u], Cosh[v] Sin[u], v}, {u, v}]["H"], 0.7, "Catenoid: H = 0"],
   curvatureSurface[{v Cos[u], v Sin[u], u/2}, {u, 0, 2 π}, {v, -1.5, 1.5},
    surfaceCurvatures[{v Cos[u], v Sin[u], u/2}, {u, v}]["H"], 0.7, "Helicoid: H = 0", ViewPoint -> {2.5, -1.5, 1}]};
{Htorus, Legended[GraphicsRow[Prepend[minimal, torusPlot], ImageSize -> 760], κLegend[0.7, "H"]]}"""),
]

# ---------------------------------------------------------------- 4: mean values pictured
ADD[4] = [
("Subsection", "4.1 Pictures: geodesic circles, and where the flat formula fails"),
("Text", "Left: the test function on S² with geodesic circles about the north pole at r = 0.3, 0.6, …, 1.5. "
         "Right: the error of three approximations to the exact circle mean, on log–log axes. The flat-space formula (K = 0) misses the KΔf/96 term, so its error falls only like r⁴. "
         "Adding that term makes the error fall like r⁶, and adding the r⁶ terms makes it fall like r⁸: the curvature terms are exactly the right ones."),
("Input",
"""exactMean[r0_] := NIntegrate[F0[{Sin[r0] Cos[φ], Sin[r0] Sin[φ], Cos[r0]}], {φ, 0, 2 π}, WorkingPrecision -> 40, PrecisionGoal -> 30]/(2 π);
{p0, d1, d2, d3} = atPole /@ {ext, L1, L2, L3};
flat4[r_] := p0 + r^2/4 d1 + r^4 d2/64;
curved4[r_] := flat4[r] + r^4 d1/96;
curved6[r_] := curved4[r] + r^6 (d3/2304 + d2/1152 + d1/1440);
rs = Table[2^-k, {k, 1, 6, 1/4}];
errs = Table[With[{ex = exactMean[r]}, {Abs[ex - flat4[r]], Abs[ex - curved4[r]], Abs[ex - curved6[r]]}], {r, rs}];
sphereView = Show[SphericalPlot3D[1, {θ, 0, π}, {φ, 0, 2 π}, Mesh -> None, PlotPoints -> 50,
    ColorFunction -> Function[{x, y, z}, ColorData["SunsetColors"][Rescale[F0[{x, y, z}], {0, 12}]]], ColorFunctionScaling -> False],
   Graphics3D[{Thick, RGBColor[0.18, 0.36, 0.78], Table[Line[Table[1.005 {Sin[r] Cos[φ], Sin[r] Sin[φ], Cos[r]}, {φ, 0, 2 π, π/60}]], {r, 0.3, 1.5, 0.3}],
     Black, PointSize[0.02], Point[{0, 0, 1.01}]}], Boxed -> False, Axes -> False, ViewPoint -> {2, -1.5, 1.5},
   PlotLabel -> "Geodesic circles about the pole", ImageSize -> 300];
slopes = Table[D[Fit[Log[Transpose[{rs, errs[[All, k]]}]][[-12 ;;]], {1, x}, x], x], {k, 3}];
errPlot = ListLogLogPlot[Table[Transpose[{rs, errs[[All, k]]}], {k, 3}], Joined -> True, PlotMarkers -> Automatic,
   PlotStyle -> {Gray, RGBColor[0.98, 0.56, 0.17], RGBColor[0.18, 0.36, 0.78]},
   PlotLegends -> {"flat formula (K = 0)", "+ KΔf/96 at r^4", "+ r^6 curvature terms"},
   AxesLabel -> {"r", "|error|"}, PlotLabel -> Row[{"error slopes ≈ ", NumberForm[N[slopes], 3]}], ImageSize -> 440];
Row[{sphereView, errPlot}]"""),
("Text", "Area of a geodesic disc divided by the flat value πr², for K = 1 (sphere), 0 (plane) and −1 (hyperbolic plane). Positive curvature makes discs smaller than flat ones, negative curvature larger: the −Kr²/12 term."),
("Input",
"""Plot[{2 (1 - Cos[r])/r^2, 1, 2 (Cosh[r] - 1)/r^2}, {r, 0.01, 2.5},
 PlotStyle -> {RGBColor[0.98, 0.56, 0.17], Gray, RGBColor[0.18, 0.36, 0.78]},
 PlotLegends -> {"K = 1", "K = 0", "K = −1"}, AxesLabel -> {"r", "A(r)/πr²"},
 PlotLabel -> "Geodesic discs: A(r)/πr² = 1 − Kr²/12 + …", ImageSize -> 420]"""),
]

# ---------------------------------------------------------------- 5: heat trace pictured
ADD[5] = [
("Subsection", "5.1 Two drums with the same area: the sphere and the flat torus"),
("Text", "Normalise the heat trace by its leading Weyl term, Area/(4πt). For the unit sphere (K = 1) the ratio rises like 1 + t/3: the slope is ∫S/(6·Area) = 1/3. "
         "For the flat square torus of the same area (K = 0) the ratio stays at 1 for small t. The first correction to Weyl’s law hears the curvature."),
("Input",
"""L0 = 2 Sqrt[π];   (* flat torus side, so area = 4π like the unit sphere *)
torusTrace[t_?NumericQ] := EllipticTheta[3, 0, Exp[-(2 π/L0)^2 t]]^2;
ratio[tr_, t_] := tr[t]/((4 π)/(4 π t));
Plot[{ratio[heatTrace, t], 1 + t/3 + t^2/15, ratio[torusTrace, t]}, {t, 0.005, 0.4},
 PlotStyle -> {{RGBColor[0.98, 0.56, 0.17], Thick}, {Black, Dashed}, {RGBColor[0.18, 0.36, 0.78], Thick}},
 PlotLegends -> {"sphere S²", "1 + t/3 + t²/15", "flat torus, same area"},
 AxesLabel -> {"t", "Tr e^{tΔ} ÷ (Area/4πt)"}, PlotLabel -> "Curvature is the first correction to Weyl’s law", ImageSize -> 460]"""),
]

# ---------------------------------------------------------------- 6: comparison pictured + Bochner on the torus
ADD[6] = [
("Subsection", "6.1 Worked example: Bochner on a surface whose curvature changes sign"),
("Text", "On the torus Ric = K g with K = cos v/(2 + cos v), which is positive outside and negative inside. The Bochner identity still holds pointwise, with that variable K."),
("Input",
"""gTor = {{(2 + Cos[v])^2, 0}, {0, 1}}; \U0001D4CDT = {u, v}; Ktor = Cos[v]/(2 + Cos[v]);
ΔT = laplaceBeltrami[gTor, \U0001D4CDT]; FT = \U0001D4BB[u, v];
Simplify[1/2 ΔT[gradNorm2[gTor, \U0001D4CDT][FT]] - (hessNorm2[gTor, \U0001D4CDT][FT] +
    Sum[Inverse[gTor][[i, j]] D[FT, \U0001D4CDT[[i]]] D[ΔT[FT], \U0001D4CDT[[j]]], {i, 2}, {j, 2}] + Ktor gradNorm2[gTor, \U0001D4CDT][FT])]"""),
("Subsection", "6.2 Laplacian comparison pictured"),
("Text", "Δr is the geodesic curvature of the circle of radius r: cot r for K = 1, 1/r for K = 0, coth r for K = −1. A lower bound on curvature caps it from above (Laplacian comparison), and integrating it gives Bishop–Gromov: circumference/2πr = sin r/r, 1, sinh r/r."),
("Input",
"""Row[{
  Plot[{Cot[r], 1/r, Coth[r]}, {r, 0.05, 3}, PlotRange -> {-2, 4},
   PlotStyle -> {RGBColor[0.98, 0.56, 0.17], Gray, RGBColor[0.18, 0.36, 0.78]},
   PlotLegends -> {"K = 1: cot r", "K = 0: 1/r", "K = −1: coth r"}, AxesLabel -> {"r", "Δr"}, PlotLabel -> "Δr = curvature of geodesic circles", ImageSize -> 400],
  Plot[{Sin[r]/r, 1, Sinh[r]/r}, {r, 0.01, 3},
   PlotStyle -> {RGBColor[0.98, 0.56, 0.17], Gray, RGBColor[0.18, 0.36, 0.78]},
   PlotLegends -> {"K = 1", "K = 0", "K = −1"}, AxesLabel -> {"r", "length/2πr"}, PlotLabel -> "Bishop–Gromov: circle length vs flat", ImageSize -> 320]}]"""),
("Text", "Lichnerowicz pictured: the first nonzero eigenvalue of S² is 2 = nk, attained by the coordinate functions. The eigenfunction Y₁⁰ = z is drawn on the sphere."),
("Input",
"""SphericalPlot3D[1, {θ, 0, π}, {φ, 0, 2 π}, Mesh -> None, PlotPoints -> 40,
 ColorFunction -> Function[{x, y, z}, κColour[z, 1]], ColorFunctionScaling -> False, Boxed -> False, Axes -> False, Lighting -> "Neutral",
 PlotLabel -> "λ1(S²) = 2: eigenfunction z (Lichnerowicz equality)", ImageSize -> 300]"""),
]

# ---------------------------------------------------------------- 7: torus mesh
ADD[7] = [
("Subsection", "7.1 Worked example: a torus mesh, where Gauss–Bonnet gives zero"),
("Text", "A 40 × 20 triangulated torus. The angle defect is positive on the outer half and negative on the inner half; its total is exactly 0 = 2πχ(torus). "
         "Divided by the vertex area it approximates the smooth K = cos v/(2 + cos v), and the cotangent Laplacian of the positions approximates −2H\U0001D427."),
("Input",
"""meshCurvature[P_, T_] := Module[{nv = Length[P], ang, def, Wm, Am},
  ang[i_, j_, k_] := VectorAngle[P[[j]] - P[[i]], P[[k]] - P[[i]]];
  def = ConstantArray[2. π, nv]; Wm = SparseArray[{}, {nv, nv}, 0.]; Am = ConstantArray[0., nv];
  Do[Module[{a, b, c}, {a, b, c} = tri;
    def[[a]] -= ang[a, b, c]; def[[b]] -= ang[b, c, a]; def[[c]] -= ang[c, a, b];
    Wm[[b, c]] += Cot[ang[a, b, c]]/2; Wm[[c, b]] += Cot[ang[a, b, c]]/2;
    Wm[[c, a]] += Cot[ang[b, c, a]]/2; Wm[[a, c]] += Cot[ang[b, c, a]]/2;
    Wm[[a, b]] += Cot[ang[c, a, b]]/2; Wm[[b, a]] += Cot[ang[c, a, b]]/2;
    Am[[{a, b, c}]] += Norm[Cross[P[[b]] - P[[a]], P[[c]] - P[[a]]]]/6], {tri, T}];
  <|"defect" -> def, "area" -> Am, "ΔX" -> ((Wm - DiagonalMatrix[Total[Wm]]) . P)/Am|>];
{nu, nvv} = {40, 20}; idx[i_, j_] := Mod[i, nu] nvv + Mod[j, nvv] + 1;
PT = Flatten[Table[N[torusPos /. {u -> 2 π i/nu, v -> 2 π j/nvv}], {i, 0, nu - 1}, {j, 0, nvv - 1}], 1];
TT = Flatten[Table[{{idx[i, j], idx[i + 1, j], idx[i + 1, j + 1]}, {idx[i, j], idx[i + 1, j + 1], idx[i, j + 1]}}, {i, 0, nu - 1}, {j, 0, nvv - 1}], 2];
mt = meshCurvature[PT, TT];
Kmesh = mt["defect"]/mt["area"];
Ksmooth = Flatten[Table[N[Cos[2 π j/nvv]/(2 + Cos[2 π j/nvv])], {i, 0, nu - 1}, {j, 0, nvv - 1}]];
<|"Σ defect" -> Chop[Total[mt["defect"]], 10^-9], "max |K_mesh − K|" -> Max[Abs[Kmesh - Ksmooth]]|>"""),
("Input",
"""Legended[Row[{
   Graphics3D[{EdgeForm[GrayLevel[0.6, 0.5]], Table[{κColour[Mean[Kmesh[[t]]], 1], Polygon[PT[[t]]]}, {t, TT}]},
    Boxed -> False, Lighting -> "Neutral", PlotLabel -> "Angle defect / area ≈ K", ImageSize -> 340],
   ListPlot[{Transpose[{Flatten[Table[2 π j/nvv, {i, 0, nu - 1}, {j, 0, nvv - 1}]], Kmesh}],
     Table[{s, Cos[s]/(2 + Cos[s])}, {s, 0, 2 π, 0.05}]}, Joined -> {False, True},
    PlotStyle -> {RGBColor[0.98, 0.56, 0.17], Black}, AxesLabel -> {"v", "K"},
    PlotLegends -> {"mesh: defect/area", "smooth K"}, PlotLabel -> "Mesh vs smooth Gauss curvature", ImageSize -> 420]}],
 κLegend[1, "K"]]"""),
]

# ---------------------------------------------------------------- 8: graph pictures and examples
ADD[8] = [
("Subsection", "8.6 Pictures: graphs coloured by their curvature"),
("Text", "One drawing helper, then each curvature on a family of examples. The family: a binary tree (very negative), the 6-cycle (flat), the 3-cube, the complete graph K₅ (positive), the Petersen graph, the 5×5 grid with boundary, and a dumbbell (two K₅ joined by a path), whose bridge is a bottleneck. "
         "Edge curvatures colour the edges; vertex curvatures colour the vertices. Blue = negative, orange = positive."),
("Input",
"""dumbbell = Graph[UndirectedEdge @@@ Join[List @@@ EdgeList[CompleteGraph[5]], (List @@@ EdgeList[CompleteGraph[5]]) + 7, {{5, 6}, {6, 7}, {7, 8}}]];
family = <|"Binary tree" -> KaryTree[15, 2], "Cycle C6" -> CycleGraph[6], "Cube Q3" -> HypercubeGraph[3],
   "Complete K5" -> CompleteGraph[5], "Petersen" -> PetersenGraph[], "Grid 5×5" -> GridGraph[{5, 5}], "Dumbbell" -> dumbbell|>;
edgeCurvaturePlot[G_, κf_, s_, label_] := Module[{e = edges[G], k},
  k = AssociationThread[e -> (κf[G, #] & /@ e)];
  Graph[G, EdgeStyle -> Table[UndirectedEdge @@ ed -> Directive[AbsoluteThickness[4], κColour[k[ed], s]], {ed, e}],
   VertexStyle -> GrayLevel[0.35], VertexSize -> {"Scaled", 0.025}, PlotLabel -> Style[label, 10], ImageSize -> 180]];
vertexCurvaturePlot[G_, kv_List, s_, label_] := Graph[G,
  VertexStyle -> Thread[VertexList[G] -> (κColour[#, s] & /@ kv)], VertexSize -> {"Scaled", 0.05},
  EdgeStyle -> GrayLevel[0.6], PlotLabel -> Style[label, 10], ImageSize -> 180];
row[plots_] := GraphicsRow[plots, ImageSize -> 1100, Spacings -> 0];
Keys[family]"""),
("Text", "Lin–Lu–Yau curvature on every edge. In the binary tree, interior edges are −2/3 (the two neighbourhoods do not overlap) while leaf edges are +2/3 (a leaf sees only its parent). The cycle and the Petersen graph are 0, the cube is 2/3 everywhere and K₅ is 5/4. The grid is 0 inside and positive along the boundary. The dumbbell’s bridge is negative (−3/5) while its cliques are positive: the bottleneck shows up as negative curvature."),
("Input",
"""Legended[row[KeyValueMap[Function[{nm, G}, edgeCurvaturePlot[G, κLLY, 1.25, nm]], family]], κLegend[1.25, "κ_LLY"]]"""),
("Input",
"""Dataset[Map[Function[G, With[{k = κLLY[G, #] & /@ edges[G]}, <|"min" -> Min[k], "max" -> Max[k], "mean" -> N[Mean[k]]|>]], family]]"""),
("Text", "What Ollivier’s curvature measures, on one edge: the walk measures μ_x and μ_y spread mass over the two neighbourhoods. Shared neighbours (purple, the triangles) let mass stay put, which is why K₅ is positive. Across an interior tree edge the neighbourhoods do not overlap, mass must travel up to 3 steps, and κ is negative."),
("Input",
"""edgePicture[G_, {x_, y_}, label_] := Graph[G,
  VertexStyle -> Join[Thread[Union[nbr[G, x], nbr[G, y]] -> RGBColor[0.98, 0.56, 0.17]],
    Thread[Intersection[nbr[G, x], nbr[G, y]] -> RGBColor[0.55, 0.3, 0.75]], {x -> Black, y -> Black}],
  EdgeStyle -> {UndirectedEdge[x, y] -> Directive[Black, AbsoluteThickness[4]]}, VertexSize -> {"Scaled", 0.05},
  PlotLabel -> Style[Row[{label, ":  κ_LLY(x,y) = ", κLLY[G, {x, y}], ",  κ₀ = ", κOllivier[G, {x, y}, 0]}], 10], ImageSize -> 260];
GraphicsRow[{edgePicture[KaryTree[15, 2], {2, 4}, "tree, interior edge"], edgePicture[HypercubeGraph[3], {1, 2}, "cube"],
  edgePicture[CompleteGraph[5], {1, 2}, "K5 (purple = shared)"]}, ImageSize -> 780]"""),
("Text", "Bakry–Émery curvature K∞ at every vertex (the discrete Bochner inequality). Tree vertices with children are negative and leaves positive; the cycle is exactly 0; the cube is 2/3, K₅ is 7/8 and Petersen is −1/3 at every vertex; on the dumbbell the bridge vertices are negative."),
("Input",
"""Legended[row[KeyValueMap[Function[{nm, G}, vertexCurvaturePlot[G, bakryEmery[G, #] & /@ VertexList[G], 1, nm]], family]], κLegend[1, "K_BE"]]"""),
("Text", "Forman curvature (augmented with triangles) on every edge. It is purely combinatorial, so it is very negative wherever degrees are high and triangles are few."),
("Input",
"""Legended[row[KeyValueMap[Function[{nm, G}, edgeCurvaturePlot[G, formanAug, 6, nm]], family]], κLegend[6, "Forman"]]"""),
("Text", "Resistance curvature p at every vertex. The totals are always 1, a discrete Gauss–Bonnet theorem; the dumbbell’s bridge vertices carry the negative curvature."),
("Input",
"""{Legended[row[KeyValueMap[Function[{nm, G}, vertexCurvaturePlot[G, pNode[G], 0.3, nm]], family]], κLegend[0.3, "p"]],
 Map[Chop@Total[pNode[#]] &, family]}"""),
("Text", "Steinerberger curvature at every vertex. It is built from graph distance where resistance curvature uses effective resistance. On a tree the two distances coincide, so the two curvatures are exactly proportional; on the grid they are strongly correlated; on vertex-transitive graphs (cycle, cube, K₅, Petersen) both are constant."),
("Input",
"""{Legended[row[KeyValueMap[Function[{nm, G}, vertexCurvaturePlot[G, steinerberger[G], 1.5, nm]], family]], κLegend[1.5, "K_S"]],
 "correlation with resistance curvature" -> Map[Quiet@Correlation[steinerberger[#], pNode[#]] &, KeyTake[family, {"Binary tree", "Grid 5×5", "Dumbbell"}]]}"""),
("Text", "Combinatorial (Higuchi) curvature drawn on polyhedra: every vertex of a Platonic solid carries the same positive share, and the shares add to χ = 2."),
("Input",
"""higuchiVertex[name_] := Module[{F = PolyhedronData[name, "FaceIndices"], nv = Length[PolyhedronData[name, "VertexCoordinates"]]},
   Table[1 - Count[F, _?(MemberQ[#, v] &)]/2 + Total[1/Length[#] & /@ Select[F, MemberQ[#, v] &]], {v, nv}]];
GraphicsRow[Table[Show[PolyhedronData[p], PlotLabel -> Style[Row[{p, ": ", First[higuchiVertex[p]], " × ", Length[higuchiVertex[p]], " = 2"}], 9]],
   {p, {"Tetrahedron", "Cube", "Octahedron", "Dodecahedron", "Icosahedron"}}], ImageSize -> 900]"""),
]

# ---------------------------------------------------------------- 9: spectral bounds pictured
ADD[9] = [
("Subsection", "9.1 Pictures: curvature lower bounds under the spectral gap"),
("Text", "For each graph, λ₁ of the normalised Laplacian against the two curvature lower bounds. Every bar of κ_LLY and K_BE sits at or below λ₁; K₅ and Q₃ touch it, the discrete equality cases."),
("Input",
"""bounds = Map[Function[G, {spec[G][[2]], Max[0, Min[κLLY[G, #] & /@ edges[G]]], Max[0, Min[bakryEmery[G, #] & /@ VertexList[G]]]}], graphs];
BarChart[Values[bounds], ChartLabels -> {Keys[bounds], None}, ChartStyle -> {Black, RGBColor[0.98, 0.56, 0.17], RGBColor[0.18, 0.36, 0.78]},
 ChartLegends -> {"λ₁", "max(0, κ_LLY)", "max(0, K_BE)"}, PlotLabel -> "λ₁ ≥ κ and λ₁ ≥ K", ImageSize -> 520]"""),
("Text", "The point-cloud Laplacian of f = z against the exact Δz = −2z at the sampled points: they lie on the diagonal."),
("Input",
"""ListPlot[Transpose[{rhs, lhs}], AspectRatio -> 1, PlotStyle -> RGBColor[0.98, 0.56, 0.17],
 Epilog -> {Gray, Dashed, Line[{{-2, -2}, {2, 2}}]}, AxesLabel -> {"Δz = −2z", "point-cloud L z"},
 PlotLabel -> "Belkin–Niyogi on 20 000 points of S²", ImageSize -> 320]"""),
]
