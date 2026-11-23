(* ::Package:: *)

(* The Laplacian and Curvature — instances and relationships, computed *)
(* © 2026 Computational Classnotes · CC BY-NC-SA 4.0 *)

(* ::Title:: *)
(*The Laplacian and Curvature*)

(* ::Text:: *)
(*Instances and relationships, computed — a Laplacian Lab companion notebook*)

(* ::Text:: *)
(*© 2026 Computational Classnotes · CC BY-NC-SA 4.0*)

(* ::Text:: *)
(*Each section below matches a section of the write-up “The Laplacian and Curvature — Instances and Relationships”. Evaluate the notebook top to bottom: Sections 2–6 use the toolkit of Section 1 and Section 9 uses the functions of Section 8. Each section ends with a check that should return True, 0, or a number close to the value stated in the write-up. Conventions: Δ is the analyst’s Laplacian (Δ = div grad, negative semidefinite on closed manifolds); on graphs Δf(x) = mean of f over the neighbours of x minus f(x) (random-walk normalisation) unless stated otherwise.*)

(* ::Section:: *)
(*1. Riemannian toolkit (used in Sections 2–5)*)

(* ::Text:: *)
(*Laplace–Beltrami operator, Christoffel symbols, covariant Hessian, Riemann tensor and Gauss curvature for a metric g in coordinates 𝓍.*)

