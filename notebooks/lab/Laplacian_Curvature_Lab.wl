(* ::Package:: *)

(* Laplacian Curvature Lab — the notebook behind the page *)
(* © 2026 Computational Classnotes · CC BY-NC-SA 4.0 *)

(* ::Title:: *)
(*Laplacian Curvature Lab — the mathematics behind every section*)

(* ::Text:: *)
(*Curvature from the Laplacian, section by section: statements, worked by hand, checked on the kernel, drawn and animated*)

(* ::Text:: *)
(*© 2026 Computational Classnotes · CC BY-NC-SA 4.0*)

(* ::Text:: *)
(*This notebook follows the Laplacian Curvature Lab (https://lossofgenerality.github.io/laplacian/lab/Laplacian_Curvature_Lab.html) section by section. Each section states the mathematics, works its main example by hand, checks every claim on the kernel, and redraws the section’s pictures with an animator for its interactive parts. How the page itself computes, and every comparison between the page’s numbers and Wolfram’s, is gathered at the end under Production Notes.*)

(* ::Text:: *)
(*Conventions. Δ is the Laplace–Beltrami operator, negative semidefinite (Δ = ∂²/∂x² + ∂²/∂y² in the plane). On a graph, Δf(v) is the mean of f over the neighbours of v minus f(v): the normalised Laplacian, with the same sign. Evaluate from the top; the first cell clears the session.*)

(* ::Section:: *)
(*0. Toolkit*)

ClearAll["Global`*"];  (* start from a clean kernel *)
(* the colour scale used throughout: blue negative, near-white zero, CCN orange positive, saturating at ±s *)
kcol[k_?NumericQ, s_] := With[{w = Clip[k/s, {-1, 1}]}, Blend[{RGBColor[0.10, 0.27, 0.75], GrayLevel[0.97], RGBColor[0.96, 0.47, 0.02]}, (1 + Sign[w] Abs[w]^0.55)/2]];
kLegend[s_, label_] := BarLegend[{kcol[#, s] &, {-s, s}}, LegendLabel -> label];
orange = RGBColor[0.96, 0.47, 0.02]; blue = RGBColor[0.10, 0.27, 0.75];
(* a plain table: header row, then rows; numbers to seven figures *)
valGrid[head_, rows_] := Grid[Prepend[Map[If[NumericQ[#] && ! IntegerQ[#], NumberForm[N[#], 7], #] &, rows, {2}], Style[#, Bold] & /@ head],
   Frame -> All, Alignment -> Left, Background -> {None, {1 -> GrayLevel[0.93]}}, FrameStyle -> GrayLevel[0.75]];

(* ::Section:: *)
(*1. Gauss and mean curvature on six surfaces*)

(* ::Text:: *)
(*For a parametrised surface X(u, v) with first fundamental form E, F, G and second fundamental form L, M, N:*)

(* ::Text:: *)
(*K = (LN − M²)/(EG − F²),    H = (EN − 2FM + GL)/(2(EG − F²)),    dA = √(EG − F²) du dv.*)

(* ::Text:: *)
(*Gauss–Bonnet: on a closed surface ∬K dA = 2πχ, so 4π on the sphere and 0 on the torus. On the torus K is positive on the outer half, negative on the inner half and zero on the top and bottom circles.*)

(* ::Subsection:: *)
(*1.1 Worked by hand*)

(* ::Text:: *)
(*Take X(u, v) = ((2 + cos v) cos u, (2 + cos v) sin u, sin v). Then \!\(\*SubscriptBox[\(X\), \(u\)]\) = (2 + cos v)(−sin u, cos u, 0) and \!\(\*SubscriptBox[\(X\), \(v\)]\) = (−sin v cos u, −sin v sin u, cos v), so E = \!\(\*SubscriptBox[\(X\), \(u\)]\)·\!\(\*SubscriptBox[\(X\), \(u\)]\) = (2 + cos v)², F = \!\(\*SubscriptBox[\(X\), \(u\)]\)·\!\(\*SubscriptBox[\(X\), \(v\)]\) = 0, G = \!\(\*SubscriptBox[\(X\), \(v\)]\)·\!\(\*SubscriptBox[\(X\), \(v\)]\) = 1, and dA = √(EG − F²) du dv = (2 + cos v) du dv.*)

(* ::Text:: *)
(*The unit normal is n = \!\(\*SubscriptBox[\(X\), \(u\)]\) × X_v/|X_u × \!\(\*SubscriptBox[\(X\), \(v\)]\)| = (cos v cos u, cos v sin u, sin v), pointing out of the tube. Second derivatives: \!\(\*SubscriptBox[\(X\), \(uu\)]\) = −(2 + cos v)(cos u, sin u, 0), \!\(\*SubscriptBox[\(X\), \(uv\)]\) = sin v (sin u, −cos u, 0), \!\(\*SubscriptBox[\(X\), \(vv\)]\) = −(cos v cos u, cos v sin u, sin v). So L = \!\(\*SubscriptBox[\(X\), \(uu\)]\)·n = −(2 + cos v) cos v, M = \!\(\*SubscriptBox[\(X\), \(uv\)]\)·n = 0, N = \!\(\*SubscriptBox[\(X\), \(vv\)]\)·n = −1.*)

(* ::Text:: *)
(*Gauss curvature: K = (LN − M²)/(EG − F²) = (2 + cos v) cos v/(2 + cos v)² = cos v/(2 + cos v). Mean curvature: H = (EN − 2FM + GL)/(2(EG − F²)) = (−(2 + cos v)² − (2 + cos v) cos v)/(2(2 + cos v)²) = −(1 + cos v)/(2 + cos v). (The sign of H follows the outward normal.)*)

(* ::Text:: *)
(*Readings: on the outer equator v = 0, K = 1/3 and |H| = 2/3; on the inner equator v = π, K = 1/(−1)… that is cos π/(2 + cos π) = −1, and H = 0; on the top and bottom circles v = ±π/2, K = 0. These are the torus’s max K = 0.3333, min K = −1.0000 and max |H| = 0.6667 in the table of §1.2. Total: ∬K dA = ∫₀^{2π}∫₀^{2π} [cos v/(2 + cos v)](2 + cos v) dv du = 2π ∫₀^{2π} cos v dv = 0 = 2πχ(torus).*)

(* ::Text:: *)
(*How the other five follow: the sphere gives K = 1 everywhere, so ∬K dA over 0.02 ≤ v ≤ π − 0.02 is 2π ∫ sin v dv = 4π cos 0.02 = 12.5639; the cylinder has L = −1, N = 0, so K = 0 and |H| = 1/2; the catenoid is minimal (H = 0) with K = −1/cosh⁴v; the pseudosphere has K = −1. The table in §1.2 is these formulas evaluated on the grid.*)

(* ::Subsection:: *)
(*1.2 Checks on the kernel*)

(* ::Subsubsection:: *)
(*The Lab’s Wolfram cell*)

(* ::Text:: *)
(*Gauss and mean curvature, and Gauss–Bonnet on the torus:*)

(* Gauss and mean curvature of an embedded surface, and Gauss–Bonnet on the torus *)
surfaceCurvatures[pos_, \[ScriptX]_] := Module[{Xu, Xv, nn, E1, F1, G1, L1, M1, N1},
  Xu = D[pos, \[ScriptX][[1]]]; Xv = D[pos, \[ScriptX][[2]]]; nn = Cross[Xu, Xv]/Sqrt[Cross[Xu, Xv] . Cross[Xu, Xv]];
  {E1, F1, G1} = {Xu . Xu, Xu . Xv, Xv . Xv};
  {L1, M1, N1} = {D[pos, \[ScriptX][[1]], \[ScriptX][[1]]] . nn, D[pos, \[ScriptX][[1]], \[ScriptX][[2]]] . nn, D[pos, \[ScriptX][[2]], \[ScriptX][[2]]] . nn};
  <|"K" -> Simplify[(L1 N1 - M1^2)/(E1 G1 - F1^2)], "H" -> Simplify[(E1 N1 - 2 F1 M1 + G1 L1)/(2 (E1 G1 - F1^2))], "dA" -> Simplify[Sqrt[E1 G1 - F1^2]]|>];
torus = surfaceCurvatures[{(2 + Cos[v]) Cos[u], (2 + Cos[v]) Sin[u], Sin[v]}, {u, v}];
{torus["K"], Integrate[Simplify[torus["K"] torus["dA"], 0 < v < 2 π], {u, 0, 2 π}, {v, 0, 2 π}]}

(* ::Text:: *)
(*Expected: K = cos v/(2 + cos v) and total 0.*)

(* ::Subsubsection:: *)
(*All six surfaces*)

(* ::Text:: *)
(*The six surfaces with their drawn parameter domains: K and H symbolically, their range on a 57 × 37 grid, and ∬K dA by NIntegrate. The sphere is drawn for 0.02 ≤ v ≤ π − 0.02, so its total there is 4π cos 0.02 = 12.5639; the saddle, catenoid and pseudosphere are open patches, whose totals depend on the patch.*)

surf = <|"sphere" -> {{Sin[v] Cos[u], Sin[v] Sin[u], Cos[v]}, {0, 2 π}, {0.02, π - 0.02}},
   "cylinder" -> {{Cos[u], Sin[u], v}, {0, 2 π}, {-1, 1}},
   "torus" -> {{(2 + Cos[v]) Cos[u], (2 + Cos[v]) Sin[u], Sin[v]}, {0, 2 π}, {0, 2 π}},
   "saddle" -> {{u, v, u^2 - v^2}, {-1, 1}, {-1, 1}},
   "catenoid" -> {{Cosh[v] Cos[u], Cosh[v] Sin[u], v}, {0, 2 π}, {-1.2, 1.2}},
   "pseudosphere" -> {{Cos[u]/Cosh[v], Sin[u]/Cosh[v], v - Tanh[v]}, {0, 2 π}, {0.08, 3}}|>;
surfData[key_] := Module[{X, U, V, c, g, Ks, Hs},
   {X, U, V} = surf[key]; c = surfaceCurvatures[X, {u, v}];
   g = N@Flatten[Table[{U[[1]] + (U[[2]] - U[[1]]) i/56, V[[1]] + (V[[2]] - V[[1]]) j/36}, {i, 0, 56}, {j, 0, 36}], 1];
   Ks = (c["K"] /. {u -> #[[1]], v -> #[[2]]}) & /@ g; Hs = (Abs[c["H"]] /. {u -> #[[1]], v -> #[[2]]}) & /@ g;
   <|"kmin" -> Min[Ks], "kmax" -> Max[Ks], "hmax" -> Max[Hs],
     "total" -> Chop[Quiet[NIntegrate[c["K"] c["dA"], {u, U[[1]], U[[2]]}, {v, V[[1]], V[[2]]}, PrecisionGoal -> 10, AccuracyGoal -> 12]], 10^-12]|>];
surfVals = AssociationMap[surfData, Keys[surf]];
valGrid[{"surface", "min K", "max K", "max |H|", "∬ K dA"}, KeyValueMap[{#1, #2["kmin"], #2["kmax"], #2["hmax"], #2["total"]} &, surfVals]]

torusK = Simplify[surfaceCurvatures[surf["torus"][[1]], {u, v}]["K"]];
{torusK, Reduce[torusK > 0 && 0 <= v < 2 π, v], Solve[torusK == 0 && 0 <= v < 2 π, v]}

(* ::Text:: *)
(*K > 0 exactly where cos v > 0, and K = 0 on the circles v = π/2 and 3π/2.*)

(* ::Subsection:: *)
(*1.3 Figures and animator*)

surfPlot[key_, q_] := Module[{X, U, V, c, f},
   {X, U, V} = surf[key]; c = surfaceCurvatures[X, {u, v}]; f = If[q == "K", c["K"], Abs[c["H"]]];
   ParametricPlot3D[X, {u, U[[1]], U[[2]]}, {v, V[[1]], V[[2]]}, ColorFunction -> Function[{x, y, z, uu, vv}, kcol[f /. {u -> uu, v -> vv}, 1]],
    ColorFunctionScaling -> False, Mesh -> None, PlotPoints -> 40, Boxed -> False, Axes -> False, Lighting -> "Neutral", PlotLabel -> key, ImageSize -> 230]];
Legended[Grid[Partition[surfPlot[#, "K"] & /@ Keys[surf], 3]], kLegend[1, "K"]]

(* ::Text:: *)
(*Fig. 1. The six surfaces coloured by Gauss curvature K: blue negative, near-white zero, orange positive, saturating at  K  = 1. The torus is orange outside and blue inside; the catenoid and pseudosphere are blue throughout.*)

(* ::Text:: *)
(*The animator: pick the surface and the quantity, and drag the picture to turn it.*)

With[{surfaces = Keys[surf]},
 Manipulate[Legended[surfPlot[mSurf, mQ], kLegend[1, If[mQ == "K", "K", "|H|"]]],
  {{mSurf, "torus", "surface"}, surfaces}, {{mQ, "K", "colour by"}, {"K" -> "Gauss curvature K", "H" -> "mean curvature |H|"}}, SaveDefinitions -> True]]

(* ::Section:: *)
(*2. Ricci flow is a heat equation for the conformal factor*)

(* ::Text:: *)
(*On a surface Ric = K g, so Ricci flow ∂g/∂t = −2 Ric becomes ∂g/∂t = −2K g. With g = e^{2u}(dx² + dy²) and Liouville’s formula for K:*)

(* ::Text:: *)
(*K = −e^{−2u} Δ₀u,        ∂u/∂t = −K = e^{−2u} Δ₀u.*)

(* ::Text:: *)
(*On the flat torus a bumpy metric is ironed out and ∬K dA stays 0. Ricci flow as a heat equation, with the maximum principle, energy and entropy, and reaction against diffusion, is the subject of its own notebook: Ricci Flow and the Curvature–Laplacian Relations (series notebook 14).*)

(* ::Subsection:: *)
(*2.1 Worked by hand*)

(* ::Text:: *)
(*Stereographic sphere. With u = log(2/(1 + r²)), r² = x² + y², write u = log 2 − log(1 + r²). For a radial function the flat Laplacian is Δ₀ = d²/dr² + (1/r) d/dr, and for log(1 + r²) it gives 2(1 − r²)/(1 + r²)² + 2/(1 + r²) = 4/(1 + r²)². So Δ₀u = −4/(1 + r²)², e^{−2u} = (1 + r²)²/4, and K = −e^{−2u}Δ₀u = 1.*)

(* ::Text:: *)
(*Half-plane. u = log(1/y) = −log y: Δ₀u = 1/y², e^{−2u} = y², K = −y²·(1/y²) = −1.*)

(* ::Text:: *)
(*Shrinking sphere. The round metric g₀ on S² has Ric = g₀. Try g(t) = c(t) g₀: Ricci curvature does not change under constant scaling, so Ric(g(t)) = g₀ and Ricci flow ∂g/∂t = −2Ric reads c′ g₀ = −2 g₀, so c = 1 − 2t: the sphere shrinks to a point at t = 1/2.*)

(* ::Text:: *)
(*Why ∬K dA stays 0 on the grid. With dA = e^{2u} dx dy, K dA = −Δ₀u dx dy, and the integral of a Laplacian over the flat torus is 0. On the 32 × 32 grid the five-point Laplacian sums to exactly 0 over a periodic grid (each value enters once with +4 and four times with −1), so the grid total is 0 to round-off, about 10⁻¹⁵.*)

(* ::Text:: *)
(*Why max|K| falls. ∂u/∂t = e^{−2u}Δ₀u is a heat equation for u; a single Fourier mode a cos x decays like e^{−t}, and K ≈ −Δ₀u for small u, so max|K| falls by about e² ≈ 7.4 between t = 0 and t = 2 for the slowest mode, and faster for the sin 2y cos(x + y) part. Here 4.63 → 0.059 is a factor 79 because the bump is not small at first (e^{−2u} amplifies the start).*)

(* ::Subsection:: *)
(*2.2 Checks on the kernel*)

(* ::Subsubsection:: *)
(*The Lab’s Wolfram cell*)

(* ::Text:: *)
(*Liouville form of K, and the shrinking sphere:*)

ClearAll[t];  (* t is a variable here *)

(* Liouville form of Gauss curvature, and the shrinking sphere under Ricci flow *)
Kconformal[w_] := Simplify[-Exp[-2 w] (D[w, {x, 2}] + D[w, {y, 2}])];
{Kconformal[Log[2/(1 + x^2 + y^2)]], Kconformal[Log[1/y]], Simplify[D[(1 - 2 t) {{1, 0}, {0, Sin[θ]^2}}, t] + 2 {{1, 0}, {0, Sin[θ]^2}}]}

(* ::Text:: *)
(*Expected {1, −1, 0}: the stereographic sphere has K = 1, the half-plane K = −1, and (1 − 2t)\!\(\*SubscriptBox[\(g\), \(S²\)]\) solves ∂g/∂t = −2 Ric = −2g.*)

(* ::Subsubsection:: *)
(*The conformal form of the flow*)

(* the conformal form: g = e^(2w) g0 and ∂g/∂t = −2 K g give ∂w/∂t = −K = e^(−2w) Δ0 w *)
Simplify[(D[Exp[2 w[x, y, t]], t] == -2 (-Exp[-2 w[x, y, t]] (D[w[x, y, t], {x, 2}] + D[w[x, y, t], {y, 2}])) Exp[2 w[x, y, t]]) /.
   Derivative[0, 0, 1][w][x, y, t] -> Exp[-2 w[x, y, t]] (D[w[x, y, t], {x, 2}] + D[w[x, y, t], {y, 2}])]

(* ::Subsubsection:: *)
(*The flow on a 32 × 32 grid*)

(* ::Text:: *)
(*A 32 × 32 periodic grid on [0, 2π)², initial u = a cos x + b sin 2y cos(x + y) with a = 0.3, b = 0.83a, the five-point Laplacian, and explicit steps dt = 0.2 h² e^{2 min u}, one at a time, until t ≥ 2.*)

ricciRun[a_, b_, N_] := Module[{h = 2. π/N, U, lap, Kf, t = 0., K0},
   U = Table[a Cos[i h] + b Sin[2 j h] Cos[i h + j h], {i, 0, N - 1}, {j, 0, N - 1}];
   lap[W_] := (RotateLeft[W, {1, 0}] + RotateRight[W, {1, 0}] + RotateLeft[W, {0, 1}] + RotateRight[W, {0, 1}] - 4 W)/h^2;
   Kf[W_] := -Exp[-2 W] lap[W]; K0 = Max[Abs[Kf[U]]];
   While[t < 2, With[{dt = 0.2 h^2 Exp[2 Min[U]]}, U = U + dt Exp[-2 U] lap[U]; t += dt]];
   <|"maxK0" -> K0, "t" -> t, "maxK" -> Max[Abs[Kf[U]]], "totalK" -> -Total[lap[U], 2] h^2|>];
rr = ricciRun[0.3, 0.3 0.83, 32];
valGrid[{"quantity", "value"}, {{"max |K| at t = 0", rr["maxK0"]}, {"t at the end", rr["t"]}, {"max |K| at the end", rr["maxK"]}, {"∬ K dA (−h² Σ Δ₀u)", rr["totalK"]}}]

(* ::Text:: *)
(*∬K dA = −h²ΣΔ₀u is 0 to round-off, because a periodic five-point Laplacian sums to zero exactly.*)

(* ::Subsection:: *)
(*2.3 Figures and animator*)

ricciHistory[a_, b_, N_] := Module[{h = 2. π/N, U, lap, Kf, t = 0., hist = {}, frames = {}, next = 0.},
   U = Table[a Cos[i h] + b Sin[2 j h] Cos[i h + j h], {i, 0, N - 1}, {j, 0, N - 1}];
   lap[W_] := (RotateLeft[W, {1, 0}] + RotateRight[W, {1, 0}] + RotateLeft[W, {0, 1}] + RotateRight[W, {0, 1}] - 4 W)/h^2;
   Kf[W_] := -Exp[-2 W] lap[W];
   While[t < 2, AppendTo[hist, {t, Max[Abs[Kf[U]]]}]; If[t >= next, AppendTo[frames, {t, Kf[U]}]; next += 0.05];
    Do[With[{dt = 0.2 h^2 Exp[2 Min[U]]}, U = U + dt Exp[-2 U] lap[U]; t += dt], {5}]];
   AppendTo[hist, {t, Max[Abs[Kf[U]]]}]; AppendTo[frames, {t, Kf[U]}]; <|"hist" -> hist, "frames" -> frames|>];
rh = ricciHistory[0.3, 0.3 0.83, 32];
kField[{t_, K_}] := ArrayPlot[Reverse[Transpose[K]], ColorFunction -> (kcol[#, 1.5] &), ColorFunctionScaling -> False, Frame -> False,
   PlotLabel -> Row[{"t = ", NumberForm[t, {3, 2}]}], ImageSize -> 160];
Legended[Row[{ListLogPlot[rh["hist"], Joined -> True, PlotStyle -> orange, PlotRange -> {0.01, 10}, AxesLabel -> {"t", "max |K|"}, ImageSize -> 300],
    kField[rh["frames"][[1]]], kField[SelectFirst[rh["frames"], #[[1]] >= 0.5 &]], kField[rh["frames"][[-1]]]}, "  "], kLegend[1.5, "K"]]

(* ::Text:: *)
(*Fig. 2. Ricci flow on the flat torus at the default bump 0.3: max K  on a log scale against t, and the curvature field at t = 0, 0.5 and the end (colours saturate at  K  = 1.5).*)

(* ::Text:: *)
(*The animator plays the flow frame by frame (every 0.05 in t); press the play button.*)

With[{nFrames = Length[rh["frames"]]},
 Manipulate[Legended[kField[rh["frames"][[mFrame]]], kLegend[1.5, "K"]], {{mFrame, 1, "frame"}, 1, nFrames, 1, ControlType -> Animator, AnimationRate -> 8}, SaveDefinitions -> True]]

(* ::Text:: *)
(*Ricci flow as a heat equation (the maximum principle, energy and entropy, reaction against diffusion) has its own notebook: notebooks/series/14-Ricci-Flow.nb, which regenerates those readings and charts.*)

(* ::Section:: *)
(*3. The mean-value origin of Δ, on a curved surface*)

(* ::Text:: *)
(*On a surface of constant curvature K the mean of f over the geodesic circle of radius r is*)

(* ::Text:: *)
(*\!\(\*SubscriptBox[\(M\), \(r\)]\) f = f + (r²/4)Δf + r⁴(Δ²f/64 + KΔf/96) + r⁶(Δ³f/2304 + KΔ²f/1152 + K²Δf/1440) + O(r⁸).*)

(* ::Text:: *)
(*For f = eˣ(1 + z)² + yz³ on the unit sphere, at the north pole f = 4, Δf = −4, Δ²f = −20, Δ³f = 500. The errors of the flat formula, of the formula with KΔf/96, and of the formula with the r⁶ terms fall like r⁴, r⁶ and r⁸. The area of a geodesic disc is*)

(* ::Text:: *)
(*A(r)/πr² = 1 − Kr²/12 + K²r⁴/360 − …*)

(* ::Subsection:: *)
(*3.1 Worked by hand*)

(* ::Text:: *)
(*Near the north pole write x = sin r cos φ, y = sin r sin φ, z = cos r. To order r²: x ≈ r cos φ, y ≈ r sin φ, z ≈ 1 − r²/2. Then eˣ ≈ 1 + x + x²/2, (1 + z)² ≈ (2 − r²/2)² ≈ 4 − 2r², and yz³ ≈ y. So f ≈ (1 + x + x²/2)(4 − 2r²) + y ≈ 4 + 4x + 2x² − 2r² + y.*)

(* ::Text:: *)
(*Average over the circle (over φ): the means of x and y are 0 and the mean of x² is r²/2. So \!\(\*SubscriptBox[\(M\), \(r\)]\) f ≈ 4 + 2·r²/2 − 2r² = 4 − r². The expansion says \!\(\*SubscriptBox[\(M\), \(r\)]\) f = f + (r²/4)Δf + …, so f = 4 and Δf/4 = −1: Δf = −4 at the pole, the snippet’s second value.*)

(* ::Text:: *)
(*Why the flat formula has slope 4. The flat formula keeps f + r²Δf/4 + r⁴Δ²f/64 and misses the curvature term r⁴KΔf/96 = r⁴(1)(−4)/96 = −r⁴/24. So its error is about r⁴/24 for small r: at r = 0.1 that is 4.17 × 10⁻⁶ (the r⁶ terms change it a little). Adding KΔf/96 leaves the r⁶ terms, r⁶(500/2304 − 20/1152 − 4/1440) = 0.1969 r⁶: slope 6. Adding those leaves r⁸: slope 8.*)

(* ::Text:: *)
(*Disc area. On the unit sphere the geodesic disc of radius r has area 2π(1 − cos r), so A/πr² = 2(1 − cos r)/r² = 1 − r²/12 + r⁴/360 − …; for curvature K replace r by √K r and divide by K: 1 − Kr²/12 + K²r⁴/360, the formula stated above.*)

(* ::Subsection:: *)
(*3.2 Checks on the kernel*)

(* ::Subsubsection:: *)
(*The Lab’s Wolfram cell*)

(* ::Text:: *)
(*The pole values, and the r⁶ expansion checked exactly (the last entry must be 0):*)

(* circle mean on S² of f = e^x(1+z)^2 + y z^3, exact to r^6 *)
F0[{x_, y_, z_}] := Exp[x] (1 + z)^2 + y z^3;
ext = F0[{x, y, z}/Sqrt[x^2 + y^2 + z^2]];
ΔS2amb[h_] := Simplify[(x^2 + y^2 + z^2) Laplacian[h, {x, y, z}]];
L1 = ΔS2amb[ext]; L2 = ΔS2amb[L1]; L3 = ΔS2amb[L2]; atPole[h_] := h /. {x -> 0, y -> 0, z -> 1};
circleMean = Integrate[Normal@Series[F0[{Sin[r] Cos[φ], Sin[r] Sin[φ], Cos[r]}], {r, 0, 6}], {φ, 0, 2 π}]/(2 π);
formula = atPole[ext] + r^2/4 atPole[L1] + r^4 (atPole[L2]/64 + atPole[L1]/96) + r^6 (atPole[L3]/2304 + atPole[L2]/1152 + atPole[L1]/1440);
{atPole /@ {ext, L1, L2, L3}, Simplify[Expand[circleMean - formula]]}

(* ::Subsubsection:: *)
(*The error slopes*)

(* ::Text:: *)
(*The exact circle mean (NIntegrate at 30 digits) on r = 2^{−k/4}, k = 4 … 24, with log–log slopes fitted on 0.04 < r < 0.16:*)

F0[{x_, y_, z_}] := Exp[x] (1 + z)^2 + y z^3; pole = {4, -4, -20, 500};
cm[r_] := NIntegrate[F0[{Sin[r] Cos[φ], Sin[r] Sin[φ], Cos[r]}], {φ, 0, 2 π}, WorkingPrecision -> 30, PrecisionGoal -> 25]/(2 π);
flat[r_] := pole[[1]] + r^2/4 pole[[2]] + r^4 pole[[3]]/64; c4[r_] := flat[r] + r^4 pole[[2]]/96;
c6[r_] := c4[r] + r^6 (pole[[4]]/2304 + pole[[3]]/1152 + pole[[2]]/1440);
rs = Select[N[2^(-Range[4, 24]/4), 30], 0.04 < # < 0.16 &];
slopes = Table[Coefficient[Fit[{Log[#], Log[Abs[cm[#] - ap[#]]]} & /@ rs, {1, s}, s], s], {ap, {flat, c4, c6}}];
valGrid[{"approximation", "log–log slope"}, Transpose[{{"flat formula", "+ KΔf/96 at r^4", "+ r^6 terms"}, slopes}]]

(* ::Text:: *)
(*Slopes near 4, 6 and 8; not exactly integers, because each error still carries its next-order term on this window.*)

(* ::Subsubsection:: *)
(*The disc area*)

(* disc area on a surface of constant curvature K: A(r) = 2π(1 − cos √K r)/K *)
Series[2 π (1 - Cos[Sqrt[K] r])/K/(π r^2), {r, 0, 5}]

(* ::Subsection:: *)
(*3.3 Figures and animator*)

rsAll = N[2^(-Range[4, 24]/4), 30];
errs = Table[With[{e = cm[r]}, {r, Abs[e - flat[r]], Abs[e - c4[r]], Abs[e - c6[r]]}], {r, rsAll}];
ListLogLogPlot[{errs[[All, {1, 2}]], errs[[All, {1, 3}]], errs[[All, {1, 4}]]}, Joined -> True, PlotMarkers -> Automatic,
 PlotStyle -> {GrayLevel[0.5], orange, blue}, AxesLabel -> {"r", "|error|"}, ImageSize -> 420,
 PlotLegends -> {"flat formula (K = 0)", "+ K Δf/96", "+ r^6 terms"}]

(* ::Text:: *)
(*Fig. 3. Errors of the three approximations to the exact circle mean of f = eˣ(1 + z)² + yz³ on the unit sphere, on log–log axes. The lines have slopes 4, 6 and 8; with the circle mean at 30 digits the blue line keeps falling below 10⁻¹³.*)

discRatio[K_, r_] := Which[K == 0, 1, K > 0, 2 (1 - Cos[Sqrt[K] r])/(K r^2), True, 2 (Cosh[Sqrt[-K] r] - 1)/(-K r^2)];
Plot[{1, discRatio[1, r], discRatio[-1, r]}, {r, 0.02, 3}, PlotRange -> {0, 2}, PlotStyle -> {Directive[GrayLevel[0.5], Dashed], orange, blue},
 AxesLabel -> {"r", "A(r)/π r^2"}, PlotLegends -> {"K = 0", "K = 1", "K = −1"}, ImageSize -> 380]

(* ::Text:: *)
(*Fig. 4. Area of a geodesic disc divided by the flat area πr², for K = 1, 0 and −1.*)

Manipulate[Plot[{1, discRatio[mK, r]}, {r, 0.02, 3}, PlotRange -> {0, 2}, PlotStyle -> {Directive[GrayLevel[0.5], Dashed], If[mK >= 0, orange, blue]},
  AxesLabel -> {"r", "A(r)/π r^2"}, PlotLabel -> Row[{"K = ", mK, ":  1 − K r²/12 + K² r⁴/360 − …"}], ImageSize -> 380], {{mK, 1, "K"}, -1, 1, 0.1, Appearance -> "Labeled"}, SaveDefinitions -> True]

(* ::Section:: *)
(*4. Curvature is the first correction to Weyl’s law*)

(* ::Text:: *)
(*The heat trace has the small-t expansion (McKean–Singer)*)

(* ::Text:: *)
(*Tr e^{tΔ} ~ (4πt)^{−n/2}(Vol + (t/6)∫S dV + …).*)

(* ::Text:: *)
(*For the unit sphere (eigenvalues l(l + 1), multiplicity 2l + 1, area 4π) the ratio to Weyl’s Area/(4πt), which is t·Tr e^{tΔ}, is 1 + t/3 + t²/15 + …; for a flat torus of the same area it is 1 up to exponentially small terms.*)

(* ::Subsection:: *)
(*4.1 Worked by hand*)

(* ::Text:: *)
(*Put x = l + ½. Then (2l + 1) = 2x and l(l + 1) = x² − ¼, so Tr e^{tΔ} = \!\(\*SubscriptBox[\(Σ\), \(l≥0\)]\) g(l + ½) with g(x) = 2x e^{−(x² − ¼)t} = 2 e^{t/4} x e^{−x²t}.*)

(* ::Text:: *)
(*A sum over half-integers is the integral plus corrections at the end point (the midpoint Euler–Maclaurin formula): \!\(\*SubscriptBox[\(Σ\), \(l≥0\)]\) g(l + ½) = ∫₀^∞ g dx + g′(0)/24 − 7g‴(0)/5760 + … Here ∫₀^∞ 2x e^{−x²t} dx = 1/t, g′(0) = 2e^{t/4} and g‴(0) = −12t e^{t/4}. So Tr e^{tΔ} = e^{t/4}(1/t + 1/12 + 7t/480 + …).*)

(* ::Text:: *)
(*Multiply by t and expand e^{t/4} = 1 + t/4 + t²/32 + …: t·Tr = (1 + t/4 + t²/32)(1 + t/12 + 7t²/480) = 1 + (1/4 + 1/12) t + (1/32 + 1/48 + 7/480) t² = 1 + t/3 + t²/15. The t/3 is McKean–Singer’s (t/6)∫S/Area with S = 2 (the scalar curvature of the unit sphere): (t/6)(2·4π)/(4π) = t/3.*)

(* ::Text:: *)
(*The flat square torus of area 4π has side 2√π and eigenvalues π(m² + n²), so Tr e^{tΔ} = θ₃(0, e^{−πt})², and the Jacobi identity θ₃(0, e^{−πt}) = t^{−1/2} θ₃(0, e^{−π/t}) gives t·Tr = θ₃(0, e^{−π/t})² = 1 + 4e^{−π/t} + …: no t-term, because the torus is flat. At t = 0.05 the sphere gives 1.016835, the torus 1.000000, and 1 + t/3 + t²/15 = 1.016833.*)

(* ::Subsection:: *)
(*4.2 Checks on the kernel*)

(* ::Subsubsection:: *)
(*The Lab’s Wolfram cell*)

(* ::Text:: *)
(*The heat trace of the unit sphere against 1 + t/3 + t²/15:*)

(* heat trace of the unit sphere against 1 + t/3 + t^2/15 *)
heatTrace[t_?NumericQ] := Sum[(2 j + 1) Exp[-j (j + 1) t], {j, 0, 2000}];
Table[{t, t heatTrace[t], 1 + t/3 + t^2/15}, {t, {0.1, 0.03, 0.01}}]

(* ::Subsubsection:: *)
(*Sphere and flat torus*)

sph[t_] := With[{s = SetPrecision[t, 30]}, s Sum[(2 l + 1) Exp[-l (l + 1) s], {l, 0, 600}]];  (* terms beyond l = 600 are below e^(−1800) for t ≥ 0.005 *)
tor[t_] := t (EllipticTheta[3, 0, Exp[-π t]])^2;  (* side 2√π: eigenvalues π(m² + n²) *)
valGrid[{"t", "sphere t·Tr", "1 + t/3 + t²/15", "flat torus t·Tr"}, Table[{t, sph[t], 1 + t/3 + t^2/15, tor[t]}, {t, {0.01, 0.05, 0.1}}]]

(* why the torus line is flat: by Poisson summation θ3(0, e^(−πt)) = t^(−1/2) θ3(0, e^(−π/t)) *)
Table[N[tor[t] - 1, 20], {t, {0.01, 0.05, 0.1, 0.4}}]

(* ::Text:: *)
(*The torus ratio is θ₃(0, e^{−π/t})² = 1 + 4e^{−π/t} + …: 1 to machine precision for t ≤ 0.1, and 1.0016 at t = 0.4.*)

(* ::Subsection:: *)
(*4.3 Figures and animator*)

sphM[t_?NumericQ] := t Sum[(2 l + 1) Exp[-l (l + 1) t], {l, 0, 400}];
heatPlot[tt_] := Show[Plot[{sphM[t], 1 + t/3 + t^2/15, tor[t]}, {t, 0.004, 0.4}, PlotRange -> {0.98, 1.16}, AxesLabel -> {"t", "t Tr e^(tΔ)"},
    PlotStyle -> {orange, Directive[Black, Dashed], blue}, PlotLegends -> {"unit sphere, K = 1", "1 + t/3 + t^2/15", "flat torus, same area"}, ImageSize -> 420],
   Graphics[{GrayLevel[0.5], Line[{{tt, 0.98}, {tt, 1.16}}]}]];
heatPlot[0.05]

(* ::Text:: *)
(*Fig. 5. The heat trace divided by Weyl’s Area/(4πt) for the unit sphere and for a flat torus of the same area, against 1 + t/3 + t²/15 (the grey line marks t = 0.05).*)

(* ::Text:: *)
(*The animator: slide t; the readout gives the sphere’s ratio, 1 + t/3 + t²/15, the torus’s ratio and their difference.*)

Manipulate[Column[{heatPlot[mT], Grid[{{"sphere", NumberForm[sphM[mT], 7]}, {"1 + t/3 + t²/15", NumberForm[1 + mT/3 + mT^2/15, 7]}, {"flat torus", NumberForm[tor[mT], 7]},
     {"difference ≈ t/3", NumberForm[sphM[mT] - tor[mT], 7]}}, Alignment -> Left]}], {{mT, 0.05, "t"}, 0.005, 0.4, 0.005, Appearance -> "Labeled"}, SaveDefinitions -> True]

(* ::Section:: *)
(*5. Bochner’s formula, and what a curvature bound controls*)

(* ::Text:: *)
(*½Δ|∇f|² = |Hess f|² + ⟨∇f, ∇Δf⟩ + Ric(∇f, ∇f).*)

(* ::Text:: *)
(*Integrated, it gives Lichnerowicz’s bound λ₁ ≥ nk when Ric ≥ (n − 1)k; along geodesics it gives the comparison Δr ≤ (n − 1)√k cot(√k r). The carré du champ Γ(f) = ½(Δ(f²) − 2fΔf) = |∇f|² and Γ₂(f) = ½ΔΓ(f) − Γ(f, Δf) carry the formula to spaces without derivatives. On a surface of curvature K > 0: λ₁ ≥ 2K, equality for the round sphere; diameter ≤ π/√K (Bonnet–Myers); Δr changes sign at r = π/(2√K). For K ≤ 0, Δr → √|K|.*)

(* ::Subsection:: *)
(*5.1 Worked by hand*)

(* ::Text:: *)
(*Take f = z = cos θ. It is a first spherical harmonic, so Δf = −2f. Its gradient on the sphere has |∇f|² = sin²θ = 1 − z².*)

(* ::Text:: *)
(*Left side. z² = (z² − 1/3) + 1/3 and z² − 1/3 is a second harmonic (eigenvalue −6), so Δ(z²) = −6(z² − 1/3) = −6z² + 2, and ½Δ|∇f|² = ½Δ(1 − z²) = 3z² − 1.*)

(* ::Text:: *)
(*Right side. The Hessian of the restriction of a linear function to the unit sphere is −f·g, so |Hess f|² = 2z² (two directions, each −z). ⟨∇f, ∇Δf⟩ = ⟨∇f, −2∇f⟩ = −2(1 − z²). Ric = g on the unit sphere, so Ric(∇f, ∇f) = 1 − z². Sum: 2z² − 2 + 2z² + 1 − z² = 3z² − 1, equal to the left side.*)

(* ::Text:: *)
(*Lichnerowicz with equality. Integrate Bochner over the sphere: ∫½Δ|∇f|² = 0, so 0 = ∫|Hess f|² − ∫(Δf)² + ∫Ric(∇f, ∇f). For an eigenfunction Δf = −λf, and |Hess f|² ≥ (Δf)²/n, which gives λ ≥ n k when Ric ≥ (n − 1)k; on S² (n = 2, k = 1) that is λ₁ ≥ 2, and f = z attains it because its Hessian is a multiple of g. For curvature K: λ₁ ≥ 2K, the round sphere has λ₁ = 2K, diameter ≤ π/√K (Bonnet–Myers), and Δr = √K cot(√K r) changes sign at r = π/(2√K).*)

(* ::Subsection:: *)
(*5.2 Checks on the kernel*)

(* ::Subsubsection:: *)
(*The Lab’s Wolfram cell*)

(* ::Text:: *)
(*Bochner on S² for an arbitrary function (must return 0):*)

(* Bochner formula on S² for an arbitrary function *)
X = {θ, φ}; g = {{1, 0}, {0, Sin[θ]^2}}; gi = Inverse[g];
Γ = Table[1/2 Sum[gi[[i, l]] (D[g[[l, j]], X[[k]]] + D[g[[l, k]], X[[j]]] - D[g[[j, k]], X[[l]]]), {l, 2}], {i, 2}, {j, 2}, {k, 2}];
Lap[w_] := 1/Sqrt[Det[g]] Sum[D[Sqrt[Det[g]] gi[[i, j]] D[w, X[[j]]], X[[i]]], {i, 2}, {j, 2}];
g2[w_] := Sum[gi[[i, j]] D[w, X[[i]]] D[w, X[[j]]], {i, 2}, {j, 2}];
Hs[w_] := Table[D[w, X[[i]], X[[j]]] - Sum[Γ[[k, i, j]] D[w, X[[k]]], {k, 2}], {i, 2}, {j, 2}];
f = \[ScriptF][θ, φ];
Simplify[1/2 Lap[g2[f]] - (Tr[gi . Hs[f] . gi . Hs[f]] + Sum[gi[[i, j]] D[f, X[[i]]] D[Lap[f], X[[j]]], {i, 2}, {j, 2}] + g2[f])]

(* ::Subsubsection:: *)
(*Comparison, Lichnerowicz and the carré du champ*)

(* on a surface of constant curvature K in geodesic polar coordinates, ds² = dr² + sn(r)² dθ², Δr = sn'(r)/sn(r) *)
sn[K_, r_] := Sin[Sqrt[K] r]/Sqrt[K];
{Simplify[D[sn[K, r], r]/sn[K, r] - Sqrt[K] Cot[Sqrt[K] r], K > 0], Normal[Series[Sqrt[K] Cot[Sqrt[K] r], {K, 0, 0}]],
 Limit[Sqrt[-K] Coth[Sqrt[-K] r], r -> ∞, Assumptions -> K < 0], Reduce[Sqrt[K] Cot[Sqrt[K] r] == 0 && 0 < r < π/Sqrt[K] && K > 0, r]}

(* round sphere of curvature K: λ1 = 2K, the Lichnerowicz equality case for n = 2; Γ is |∇f|² *)
With[{K = 7/3}, {Min[Select[Table[l (l + 1) K, {l, 0, 4}], # > 0 &]], 2 K}]

X = {θ, φ}; g = {{1, 0}, {0, Sin[θ]^2}}; Lap[w_] := 1/Sin[θ] (D[Sin[θ] D[w, θ], θ] + D[w, φ, φ]/Sin[θ]);
Simplify[1/2 (Lap[\[ScriptF][θ, φ]^2] - 2 \[ScriptF][θ, φ] Lap[\[ScriptF][θ, φ]]) - (D[\[ScriptF][θ, φ], θ]^2 + D[\[ScriptF][θ, φ], φ]^2/Sin[θ]^2)]

(* ::Subsection:: *)
(*5.3 Figures and animator*)

lapDist[K_, r_] := Which[K == 0, 1/r, K > 0, Sqrt[K] Cot[Sqrt[K] r], True, Sqrt[-K] Coth[Sqrt[-K] r]];
Plot[{lapDist[0, r], lapDist[1, r], lapDist[-1, r]}, {r, 0.05, 3.2}, PlotRange -> {-3, 5}, AxesLabel -> {"r", "Δr"},
 PlotStyle -> {Directive[GrayLevel[0.5], Dashed], orange, blue}, PlotLegends -> {"K = 0: 1/r", "K = 1: cot r", "K = −1: coth r"}, ImageSize -> 400]

(* ::Text:: *)
(*Fig. 6. Laplacian of the distance function on surfaces of constant curvature K = 1, 0, −1: positive curvature makes Δr smaller than the flat 1/r and negative at r > π/2; negative curvature keeps it above √ K .*)

Manipulate[Column[{Plot[{lapDist[0, r], lapDist[mK, r]}, {r, 0.05, 3.2}, PlotRange -> {-3, 5}, AxesLabel -> {"r", "Δr"},
    PlotStyle -> {Directive[GrayLevel[0.5], Dashed], If[mK >= 0, orange, blue]}, ImageSize -> 400],
   If[mK > 0, Grid[{{"Lichnerowicz λ₁ ≥ nK", 2 mK}, {"round sphere λ₁ = 2K", 2 mK}, {"Bonnet–Myers diam ≤ π/√K", N[π/Sqrt[mK]]}, {"Δr changes sign at r", N[π/(2 Sqrt[mK])]}}, Alignment -> Left],
    Grid[{{"Lichnerowicz", "no bound for K ≤ 0"}, {"Δr → √|K| as r → ∞", N[Sqrt[-mK]]}}, Alignment -> Left]]}],
 {{mK, 1, "K"}, -1, 2, 0.1, Appearance -> "Labeled"}, SaveDefinitions -> True]

(* ::Section:: *)
(*6. On a mesh, angle defect is curvature and the cotangent Laplacian is −2Hn*)

(* ::Text:: *)
(*(Δf)_i = (1/2A_i) \!\(\*SubscriptBox[\(Σ\), \(j\)]\) (cot \!\(\*SubscriptBox[\(α\), \(ij\)]\) + cot \!\(\*SubscriptBox[\(β\), \(ij\)]\))(\!\(\*SubscriptBox[\(f\), \(j\)]\) − \!\(\*SubscriptBox[\(f\), \(i\)]\)),        \!\(\*SubscriptBox[\(δ\), \(i\)]\) = 2π − Σ \!\(\*SubscriptBox[\(θ\), \(i\)]\),        \!\(\*SubscriptBox[\(K\), \(i\)]\) ≈ δ_i/A_i.*)

(* ::Text:: *)
(*Here \!\(\*SubscriptBox[\(θ\), \(i\)]\) are the corner angles at vertex i, \!\(\*SubscriptBox[\(α\), \(ij\)]\) and \!\(\*SubscriptBox[\(β\), \(ij\)]\) the angles opposite edge ij, and \!\(\*SubscriptBox[\(A\), \(i\)]\) the barycentric area (one third of each incident triangle). The defects of a closed mesh add to exactly 2πχ: a cube corner has δ = 2π − 3·π/2 = π/2, and eight of them give 4π. The corner angle at vertex i of triangle ijk is ang[i, j, k] = VectorAngle[P[[j]] − P[[i]], P[[k]] − P[[i]]].*)

(* ::Subsection:: *)
(*6.1 Worked by hand*)

(* ::Text:: *)
(*Corner angles of the right triangle P₁ = (0, 0, 0), P₂ = (1, 0, 0), P₃ = (0, 1, 0). At P₁ the edges are (1, 0, 0) and (0, 1, 0): dot product 0, angle π/2. At P₂ they are (−1, 1, 0) and (−1, 0, 0): cos = 1/(√2·1), angle π/4; likewise π/4 at P₃. Sum π.*)

(* ::Text:: *)
(*Cube corner: three squares meet, each with corner angle π/2, so δ = 2π − 3π/2 = π/2; eight corners give 4π = 2π·2. Icosahedron vertex: five equilateral triangles, δ = 2π − 5π/3 = π/3; twelve vertices give 4π. Square-pyramid apex with unit edges: four equilateral corners, δ = 2π − 4π/3 = 2π/3.*)

(* ::Text:: *)
(*Torus mesh at the outer equator (v = 0) and the barycentric area. A vertex of the 40 × 20 mesh touches six triangles; its area \!\(\*SubscriptBox[\(A\), \(i\)]\) is one third of their total, about one mesh cell: (2π·3/40)(2π/20) = 0.148. Its six corner angles add to slightly less than 2π because the surface is convex there; the defect is about K \!\(\*SubscriptBox[\(A\), \(i\)]\) = (1/3)(0.148) = 0.049, and the ratio defect/area at that vertex is 0.3352 against the smooth 1/3 (table in §6.2).*)

(* ::Text:: *)
(*Why the total is exactly 0. Summing \!\(\*SubscriptBox[\(δ\), \(i\)]\) = 2π − Σθ over all V vertices gives 2πV − πF (each of the F triangles contributes π). Every triangle has three edges and every edge two triangles, so E = 3F/2, and 2πV − πF = 2π(V − E + F) = 2πχ. For the torus mesh V = 800, E = 2400, F = 1600, so χ = 0.*)

(* ::Subsection:: *)
(*6.2 Checks on the kernel*)

(* ::Subsubsection:: *)
(*ang on triangles, fans, a pyramid and a saddle*)

SeedRandom[7]; angSum[P_] := Module[{ang}, ang[i_, j_, k_] := VectorAngle[P[[j]] - P[[i]], P[[k]] - P[[i]]];
   ang[1, 2, 3] + ang[2, 3, 1] + ang[3, 1, 2]];
<|"right triangle" -> Module[{P = {{0, 0, 0}, {1, 0, 0}, {0, 1, 0}}, ang}, ang[i_, j_, k_] := VectorAngle[P[[j]] - P[[i]], P[[k]] - P[[i]]]; {ang[1, 2, 3], ang[2, 3, 1], ang[3, 1, 2]}],
  "max |angle sum − π|, 1000 random triangles" -> Max[Table[Abs[angSum[RandomReal[{-1, 1}, {3, 3}]] - π], {1000}]],
  "symmetric in j, k" -> Module[{P = RandomReal[1, {3, 3}]}, VectorAngle[P[[2]] - P[[1]], P[[3]] - P[[1]]] == VectorAngle[P[[3]] - P[[1]], P[[2]] - P[[1]]]]|>

defectAt[apex_, ring_] := 2 π - Total[Table[VectorAngle[ring[[k]] - apex, ring[[Mod[k, Length[ring]] + 1]] - apex], {k, Length[ring]}]];
hex = Table[{Cos[2 π k/6], Sin[2 π k/6], 0}, {k, 0, 5}];
<|"flat fan of six triangles" -> Chop[defectAt[{0, 0, 0}, hex]],
  "square-pyramid apex (unit edges)" -> FullSimplify[defectAt[{0, 0, 1/Sqrt[2]}, {{1, 0, 0}, {0, 1, 0}, {-1, 0, 0}, {0, -1, 0}}/Sqrt[2]]],
  "saddle vertex on z = (x² − y²)/2, eight neighbours on the unit circle" -> N[defectAt[{0, 0, 0}, Table[With[{t = 2 π k/8}, {Cos[t], Sin[t], (Cos[t]^2 - Sin[t]^2)/2}], {k, 0, 7}]]]|>

(* ::Text:: *)
(*The square-pyramid apex with unit edges has four equilateral corners: 2π − 4π/3 = 2π/3. The saddle ring alternates up and down, so its corner angles add to more than 2π: −0.8054.*)

(* ::Subsubsection:: *)
(*The five regular polyhedra*)

polyDefects[name_] := Module[{P = N[PolyhedronData[name, "VertexCoordinates"]], F = PolyhedronData[name, "FaceIndices"], def},
   def = ConstantArray[2. π, Length[P]];
   Do[Do[With[{i = f[[k]], j = f[[Mod[k, Length[f]] + 1]], l = f[[Mod[k - 2, Length[f]] + 1]]}, def[[i]] -= VectorAngle[P[[j]] - P[[i]], P[[l]] - P[[i]]]], {k, Length[f]}], {f, F}];
   {name, Length[P], Union[Rationalize[def/π, 10^-9]] π, Chop[Total[def]/(2 π), 10^-12]}];
Grid[Prepend[polyDefects /@ {"Tetrahedron", "Cube", "Octahedron", "Dodecahedron", "Icosahedron"}, Style[#, Bold] & /@ {"polyhedron", "vertices", "defect at each vertex", "Σ defect / 2π"}], Frame -> All]

(* ::Subsubsection:: *)
(*The Lab’s Wolfram cell*)

(* ::Text:: *)
(*Angle defect on a 40 × 20 torus mesh (must return 0):*)

(* angle defect on a torus mesh: total is exactly 0 = 2πχ *)
torusPos = {(2 + Cos[v]) Cos[u], (2 + Cos[v]) Sin[u], Sin[v]}; {nu, nv} = {40, 20};
idx[i_, j_] := Mod[i, nu] nv + Mod[j, nv] + 1;
P = Flatten[Table[N[torusPos /. {u -> 2 π i/nu, v -> 2 π j/nv}], {i, 0, nu - 1}, {j, 0, nv - 1}], 1];
T = Flatten[Table[{{idx[i, j], idx[i + 1, j], idx[i + 1, j + 1]}, {idx[i, j], idx[i + 1, j + 1], idx[i, j + 1]}}, {i, 0, nu - 1}, {j, 0, nv - 1}], 2];
ang[i_, j_, k_] := VectorAngle[P[[j]] - P[[i]], P[[k]] - P[[i]]];
defect = ConstantArray[2. π, Length[P]];
Do[{a, b, c} = tr; defect[[a]] -= ang[a, b, c]; defect[[b]] -= ang[b, c, a]; defect[[c]] -= ang[c, a, b], {tr, T}];
Chop[Total[defect], 10^-9]

(* ::Subsubsection:: *)
(*The torus mesh at four resolutions*)

(* ::Text:: *)
(*Vertices, total defect and the largest error of defect/area against the smooth K = cos v/(2 + cos v):*)

meshCurvature[P_, T_] := Module[{nv = Length[P], ang, def, Am},
   ang[i_, j_, k_] := VectorAngle[P[[j]] - P[[i]], P[[k]] - P[[i]]];
   def = ConstantArray[2. π, nv]; Am = ConstantArray[0., nv];
   Do[Module[{a, b, c}, {a, b, c} = tri; def[[a]] -= ang[a, b, c]; def[[b]] -= ang[b, c, a]; def[[c]] -= ang[c, a, b];
     Am[[{a, b, c}]] += Norm[Cross[P[[b]] - P[[a]], P[[c]] - P[[a]]]]/6], {tri, T}];
   <|"defect" -> def, "area" -> Am|>];
torusMesh[nu_, nv_] := Module[{id}, id[i_, j_] := Mod[i, nu] nv + Mod[j, nv] + 1;
   {Flatten[Table[N[{(2 + Cos[2 π j/nv]) Cos[2 π i/nu], (2 + Cos[2 π j/nv]) Sin[2 π i/nu], Sin[2 π j/nv]}], {i, 0, nu - 1}, {j, 0, nv - 1}], 1],
    Flatten[Table[{{id[i, j], id[i + 1, j], id[i + 1, j + 1]}, {id[i, j], id[i + 1, j + 1], id[i, j + 1]}}, {i, 0, nu - 1}, {j, 0, nv - 1}], 2]}];
meshData[{nu_, nv_}] := Module[{P, T, M, Km, Ks},
   {P, T} = torusMesh[nu, nv]; M = meshCurvature[P, T]; Km = M["defect"]/M["area"];
   Ks = Flatten[Table[N[Cos[2 π j/nv]/(2 + Cos[2 π j/nv])], {i, 0, nu - 1}, {j, 0, nv - 1}]];
   <|"nu" -> nu, "nv" -> nv, "vertices" -> Length[P], "defect" -> Total[M["defect"]], "err" -> Max[Abs[Km - Ks]], "Kouter" -> Km[[1]]|>];
meshVals = meshData /@ {{12, 6}, {24, 12}, {40, 20}, {64, 32}};
valGrid[{"mesh", "vertices", "Σ defect", "max |Kmesh − K|", "Kmesh at the outer equator (K = 1/3)"},
 {ToString[#["nu"]] <> " × " <> ToString[#["nv"]], #["vertices"], #["defect"], #["err"], #["Kouter"]} & /@ meshVals]

(* ::Text:: *)
(*The total defect is 0 = 2πχ(torus) at every resolution, to round-off; the pointwise error falls by about 2.6 for each 1.6-fold refinement, like h².*)

(* ::Subsection:: *)
(*6.3 Figures and animator*)

meshPicture[{nu_, nv_}] := Module[{P, T, M, Km}, {P, T} = torusMesh[nu, nv]; M = meshCurvature[P, T]; Km = M["defect"]/M["area"];
   Legended[Graphics3D[{EdgeForm[GrayLevel[0.4, 0.5]], Table[{kcol[Mean[Km[[tr]]], 1], Polygon[P[[tr]]]}, {tr, T}]}, Boxed -> False, Lighting -> "Neutral",
     PlotLabel -> Row[{nu, " × ", nv, ":  Σ defect = ", NumberForm[Chop[Total[M["defect"]], 10^-9], 3]}], ImageSize -> 360], kLegend[1, "defect/area"]]];
{P40, T40} = torusMesh[40, 20]; M40 = meshCurvature[P40, T40];
Row[{meshPicture[{40, 20}], Show[Plot[Cos[v]/(2 + Cos[v]), {v, 0, 2 π}, PlotStyle -> Black, AxesLabel -> {"v (around the tube)", "K"}],
    ListPlot[Table[{2 π j/20, (M40["defect"]/M40["area"])[[j + 1]]}, {j, 0, 19}], PlotStyle -> Directive[orange, PointSize[0.02]]], PlotRange -> {-1.1, 0.5}, ImageSize -> 340]}]

(* ::Text:: *)
(*Fig. 7. The 40 × 20 torus mesh coloured by angle defect divided by vertex area, and that ratio around the tube (orange dots) against the smooth K = cos v/(2 + cos v) (black).*)

ListLogLogPlot[{2 π/#[[2]], #[[3]]} & /@ ({#["nu"], #["nv"], #["err"]} & /@ meshVals), Joined -> True, PlotMarkers -> Automatic, PlotStyle -> orange,
 AxesLabel -> {"edge length 2π/nv", "max |Kmesh − K|"}, PlotLabel -> Row[{"fitted slope ", NumberForm[Coefficient[Fit[Log[{2 π/#["nv"], #["err"]}] & /@ meshVals, {1, s}, s], s], 3]}], ImageSize -> 380]

(* ::Text:: *)
(*Fig. 8. Largest error of the mesh curvature against the mesh size for the four resolutions: slope about 2, second-order convergence.*)

Manipulate[meshPicture[mRes], {{mRes, {40, 20}, "resolution"}, {{12, 6} -> "12 × 6", {24, 12} -> "24 × 12", {40, 20} -> "40 × 20", {64, 32} -> "64 × 32"}}, SaveDefinitions -> True]

(* ::Section:: *)
(*7. Seven graph curvatures, each built from the graph Laplacian*)

(* ::Text:: *)
(*Seven graphs: the binary tree on 15 vertices, the cycle C₆, the cube Q₃, the complete graph K₅, the Petersen graph, the 5 × 5 grid, and the dumbbell (two K₅ joined by a path of three edges). Seven curvatures:*)

(* ::Text:: *)
(*Lin–Lu–Yau \!\(\*SubscriptBox[\(κ\), \(LLY\)]\) on edges: the limit of Ollivier curvature as the walk becomes idle (\!\(\*SubscriptBox[\(κ\), \(LLY\)]\) = 2κ_{1/2}).*)

(* ::Text:: *)
(*Ollivier κ₀ on edges, with the non-lazy walk.*)

(* ::Text:: *)
(*Bakry–Émery K_∞ on vertices: the largest K with Γ₂ ≥ KΓ.*)

(* ::Text:: *)
(*Forman F = 4 − \!\(\*SubscriptBox[\(d\), \(x\)]\) − \!\(\*SubscriptBox[\(d\), \(y\)]\) on edges, and Forman with triangles F + 3·#triangles.*)

(* ::Text:: *)
(*Resistance curvature \!\(\*SubscriptBox[\(p\), \(i\)]\) = 1 − ½\!\(\*SubscriptBox[\(Σ\), \(j∼i\)]\) \!\(\*SubscriptBox[\(ω\), \(ij\)]\) on vertices, with ω the effective resistance.*)

(* ::Text:: *)
(*Steinerberger curvature w on vertices, solving Dw = n·1 with D the distance matrix.*)

(* ::Text:: *)
(*The discrete Lichnerowicz bounds λ₁ ≥ min \!\(\*SubscriptBox[\(κ\), \(LLY\)]\) and λ₁ ≥ min K_∞ hold for the normalised Laplacian.*)

(* ::Subsection:: *)
(*7.1 Worked by hand*)

(* ::Text:: *)
(*Lin–Lu–Yau on an edge xy of K₅. With idleness ½, \!\(\*SubscriptBox[\(μ\), \(x\)]\) puts ½ on x and ⅛ on each of its four neighbours; \!\(\*SubscriptBox[\(μ\), \(y\)]\) the same around y. The three other vertices get ⅛ from both, so nothing moves there. At x, \!\(\*SubscriptBox[\(μ\), \(x\)]\) has ½ and \!\(\*SubscriptBox[\(μ\), \(y\)]\) has ⅛: an excess of ⅜, which must go to y (where \!\(\*SubscriptBox[\(μ\), \(y\)]\) has ½ and \!\(\*SubscriptBox[\(μ\), \(x\)]\) ⅛), distance 1. So W₁ = ⅜, κ_{1/2} = 1 − ⅜ = ⅝ and \!\(\*SubscriptBox[\(κ\), \(LLY\)]\) = 2κ_{1/2} = 5/4. Non-lazy: \!\(\*SubscriptBox[\(μ\), \(x\)]\) is ¼ on y and on the three others, \!\(\*SubscriptBox[\(μ\), \(y\)]\) ¼ on x and on the three others; ¼ moves from y to x, W₁ = ¼, κ₀ = ¾.*)

(* ::Text:: *)
(*Forman on K₅: F = 4 − \!\(\*SubscriptBox[\(d\), \(x\)]\) − \!\(\*SubscriptBox[\(d\), \(y\)]\) = 4 − 4 − 4 = −4; each edge lies in three triangles, so F + 3·3 = 5. On C₆: F = 4 − 2 − 2 = 0, and no triangles.*)

(* ::Text:: *)
(*Resistance curvature on C₆. Between neighbours the cycle is a resistor of 1 in parallel with one of 5, so ω = 5/6. Then p = 1 − ½(5/6 + 5/6) = 1/6 at every vertex, and Σp = 6·(1/6) = 1. Steinerberger on C₆: the distances from a vertex are 1, 1, 2, 2, 3, which add to 9; by symmetry w is constant, so 9w = n = 6 and w = 2/3.*)

(* ::Text:: *)
(*Spectral gap of Petersen. Its adjacency eigenvalues are 3, 1 (five times) and −2 (four times); the normalised Laplacian 1 − A/3 has eigenvalues 0, 2/3, 5/3. So λ₁ = 2/3 and \!\(\*SubscriptBox[\(λ\), \(max\)]\) = 5/3. On the cube, adjacency eigenvalues 3, 1, −1, −3 give λ₁ = 1 − 1/3 = 2/3 = \!\(\*SubscriptBox[\(κ\), \(LLY\)]\) = K_∞: the equality case.*)

(* ::Text:: *)
(*Tree root edge. The root has degree 2 and its child degree 3, with no common neighbour and no 4-cycle, so the tree formula \!\(\*SubscriptBox[\(κ\), \(LLY\)]\) = 2/d_x + 2/d_y − 2 gives 2/2 + 2/3 − 2 = −1/3; an interior edge between two vertices of degree 3 gives 2/3 + 2/3 − 2 = −2/3; a leaf edge 2/3 + 2/1 − 2 = 2/3. The dumbbell edge from a clique vertex (degree 5) to the path (degree 2): 2/5 + 2/2 − 2 = −3/5; the middle path edge (degrees 2 and 2) is 0.*)

(* ::Subsection:: *)
(*7.2 Checks on the kernel*)

(* ::Subsubsection:: *)
(*The seven graphs*)

(* ::Text:: *)
(*Edge lists, vertices numbered from 1 (the tree: i joined to 2i and 2i + 1):*)

graphEdges = <|"tree" -> {{1, 2}, {1, 3}, {2, 4}, {2, 5}, {3, 6}, {3, 7}, {4, 8}, {4, 9}, {5, 10}, {5, 11}, {6, 12}, {6, 13}, {7, 14}, {7, 15}}, "cycle" -> {{1, 2}, {2, 3}, {3, 4}, {4, 5}, {5, 6}, {6, 1}}, "cube" -> {{1, 2}, {1, 3}, {1, 5}, {2, 4}, {2, 6}, {3, 4}, {3, 7}, {4, 8}, {5, 6}, {5, 7}, {6, 8}, {7, 8}}, "complete" -> {{1, 2}, {1, 3}, {1, 4}, {1, 5}, {2, 3}, {2, 4}, {2, 5}, {3, 4}, {3, 5}, {4, 5}}, "petersen" -> {{1, 2}, {1, 6}, {6, 8}, {2, 3}, {2, 7}, {7, 9}, {3, 4}, {3, 8}, {8, 10}, {4, 5}, {4, 9}, {9, 6}, {5, 1}, {5, 10}, {10, 7}}, "grid" -> {{1, 2}, {1, 6}, {2, 3}, {2, 7}, {3, 4}, {3, 8}, {4, 5}, {4, 9}, {5, 10}, {6, 7}, {6, 11}, {7, 8}, {7, 12}, {8, 9}, {8, 13}, {9, 10}, {9, 14}, {10, 15}, {11, 12}, {11, 16}, {12, 13}, {12, 17}, {13, 14}, {13, 18}, {14, 15}, {14, 19}, {15, 20}, {16, 17}, {16, 21}, {17, 18}, {17, 22}, {18, 19}, {18, 23}, {19, 20}, {19, 24}, {20, 25}, {21, 22}, {22, 23}, {23, 24}, {24, 25}}, "dumbbell" -> {{1, 2}, {8, 9}, {1, 3}, {8, 10}, {1, 4}, {8, 11}, {1, 5}, {8, 12}, {2, 3}, {9, 10}, {2, 4}, {9, 11}, {2, 5}, {9, 12}, {3, 4}, {10, 11}, {3, 5}, {10, 12}, {4, 5}, {11, 12}, {5, 6}, {6, 7}, {7, 8}}|>;

(* ::Subsubsection:: *)
(*The Lab’s Wolfram cell*)

(* ::Text:: *)
(*Lin–Lu–Yau by the Münch–Wojciechowski linear programme, and λ₁ on Q₃:*)

(* Lin–Lu–Yau curvature (Münch–Wojciechowski LP) and the spectral gap *)
nbr[G_, v_] := AdjacencyList[G, v]; Δg[G_, f_][v_] := Mean[f /@ nbr[G, v]] - f[v];
κLLY[G_, {x_, y_}] := Module[{S, vars, f, cons}, S = Union[{x, y}, nbr[G, x], nbr[G, y]];
  vars = Table[Unique["f"], {Length[S]}]; f = AssociationThread[S -> vars];
  cons = Flatten[{f[y] - f[x] == 1, f[x] == 0, Table[With[{d = GraphDistance[G, S[[i]], S[[j]]]}, {f[S[[i]]] - f[S[[j]]] <= d, f[S[[j]]] - f[S[[i]]] <= d}], {i, Length[S]}, {j, i + 1, Length[S]}]}];
  LinearOptimization[Δg[G, f][x] - Δg[G, f][y], cons, vars, "PrimalMinimumValue"]];
G = HypercubeGraph[3]; A = N@AdjacencyMatrix[G]; d = Total[A];
{Union[κLLY[G, #] & /@ (List @@@ EdgeList[G])], Sort[Eigenvalues[IdentityMatrix[8] - DiagonalMatrix[d^(-1/2)] . A . DiagonalMatrix[d^(-1/2)]]][[2]]}

(* ::Text:: *)
(*Expected {{2/3}, 2/3}.*)

(* ::Subsubsection:: *)
(*All seven curvatures*)

(* ::Text:: *)
(*\!\(\*SubscriptBox[\(κ\), \(LLY\)]\) and κ₀ by optimal transport between the neighbourhood measures (LinearOptimization); K_∞ as the largest K with Γ₂ − KΓ ⪰ 0 on functions on the ball of radius 2, the quadratic forms built symbolically from Δ and the bound found by bisection on the least eigenvalue; resistance and Steinerberger curvature from pseudoinverses.*)

W1[G_, m1_, m2_] := Module[{s1 = Keys[m1], s2 = Keys[m2], x, vars, d},
   vars = Table[x[i, j], {i, Length[s1]}, {j, Length[s2]}];
   d = Table[GraphDistance[G, a, b], {a, s1}, {b, s2}];
   LinearOptimization[Total[d vars, 2], {Thread[Total[vars, {2}] == Values[m1]], Thread[Total[vars] == Values[m2]], Thread[Flatten[vars] >= 0]}, Flatten[vars], "PrimalMinimumValue"]];
μ[G_, v_, α_] := Merge[{<|v -> α|>, AssociationThread[AdjacencyList[G, v] -> (1 - α)/Length[AdjacencyList[G, v]]]}, Total];
κα[G_, {x_, y_}, α_] := 1 - W1[G, μ[G, x, α], μ[G, y, α]];
κLLYedge[G_, e_] := 2 κα[G, e, 1/2];   (* Bourne et al.: κ_LLY = 2 κ_(1/2) *)
κ0edge[G_, e_] := κα[G, e, 0];
formanE[G_, {x_, y_}] := 4 - VertexDegree[G, x] - VertexDegree[G, y];
formanT[G_, {x_, y_}] := formanE[G, {x, y}] + 3 Length[Intersection[AdjacencyList[G, x], AdjacencyList[G, y]]];
KBE[G_, x_] := Module[{B, n, e, f, lap, gam, q1, q2, M1, M2, lo = -10., hi = 10., mid},
   B = Union[{x}, AdjacencyList[G, x], Flatten[AdjacencyList[G, #] & /@ AdjacencyList[G, x]]]; n = Length[B];
   f = AssociationThread[B -> Array[e, n]];
   lap[v_] := Mean[f /@ AdjacencyList[G, v]] - f[v];
   gam[v_] := 1/2 Mean[(f[#] - f[v])^2 & /@ AdjacencyList[G, v]];
   q1 = gam[x]; q2 = 1/2 (Mean[gam /@ AdjacencyList[G, x]] - gam[x]) - 1/2 Mean[(f[#] - f[x]) (lap[#] - lap[x]) & /@ AdjacencyList[G, x]];
   M1 = D[q1, {Array[e, n], 2}]/2; M2 = D[q2, {Array[e, n], 2}]/2;
   (* K∞(x) is the largest K with Γ₂ − KΓ ⪰ 0 on functions on the 2-ball: bisect on the least eigenvalue *)
   Do[mid = (lo + hi)/2; If[Min[Eigenvalues[N[M2 - mid M1]]] >= -10^-10, lo = mid, hi = mid], {60}]; lo];
resistanceP[G_] := Module[{L = N@KirchhoffMatrix[G], P}, P = PseudoInverse[L];
   Table[1 - 1/2 Total[Function[j, P[[i, i]] + P[[j, j]] - 2 P[[i, j]]] /@ AdjacencyList[G, i]], {i, VertexCount[G]}]];
steinerbergerW[G_] := VertexCount[G] Total[PseudoInverse[N@GraphDistanceMatrix[G]], {2}];
normSpec[G_] := Module[{A = N@AdjacencyMatrix[G], d}, d = Total[A]; Sort[Eigenvalues[IdentityMatrix[Length[d]] - DiagonalMatrix[d^(-1/2)] . A . DiagonalMatrix[d^(-1/2)]]]];

curvs = <|"lly" -> {"Lin–Lu–Yau κ", "e", κLLYedge}, "k0" -> {"Ollivier κ₀", "e", κ0edge}, "be" -> {"Bakry–Émery K∞", "v", KBE},
   "forman" -> {"Forman", "e", formanE}, "formanAug" -> {"Forman + triangles", "e", formanT}, "res" -> {"resistance p", "all", resistanceP}, "stein" -> {"Steinerberger", "all", steinerbergerW}|>;
graphOf[g_] := Graph[Range[Max[graphEdges[g]]], UndirectedEdge @@@ graphEdges[g]];
wlValues[g_, k_] := With[{G = graphOf[g], c = curvs[k]}, Switch[c[[2]], "e", c[[3]][G, #] & /@ graphEdges[g], "v", c[[3]][G, #] & /@ VertexList[G], "all", c[[3]][G]]];
graphSummary[g_] := With[{sp = normSpec[graphOf[g]]}, Join[Table[With[{w = N[wlValues[g, k]]}, {If[k == "lly", g, ""], curvs[k][[1]], Min[w], Max[w], If[k == "res", Total[w], Mean[w]]}], {k, Keys[curvs]}],
   {{"", "λ₁ · λmax (normalised)", sp[[2]], sp[[-1]], ""}}]];
valGrid[{"graph", "curvature", "min", "max", "mean (sum for p)"}, graphSummary["dumbbell"]]

Column[{Style[#, Bold], valGrid[{"graph", "curvature", "min", "max", "mean (sum for p)"}, graphSummary[#]]}, Spacings -> 1] & /@ {"tree", "cycle", "cube", "complete", "petersen", "grid"} // Column

(* ::Subsubsection:: *)
(*The facts stated for each graph*)

val[g_, k_] := N[wlValues[g, k]]; edgeIdx[g_, pred_] := Position[graphEdges[g], _?pred, {1}, Heads -> False][[All, 1]];
treeG = graphOf["tree"]; leaves = Select[VertexList[treeG], VertexDegree[treeG, #] == 1 &];
<|"tree: interior edges κLLY" -> Union[Rationalize[val["tree", "lly"][[edgeIdx["tree", ! IntersectingQ[#, leaves] &]]], 10^-6]],
  "tree: leaf edges κLLY" -> Union[Rationalize[val["tree", "lly"][[edgeIdx["tree", IntersectingQ[#, leaves] &]]], 10^-6]],
  "tree: Steinerberger = c × resistance, with c and the largest residual" -> With[{w = val["tree", "stein"], p = val["tree", "res"]}, {w . p/p . p, Max[Abs[w - (w . p/p . p) p]]}],
  "tree: κLLY on the two edges at the root (degree 2)" -> Union[Rationalize[val["tree", "lly"][[edgeIdx["tree", MemberQ[#, 1] &]]], 10^-6]],
  "tree: resistance = distance" -> (Chop[Table[With[{P = PseudoInverse[N@KirchhoffMatrix[treeG]]}, P[[i, i]] + P[[j, j]] - 2 P[[i, j]]], {i, 15}, {j, 15}] - GraphDistanceMatrix[treeG], 10^-6] == ConstantArray[0, {15, 15}]),
  "C6: κLLY, κ0, K∞" -> (Union /@ Rationalize[{val["cycle", "lly"], val["cycle", "k0"], val["cycle", "be"]}, 10^-6]),
  "Q3: κLLY, K∞, λ1" -> {Union[Rationalize[val["cube", "lly"], 10^-6]], Union[Rationalize[val["cube", "be"], 10^-6]], Rationalize[normSpec[graphOf["cube"]][[2]], 10^-6]},
  "K5: κLLY, λ1" -> {Union[Rationalize[val["complete", "lly"], 10^-6]], Rationalize[normSpec[graphOf["complete"]][[2]], 10^-6]},
  "Petersen: κLLY, κ0, K∞, λ1" -> {Union[Rationalize[val["petersen", "lly"], 10^-6]], Union[Rationalize[val["petersen", "k0"], 10^-6]], Union[Rationalize[val["petersen", "be"], 10^-6]], Rationalize[normSpec[graphOf["petersen"]][[2]], 10^-6]},
  "grid: κLLY by the degrees of the edge's ends (corner 2, side 3, interior 4)" -> With[{deg = VertexDegree[graphOf["grid"]]},
     GroupBy[Transpose[{Sort[deg[[#]]] & /@ graphEdges["grid"], Rationalize[val["grid", "lly"], 10^-6]}], First -> Last, Union]],
  "dumbbell: κLLY on the three bridge edges" -> Rationalize[val["dumbbell", "lly"][[-3 ;;]], 10^-6]|>

(* ::Text:: *)
(*On the tree the interior edges have \!\(\*SubscriptBox[\(κ\), \(LLY\)]\) = −2/3 except the two at the root, whose end has degree 2 (−1/3), and the leaf edges +2/3. On a tree effective resistance equals distance, and Steinerberger curvature is exactly 2n/(n − 1) = 15/7 times resistance curvature: the inverse distance matrix of a tree is −½L + ττᵀ/(2(n − 1)) with τ = 2 − degree (Graham–Lovász), so D⁻¹1 = τ/(n − 1) and p = τ/2. C₆ is flat for all three. Q₃ has \!\(\*SubscriptBox[\(κ\), \(LLY\)]\) = K_∞ = λ₁ = 2/3 and K₅ has \!\(\*SubscriptBox[\(κ\), \(LLY\)]\) = λ₁ = 5/4: equality cases of λ₁ ≥ κ. Petersen has \!\(\*SubscriptBox[\(κ\), \(LLY\)]\) = 0, κ₀ = −1/3, K_∞ = −1/3, λ₁ = 2/3. On the grid \!\(\*SubscriptBox[\(κ\), \(LLY\)]\) is 0 on interior edges and along the sides, +1/6 on edges from a side inward and +1/3 at the corners. On the dumbbell the two edges joining a clique to the path have \!\(\*SubscriptBox[\(κ\), \(LLY\)]\) = −3/5, the middle edge 0.*)

(* the two discrete Lichnerowicz bounds and Foster's theorem, on every graph *)
Table[With[{G = graphOf[g]}, {g, normSpec[G][[2]] >= Min[val[g, "lly"]] - 10^-9, normSpec[G][[2]] >= Min[val[g, "be"]] - 10^-6, Chop[Total[val[g, "res"]] - 1, 10^-9] == 0}], {g, Keys[graphEdges]}] //
 Grid[Prepend[#, Style[#, Bold] & /@ {"graph", "λ₁ ≥ min κLLY", "λ₁ ≥ min K∞", "Σ p = 1 (Foster)"}], Frame -> All] &

(* ::Subsection:: *)
(*7.3 Figures and animator*)

kScale = <|"lly" -> 1.25, "k0" -> 1, "be" -> 1, "forman" -> 6, "formanAug" -> 6, "res" -> 0.3, "stein" -> 1.5|>;
graphPicture[g_, k_] := Module[{G = graphOf[g], vals = N[wlValues[g, k]], e = UndirectedEdge @@@ graphEdges[g], s = kScale[k]},
   If[curvs[k][[2]] == "e",
    Graph[G, EdgeStyle -> Thread[e -> (Directive[kcol[#, s], AbsoluteThickness[5]] & /@ vals)], VertexStyle -> GrayLevel[0.6], VertexSize -> 0.2, PlotLabel -> g, ImageSize -> 190],
    Graph[G, VertexStyle -> Thread[VertexList[G] -> (kcol[#, s] & /@ vals)], VertexSize -> 0.35, EdgeStyle -> GrayLevel[0.7], PlotLabel -> g, ImageSize -> 190]]];
Legended[Grid[Partition[graphPicture[#, "lly"] & /@ Keys[graphEdges], 4, 4, 1, ""]], kLegend[1.25, Subscript["κ", "LLY"]]]

(* ::Text:: *)
(*Fig. 9. The seven graphs with every edge coloured by its Lin–Lu–Yau curvature: the tree and the dumbbell’s bridge are blue, the cube and K₅ orange, C₆ and Petersen white.*)

Legended[Grid[Partition[graphPicture[#, "be"] & /@ Keys[graphEdges], 4, 4, 1, ""]], kLegend[1, Subscript["K", "∞"]]]

(* ::Text:: *)
(*Fig. 10. The same graphs with every vertex coloured by its Bakry–Émery curvature K_∞.*)

(* ::Text:: *)
(*The animator: pick a graph and a curvature; the readout gives min, max, mean (sum for resistance curvature) and the spectral bounds.*)

With[{graphs = Keys[graphEdges], curvatures = Normal[curvs[[All, 1]]]},
 Manipulate[With[{w = N[wlValues[mGraph, mCurv]], sp = normSpec[graphOf[mGraph]]},
   Column[{Legended[graphPicture[mGraph, mCurv], kLegend[kScale[mCurv], curvs[mCurv][[1]]]],
     Grid[{{"min", Min[w]}, {"max", Max[w]}, {If[mCurv == "res", "sum", "mean"], If[mCurv == "res", Total[w], Mean[w]]}, {"λ₁ (normalised)", sp[[2]]}, {"λmax", sp[[-1]]},
       {"λ₁ ≥ min κLLY", sp[[2]] >= Min[N[wlValues[mGraph, "lly"]]] - 10^-9}}, Alignment -> Left]}]],
  {{mGraph, "dumbbell", "graph"}, graphs}, {{mCurv, "lly", "curvature"}, curvatures}, SaveDefinitions -> True]]

(* ::Section:: *)
(*8. Mean-curvature flow: a curve rounds itself off*)

(* ::Text:: *)
(*∂X/∂t = ΔX = κN.*)

(* ::Text:: *)
(*In the plane any embedded closed curve becomes convex, then round, and shrinks to a point (Gage–Hamilton–Grayson). The area falls at exactly 2π per unit time, because ∮κ ds = 2π. A polygon is moved by the cycle-graph Laplacian weighted by arc length: vertex i moves by k(\!\(\*SubscriptBox[\(t\), \(f\)]\) − \!\(\*SubscriptBox[\(t\), \(b\)]\)) with k = 2/(ℓ_f + \!\(\*SubscriptBox[\(ℓ\), \(b\)]\)), ℓ the lengths and t the unit directions of the edges out of and into it.*)

(* ::Subsection:: *)
(*8.1 Worked by hand*)

(* ::Text:: *)
(*Why the area falls at 2π. For a closed embedded plane curve moving by ∂X/∂t = κN (N the inward normal), the area changes by dA/dt = −∮κ ds, and ∮κ ds is the total turning of the tangent, 2π for any simple closed curve (Hopf’s Umlaufsatz). So A(t) = A₀ − 2πt, independent of the shape, and the curve vanishes at t = A₀/2π: 3.3934/2π = 0.540 for the wiggly start.*)

(* ::Text:: *)
(*The polygon’s rate. Vertex i moves by k(\!\(\*SubscriptBox[\(t\), \(f\)]\) − \!\(\*SubscriptBox[\(t\), \(b\)]\)) with k = 2/(ℓ_f + \!\(\*SubscriptBox[\(ℓ\), \(b\)]\)), where \!\(\*SubscriptBox[\(t\), \(b\)]\), \!\(\*SubscriptBox[\(t\), \(f\)]\) are the unit directions of the edges into and out of it. The area swept per unit time near vertex i is that velocity’s inward component times (\!\(\*SubscriptBox[\(ℓ\), \(f\)]\) + ℓ_b)/2, which is |\!\(\*SubscriptBox[\(t\), \(f\)]\) − \!\(\*SubscriptBox[\(t\), \(b\)]\)| = 2 sin(θ_i/2), \!\(\*SubscriptBox[\(θ\), \(i\)]\) the turning angle. So dA/dt = −Σ 2 sin(θ_i/2), slightly less than \!\(\*SubscriptBox[\(Σθ\), \(i\)]\) = 2π; for a regular 160-gon it is −320 sin(π/160) = −6.2828 against −2π = −6.2832.*)

(* ::Text:: *)
(*Sphere under mean-curvature flow. A sphere of radius R has H = 1/R (the mean of the two principal curvatures) and ΔX = −2H n, so dR/dt = −2/R, R dR = −2 dt and R² = R₀² − 4t: the snippet’s √(R₀² − 4t), with residual 0.*)

(* ::Subsection:: *)
(*8.2 Checks on the kernel*)

(* ::Subsubsection:: *)
(*The Lab’s Wolfram cell*)

(* ::Text:: *)
(*Exact flows: the round sphere under Ricci flow, and a sphere of radius √(R₀² − 4t) under mean-curvature flow (both residuals 0):*)

ClearAll[t];  (* t is a variable here *)

(* exact flows: Ricci flow on the round sphere, mean-curvature flow of a sphere *)
{Simplify[D[Sqrt[R0^2 - 4 t], t] + 2/Sqrt[R0^2 - 4 t]], Simplify[D[(1 - 2 t) {{1, 0}, {0, Sin[θ]^2}}, t] + 2 {{1, 0}, {0, Sin[θ]^2}}]}

(* ::Subsubsection:: *)
(*The polygon flow on four starting curves*)

(* ::Text:: *)
(*Explicit steps of at most 0.2 × (shortest edge)², the stability limit of an explicit heat step; every 20 steps the polygon is resampled by arc length when 160 × (perimeter/initial perimeter) vertices (at least 24) is under 85% of the current count, or when the longest edge exceeds three times the shortest. Run until the area is below 8% of its start; the mean dA/dt should be −2π = −6.2832.*)

curveInit[kind_, n_: 160] := Module[{f = <|"wiggle" -> (1 + 0.35 Cos[3 #] + 0.2 Sin[5 #] &), "star" -> (1 + 0.45 Cos[5 #] &),
      "ellipse" -> (1/Sqrt[Cos[#]^2/1.6 + Sin[#]^2 1.6] &), "bean" -> (1 + 0.5 Cos[2 #] Sin[#] + 0.25 Cos[3 #] &)|>[kind]},
   Table[With[{t = 2. π k/n}, f[t] {Cos[t], Sin[t]}], {k, 0, n - 1}]];
curveStep[X_, dt_] := Module[{fw = RotateLeft[X] - X, bw = X - RotateRight[X], lf, lb},
   lf = Norm /@ fw; lb = Norm /@ bw; X + dt (2/(lf + lb)) (fw/lf - bw/lb)];
perimeter[X_] := Total[Norm /@ (RotateLeft[X] - X)];
polyArea[X_] := Abs[Total[X[[All, 1]] RotateLeft[X][[All, 2]] - RotateLeft[X][[All, 1]] X[[All, 2]]]]/2;
resample[X_, n_] := Module[{c = Append[X, First[X]], s, L, f}, s = Accumulate[Prepend[Norm /@ Differences[c], 0.]]; L = Last[s];
   f = Interpolation[Transpose[{s, #}], InterpolationOrder -> 1] & /@ Transpose[c]; Table[Through[f[L i/n]], {i, 0, n - 1}]];
flowRun[kind_] := Module[{X = curveInit[kind], A0, L0, t = 0., k = 0, h, dt, hist = {}, frames = {}},
   A0 = polyArea[X]; L0 = perimeter[X]; hist = {{0., A0}}; frames = {X};
   While[polyArea[X] > 0.08 A0, h = Min[Norm /@ (RotateLeft[X] - X)]; dt = 0.2 h^2; X = curveStep[X, dt]; t += dt; k++;
    If[Mod[k, 40] == 0, AppendTo[hist, {t, polyArea[X]}]; AppendTo[frames, X]];
    If[Mod[k, 20] == 0, With[{e = Norm /@ (RotateLeft[X] - X), target = Max[24, Min[160, Round[160 perimeter[X]/L0]]]},
      If[target < 0.85 Length[X] || Max[e] > 3 Min[e], X = resample[X, target]]]]];
   <|"t" -> t, "rate" -> (polyArea[X] - A0)/t, "vertices" -> Length[X], "X" -> X, "A0" -> A0, "hist" -> Append[hist, {t, polyArea[X]}], "frames" -> Append[frames, X]|>];
runs = AssociationMap[flowRun, {"wiggle", "star", "bean", "ellipse"}];
valGrid[{"start", "mean dA/dt", "t when area < 8%", "vertices at the end"}, {#, runs[#, "rate"], runs[#, "t"], runs[#, "vertices"]} & /@ Keys[runs]]

(* ::Text:: *)
(*All four rates are within about 0.5% of −2π. The small excess is the area lost at each resampling (it cuts corners); between resamplings the polygon’s rate is −Σ 2 sin(θ_i/2) over its turning angles \!\(\*SubscriptBox[\(θ\), \(i\)]\), just under 2π.*)

Row[Table[Graphics[{RGBColor[0.98, 0.56, 0.17], Thickness[0.012], Line[Append[#, First[#]] &[runs[k, "X"]]]}, PlotLabel -> k, ImageSize -> 140, PlotRange -> 0.45], {k, Keys[runs]}], "  "]

(* ::Text:: *)
(*Fig. 11. The last frame of curve shortening for the four starting curves: smooth near-circles.*)

(* ::Subsection:: *)
(*8.3 Figures and animator*)

Row[{ListLinePlot[Table[runs[k, "hist"], {k, Keys[runs]}], PlotStyle -> {orange, blue, Darker[Green], Purple}, PlotLegends -> Keys[runs],
    Epilog -> {Dashed, GrayLevel[0.5], Line[{{0, runs["wiggle", "A0"]}, {runs["wiggle", "A0"]/(2 π), 0}}]}, AxesLabel -> {"t", "area"}, ImageSize -> 360],
   Graphics[{Table[{Opacity[0.25 + 0.75 j/6], orange, Line[Append[#, First[#]] &[runs["wiggle", "frames"][[Round[1 + (Length[runs["wiggle", "frames"]] - 1) j/6]]]]]}, {j, 0, 6}]},
    PlotLabel -> "wiggly start, seven moments", ImageSize -> 260]}]

(* ::Text:: *)
(*Fig. 12. Area against time for the four starting curves, with the line of slope −2π from the wiggly start (dashed), and the wiggly curve at seven moments: it becomes convex, then round, and shrinks to a point.*)

With[{starts = Keys[runs], nFrames = Max[Length[runs[#, "frames"]] & /@ Keys[runs]]},
 Manipulate[With[{fr = runs[mStart, "frames"]}, With[{X = fr[[Min[mFrame, Length[fr]]]]},
    Graphics[{Dashed, GrayLevel[0.6], Line[Append[fr[[1]], First[fr[[1]]]]], Dashing[{}], orange, Thickness[0.008], Line[Append[X, First[X]]]},
     PlotRange -> 1.6, ImageSize -> 380, PlotLabel -> Row[{"area ", NumberForm[polyArea[X], 4], ",  vertices ", Length[X]}]]]],
  {{mStart, "wiggle", "start"}, starts}, {{mFrame, 1, "frame"}, 1, nFrames, 1, ControlType -> Animator, AnimationRate -> 10}, SaveDefinitions -> True]]

(* ::Section:: *)
(*9. Comparing two ball averages measures Ricci curvature*)

(* ::Text:: *)
(*κ(x, y) = 1 − W₁(\!\(\*SubscriptBox[\(μ\), \(x\)]\), μ_y)/d(x, y),        κ ≈ ε² Ric(v, v)/(2(n + 2)) = ε²K/8 on a surface,*)

(* ::Text:: *)
(*with μ uniform on ε-balls (Ollivier). Sliding the surface along the geodesic carries one ball onto the other, and a point at distance λ from the geodesic moves δ cos(√K λ), so κ is a plain integral over the ball.*)

(* ::Subsection:: *)
(*9.1 Worked by hand*)

(* ::Text:: *)
(*Slide the surface a distance δ along the geodesic from x to y. A point of the ball at distance λ from the geodesic moves δ cos(√K λ) ≈ δ(1 − Kλ²/2) on a surface of curvature K (geodesics at distance λ converge or spread like cos √K λ). This sliding carries \!\(\*SubscriptBox[\(μ\), \(x\)]\) onto \!\(\*SubscriptBox[\(μ\), \(y\)]\), and for small balls it is the optimal plan, so W₁(\!\(\*SubscriptBox[\(μ\), \(x\)]\), \!\(\*SubscriptBox[\(μ\), \(y\)]\)) ≈ δ(1 − K⟨λ²⟩/2), with ⟨λ²⟩ the mean of λ² over the ball.*)

(* ::Text:: *)
(*In polar coordinates (ρ, α) about x, λ = ρ|sin α|, and the mean of ρ² sin²α over a flat disc of radius ε is (ε²/2)(1/2) = ε²/4. So W₁ ≈ δ(1 − Kε²/8), and κ = 1 − W₁/δ ≈ Kε²/8: 0.125 for the unit sphere. At ε = 0.05, κ/ε² = 0.12496 = 1/8 − 0.000039 (table in §9.2); the correction is of order ε², from the curvature of the ball itself.*)

(* ::Subsection:: *)
(*9.2 Checks on the kernel*)

(* ::Subsubsection:: *)
(*The Lab’s Wolfram cell*)

(* ::Text:: *)
(*κ/ε² → K/8 on S² and H²:*)

(* Ollivier curvature of ε-balls: κ/ε² → K/8 on S² and H² *)
κS2[ε_?NumericQ] := NIntegrate[With[{s = Sin[ρ] Sin[α]}, s^2/(1 + Sqrt[1 - s^2])] Sin[ρ], {ρ, 0, ε}, {α, 0, 2 π}]/(2 π (1 - Cos[ε]));
κH2[ε_?NumericQ] := -NIntegrate[With[{s = Sinh[ρ] Sin[α]}, s^2/(1 + Sqrt[1 + s^2])] Sinh[ρ], {ρ, 0, ε}, {α, 0, 2 π}]/(2 π (Cosh[ε] - 1));
Table[{ε, κS2[ε]/ε^2, κH2[ε]/ε^2}, {ε, {0.05, 0.2, 0.8}}]

(* ::Subsubsection:: *)
(*κ/ε² for five curvatures*)

κball[K_, ε_?NumericQ] := κball[K, ε] = Which[K == 0, 0, K > 0, With[{R = 1/Sqrt[K]},
     NIntegrate[With[{s = Sin[ρ/R] Sin[α]}, s^2/(1 + Sqrt[1 - s^2])] Sin[ρ/R], {ρ, 0, ε}, {α, 0, 2 π}, PrecisionGoal -> 10]/NIntegrate[Sin[ρ/R] 2 π, {ρ, 0, ε}]],
   True, With[{R = 1/Sqrt[-K]}, -NIntegrate[With[{s = Sinh[ρ/R] Sin[α]}, s^2/(1 + Sqrt[1 + s^2])] Sinh[ρ/R], {ρ, 0, ε}, {α, 0, 2 π}, PrecisionGoal -> 10]/NIntegrate[Sinh[ρ/R] 2 π, {ρ, 0, ε}]]];
emax[K_] := If[K == 0, 1.2, Min[1.2, 0.9 π/Sqrt[Abs[K]]/2]];
valGrid[{"K", "κ/ε² at ε = 0.05", "K/8", "largest ε drawn", "κ/ε² there"}, Table[{K, κball[K, 0.05]/0.05^2, K/8, emax[K], κball[K, emax[K]]/emax[K]^2}, {K, {-2, -1, 0, 1, 2}}]]

(* ::Subsection:: *)
(*9.3 Figures and animator*)

(* the same integral as κball at plotting accuracy (six digits), on twelve values of ε *)
κfast[K_, ε_?NumericQ] := Which[K == 0, 0, K > 0, With[{R = 1/Sqrt[K]},
     Quiet@NIntegrate[With[{s = Sin[ρ/R] Sin[α]}, s^2/(1 + Sqrt[1 - s^2])] Sin[ρ/R], {ρ, 0, ε}, {α, 0, 2 π}, PrecisionGoal -> 6]/(2 π R (1 - Cos[ε/R]))],
   True, With[{R = 1/Sqrt[-K]}, -Quiet@NIntegrate[With[{s = Sinh[ρ/R] Sin[α]}, s^2/(1 + Sqrt[1 + s^2])] Sinh[ρ/R], {ρ, 0, ε}, {α, 0, 2 π}, PrecisionGoal -> 6]/(2 π R (Cosh[ε/R] - 1))]];
ollPlot[K_] := With[{emax = If[K == 0, 1.2, Min[1.2, 0.9 π/Sqrt[Abs[K]]/2]]},
   ListLinePlot[Table[{e, κfast[K, e]/e^2}, {e, emax/12, emax, emax/12}], PlotStyle -> If[K >= 0, orange, blue], PlotRange -> {-Max[0.05, 1.6 Abs[K]/8], Max[0.05, 1.6 Abs[K]/8]},
    Epilog -> {Dashed, GrayLevel[0.5], Line[{{0, K/8}, {emax, K/8}}]}, AxesLabel -> {"ε", "κ/ε^2"}, PlotLabel -> Row[{"K = ", K}], ImageSize -> 300]];
Row[{ollPlot[1], ollPlot[0], ollPlot[-1]}]

(* ::Text:: *)
(*Fig. 13. Ollivier curvature of ε-balls divided by ε², against ε, for K = 1, 0 and −1; the dashed line is K/8.*)

Manipulate[ollPlot[mK], {{mK, 1, "K"}, -2, 2, 0.25, Appearance -> "Labeled"}, SaveDefinitions -> True]

(* ::Section:: *)
(*10. Every Laplacian–curvature relationship on one sheet*)

(* ::Text:: *)
(*The sheet restates formulas checked in the sections above and in the write-up notebook (LaplacianCurvature.nb §2–§10). Two further Wolfram cells of the Lab, and the ball-volume line of the sheet:*)

(* ::Subsubsection:: *)
(*Yamabe: u⁴ times the flat metric of ℝ³ is the round S³, scalar curvature 6*)

(* Yamabe: u^4 times the flat metric of R^3 is the round S^3, scalar curvature 6 *)
uY = (2/(1 + x^2 + y^2 + z^2))^(1/2); Simplify[-8 uY^-5 Laplacian[uY, {x, y, z}]]

(* ::Subsubsection:: *)
(*Weitzenböck on S²: \!\(\*SubscriptBox[\(Δ\), \(Hodge\)]\) ω − ∇*∇ω = Ric(ω) = ω for every 1-form df + ⋆dh (must return {0, 0})*)

(* Weitzenböck on S²: Hodge Laplacian ω − ∇*∇ω = Ric(ω) = ω for every 1-form df + ⋆dh *)
X = {θ, φ}; g = {{1, 0}, {0, Sin[θ]^2}}; gi = Inverse[g];
Γ = Table[1/2 Sum[gi[[i, l]] (D[g[[l, j]], X[[k]]] + D[g[[l, k]], X[[j]]] - D[g[[j, k]], X[[l]]]), {l, 2}], {i, 2}, {j, 2}, {k, 2}];
Lap[w_] := 1/Sin[θ] (D[Sin[θ] D[w, θ], θ] + D[w, φ, φ]/Sin[θ]);
rough[ω_] := Module[{T, TT}, T = Table[D[ω[[i]], X[[j]]] - Sum[Γ[[k, i, j]] ω[[k]], {k, 2}], {i, 2}, {j, 2}];
  TT = Table[D[T[[i, j]], X[[k]]] - Sum[Γ[[m, k, i]] T[[m, j]] + Γ[[m, k, j]] T[[i, m]], {m, 2}], {i, 2}, {j, 2}, {k, 2}];
  Table[-Sum[gi[[j, k]] TT[[i, j, k]], {j, 2}, {k, 2}], {i, 2}]];
d1[w_] := {D[w, θ], D[w, φ]}; star[{a_, b_}] := {-b/Sin[θ], a Sin[θ]};
ω = d1[\[ScriptF][θ, φ]] + star[d1[\[ScriptH][θ, φ]]];
Simplify[d1[-Lap[\[ScriptF][θ, φ]]] + star[d1[-Lap[\[ScriptH][θ, φ]]]] - (rough[ω] + ω)]

(* ::Subsubsection:: *)
(*Ball volume*)

(* the ball-volume line of the sheet, n = 2 and n = 3 on spheres of curvature K: Vol B_r = ω_n r^n (1 − S r²/(6(n + 2)) + …), S = n(n − 1)K *)
{Series[2 π (1 - Cos[Sqrt[K] r])/K/(π r^2), {r, 0, 2}], Series[4 π/K^(3/2) (Sqrt[K] r/2 - Sin[2 Sqrt[K] r]/4)/(4/3 π r^3), {r, 0, 2}], {1 - 2 K r^2/(6 4), 1 - 6 K r^2/(6 5)}}

(* ::Section:: *)
(*11. Self-check: the answers*)

tK = Simplify[(Cos[v]/(1 (2 + 1 Cos[v])))];
<|"1. torus K < 0 on the inner half" -> Reduce[tK < 0 && 0 <= v < 2 π, v],
  "1. ∬K dA on the torus" -> Integrate[tK (2 + Cos[v]), {u, 0, 2 π}, {v, 0, 2 π}],
  "2. order at which K enters the circle mean (coefficient of K)" -> (Coefficient[r^2/4 d1 + r^4 (d2/64 + K d1/96) + r^6 (d3/2304 + K d2/1152 + K^2 d1/1440), K] /. {d1 -> 1, d2 -> 1, d3 -> 1} // Expand),
  "3. heat trace t-term on the unit sphere: ratio − 1 ≈ t/3 = (1/6)∫S/Area" -> {N[sph[0.001] - 1, 6], 0.001/3},
  "6. Σ resistance curvature on every graph" -> (Round[Total[val[#, "res"]], 10^-9] & /@ Keys[graphEdges]),
  "7. dA/dt for the four curves" -> (runs[#, "rate"] & /@ Keys[runs]),
  "8. ∂u/∂t = −K under 2-D Ricci flow" -> "§2 above"|>

(* ::Text:: *)
(*Question 4 (Bakry–Émery copies Bochner, Γ₂ ≥ KΓ) and question 5 (the dumbbell’s bridge is negative because its two neighbourhoods barely overlap) are checked in §5 and §7.*)

(* ::Section:: *)
(*Production Notes*)

(* ::Text:: *)
(*How the Lab page computes, and every number it prints set beside Wolfram’s. The page computes in the browser with JavaScript (lab/core.js, driven by lab/app.js). The association page below holds its readouts at the default settings and for every choice of every selector; it is produced by running lab/core.js under Node exactly as the browser runs it (tools/lab_nb/js_readouts.js). Each table gives the page value, the Wolfram value from the sections above, and their difference. Evaluate the sections above first.*)

page = <|"surfaces" -> <|"sphere" -> <|"kmin" -> 1.00000049942, "kmax" -> 1.00000050055, "hmax" -> 1.00000025028, "total" -> 12.5640562371|>, "cylinder" -> <|"kmin" -> 0, "kmax" -> 0, "hmax" -> 0.500000125097, "total" -> 0|>, "torus" -> <|"kmin" -> -1.00000050023, "kmax" -> 0.333333500354, "hmax" -> 0.666666833778, "total" -> 4.25303153589*^-10|>, "saddle" -> <|"kmin" -> -4, "kmax" -> -0.0493827160358, "hmax" -> 0.384874056641, "total" -> -3.70920926624|>, "catenoid" -> <|"kmin" -> -1.00000033333, "kmax" -> -0.0930371859697, "hmax" -> 9.39088820888*^-8, "total" -> -10.4760732021|>, "pseudosphere" -> <|"kmin" -> -1.00000033401, "kmax" -> -1.0000003307, "hmax" -> 6.20297269919, "total" -> -5.63913102461|>|>, "ricci" -> <|"a" -> 0.3, "b" -> 0.249, "N" -> 32, "maxK0" -> 4.63274553095, "t" -> 2.00336484118, "maxK" -> 0.0589607806405, "totalK" -> -2.27388738831*^-17, "start" -> <|"t" -> 0, "area" -> 44.4643488708, "energy" -> 5.36072886058, "K2" -> 38.1791657969, "entropy" -> 3.56080482591, "umin" -> -0.507209863349, "umax" -> 0.507209863349, "kmin" -> -4.63274553095, "kmax" -> 1.28912204446|>, "end" -> <|"t" -> 2.00336484118, "area" -> 44.4867486686, "energy" -> 0.0485751778654, "K2" -> 0.0434005817792, "entropy" -> 3.67329926729, "umin" -> 0.00753501592274, "umax" -> 0.122834499805, "kmin" -> -0.0432199320327, "kmax" -> 0.0589607806405|>|>, "rd" -> <|"blowT" -> 1.32496109544, "blowMax" -> 60.3575681887, "heatEnd" -> 0.607308263911|>, "means" -> <|"slopes" -> {3.92190148003, 5.99748062687, 8.00540743523}, "pole" -> <|"f" -> 4, "d1" -> -4, "d2" -> -20, "d3" -> 500|>|>, "heat" -> {<|"t" -> 0.01, "sphere" -> 1.00334001273, "series" -> 1.00334, "torus" -> 1|>, <|"t" -> 0.05, "sphere" -> 1.01683494085, "series" -> 1.01683333333, "torus" -> 1|>, <|"t" -> 0.1, "sphere" -> 1.03401302802, "series" -> 1.034, "torus" -> 1|>}, "mesh" -> {<|"nu" -> 12, "nv" -> 6, "vertices" -> 72, "defect" -> -1.11022302463*^-16, "err" -> 0.133157452146, "Kouter" -> 0.356935166763|>, <|"nu" -> 24, "nv" -> 12, "vertices" -> 288, "defect" -> -3.25295346215*^-14, "err" -> 0.0420201151318, "Kouter" -> 0.338628019448|>, <|"nu" -> 40, "nv" -> 20, "vertices" -> 800, "defect" -> -2.64344102163*^-13, "err" -> 0.0159537754306, "Kouter" -> 0.335189630252|>, <|"nu" -> 64, "nv" -> 32, "vertices" -> 2048, "defect" -> -6.07403016772*^-13, "err" -> 0.00634882194803, "Kouter" -> 0.334051663552|>}, "graphs" -> <|"tree" -> <|"n" -> 15, "edges" -> {{1, 2}, {1, 3}, {2, 4}, {2, 5}, {3, 6}, {3, 7}, {4, 8}, {4, 9}, {5, 10}, {5, 11}, {6, 12}, {6, 13}, {7, 14}, {7, 15}}, "lambda1" -> 0.0571909584179, "lambdaMax" -> 2, "lly" -> {-0.333333333333, -0.333333333333, -0.666666666667, -0.666666666667, -0.666666666667, -0.666666666667, 0.666666666667, 0.666666666667, 0.666666666667, 0.666666666667, 0.666666666667, 0.666666666667, 0.666666666667, 0.666666666667}, "k0" -> {-0.333333333333, -0.333333333333, -0.666666666667, -0.666666666667, -0.666666666667, -0.666666666667, 0, 0, 0, 0, 0, 0, 0, 0}, "be" -> {-0.333334, -0.333334, -0.333334, -0.124094, -0.124094, -0.124094, -0.124094, 0.666666, 0.666666, 0.666666, 0.666666, 0.666666, 0.666666, 0.666666, 0.666666}, "forman" -> {-1, -1, -2, -2, -2, -2, 0, 0, 0, 0, 0, 0, 0, 0}, "formanAug" -> {-1, -1, -2, -2, -2, -2, 0, 0, 0, 0, 0, 0, 0, 0}, "res" -> {-4.4408920985*^-16, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5}, "stein" -> {-1.81694936874*^-14, -1.07142857143, -1.07142857143, -1.07142857143, -1.07142857143, -1.07142857143, -1.07142857143, 1.07142857143, 1.07142857143, 1.07142857143, 1.07142857143, 1.07142857143, 1.07142857143, 1.07142857143, 1.07142857143}|>, "cycle" -> <|"n" -> 6, "edges" -> {{1, 2}, {2, 3}, {3, 4}, {4, 5}, {5, 6}, {6, 1}}, "lambda1" -> 0.5, "lambdaMax" -> 2, "lly" -> {0, 0, 0, 0, 0, 0}, "k0" -> {0, 0, 0, 0, 0, 0}, "be" -> {0, 0, 0, 0, 0, 0}, "forman" -> {0, 0, 0, 0, 0, 0}, "formanAug" -> {0, 0, 0, 0, 0, 0}, "res" -> {0.166666666667, 0.166666666667, 0.166666666667, 0.166666666667, 0.166666666667, 0.166666666667}, "stein" -> {0.666666666667, 0.666666666667, 0.666666666667, 0.666666666667, 0.666666666667, 0.666666666667}|>, "cube" -> <|"n" -> 8, "edges" -> {{1, 2}, {1, 3}, {1, 5}, {2, 4}, {2, 6}, {3, 4}, {3, 7}, {4, 8}, {5, 6}, {5, 7}, {6, 8}, {7, 8}}, "lambda1" -> 0.666666666667, "lambdaMax" -> 2, "lly" -> {0.666666666667, 0.666666666667, 0.666666666667, 0.666666666667, 0.666666666667, 0.666666666667, 0.666666666667, 0.666666666667, 0.666666666667, 0.666666666667, 0.666666666667, 0.666666666667}, "k0" -> {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, "be" -> {0.666666, 0.666666, 0.666666, 0.666666, 0.666666, 0.666666, 0.666666, 0.666666}, "forman" -> {-2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2}, "formanAug" -> {-2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2}, "res" -> {0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125}, "stein" -> {0.666666666667, 0.666666666667, 0.666666666667, 0.666666666667, 0.666666666667, 0.666666666667, 0.666666666667, 0.666666666667}|>, "complete" -> <|"n" -> 5, "edges" -> {{1, 2}, {1, 3}, {1, 4}, {1, 5}, {2, 3}, {2, 4}, {2, 5}, {3, 4}, {3, 5}, {4, 5}}, "lambda1" -> 1.25, "lambdaMax" -> 1.25, "lly" -> {1.25, 1.25, 1.25, 1.25, 1.25, 1.25, 1.25, 1.25, 1.25, 1.25}, "k0" -> {0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75}, "be" -> {0.875, 0.875, 0.875, 0.875, 0.875}, "forman" -> {-4, -4, -4, -4, -4, -4, -4, -4, -4, -4}, "formanAug" -> {5, 5, 5, 5, 5, 5, 5, 5, 5, 5}, "res" -> {0.2, 0.2, 0.2, 0.2, 0.2}, "stein" -> {1.25, 1.25, 1.25, 1.25, 1.25}|>, "petersen" -> <|"n" -> 10, "edges" -> {{1, 2}, {1, 6}, {6, 8}, {2, 3}, {2, 7}, {7, 9}, {3, 4}, {3, 8}, {8, 10}, {4, 5}, {4, 9}, {9, 6}, {5, 1}, {5, 10}, {10, 7}}, "lambda1" -> 0.666666666667, "lambdaMax" -> 1.66666666667, "lly" -> {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, "k0" -> {-0.333333333333, -0.333333333333, -0.333333333333, -0.333333333333, -0.333333333333, -0.333333333333, -0.333333333333, -0.333333333333, -0.333333333333, -0.333333333333, -0.333333333333, -0.333333333333, -0.333333333333, -0.333333333333, -0.333333333333}, "be" -> {-0.333334, -0.333334, -0.333334, -0.333334, -0.333334, -0.333334, -0.333334, -0.333334, -0.333334, -0.333334}, "forman" -> {-2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2}, "formanAug" -> {-2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2}, "res" -> {0.1, 0.1, 0.0999999999999, 0.1, 0.1, 0.1, 0.1, 0.1, 0.0999999999999, 0.1}, "stein" -> {0.666666666667, 0.666666666667, 0.666666666667, 0.666666666667, 0.666666666667, 0.666666666667, 0.666666666667, 0.666666666667, 0.666666666667, 0.666666666667}|>, "grid" -> <|"n" -> 25, "edges" -> {{1, 2}, {1, 6}, {2, 3}, {2, 7}, {3, 4}, {3, 8}, {4, 5}, {4, 9}, {5, 10}, {6, 7}, {6, 11}, {7, 8}, {7, 12}, {8, 9}, {8, 13}, {9, 10}, {9, 14}, {10, 15}, {11, 12}, {11, 16}, {12, 13}, {12, 17}, {13, 14}, {13, 18}, {14, 15}, {14, 19}, {15, 20}, {16, 17}, {16, 21}, {17, 18}, {17, 22}, {18, 19}, {18, 23}, {19, 20}, {19, 24}, {20, 25}, {21, 22}, {22, 23}, {23, 24}, {24, 25}}, "lambda1" -> 0.131300889668, "lambdaMax" -> 2, "lly" -> {0.333333333333, 0.333333333333, 0, 0.166666666667, 0, 0.166666666667, 0.333333333333, 0.166666666667, 0.333333333333, 0.166666666667, 0, 0, 0, 0, 0, 0.166666666667, 0, 0, 0.166666666667, 0, 0, 0, 0, 0, 0.166666666667, 0, 0, 0.166666666667, 0.333333333333, 0, 0.166666666667, 0, 0.166666666667, 0.166666666667, 0.166666666667, 0.333333333333, 0.333333333333, 0, 0, 0.333333333333}, "k0" -> {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, "be" -> {0.333333, 0.087613, -0.04762, 0.087613, 0.333333, 0.087613, 0.121608, 0.035714, 0.121608, 0.087613, -0.04762, 0.035714, 0, 0.035714, -0.04762, 0.087613, 0.121608, 0.035714, 0.121608, 0.087613, 0.333333, 0.087613, -0.04762, 0.087613, 0.333333}, "forman" -> {-1, -1, -2, -3, -2, -3, -1, -3, -1, -3, -2, -4, -4, -4, -4, -3, -4, -2, -3, -2, -4, -4, -4, -4, -3, -4, -2, -3, -1, -4, -3, -4, -3, -3, -3, -1, -1, -2, -2, -1}, "formanAug" -> {-1, -1, -2, -3, -2, -3, -1, -3, -1, -3, -2, -4, -4, -4, -4, -3, -4, -2, -3, -2, -4, -4, -4, -4, -3, -4, -2, -3, -1, -4, -3, -4, -3, -3, -3, -1, -1, -2, -2, -1}, "res" -> {0.301060606061, 0.0380303030303, 0.0627272727273, 0.0380303030303, 0.301060606061, 0.0380303030303, -0.101515151515, -0.0760606060606, -0.101515151515, 0.0380303030303, 0.0627272727273, -0.0760606060606, -0.0490909090909, -0.0760606060606, 0.0627272727273, 0.0380303030303, -0.101515151515, -0.0760606060606, -0.101515151515, 0.0380303030303, 0.301060606061, 0.0380303030303, 0.0627272727273, 0.0380303030303, 0.301060606061}, "stein" -> {1, 0.375, 0.375, 0.375, 1, 0.375, -0.25, -0.25, -0.25, 0.375, 0.375, -0.25, -0.25, -0.25, 0.375, 0.375, -0.25, -0.25, -0.25, 0.375, 1, 0.375, 0.375, 0.375, 1}|>, "dumbbell" -> <|"n" -> 12, "edges" -> {{1, 2}, {8, 9}, {1, 3}, {8, 10}, {1, 4}, {8, 11}, {1, 5}, {8, 12}, {2, 3}, {9, 10}, {2, 4}, {9, 11}, {2, 5}, {9, 12}, {3, 4}, {10, 11}, {3, 5}, {10, 12}, {4, 5}, {11, 12}, {5, 6}, {6, 7}, {7, 8}}, "lambda1" -> 0.0286185595244, "lambdaMax" -> 1.68374064344, "lly" -> {1.25, 0.85, 1.25, 0.85, 1.25, 0.85, 0.85, 0.85, 1.25, 1.25, 1.25, 1.25, 0.85, 1.25, 1.25, 1.25, 0.85, 1.25, 0.85, 1.25, -0.6, 0, -0.6}, "k0" -> {0.75, 0.6, 0.75, 0.6, 0.75, 0.6, 0.6, 0.6, 0.75, 0.75, 0.75, 0.75, 0.6, 0.75, 0.75, 0.75, 0.6, 0.75, 0.6, 0.75, -0.6, 0, -0.6}, "be" -> {0.810496, 0.810496, 0.810496, 0.810496, -0.027695, -0.383096, -0.383096, -0.027695, 0.810496, 0.810496, 0.810496, 0.810496}, "forman" -> {-4, -5, -4, -5, -4, -5, -5, -5, -4, -4, -4, -4, -5, -4, -4, -4, -5, -4, -5, -4, -3, 0, -3}, "formanAug" -> {5, 4, 5, 4, 5, 4, 4, 4, 5, 5, 5, 5, 4, 5, 5, 5, 4, 5, 4, 5, -3, 0, -3}, "res" -> {0.2, 0.2, 0.2, 0.2, -0.3, -6.66133814775*^-16, -1.33226762955*^-15, -0.3, 0.2, 0.2, 0.2, 0.2}, "stein" -> {0.774193548387, 0.774193548387, 0.774193548387, 0.774193548387, -1.16129032258, 4.60742555219*^-15, -6.60582699652*^-15, -1.16129032258, 0.774193548387, 0.774193548387, 0.774193548387, 0.774193548387}|>|>, "flows" -> <|"wiggle" -> <|"A0" -> 3.39343363459, "t" -> 0.498, "A" -> 0.255225351169, "rate" -> -6.30162305908, "vertices" -> 36|>, "star" -> <|"A0" -> 3.45267940093, "t" -> 0.504, "A" -> 0.271862433851, "rate" -> -6.31114477595, "vertices" -> 31|>, "bean" -> <|"A0" -> 3.43379755367, "t" -> 0.504, "A" -> 0.260886381609, "rate" -> -6.29545867472, "vertices" -> 39|>, "ellipse" -> <|"A0" -> 3.14049769671, "t" -> 0.462, "A" -> 0.234885799578, "rate" -> -6.28920324055, "vertices" -> 47|>|>, "ollivier" -> {<|"K" -> -2, "at005" -> -0.250151370483, "emax" -> 0.999648661086, "atmax" -> -0.314776689329|>, <|"K" -> -1, "at005" -> -0.125036620424, "emax" -> 1.2, "atmax" -> -0.14806796806|>, <|"K" -> 0, "at005" -> 0, "emax" -> 1.2, "atmax" -> 0|>, <|"K" -> 1, "at005" -> 0.124958499746, "emax" -> 1.2, "atmax" -> 0.102857388946|>, <|"K" -> 2, "at005" -> 0.249838887759, "emax" -> 0.999648661086, "atmax" -> 0.188624395888|>}|>;

(* page[...] holds the readouts the page computes in the browser; cmpGrid lays them beside the Wolfram values *)
cmpRow[label_, q_, p_, w_] := {label, q, p, w, Abs[p - w]};
cmpGrid[rows_] := valGrid[{"", "quantity", "page (JavaScript)", "Wolfram", "|difference|"}, rows];

(* ::Subsection:: *)
(*PN 1. Surfaces*)

(* ::Text:: *)
(*The page takes K and H by central finite differences with step 10⁻³ on a 57 × 37 grid, and ∬K dA by a 160 × 160 midpoint rule.*)

cmpGrid[Join @@ Table[{cmpRow[key, "min K", page["surfaces", key, "kmin"], surfVals[key, "kmin"]], cmpRow["", "max K", page["surfaces", key, "kmax"], surfVals[key, "kmax"]],
    cmpRow["", "max |H|", page["surfaces", key, "hmax"], surfVals[key, "hmax"]], cmpRow["", "∬ K dA", page["surfaces", key, "total"], surfVals[key, "total"]]}, {key, Keys[surf]}]]

(* ::Text:: *)
(*The finite differences agree with the exact values to about 5 × 10⁻⁷ (the O(h²) error of step 10⁻³), except max |H| on the pseudosphere (3 × 10⁻⁴), which is reached at the edge of the patch where H grows fastest; the totals agree to the accuracy of the midpoint rule (2 × 10⁻⁴ at most, on the sphere).*)

(* ::Subsection:: *)
(*PN 2. Ricci flow*)

(* ::Text:: *)
(*The page runs the scheme of §2 exactly, one explicit step per animation frame; the readings agree to round-off. The page’s check line once quoted the write-up notebook §10.2 (NDSolve on a 31 × 31 grid: max|K| 4.83 → 0.059), a different bump and grid; it now quotes this run, 4.63 → 0.059 by t = 2.00. On 23 Nov 2026 the page’s colours were made to follow max|K| (with a fixed ±1.5 option), because on a fixed scale the end of the run looked blank.*)

cmpGrid[{cmpRow["bump 0.3", "max |K| at t = 0", page["ricci", "maxK0"], rr["maxK0"]], cmpRow["", "t at the end", page["ricci", "t"], rr["t"]],
  cmpRow["", "max |K| at the end", page["ricci", "maxK"], rr["maxK"]], cmpRow["", "∬ K dA", page["ricci", "totalK"], rr["totalK"]]}]

(* ::Subsection:: *)
(*PN 3. Curved mean values*)

(* ::Text:: *)
(*The page’s circle mean is a 720-point rule in double precision, fitted on the same window. The last slope differs in the third decimal (8.005 on the page, 8.000 here) because those errors are near 10⁻¹³, where double precision shows; here the circle mean is computed to 25 digits.*)

cmpGrid[MapThread[cmpRow[#1, "log–log slope", #2, #3] &, {{"flat formula", "+ KΔf/96 at r^4", "+ r^6 terms"}, page["means", "slopes"], slopes}]]

(* ::Subsection:: *)
(*PN 4. Heat trace*)

(* ::Text:: *)
(*The page sums the sphere’s eigenvalues and the torus’s theta function in double precision, at the slider value (default t = 0.05).*)

cmpGrid[Join @@ Table[With[{t = h["t"]}, {cmpRow["t = " <> ToString[t], "sphere t·Tr", h["sphere"], sph[t]],
     cmpRow["", "1 + t/3 + t²/15", h["series"], 1 + t/3 + t^2/15], cmpRow["", "flat torus t·Tr", h["torus"], tor[t]]}], {h, page["heat"]}]]

(* ::Subsection:: *)
(*PN 5. Meshes*)

(* ::Text:: *)
(*The page’s mesh, barycentric area and corner angles are those of §6, in JavaScript.*)

cmpGrid[Join @@ MapThread[{cmpRow[ToString[#2["nu"]] <> " × " <> ToString[#2["nv"]], "vertices", #1["vertices"], #2["vertices"]], cmpRow["", "Σ defect", #1["defect"], #2["defect"]],
     cmpRow["", "max |Kmesh − K|", #1["err"], #2["err"]], cmpRow["", "Kmesh at the outer equator", #1["Kouter"], #2["Kouter"]]} &, {page["mesh"], meshVals}]]

(* ::Subsection:: *)
(*PN 6. Graph curvatures*)

(* ::Text:: *)
(*The page computes \!\(\*SubscriptBox[\(κ\), \(LLY\)]\) and κ₀ by its own transport solver, K_∞ by bisection rounded down to 10⁻⁶ (hence differences below 10⁻⁶), and the rest by matrix pseudoinverses. Its notes under each graph were corrected on 23 Nov 2026 from §7: the tree’s two root edges are −1/3, not −2/3; on the grid only the corner edges (+1/3) and the edges from a side inward (+1/6) are positive, not the whole boundary; on the dumbbell the middle edge of the bridge is 0, not −3/5. The note that Steinerberger and resistance curvature are proportional on the tree was right (the factor is 15/7).*)

graphTable[g_] := Module[{sp = normSpec[graphOf[g]]},
   Join[Join @@ Table[With[{w = N[wlValues[g, k]], p = page["graphs", g, k]},
       {{If[k == "lly", g, ""], curvs[k][[1]] <> ": min", Min[p], Min[w], Abs[Min[p] - Min[w]]},
        {"", "   max", Max[p], Max[w], Abs[Max[p] - Max[w]]},
        {"", "   largest |page − Wolfram| over all " <> If[curvs[k][[2]] == "e", "edges", "vertices"], "", "", Max[Abs[p - w]]}}], {k, Keys[curvs]}],
    {cmpRow["", "λ₁ (normalised)", page["graphs", g, "lambda1"], sp[[2]]], cmpRow["", "λmax", page["graphs", g, "lambdaMax"], sp[[-1]]]}]];
{page["graphs", #, "edges"] == graphEdges[#] & /@ Keys[graphEdges], Column[{Style[#, Bold], cmpGrid[graphTable[#]]}, Spacings -> 1] & /@ Keys[graphEdges] // Column}

(* ::Subsection:: *)
(*PN 7. Curve shortening*)

(* ::Text:: *)
(*The page advances the flow of §8 in animation frames of 3 × 10⁻³ and stops at the end of the first frame below 8%, so its t is a little later than Wolfram’s, which stops at the first step. Before 23 Nov 2026 the page used a fixed step 2 × 10⁻⁴: as the curve shrank its edges fell below the stability limit, the polygon broke into a zig-zag at the end, and the mean dA/dt read about −5.6 instead of −2π.*)

cmpGrid[Flatten[Table[{cmpRow[k, "mean dA/dt", page["flows", k, "rate"], runs[k, "rate"]], cmpRow["", "t when area < 8%", page["flows", k, "t"], runs[k, "t"]]}, {k, Keys[runs]}], 1]]

(* ::Subsection:: *)
(*PN 8. Ollivier on manifolds*)

(* ::Text:: *)
(*The page integrates over the ball with a 160 × 160 midpoint rule (80 × 80 at the largest ε). Its check line quotes κ/ε² = 0.12496 (sphere), 0 (plane) and −0.12504 (hyperbolic plane) at ε = 0.05 from notebook 07-Ollivier §8; the converged values of §9 agree to five figures.*)

cmpGrid[Flatten[Table[{cmpRow["K = " <> ToString[o["K"]], "κ/ε² at ε = 0.05", o["at005"], κball[o["K"], 0.05]/0.05^2],
     cmpRow["", "κ/ε² at ε = " <> ToString[NumberForm[o["emax"], 3]], o["atmax"], κball[o["K"], o["emax"]]/o["emax"]^2]}, {o, page["ollivier"]}], 1]]

(* ::Subsection:: *)
(*PN 9. The Lab’s Wolfram cells*)

(* ::Text:: *)
(*The snippets in §§1–10 are the Lab’s Wolfram cells exactly as the page offers them (lab/app.js, SNIP), with script letters written as named characters. On the page they run on the CCN Wolfram Cloud kernel after the reader enters a CCN-KEY.*)

(* ::Text:: *)
(*© 2026 Computational Classnotes · CC BY-NC-SA 4.0*)