ClearAll[christoffel, laplaceBeltrami, gradNorm2, hessian, hessNorm2, gaussCurvature];
christoffel[g_, 𝓍_] := Module[{gi = Inverse[g], n = Length[𝓍]},
  Table[1/2 Sum[gi[[i, l]] (D[g[[l, j]], 𝓍[[k]]] + D[g[[l, k]], 𝓍[[j]]] - D[g[[j, k]], 𝓍[[l]]]), {l, n}],
   {i, n}, {j, n}, {k, n}] // Simplify];
laplaceBeltrami[g_, 𝓍_][u_] := Module[{gi = Inverse[g], s = Sqrt[Det[g]], n = Length[𝓍]},
  1/s Sum[D[s gi[[i, j]] D[u, 𝓍[[j]]], 𝓍[[i]]], {i, n}, {j, n}]];
gradNorm2[g_, 𝓍_][u_] := With[{gi = Inverse[g]}, Sum[gi[[i, j]] D[u, 𝓍[[i]]] D[u, 𝓍[[j]]], {i, Length[𝓍]}, {j, Length[𝓍]}]];
hessian[g_, 𝓍_][u_] := With[{Γ = christoffel[g, 𝓍], n = Length[𝓍]},
  Table[D[u, 𝓍[[i]], 𝓍[[j]]] - Sum[Γ[[k, i, j]] D[u, 𝓍[[k]]], {k, n}], {i, n}, {j, n}]];
hessNorm2[g_, 𝓍_][u_] := With[{gi = Inverse[g], H = hessian[g, 𝓍][u]}, Tr[gi . H . gi . H]];
gaussCurvature[g_, 𝓍_] := Module[{Γ = christoffel[g, 𝓍], R},
  R[i_, j_, k_, l_] := D[Γ[[i, j, l]], 𝓍[[k]]] - D[Γ[[i, j, k]], 𝓍[[l]]] +
     Sum[Γ[[i, k, m]] Γ[[m, j, l]] - Γ[[i, l, m]] Γ[[m, j, k]], {m, 2}];
  Simplify[Sum[g[[1, i]] R[i, 2, 1, 2], {i, 2}]/Det[g]]];
gS2 = {{1, 0}, {0, Sin[θ]^2}}; 𝓍S2 = {θ, φ};
gaussCurvature[gS2, 𝓍S2]

(* ::Subsection:: *)
(*1.1 Curvatures of an embedded surface, and a colour scale*)

(* ::Text:: *)
(*For a parametrised surface X(u, v) in ℝ³: first fundamental form E, F, G, second fundamental form L, M, N, K = (LN − M²)/(EG − F²), H = (EN − 2FM + GL)/(2(EG − F²)). Colours below: blue = negative curvature, near-white = zero, orange = positive.*)

surfaceCurvatures[pos_, 𝓍_] := Module[{Xu, Xv, nn, E1, F1, G1, L1, M1, N1},
  Xu = D[pos, 𝓍[[1]]]; Xv = D[pos, 𝓍[[2]]];
  nn = Cross[Xu, Xv]/Sqrt[Cross[Xu, Xv] . Cross[Xu, Xv]];
  {E1, F1, G1} = {Xu . Xu, Xu . Xv, Xv . Xv};
  {L1, M1, N1} = {D[pos, 𝓍[[1]], 𝓍[[1]]] . nn, D[pos, 𝓍[[1]], 𝓍[[2]]] . nn, D[pos, 𝓍[[2]], 𝓍[[2]]] . nn};
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
surfaceCurvatures[{(2 + Cos[v]) Cos[u], (2 + Cos[v]) Sin[u], Sin[v]}, {u, v}]

(* ::Section:: *)
(*2. Gauss curvature is a Laplacian: conformal metrics and Liouville’s equation*)

(* ::Text:: *)
(*For g = e^{2u}(dx² + dy²) the Gauss curvature is K = −e^{−2u} Δ₀u, where Δ₀ is the flat Laplacian. Equivalently Δ₀u = −K e^{2u} (Liouville’s equation when K is constant). Checks: the round sphere through stereographic projection gives K = 1, the Poincaré half-plane gives K = −1, and the formula agrees with the Riemann-tensor computation for a generic u.*)

Kconformal[u_] := Simplify[-Exp[-2 u] (D[u, {x, 2}] + D[u, {y, 2}])];
{Kconformal[Log[2/(1 + x^2 + y^2)]],          (* unit sphere, stereographic *)
 Kconformal[Log[1/y]],                         (* hyperbolic half-plane *)
 Kconformal[Log[2/(1 - x^2 - y^2)]],           (* Poincaré disc *)
 Simplify[Kconformal[w[x, y]] - gaussCurvature[Exp[2 w[x, y]] IdentityMatrix[2], {x, y}]]}

(* ::Subsection:: *)
(*2.1 Worked examples: positive, zero and negative Gauss curvature*)

(* ::Text:: *)
(*Six classical surfaces, each coloured by its Gauss curvature K. The sphere is K = 1 everywhere; the cylinder is K = 0 (it unrolls flat); the torus is positive on the outside, negative on the inside and zero on the top and bottom circles; the saddle, catenoid and pseudosphere are negatively curved, the pseudosphere with K = −1 everywhere.*)

surfaces = {
   {"Sphere", {Sin[v] Cos[u], Sin[v] Sin[u], Cos[v]}, {0, 2 π}, {0.01, π - 0.01}},
   {"Cylinder", {Cos[u], Sin[u], v}, {0, 2 π}, {-1, 1}},
   {"Torus (R = 2, r = 1)", {(2 + Cos[v]) Cos[u], (2 + Cos[v]) Sin[u], Sin[v]}, {0, 2 π}, {0, 2 π}},
   {"Saddle z = x² − y²", {u, v, u^2 - v^2}, {-1, 1}, {-1, 1}},
   {"Catenoid", {Cosh[v] Cos[u], Cosh[v] Sin[u], v}, {0, 2 π}, {-1.2, 1.2}},
   {"Pseudosphere", {Sech[v] Cos[u], Sech[v] Sin[u], v - Tanh[v]}, {0, 2 π}, {0.05, 3}}};
Kformulas = Table[{s[[1]], surfaceCurvatures[s[[2]], {u, v}]["K"]}, {s, surfaces}];
TableForm[Kformulas, TableHeadings -> {None, {"surface", "K(u, v)"}}]

Legended[GraphicsGrid[Partition[Table[With[{s = surfaces[[i]], K = Kformulas[[i, 2]]},
     curvatureSurface[s[[2]], {u, s[[3, 1]], s[[3, 2]]}, {v, s[[4, 1]], s[[4, 2]]}, K, 1, s[[1]]]], {i, 6}], 3],
   ImageSize -> 760, Spacings -> {10, 10}], κLegend[1, "K"]]

(* ::Text:: *)
(*Gauss–Bonnet on the examples: ∬K dA = 2πχ. The torus (χ = 0) integrates to 0, the sphere (χ = 2) to 4π. The Liouville form of Section 2 reproduces the sphere’s K from the stereographic conformal factor.*)

With[{t = surfaceCurvatures[{(2 + Cos[v]) Cos[u], (2 + Cos[v]) Sin[u], Sin[v]}, {u, v}],
   s = surfaceCurvatures[{Sin[v] Cos[u], Sin[v] Sin[u], Cos[v]}, {u, v}]},
 {"torus ∬K dA" -> Integrate[Simplify[t["K"] t["dA"], 0 < v < 2 π], {u, 0, 2 π}, {v, 0, 2 π}],
  "sphere ∬K dA" -> Integrate[Simplify[s["K"] s["dA"], 0 < v < π], {u, 0, 2 π}, {v, 0, π}]}]

(* ::Section:: *)
(*3. Mean curvature is a Laplacian: ΔX = −2H𝐧*)

(* ::Text:: *)
(*For a surface X : U → ℝ³ with induced metric, the Laplace–Beltrami operator applied to each coordinate of the position vector gives the mean-curvature vector: ΔX = −2H𝐧 (H the mean of the principal curvatures, 𝐧 the unit normal; the sign depends on orientation). Consequence: a surface is minimal exactly when its coordinate functions are harmonic. Checks: sphere (H = 1/a), torus, and the catenoid (H = 0).*)

meanCurvatureVector[pos_, 𝓍_, assum_ : True] := Module[{g, n, ΔX},
  g = Simplify[Table[D[pos, 𝓍[[i]]] . D[pos, 𝓍[[j]]], {i, 2}, {j, 2}]];
  ΔX = Simplify[laplaceBeltrami[g, 𝓍] /@ pos];
  n = Simplify[Normalize[Cross[D[pos, 𝓍[[1]]], D[pos, 𝓍[[2]]]]], 𝓍 ∈ Reals && assum];
  <|"H" -> Simplify[-ΔX . n/2, 𝓍 ∈ Reals && assum],
    "tangential part" -> Simplify[{ΔX . D[pos, 𝓍[[1]]], ΔX . D[pos, 𝓍[[2]]]}]|>];
{meanCurvatureVector[3 {Sin[θ] Cos[φ], Sin[θ] Sin[φ], Cos[θ]}, {θ, φ}, 0 < θ < π],
 meanCurvatureVector[{(2 + Cos[v]) Cos[u], (2 + Cos[v]) Sin[u], Sin[v]}, {u, v}],
 meanCurvatureVector[{Cosh[v] Cos[u], Cosh[v] Sin[u], v}, {u, v}]}

(* ::Subsection:: *)
(*3.1 Worked examples: the mean-curvature vector drawn*)

(* ::Text:: *)
(*Left: the torus coloured by H, with −ΔX drawn as arrows (ΔX itself points into the tube). The arrows are normal to the surface, longest on the outer equator where H = 2/3, and vanish on the inner equator where H = 0. Right: the catenoid and the helicoid are minimal surfaces (H = 0): their coordinate functions are harmonic, so ΔX vanishes and no arrows appear.*)

torusPos = {(2 + Cos[v]) Cos[u], (2 + Cos[v]) Sin[u], Sin[v]};
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
{Htorus, Legended[GraphicsRow[Prepend[minimal, torusPlot], ImageSize -> 760], κLegend[0.7, "H"]]}

(* ::Section:: *)
(*4. Mean values and volumes: curvature in the mean-value expansion of Δ*)

(* ::Text:: *)
(*Laplacian Lab Section 1 derives Δ from the sphere mean in flat space: M_r f = f + r²/(2n) Δf + …. On a curved manifold the same expansion picks up curvature (Gray–Willmore 1982). On a surface of constant curvature K the geodesic-circle mean is*)

(* ::Text:: *)
(*  M_r f(p) = f + (r²/4) Δf + r⁴ (Δ²f/64 + K Δf/96) + r⁶ (Δ³f/2304 + K Δ²f/1152 + K² Δf/1440) + O(r⁸).*)

(* ::Text:: *)
(*Derivation on the unit sphere: the circle-mean operator acts on a degree-l spherical harmonic as the Legendre polynomial P_l(cos r), and Δ acts as λ = −l(l+1). Matching the series of P_l(cos r) in powers of λ gives the coefficients; scaling the sphere restores K.*)

λ = -l (l + 1);
ser = Expand@Normal@Series[LegendreP[l, Cos[r]], {r, 0, 6}];
{Factor@Coefficient[ser, r, 2],
 SolveAlways[Coefficient[ser, r, 4] == a λ^2 + b λ, l],
 SolveAlways[Coefficient[ser, r, 6] == a3 λ^3 + b3 λ^2 + c3 λ, l]}

(* ::Text:: *)
(*Direct check on S² with a non-symmetric test function. Write it in ambient coordinates and extend it as a degree-0 function F(X/|X|); then |X|²·Δ_ℝ³ of it is again degree 0 and equals Δ_S² F. Average F over the geodesic circle of colatitude r about the north pole and compare with the formula evaluated at the pole.*)

F0[{x_, y_, z_}] := Exp[x] (1 + z)^2 + y z^3;
ext = F0[{x, y, z}/Sqrt[x^2 + y^2 + z^2]];
ΔS2amb[h_] := Simplify[(x^2 + y^2 + z^2) Laplacian[h, {x, y, z}]];
L1 = ΔS2amb[ext]; L2 = ΔS2amb[L1]; L3 = ΔS2amb[L2];
atPole[h_] := h /. {x -> 0, y -> 0, z -> 1};
circleMean = Integrate[Normal@Series[F0[{Sin[r] Cos[φ], Sin[r] Sin[φ], Cos[r]}], {r, 0, 6}], {φ, 0, 2 π}]/(2 π);
formula = atPole[ext] + r^2/4 atPole[L1] + r^4 (atPole[L2]/64 + atPole[L1]/96) +
   r^6 (atPole[L3]/2304 + atPole[L2]/1152 + atPole[L1]/1440);
Simplify[Expand[circleMean - formula]]

(* ::Text:: *)
(*Volumes. Area of a geodesic disc on a surface of curvature K: A(r) = πr²(1 − K r²/12 + K²r⁴/360 − …) (Bertrand–Diguet–Puiseux). In dimension n: Vol B_r = ω_n rⁿ (1 − S r²/(6(n+2)) + O(r⁴)), S the scalar curvature. Check on S³ (S = 6).*)

areaK = 2 π Integrate[Sin[Sqrt[K] ρ]/Sqrt[K], {ρ, 0, r}];
volS3 = 4 π Integrate[Sin[ρ]^2, {ρ, 0, r}];
{Series[areaK/(π r^2), {r, 0, 4}], Series[volS3/(4/3 π r^3), {r, 0, 2}], 1 - 6 r^2/(6 (3 + 2))}

(* ::Subsection:: *)
(*4.1 Pictures: geodesic circles, and where the flat formula fails*)

(* ::Text:: *)
(*Left: the test function on S² with geodesic circles about the north pole at r = 0.3, 0.6, …, 1.5. Right: the error of three approximations to the exact circle mean, on log–log axes. The flat-space formula (K = 0) misses the KΔf/96 term, so its error falls only like r⁴. Adding that term makes the error fall like r⁶, and adding the r⁶ terms makes it fall like r⁸: the curvature terms are exactly the right ones.*)

exactMean[r0_] := NIntegrate[F0[{Sin[r0] Cos[φ], Sin[r0] Sin[φ], Cos[r0]}], {φ, 0, 2 π}, WorkingPrecision -> 40, PrecisionGoal -> 30]/(2 π);
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
Row[{sphereView, errPlot}]

(* ::Text:: *)
(*Area of a geodesic disc divided by the flat value πr², for K = 1 (sphere), 0 (plane) and −1 (hyperbolic plane). Positive curvature makes discs smaller than flat ones, negative curvature larger: the −Kr²/12 term.*)

Plot[{2 (1 - Cos[r])/r^2, 1, 2 (Cosh[r] - 1)/r^2}, {r, 0.01, 2.5},
 PlotStyle -> {RGBColor[0.98, 0.56, 0.17], Gray, RGBColor[0.18, 0.36, 0.78]},
 PlotLegends -> {"K = 1", "K = 0", "K = −1"}, AxesLabel -> {"r", "A(r)/πr²"},
 PlotLabel -> "Geodesic discs: A(r)/πr² = 1 − Kr²/12 + …", ImageSize -> 420]

(* ::Section:: *)
(*5. Heat kernel and spectrum: curvature is audible*)

(* ::Text:: *)
(*Minakshisundaram–Pleijel / McKean–Singer: Tr e^{tΔ} ~ (4plan)^{−n/2} (Vol + (t/6)∫S + O(t²)). On the unit S² (area 4π, S = 2) the spectrum is l(l+1) with multiplicity 2l+1, so t·Tr e^{tΔ} → 1 + t/3 + t²/15 + …. For a surface the t⁰ coefficient is (1/12π)∫K = χ/6, so the Euler characteristic can be heard.*)

heatTrace[t_?NumericQ] := Sum[(2 j + 1) Exp[-j (j + 1) t], {j, 0, 2000}];
TableForm[Table[{t, t heatTrace[t], 1 + t/3 + t^2/15}, {t, {0.1, 0.03, 0.01}}],
 TableHeadings -> {None, {"t", "t·Tr e^{tΔ}", "1 + t/3 + t²/15"}}]

(* ::Subsection:: *)
(*5.1 Two drums with the same area: the sphere and the flat torus*)

(* ::Text:: *)
(*Normalise the heat trace by its leading Weyl term, Area/(4πt). For the unit sphere (K = 1) the ratio rises like 1 + t/3: the slope is ∫S/(6·Area) = 1/3. For the flat square torus of the same area (K = 0) the ratio stays at 1 for small t. The first correction to Weyl’s law hears the curvature.*)

L0 = 2 Sqrt[π];   (* flat torus side, so area = 4π like the unit sphere *)
torusTrace[t_?NumericQ] := EllipticTheta[3, 0, Exp[-(2 π/L0)^2 t]]^2;
ratio[tr_, t_] := tr[t]/((4 π)/(4 π t));
Plot[{ratio[heatTrace, t], 1 + t/3 + t^2/15, ratio[torusTrace, t]}, {t, 0.005, 0.4},
 PlotStyle -> {{RGBColor[0.98, 0.56, 0.17], Thick}, {Black, Dashed}, {RGBColor[0.18, 0.36, 0.78], Thick}},
 PlotLegends -> {"sphere S²", "1 + t/3 + t²/15", "flat torus, same area"},
 AxesLabel -> {"t", "Tr e^{tΔ} ÷ (Area/4πt)"}, PlotLabel -> "Curvature is the first correction to Weyl’s law", ImageSize -> 460]

(* ::Section:: *)
(*6. Bochner formula, Lichnerowicz bound and Laplacian comparison*)

(* ::Text:: *)
(*Bochner: ½Δ|∇f|² = |Hess f|² + ⟨∇f, ∇Δf⟩ + Ric(∇f, ∇f). This is the identity every “Bakry–Émery” curvature (Section 8) copies. Verified for an arbitrary f on S² (Ric = g).*)

ΔS2 = laplaceBeltrami[gS2, 𝓍S2];
F = 𝒻[θ, φ];
Simplify[1/2 ΔS2[gradNorm2[gS2, 𝓍S2][F]] - (hessNorm2[gS2, 𝓍S2][F] +
     Sum[Inverse[gS2][[i, j]] D[F, 𝓍S2[[i]]] D[ΔS2[F], 𝓍S2[[j]]], {i, 2}, {j, 2}] + gradNorm2[gS2, 𝓍S2][F])]

(* ::Text:: *)
(*Lichnerowicz: Ric ≥ (n−1)k > 0 implies λ₁ ≥ nk. On the unit S² (n = 2, k = 1) the first eigenvalue is exactly 2: equality (Obata). Laplacian comparison: Ric ≥ 0 gives Δr ≤ (n−1)/r; on S² the distance from the pole has Δr = cot r ≤ 1/r.*)

{Simplify[ΔS2[SphericalHarmonicY[1, 0, θ, φ]]/SphericalHarmonicY[1, 0, θ, φ]],
 Simplify[ΔS2[θ]],
 And @@ Table[Cot[r] <= 1/r, {r, 0.01, 3.13, 0.01}]}

(* ::Subsection:: *)
(*6.1 Worked example: Bochner on a surface whose curvature changes sign*)

(* ::Text:: *)
(*On the torus Ric = K g with K = cos v/(2 + cos v), which is positive outside and negative inside. The Bochner identity still holds pointwise, with that variable K.*)

gTor = {{(2 + Cos[v])^2, 0}, {0, 1}}; 𝓍T = {u, v}; Ktor = Cos[v]/(2 + Cos[v]);
ΔT = laplaceBeltrami[gTor, 𝓍T]; FT = 𝒻[u, v];
Simplify[1/2 ΔT[gradNorm2[gTor, 𝓍T][FT]] - (hessNorm2[gTor, 𝓍T][FT] +
    Sum[Inverse[gTor][[i, j]] D[FT, 𝓍T[[i]]] D[ΔT[FT], 𝓍T[[j]]], {i, 2}, {j, 2}] + Ktor gradNorm2[gTor, 𝓍T][FT])]

(* ::Subsection:: *)
(*6.2 Laplacian comparison pictured*)

(* ::Text:: *)
(*Δr is the geodesic curvature of the circle of radius r: cot r for K = 1, 1/r for K = 0, coth r for K = −1. A lower bound on curvature caps it from above (Laplacian comparison), and integrating it gives Bishop–Gromov: circumference/2πr = sin r/r, 1, sinh r/r.*)

Row[{
  Plot[{Cot[r], 1/r, Coth[r]}, {r, 0.05, 3}, PlotRange -> {-2, 4},
   PlotStyle -> {RGBColor[0.98, 0.56, 0.17], Gray, RGBColor[0.18, 0.36, 0.78]},
   PlotLegends -> {"K = 1: cot r", "K = 0: 1/r", "K = −1: coth r"}, AxesLabel -> {"r", "Δr"}, PlotLabel -> "Δr = curvature of geodesic circles", ImageSize -> 400],
  Plot[{Sin[r]/r, 1, Sinh[r]/r}, {r, 0.01, 3},
   PlotStyle -> {RGBColor[0.98, 0.56, 0.17], Gray, RGBColor[0.18, 0.36, 0.78]},
   PlotLegends -> {"K = 1", "K = 0", "K = −1"}, AxesLabel -> {"r", "length/2πr"}, PlotLabel -> "Bishop–Gromov: circle length vs flat", ImageSize -> 320]}]

(* ::Text:: *)
(*Lichnerowicz pictured: the first nonzero eigenvalue of S² is 2 = nk, attained by the coordinate functions. The eigenfunction Y₁⁰ = z is drawn on the sphere.*)

SphericalPlot3D[1, {θ, 0, π}, {φ, 0, 2 π}, Mesh -> None, PlotPoints -> 40,
 ColorFunction -> Function[{x, y, z}, κColour[z, 1]], ColorFunctionScaling -> False, Boxed -> False, Axes -> False, Lighting -> "Neutral",
 PlotLabel -> "λ1(S²) = 2: eigenfunction z (Lichnerowicz equality)", ImageSize -> 300]

(* ::Section:: *)
(*7. Discrete surfaces: cotangent Laplacian, angle defect, discrete Gauss–Bonnet*)

(* ::Text:: *)
(*On a triangle mesh, the cotangent Laplacian (L f)_i = ½ Σ_j (cot α_ij + cot β_ij)(f_j − f_i), divided by the vertex area A_i, approximates Δ. Applied to the vertex positions it gives the discrete mean-curvature normal (Meyer–Desbrun–Schröder–Barr). The angle defect 2π − Σθ at a vertex is the discrete Gauss curvature; it sums to exactly 2πχ. Test: 400-point mesh of the unit sphere (H = 1, K = 1, χ = 2).*)

mesh = ConvexHullMesh[SpherePoints[400]];
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
  "mean ΔX·n" -> Mean[MapThread[Dot, {ΔX, P}]]|>

Graphics3D[{EdgeForm[GrayLevel[.6]], MapThread[{ColorData["SunsetColors"][Rescale[#2, MinMax[defect/A]]], Polygon[P[[#1]]]} &,
   {T, Mean[(defect/A)[[#]]] & /@ T}]}, Boxed -> False, PlotLabel -> "Angle defect / vertex area ≈ K = 1"]

(* ::Subsection:: *)
(*7.1 Worked example: a torus mesh, where Gauss–Bonnet gives zero*)

(* ::Text:: *)
(*A 40 × 20 triangulated torus. The angle defect is positive on the outer half and negative on the inner half; its total is exactly 0 = 2πχ(torus). Divided by the vertex area it approximates the smooth K = cos v/(2 + cos v), and the cotangent Laplacian of the positions approximates −2H𝐧.*)

meshCurvature[P_, T_] := Module[{nv = Length[P], ang, def, Wm, Am},
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
<|"Σ defect" -> Chop[Total[mt["defect"]], 10^-9], "max |K_mesh − K|" -> Max[Abs[Kmesh - Ksmooth]]|>

Legended[Row[{
   Graphics3D[{EdgeForm[GrayLevel[0.6, 0.5]], Table[{κColour[Mean[Kmesh[[t]]], 1], Polygon[PT[[t]]]}, {t, TT}]},
    Boxed -> False, Lighting -> "Neutral", PlotLabel -> "Angle defect / area ≈ K", ImageSize -> 340],
   ListPlot[{Transpose[{Flatten[Table[2 π j/nvv, {i, 0, nu - 1}, {j, 0, nvv - 1}]], Kmesh}],
     Table[{s, Cos[s]/(2 + Cos[s])}, {s, 0, 2 π, 0.05}]}, Joined -> {False, True},
    PlotStyle -> {RGBColor[0.98, 0.56, 0.17], Black}, AxesLabel -> {"v", "K"},
    PlotLegends -> {"mesh: defect/area", "smooth K"}, PlotLabel -> "Mesh vs smooth Gauss curvature", ImageSize -> 420]}],
 κLegend[1, "K"]]

(* ::Section:: *)
(*8. Graph curvatures built from the graph Laplacian*)

(* ::Text:: *)
(*Every notion below is defined from the graph Laplacian Δ, from the random walk it generates, or from its pseudoinverse. Test graphs: cycle C₆, complete K₅, cube Q₃, Petersen graph, 4×4 grid.*)

(* ::Subsection:: *)
(*8.1 Ollivier / Lin–Lu–Yau curvature*)

(* ::Text:: *)
(*Ollivier: κ_α(x,y) = 1 − W₁(μ_x^α, μ_y^α)/d(x,y), with μ_x^α the lazy random walk (stay with probability α). It compares averages over two small balls — the discrete twin of Section 4. Lin–Lu–Yau: κ = lim_{α→1} κ_α/(1−α); it equals 2κ_{1/2} for every edge. Münch–Wojciechowski limit-free formula: κ(x,y) = inf { ∇_{xy}Δf : f 1-Lipschitz, ∇_{yx}f = 1 }, a linear program in which the Laplacian appears explicitly. Both routes are computed and must agree.*)

nbr[G_, v_] := AdjacencyList[G, v];
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
     "min κ_0" -> Min[κOllivier[G, #, 0] & /@ edges[G]]|>], graphs]

(* ::Subsection:: *)
(*8.2 Bakry–Émery curvature (the discrete Bochner formula)*)

(* ::Text:: *)
(*Γ(f) = ½(Δf² − 2fΔf), Γ₂(f) = ½(ΔΓ(f) − 2Γ(f, Δf)). The curvature-dimension condition CD(K, ∞) at x is Γ₂(f)(x) ≥ K Γ(f)(x) for all f. Both sides are quadratic forms in the values of f on the 2-ball of x, so the best K is the largest K with Γ₂ − KΓ positive semidefinite (found by bisection).*)

bakryEmery[G_, x_] := Module[{B2, F, ff, Γv, q1, q2, M1, M2, lo = -10., hi = 10., mid},
  B2 = VertexList[NeighborhoodGraph[G, x, 2]];
  F = Array[𝒻, Length[B2]]; ff = AssociationThread[B2 -> F];
  Γv[v_] := 1/2 Mean[(ff[#] - ff[v])^2 & /@ nbr[G, v]];
  q1 = Γv[x];
  q2 = 1/2 (Mean[Γv /@ nbr[G, x]] - Γv[x]) -
    1/2 Mean[(ff[#] - ff[x]) (Δgraph[G, ff][#] - Δgraph[G, ff][x]) & /@ nbr[G, x]];
  M1 = D[q1, {F, 2}]/2; M2 = D[q2, {F, 2}]/2;
  Do[mid = (lo + hi)/2; If[Min[Eigenvalues[N[M2 - mid M1]]] >= -10^-9, lo = mid, hi = mid], {60}];
  N[Floor[lo 10^6]/10^6]];   (* rounded down, so theorem checks stay safe *)
Dataset@Map[Function[G, Min[bakryEmery[G, #] & /@ VertexList[G]]], graphs]

(* ::Subsection:: *)
(*8.3 Forman curvature (the discrete Bochner–Weitzenböck splitting)*)

(* ::Text:: *)
(*Forman splits the combinatorial Hodge Laplacian on 1-cells as □ = B + F; the diagonal part F is the curvature. For an unweighted graph, F(e) = 4 − d_x − d_y; counting triangles as 2-cells gives the augmented version 4 − d_x − d_y + 3·#triangles(e).*)

forman[G_, {x_, y_}] := 4 - VertexDegree[G, x] - VertexDegree[G, y];
formanAug[G_, {x_, y_}] := forman[G, {x, y}] + 3 Length[Intersection[nbr[G, x], nbr[G, y]]];
Dataset@Map[Function[G, <|"min Forman" -> Min[forman[G, #] & /@ edges[G]],
     "min augmented" -> Min[formanAug[G, #] & /@ edges[G]]|>], graphs]

(* ::Subsection:: *)
(*8.4 Resistance curvature (from the pseudoinverse of the Laplacian)*)

(* ::Text:: *)
(*Effective resistance ω_ij = (L⁺)_ii + (L⁺)_jj − 2(L⁺)_ij with L the Kirchhoff matrix. Node curvature p_i = 1 − ½ Σ_{j~i} ω_ij (Devriendt–Lambiotte). Foster’s theorem Σ_edges ω = n − 1 makes Σ p_i = 1 for every connected graph: a discrete Gauss–Bonnet theorem. Edge curvature κ_ij = 2(p_i + p_j)/ω_ij.*)

resistance[G_] := Module[{Lp = PseudoInverse[N@KirchhoffMatrix[G]], n = VertexCount[G]},
  Table[Lp[[i, i]] + Lp[[j, j]] - 2 Lp[[i, j]], {i, n}, {j, n}]];
pNode[G_] := With[{Ω = resistance[G], V = VertexList[G]},
  Table[1 - 1/2 Sum[Ω[[i, VertexIndex[G, j]]], {j, nbr[G, V[[i]]]}], {i, Length[V]}]];
Dataset@Map[<|"Σ p (=1)" -> Chop@Total[pNode[#]], "min p" -> Min[pNode[#]], "max p" -> Max[pNode[#]]|> &, graphs]

(* ::Subsection:: *)
(*8.5 Steinerberger curvature and combinatorial (Higuchi) curvature*)

(* ::Text:: *)
(*Steinerberger: solve D·K = n·1 with D the distance matrix (least squares if singular). Higuchi’s combinatorial curvature for a polyhedral surface: κ(v) = 1 − d_v/2 + Σ_faces∋v 1/|face|; by Euler’s formula it sums to χ = 2 on every convex polyhedron.*)

steinerberger[G_] := LeastSquares[N@GraphDistanceMatrix[G], ConstantArray[N@VertexCount[G], VertexCount[G]]];
higuchiTotal[name_] := Module[{F = PolyhedronData[name, "FaceIndices"], nv = Length[PolyhedronData[name, "VertexCoordinates"]]},
  Total@Table[1 - Count[F, _?(MemberQ[#, v] &)]/2 + Total[1/Length[#] & /@ Select[F, MemberQ[#, v] &]], {v, nv}]];
{Dataset@Map[<|"min K" -> Min[steinerberger[#]], "max K" -> Max[steinerberger[#]]|> &, graphs],
 AssociationMap[higuchiTotal, {"Tetrahedron", "Cube", "Dodecahedron", "Icosahedron", "TruncatedIcosahedron"}]}

(* ::Subsection:: *)
(*8.6 Pictures: graphs coloured by their curvature*)

(* ::Text:: *)
(*One drawing helper, then each curvature on a family of examples. The family: a binary tree (very negative), the 6-cycle (flat), the 3-cube, the complete graph K₅ (positive), the Petersen graph, the 5×5 grid with boundary, and a dumbbell (two K₅ joined by a path), whose bridge is a bottleneck. Edge curvatures colour the edges; vertex curvatures colour the vertices. Blue = negative, orange = positive.*)

dumbbell = Graph[UndirectedEdge @@@ Join[List @@@ EdgeList[CompleteGraph[5]], (List @@@ EdgeList[CompleteGraph[5]]) + 7, {{5, 6}, {6, 7}, {7, 8}}]];
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
Keys[family]

(* ::Text:: *)
(*Lin–Lu–Yau curvature on every edge. In the binary tree, interior edges are −2/3 (the two neighbourhoods do not overlap) while leaf edges are +2/3 (a leaf sees only its parent). The cycle and the Petersen graph are 0, the cube is 2/3 everywhere and K₅ is 5/4. The grid is 0 inside and positive along the boundary. The dumbbell’s bridge is negative (−3/5) while its cliques are positive: the bottleneck shows up as negative curvature.*)

Legended[row[KeyValueMap[Function[{nm, G}, edgeCurvaturePlot[G, κLLY, 1.25, nm]], family]], κLegend[1.25, "κ_LLY"]]

Dataset[Map[Function[G, With[{k = κLLY[G, #] & /@ edges[G]}, <|"min" -> Min[k], "max" -> Max[k], "mean" -> N[Mean[k]]|>]], family]]

(* ::Text:: *)
(*What Ollivier’s curvature measures, on one edge: the walk measures μ_x and μ_y spread mass over the two neighbourhoods. Shared neighbours (purple, the triangles) let mass stay put, which is why K₅ is positive. Across an interior tree edge the neighbourhoods do not overlap, mass must travel up to 3 steps, and κ is negative.*)

edgePicture[G_, {x_, y_}, label_] := Graph[G,
  VertexStyle -> Join[Thread[Union[nbr[G, x], nbr[G, y]] -> RGBColor[0.98, 0.56, 0.17]],
    Thread[Intersection[nbr[G, x], nbr[G, y]] -> RGBColor[0.55, 0.3, 0.75]], {x -> Black, y -> Black}],
  EdgeStyle -> {UndirectedEdge[x, y] -> Directive[Black, AbsoluteThickness[4]]}, VertexSize -> {"Scaled", 0.05},
  PlotLabel -> Style[Row[{label, ":  κ_LLY(x,y) = ", κLLY[G, {x, y}], ",  κ₀ = ", κOllivier[G, {x, y}, 0]}], 10], ImageSize -> 260];
GraphicsRow[{edgePicture[KaryTree[15, 2], {2, 4}, "tree, interior edge"], edgePicture[HypercubeGraph[3], {1, 2}, "cube"],
  edgePicture[CompleteGraph[5], {1, 2}, "K5 (purple = shared)"]}, ImageSize -> 780]

(* ::Text:: *)
(*Bakry–Émery curvature K∞ at every vertex (the discrete Bochner inequality). Tree vertices with children are negative and leaves positive; the cycle is exactly 0; the cube is 2/3, K₅ is 7/8 and Petersen is −1/3 at every vertex; on the dumbbell the bridge vertices are negative.*)

Legended[row[KeyValueMap[Function[{nm, G}, vertexCurvaturePlot[G, bakryEmery[G, #] & /@ VertexList[G], 1, nm]], family]], κLegend[1, "K_BE"]]

(* ::Text:: *)
(*Forman curvature (augmented with triangles) on every edge. It is purely combinatorial, so it is very negative wherever degrees are high and triangles are few.*)

Legended[row[KeyValueMap[Function[{nm, G}, edgeCurvaturePlot[G, formanAug, 6, nm]], family]], κLegend[6, "Forman"]]

(* ::Text:: *)
(*Resistance curvature p at every vertex. The totals are always 1, a discrete Gauss–Bonnet theorem; the dumbbell’s bridge vertices carry the negative curvature.*)

{Legended[row[KeyValueMap[Function[{nm, G}, vertexCurvaturePlot[G, pNode[G], 0.3, nm]], family]], κLegend[0.3, "p"]],
 Map[Chop@Total[pNode[#]] &, family]}

(* ::Text:: *)
(*Steinerberger curvature at every vertex. It is built from graph distance where resistance curvature uses effective resistance. On a tree the two distances coincide, so the two curvatures are exactly proportional; on the grid they are strongly correlated; on vertex-transitive graphs (cycle, cube, K₅, Petersen) both are constant.*)

{Legended[row[KeyValueMap[Function[{nm, G}, vertexCurvaturePlot[G, steinerberger[G], 1.5, nm]], family]], κLegend[1.5, "K_S"]],
 "correlation with resistance curvature" -> Map[Quiet@Correlation[steinerberger[#], pNode[#]] &, KeyTake[family, {"Binary tree", "Grid 5×5", "Dumbbell"}]]}

(* ::Text:: *)
(*Combinatorial (Higuchi) curvature drawn on polyhedra: every vertex of a Platonic solid carries the same positive share, and the shares add to χ = 2.*)

higuchiVertex[name_] := Module[{F = PolyhedronData[name, "FaceIndices"], nv = Length[PolyhedronData[name, "VertexCoordinates"]]},
   Table[1 - Count[F, _?(MemberQ[#, v] &)]/2 + Total[1/Length[#] & /@ Select[F, MemberQ[#, v] &]], {v, nv}]];
GraphicsRow[Table[Show[PolyhedronData[p], PlotLabel -> Style[Row[{p, ": ", First[higuchiVertex[p]], " × ", Length[higuchiVertex[p]], " = 2"}], 9]],
   {p, {"Tetrahedron", "Cube", "Octahedron", "Dodecahedron", "Icosahedron"}}], ImageSize -> 900]

(* ::Section:: *)
(*9. Spectral consequences on graphs, and the graph-to-manifold limit*)

(* ::Text:: *)
(*Discrete Lichnerowicz theorems for the normalised Laplacian I − D^{−1/2}AD^{−1/2}: Ollivier curvature ≥ κ > 0 gives λ₁ ≥ κ (Ollivier; Lin–Lu–Yau); CD(K,∞) gives λ₁ ≥ K (Bakry–Émery; Lin–Yau); and λ_max ≤ 2 − κ₀ (Ollivier, Bauer–Jost–Liu).*)

normLap[G_] := Module[{A = N@AdjacencyMatrix[G], d}, d = Total[A];
   IdentityMatrix[Length[d]] - DiagonalMatrix[d^(-1/2)] . A . DiagonalMatrix[d^(-1/2)]];
spec[G_] := Sort[Eigenvalues[normLap[G]]];
Dataset@Map[Function[G, With[{s = spec[G], kL = Min[κLLY[G, #] & /@ edges[G]], kB = Min[bakryEmery[G, #] & /@ VertexList[G]],
      k0 = Min[κOllivier[G, #, 0] & /@ edges[G]]},
     <|"λ1" -> s[[2]], "λmax" -> Last[s], "λ1 ≥ κ_LLY" -> s[[2]] >= kL - 10^-9,
       "λ1 ≥ K_BE" -> s[[2]] >= kB - 10^-6, "λmax ≤ 2 − κ0" -> Last[s] <= 2 - k0 + 10^-9|>]], graphs]

(* ::Text:: *)
(*Belkin–Niyogi: on points sampled from a manifold, the heat-kernel graph Laplacian (weighted mean − value)/t converges to Δ. Check on 20 000 points of S² with f = z, for which Δf = −2f: the fitted ratio should be close to 1.*)

pts = SpherePoints[20000]; tPC = 0.002; nf = Nearest[pts];
Lpc[p_] := Module[{q = nf[p, {All, 6 Sqrt[tPC]}], w}, w = Exp[-SquaredEuclideanDistance[p, #]/(4 tPC)] & /@ q;
   (w . q[[All, 3]]/Total[w] - p[[3]])/tPC];
sPC = pts[[;; ;; 200]]; lhs = Lpc /@ sPC; rhs = -2 sPC[[All, 3]];
<|"fitted ratio" -> (lhs . rhs)/(rhs . rhs), "correlation" -> Correlation[lhs, rhs]|>

(* ::Subsection:: *)
(*9.1 Pictures: curvature lower bounds under the spectral gap*)

(* ::Text:: *)
(*For each graph, λ₁ of the normalised Laplacian against the two curvature lower bounds. Every bar of κ_LLY and K_BE sits at or below λ₁; K₅ and Q₃ touch it, the discrete equality cases.*)

bounds = Map[Function[G, {spec[G][[2]], Max[0, Min[κLLY[G, #] & /@ edges[G]]], Max[0, Min[bakryEmery[G, #] & /@ VertexList[G]]]}], graphs];
BarChart[Values[bounds], ChartLabels -> {Keys[bounds], None}, ChartStyle -> {Black, RGBColor[0.98, 0.56, 0.17], RGBColor[0.18, 0.36, 0.78]},
 ChartLegends -> {"λ₁", "max(0, κ_LLY)", "max(0, K_BE)"}, PlotLabel -> "λ₁ ≥ κ and λ₁ ≥ K", ImageSize -> 520]

(* ::Text:: *)
(*The point-cloud Laplacian of f = z against the exact Δz = −2z at the sampled points: they lie on the diagonal.*)

ListPlot[Transpose[{rhs, lhs}], AspectRatio -> 1, PlotStyle -> RGBColor[0.98, 0.56, 0.17],
 Epilog -> {Gray, Dashed, Line[{{-2, -2}, {2, 2}}]}, AxesLabel -> {"Δz = −2z", "point-cloud L z"},
 PlotLabel -> "Belkin–Niyogi on 20 000 points of S²", ImageSize -> 320]

(* ::Section:: *)
(*10. Further instances, worked out: Weitzenböck, Ricci flow, mean-curvature flow, Ollivier on manifolds, Yamabe*)

(* ::Subsection:: *)
(*10.1 Weitzenböck on 1-forms: Δ_Hodge = ∇*∇ + Ric*)

(* ::Text:: *)
(*Every 1-form on S² is df + ⋆dh (S² has no harmonic 1-forms). The Hodge Laplacian commutes with d and ⋆, and equals −Δ on functions, so Δ_Hodge(df + ⋆dh) = d(−Δf) + ⋆d(−Δh) needs no further machinery. The rough Laplacian ∇*∇ω = −g^{jk}∇_k∇_j ω is computed from Christoffel symbols. The difference Δ_Hodge − ∇*∇ must be Ric(ω) = Kω = ω. Bochner’s theorem follows: Ric > 0 leaves no room for harmonic 1-forms, so b₁ = 0.*)

roughLaplacian1[g_, 𝓍_][ω_] := Module[{Γ = christoffel[g, 𝓍], gi = Inverse[g], n = Length[𝓍], T, TT},
  T = Table[D[ω[[i]], 𝓍[[j]]] - Sum[Γ[[k, i, j]] ω[[k]], {k, n}], {i, n}, {j, n}];
  TT = Table[D[T[[i, j]], 𝓍[[k]]] - Sum[Γ[[m, k, i]] T[[m, j]] + Γ[[m, k, j]] T[[i, m]], {m, n}], {i, n}, {j, n}, {k, n}];
  Table[-Sum[gi[[j, k]] TT[[i, j, k]], {j, n}, {k, n}], {i, n}]];
ΔS2 = laplaceBeltrami[gS2, 𝓍S2];
dS2[h_] := {D[h, θ], D[h, φ]};                       (* dh as a covector *)
star1[{a_, b_}] := {-b/Sin[θ], a Sin[θ]};           (* Hodge star on 1-forms of S² *)
ω1 = dS2[𝒻[θ, φ]] + star1[dS2[𝒽[θ, φ]]];
ΔHodge = dS2[-ΔS2[𝒻[θ, φ]]] + star1[dS2[-ΔS2[𝒽[θ, φ]]]];
Simplify[ΔHodge - (roughLaplacian1[gS2, 𝓍S2][ω1] + 1 ω1)]   (* K = 1 on the unit sphere *)

(* ::Subsection:: *)
(*10.2 Ricci flow ∂g/∂t = −2Ric*)

(* ::Text:: *)
(*Exact solution: the round sphere g(t) = (1 − 2t)g₀ shrinks to a point at t = 1/2, because Ric does not change under scaling.*)

Simplify[D[(1 - 2 t) gS2, t] + 2 gS2]   (* = −2 Ric(g(t)) − ∂g/∂t, Ric(g(t)) = Ric(g₀) = g₀ *)

(* ::Text:: *)
(*Numerical example. In two dimensions write g = e^{2u}(dx² + dy²); then Ricci flow is the nonlinear heat equation ∂u/∂t = e^{−2u}Δ₀u = −K. Start from a bumpy metric on the flat torus [0, 2π]². The flow irons the curvature out: max|K| decays to 0, while the total curvature ∬K dA = −∬Δ₀u dx dy stays exactly 0 (Gauss–Bonnet, χ = 0).*)

u0[x_, y_] := 0.3 Cos[x] + 0.25 Sin[2 y] Cos[x + y];
solR = First@NDSolve[{D[w[t, x, y], t] == Exp[-2 w[t, x, y]] (D[w[t, x, y], {x, 2}] + D[w[t, x, y], {y, 2}]), w[0, x, y] == u0[x, y],
     w[t, 0, y] == w[t, 2 π, y], w[t, x, 0] == w[t, x, 2 π]}, w, {t, 0, 2}, {x, 0, 2 π}, {y, 0, 2 π},
    Method -> {"MethodOfLines", "SpatialDiscretization" -> {"TensorProductGrid", "MinPoints" -> 31, "MaxPoints" -> 31}}];
Kt[tt_, x_, y_] := -Exp[-2 w[tt, x, y]] (Derivative[0, 2, 0][w][tt, x, y] + Derivative[0, 0, 2][w][tt, x, y]) /. solR;
maxK[tt_] := Max[Table[Abs[Kt[tt, x, y]], {x, 0, 2 π, π/10}, {y, 0, 2 π, π/10}]];
totalK[tt_] := Total[Flatten@Table[-(Derivative[0, 2, 0][w][tt, x, y] + Derivative[0, 0, 2][w][tt, x, y]) /. solR,
     {x, 0, 2 π - π/20, π/20}, {y, 0, 2 π - π/20, π/20}]] (π/20)^2;
TableForm[Table[{tt, maxK[tt], Chop[totalK[tt], 10^-4]}, {tt, {0, 0.25, 0.5, 1, 2}}], TableHeadings -> {None, {"t", "max |K|", "∬K dA"}}]

Row[Append[Table[DensityPlot[Kt[tt, x, y], {x, 0, 2 π}, {y, 0, 2 π}, ColorFunction -> (κColour[#, 1.5] &), ColorFunctionScaling -> False,
     PlotPoints -> 30, FrameTicks -> None, PlotLabel -> Row[{"K at t = ", tt}], ImageSize -> 160], {tt, {0, 0.25, 0.5, 2}}],
  ListLogPlot[Table[{tt, maxK[tt]}, {tt, 0, 2, 0.1}], Joined -> True, PlotStyle -> RGBColor[0.98, 0.56, 0.17], AxesLabel -> {"t", "max |K|"}, PlotLabel -> "curvature decays", ImageSize -> 240]]]

(* ::Subsection:: *)
(*10.3 Mean-curvature flow ∂X/∂t = ΔX = −2H n*)

(* ::Text:: *)
(*Exact solution: a round sphere of radius R has H = 1/R, so dR/dt = −2/R and R(t)² = R₀² − 4t.*)

Simplify[D[Sqrt[R0^2 - 4 t], t] + 2/Sqrt[R0^2 - 4 t]]

(* ::Text:: *)
(*Numerical example in the plane (curve-shortening flow, dX/dt = κN = ∂²X/∂s²). The curve is a polygon, and ∂²X/∂s² is the arc-length-weighted Laplacian of the cycle graph C_n acting on the vertex positions, a graph Laplacian again. Gage–Hamilton–Grayson: any embedded curve becomes convex, then round, and shrinks to a point. The enclosed area falls at exactly 2π per unit time, because ∮κ ds = 2π.*)

nC = 160; Xc = Table[(1 + 0.35 Cos[3 θ] + 0.2 Sin[5 θ]) {Cos[θ], Sin[θ]}, {θ, 0., 2 π - 2 π/nC, 2 π/nC}];
lapCurve[X_] := Module[{fw = RotateLeft[X] - X, bw = X - RotateRight[X], lf, lb}, lf = Norm /@ fw; lb = Norm /@ bw; 2 (fw/lf - bw/lb)/(lf + lb)];
polyArea[X_] := 1/2 Abs[Total[MapThread[#1[[1]] #2[[2]] - #2[[1]] #1[[2]] &, {X, RotateLeft[X]}]]];
resample[X_] := Module[{c = Append[X, First[X]], s, f}, s = Prepend[Accumulate[Norm /@ Differences[c]], 0];
   f = Interpolation[Transpose[{s, c}], InterpolationOrder -> 1]; Table[f[q], {q, 0, Last[s] - Last[s]/nC, Last[s]/nC}]];
dt = 2.*10^-4; snaps = {{0., Xc}}; areas = {{0., polyArea[Xc]}}; Xcur = Xc; tcur = 0.;
Do[Xcur = Xcur + dt lapCurve[Xcur]; tcur += dt;
  If[Mod[k, 50] == 0, Xcur = resample[Xcur]; AppendTo[areas, {tcur, polyArea[Xcur]}]];
  If[Mod[k, 500] == 0, AppendTo[snaps, {tcur, Xcur}]], {k, 1, 2000}];
<|"fitted dA/dt" -> Coefficient[Fit[areas, {1, s}, s], s], "−2π" -> N[-2 π]|>

Row[{Graphics[{Table[{ColorData["SunsetColors"][1 - sn[[1]]/0.45], Thick, Line[Append[sn[[2]], First[sn[[2]]]]]}, {sn, snaps}]},
   ImageSize -> 280, PlotLabel -> "curve shortening, t = 0, 0.1, 0.2, 0.3, 0.4"],
  ListPlot[areas, PlotStyle -> RGBColor[0.98, 0.56, 0.17], Epilog -> {Gray, Dashed, Line[{{0, polyArea[Xc]}, {0.4, polyArea[Xc] - 2 π 0.4}}]},
   AxesLabel -> {"t", "area"}, PlotLabel -> "area falls at 2π per unit time (dashed)", ImageSize -> 320]}]

(* ::Subsection:: *)
(*10.4 Ollivier curvature recovers Ricci curvature on a manifold*)

(* ::Text:: *)
(*Take two points x, y at distance δ along a geodesic, and the uniform measures on their ε-balls. Sliding the whole surface along the geodesic by δ (a rotation of the sphere, a translation of the plane, a hyperbolic translation) carries one ball onto the other. The average distance moved bounds W₁ from above, so it bounds κ = 1 − W₁/δ from below, and its leading term is Ollivier’s ε² Ric/(2(n+2)) = ε²K/8 for surfaces. As δ → 0 a point at latitude λ (distance λ from the geodesic) moves δ cos λ on the unit sphere, δ cosh λ in the hyperbolic plane and δ in the plane, so κ = average of 1 − cos λ, cosh λ − 1 with a minus sign, or 0. Writing 1 − cos λ = s²/(1 + √(1 − s²)) with s = sin λ avoids cancellation.*)

κS2[ε_?NumericQ] := NIntegrate[With[{s = Sin[ρ] Sin[α]}, s^2/(1 + Sqrt[1 - s^2])] Sin[ρ], {ρ, 0, ε}, {α, 0, 2 π}]/(2 π (1 - Cos[ε]));
κH2[ε_?NumericQ] := -NIntegrate[With[{s = Sinh[ρ] Sin[α]}, s^2/(1 + Sqrt[1 + s^2])] Sinh[ρ], {ρ, 0, ε}, {α, 0, 2 π}]/(2 π (Cosh[ε] - 1));
ollivierTable = Table[{ε, κS2[ε]/ε^2, 0, κH2[ε]/ε^2}, {ε, {0.05, 0.1, 0.2, 0.4, 0.8}}];
TableForm[ollivierTable, TableHeadings -> {None, {"ε", "κ/ε² on S² (K = 1)", "plane (K = 0)", "κ/ε² on H² (K = −1)"}}]

Quiet@Plot[{κS2[ε]/ε^2, 0, κH2[ε]/ε^2}, {ε, 0.03, 1.2}, PlotRange -> {-0.16, 0.16},
 PlotStyle -> {RGBColor[0.98, 0.56, 0.17], Gray, RGBColor[0.18, 0.36, 0.78]}, Epilog -> {Dashed, Gray, Line[{{0, 1/8}, {1.2, 1/8}}], Line[{{0, -1/8}, {1.2, -1/8}}]},
 PlotLegends -> {"sphere, K = 1", "plane, K = 0", "hyperbolic plane, K = −1"}, AxesLabel -> {"ε", "κ/ε²"},
 PlotLabel -> "Ollivier curvature of ε-balls → ε²K/8 (dashed ±1/8)", ImageSize -> 460]

(* ::Subsection:: *)
(*10.5 Yamabe: prescribing scalar curvature with a conformal factor*)

(* ::Text:: *)
(*For g̃ = u^{4/(n−2)} g the scalar curvature transforms by a Laplacian: S̃ = u^{−(n+2)/(n−2)} (−4(n−1)/(n−2) Δu + S u). In ℝ³ (S = 0, n = 3) this is S̃ = −8u^{−5}Δu. The factor u = (2/(1 + r²))^{1/2} turns flat ℝ³ into the round unit S³ (stereographic projection), with S̃ = 6. The 2-D analogue is Liouville’s equation of Section 2.*)

uY = (2/(1 + x^2 + y^2 + z^2))^(1/2);
{Simplify[-8 uY^-5 Laplacian[uY, {x, y, z}]],
 Plot[Evaluate[{uY^4 /. {y -> 0, z -> 0}, 1}], {x, -4, 4}, PlotStyle -> {RGBColor[0.98, 0.56, 0.17], Gray},
  PlotLegends -> {"conformal factor u⁴", "flat"}, AxesLabel -> {"r", "u⁴"}, PlotLabel -> "u⁴ g_flat = round S³, S̃ = 6", ImageSize -> 340]}

(* ::Text:: *)
(*© 2026 Computational Classnotes · CC BY-NC-SA 4.0*)
