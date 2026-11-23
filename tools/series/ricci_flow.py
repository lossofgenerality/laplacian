# Ricci flow and the curvature–Laplacian relations — notebook 14 of "Curvature from the Laplacian".
# Built from G. Khan, An Illustrated Introduction to the Ricci Flow (arXiv:2201.04923, 2022), pp. 14–33,
# and the Laplacian Curvature Lab's Ricci flow section (lab/core.js), whose readings it regenerates.
import sys, json, pathlib
sys.path.insert(0, '/home/claude/laplacian/tools/lab_nb')
import curvature_lab as L

FILE = "14-Ricci-Flow"
TITLE = "Ricci Flow and the Curvature–Laplacian Relations"
PAGE = "https://lossofgenerality.github.io/laplacian/lab/Laplacian_Curvature_Lab.html#ricci"

TOOLKIT = r"""ClearAll["Global`*"];
kcol[k_?NumericQ, s_] := With[{w = Clip[k/s, {-1, 1}]}, Blend[{RGBColor[0.10, 0.27, 0.75], GrayLevel[0.97], RGBColor[0.96, 0.47, 0.02]}, (1 + Sign[w] Abs[w]^0.55)/2]];
kLegend[s_, label_] := BarLegend[{kcol[#, s] &, {-s, s}}, LegendLabel -> label];
orange = RGBColor[0.96, 0.47, 0.02]; blue = RGBColor[0.10, 0.27, 0.75];
cmpRow[label_, q_, p_, w_] := {label, q, p, w, Abs[p - w]};
cmpGrid[rows_] := Grid[Prepend[Map[If[NumericQ[#] && ! IntegerQ[#], NumberForm[N[#], 7], #] &, rows, {2}],
   Style[#, Bold] & /@ {"", "quantity", "page (JavaScript)", "Wolfram", "|difference|"}],
  Frame -> All, Alignment -> Left, Background -> {None, {1 -> GrayLevel[0.93]}}, FrameStyle -> GrayLevel[0.75]];"""

CELLS = [
("Title", TITLE),
("Subtitle", "The heat equation, curvature as a geometric Laplacian, the maximum principle, energy and entropy, and reaction against diffusion — Curvature from the Laplacian, notebook 14"),
("Text", "© 2026 Computational Classnotes · CC BY-NC-SA 4.0"),
("Text", "Ricci flow is a heat flow of curvature. This notebook follows G. Khan, An Illustrated Introduction to the Ricci Flow (arXiv:2201.04923, 2022), pp. 14–33, and makes each step concrete on the flow the Laplacian Curvature Lab runs (" + PAGE + "): a bumpy metric e^{2u}(dx² + dy²) on the flat torus. Every derivation is worked by hand in a Text cell, then checked on the kernel; the page’s live readings are set beside Wolfram’s; every chart on the page is redrawn as a numbered figure; the flow can be played with an animator."),
("Text", "Conventions: Δ is the Laplace–Beltrami operator, negative semidefinite (Δ₀ = ∂²/∂x² + ∂²/∂y² on the flat torus [0, 2π)²); Ric(X, X) for unit X is n − 1 times the mean sectional curvature of the planes containing X; on a surface Ric = K g. Evaluate from the top: the first cell clears the session."),

("Section", "0. Toolkit and the page’s readings"),
("Input", TOOLKIT),
("Input", L.page_data(['ricci', 'rd'])),

("Section", "1. What the flow is"),
("Text", "A Riemannian metric g is an inner product on tangent vectors at each point; lengths, angles, areas and curvature come from it. The sectional curvature K(X, Y) of the plane of unit vectors X, Y measures how a small geodesic triangle with legs εX and εY falls short of a flat one: its third side is L(ε) = ε‖X − Y‖(1 − (1/12)K(X, Y)(1 + ⟨X, Y⟩)ε²) + O(ε⁴). Ricci flow (Hamilton 1982) is ∂g/∂t = −2 Ric(g): directions of positive Ricci curvature shrink, directions of negative Ricci curvature stretch."),
("Text", "Worked by hand: L(ε) on the unit sphere. Two geodesics of length ε from one point at angle θ end at points whose distance L satisfies the spherical law of cosines, cos L = cos²ε + sin²ε cos θ. With ‖X − Y‖ = 2 sin(θ/2) and ⟨X, Y⟩ = cos θ, expanding to order ε³ gives L = 2ε sin(θ/2)(1 − (1 + cos θ)ε²/12 + …): the formula with K = 1. The cell checks the expansion."),
("Input", r"""Lsph = ArcCos[Cos[ε]^2 + Sin[ε]^2 Cos[θ]];
normXY = Sqrt[2 - 2 Cos[θ]];  (* ‖X − Y‖ for unit vectors at angle θ, = 2 sin(θ/2) *)
Simplify[Normal[Series[Lsph, {ε, 0, 3}]] - ε normXY (1 - (1 + Cos[θ]) ε^2/12), 0 < θ < π && ε > 0]"""),
("Text", "Expected 0."),
("Text", "Worked by hand: the flow on a surface. Ric = K g, so ∂g/∂t = −2K g. With g = e^{2u} g₀ and g₀ flat, ∂g/∂t = 2u_t g, hence u_t = −K. Liouville’s equation K = −e^{−2u}Δ₀u turns this into u_t = e^{−2u}Δ₀u: a heat equation for u whose conductivity e^{−2u} depends on u. Examples: the stereographic sphere u = log(2/(1 + r²)) has K = 1; the half-plane u = −log y has K = −1; the round sphere g = (1 − 2t)g₀ solves the flow and vanishes at t = ½."),
("Input", r"""Kconformal[w_] := Simplify[-Exp[-2 w] (D[w, {x, 2}] + D[w, {y, 2}])];
{Kconformal[Log[2/(1 + x^2 + y^2)]], Kconformal[Log[1/y]],
 Simplify[D[(1 - 2 t) {{1, 0}, {0, Sin[θ]^2}}, t] + 2 {{1, 0}, {0, Sin[θ]^2}}]}"""),
("Text", "Expected {1, −1, zero matrix}: for g = (1 − 2t)g₀, Ric = g₀ (Ricci curvature does not change under constant scaling), so ∂g/∂t = −2g₀ = −2 Ric."),

("Section", "2. Why −2: Ricci curvature is minus a Laplacian of the metric"),
("Text", "The Laplacian has three faces: the trace of the Hessian; the mean-value defect Δf(x) = lim (2n/ε²)(mean of f on the sphere S_ε(x) − f(x)); and the rate at which the gradient flow γ′ = −∇f changes small volumes. Curvature has the same three: sectional curvature sits at second order in L(ε); the Riemann tensor plays the Hessian (in normal coordinates g_{ij} = δ_{ij} − (1/3)R_{ikjl}x^k x^l + …); Ricci curvature is its trace, and it measures how narrow geodesic cones close up (Ric > 0) or open out (Ric < 0). In harmonic coordinates Ric_{ij} = −½Δg_{ij} + lower-order terms, so −2 Ric = Δg + …: the flow is a heat equation for the metric. With +2 Ric it could only run backwards."),
("Text", "Worked by hand, in three cells. (a) Sphere mean in ℝ³: averaging the Taylor expansion of f over the unit sphere kills odd terms and gives ⟨x_i x_j⟩ = δ_{ij}/3, so the mean of f on S_ε is f + (ε²/6)Δf + …, i.e. Δf = lim (6/ε²)(mean − f), the formula with 2n = 6. (b) The flow x′ = −∇f changes the volume of a small cube at the rate −div ∇f = −Δf. (c) On a surface in conformal coordinates g_{ij} = e^{2u}δ_{ij}, the exact Ricci tensor is Ric_{ij} = K g_{ij} = −Δ₀u δ_{ij}, while −½Δ₀g_{ij} = −(Δ₀u + 2|∇₀u|²)e^{2u}δ_{ij}: they agree in the linear term and differ only by terms quadratic in u."),
("Input", r"""fT = a0 + a1 x + a2 y + a3 z + b11 x^2 + b22 y^2 + b33 z^2 + b12 x y + b13 x z + b23 y z;
sphMean = Integrate[(fT /. {x -> ε Sin[θ] Cos[φ], y -> ε Sin[θ] Sin[φ], z -> ε Cos[θ]}) Sin[θ], {θ, 0, π}, {φ, 0, 2 π}]/(4 π);
{Simplify[6/ε^2 (sphMean - a0) - Laplacian[fT, {x, y, z}]],
 Simplify[Tr[D[-Grad[fT, {x, y, z}], {{x, y, z}}]] + Laplacian[fT, {x, y, z}]]}"""),
("Text", "Expected {0, 0}: the mean-value face and the volume-compression face (the trace of the Jacobian of the flow −∇f is −Δf)."),
("Input", r"""ric = -(D[w[x, y], {x, 2}] + D[w[x, y], {y, 2}]);
halfLap = -1/2 (D[Exp[2 w[x, y]], {x, 2}] + D[Exp[2 w[x, y]], {y, 2}]);
{Simplify[halfLap + (D[w[x, y], {x, 2}] + D[w[x, y], {y, 2}] + 2 (D[w[x, y], x]^2 + D[w[x, y], y]^2)) Exp[2 w[x, y]]],
 Normal[Series[(halfLap - ric) /. w -> Function[{x, y}, s v[x, y]], {s, 0, 1}]]}"""),
("Text", "Expected: 0 (the identity for −½Δ₀g_{ij}), then 0 to first order in the size s of u: −½Δ₀g_{ij} and Ric_{ij} have the same linear part."),

("Section", "3. Hot spots cool: the maximum principle"),
("Text", "Worked by hand. Where u is largest its Hessian is negative semidefinite, so Δ₀u ≤ 0 and u_t = e^{−2u}Δ₀u ≤ 0: max u falls; likewise min u rises, until u is constant and the metric flat. For the curvature, differentiate K = −e^{−2u}Δ₀u: K_t = 2u_t e^{−2u}Δ₀u − e^{−2u}Δ₀u_t = 2(−K)(−K) + e^{−2u}Δ₀K, that is K_t = Δ_g K + 2K² with Δ_g = e^{−2u}Δ₀. At a minimum of K both terms are ≥ 0, so min K never decreases. The cell checks the curvature equation for an arbitrary u(x, y, t) solving the flow."),
("Input", r"""Kof[f_] := -Exp[-2 f] (D[f, {x, 2}] + D[f, {y, 2}]);
flowRule = Derivative[0, 0, 1][w][x, y, t] -> Exp[-2 w[x, y, t]] (D[w[x, y, t], {x, 2}] + D[w[x, y, t], {y, 2}]);
lhs = D[Kof[w[x, y, t]], t] //. {flowRule, Derivative[a_, b_, 1][w][x, y, t] :> D[Exp[-2 w[x, y, t]] (D[w[x, y, t], {x, 2}] + D[w[x, y, t], {y, 2}]), {x, a}, {y, b}]};
rhs = Exp[-2 w[x, y, t]] (D[Kof[w[x, y, t]], {x, 2}] + D[Kof[w[x, y, t]], {y, 2}]) + 2 Kof[w[x, y, t]]^2;
Simplify[lhs - rhs]"""),
("Text", "Expected 0."),

("Section", "4. Energy and entropy"),
("Text", "Worked by hand: the heat equation. For u_t = Δu on a closed space, E = ∫u² has E′ = 2∫uΔu = −2∫|∇u|² ≤ 0 (integration by parts, no boundary): heat spreads. For u > 0, S = −∫u ln u has S′ = −∫(ln u + 1)Δu = ∫|∇u|²/u ≥ 0, the Fisher information: a second law. Perelman’s breakthrough (2002) was a monotone quantity of this kind for Ricci flow, closer to a Fisher information than to an entropy. The cell checks both on the circle for the exact positive solution u = 2 + e^{−t} cos x + ½e^{−4t} sin 2x."),
("Input", r"""uh = 2 + Exp[-t] Cos[x] + Exp[-4 t] Sin[2 x]/2;
Eh = Integrate[uh^2, {x, 0, 2 π}];
Sh[τ_?NumericQ] := NIntegrate[-uh Log[uh] /. t -> τ, {x, 0, 2 π}, WorkingPrecision -> 30, PrecisionGoal -> 20];
{Simplify[D[uh, t] - D[uh, {x, 2}]], Simplify[D[Eh, t] + 2 Integrate[D[uh, x]^2, {x, 0, 2 π}]],
 With[{t0 = 3/10, d = 10^-6}, {(Sh[t0 + d] - Sh[t0 - d])/(2 d), NIntegrate[D[uh, x]^2/uh /. t -> t0, {x, 0, 2 π}, WorkingPrecision -> 30]}]}"""),
("Text", "Expected 0, 0 and two equal numbers (S′ and ∫u_x²/u at t = 0.3)."),
("Text", "Worked by hand: the flow’s own energy and entropy. Area A = ∬e^{2u}: A′ = 2∬Δ₀u = 0 on the torus (−2∬K dA = 0, Gauss–Bonnet). Energy D = ∬|∇₀u|²: D′ = −2∬Δ₀u u_t = −2∬e^{−2u}(Δ₀u)² = −2∬K² dA ≤ 0. Entropy of the area density ρ = e^{2u}/A, S = −∬ρ ln ρ: since ∬ρ_t = 0 and ρ_t = 2Δ₀u/A, S′ = −(2/A)∬Δ₀u (2u − ln A) = (4/A)∬|∇₀u|² = 4D/A ≥ 0, with maximum ln(4π²) = 3.676 exactly for the flat metric."),
("Text", "The page’s run (32 × 32 periodic grid, initial u = 0.3 cos x + 0.249 sin 2y cos(x + y), five-point Laplacian, explicit steps dt = 0.2h²e^{2 min u} to t ≥ 2), with A, D, S, ∬K² dA, min K, max u and min u recorded at every step."),
("Input", r"""ricciRun[a_, b_, N_] := Module[{h = 2. π/N, U, lap, Kf, t = 0., rec = {}, frames = {}, next = 0., stats},
   U = Table[a Cos[i h] + b Sin[2 j h] Cos[i h + j h], {i, 0, N - 1}, {j, 0, N - 1}];
   lap[W_] := (RotateLeft[W, {1, 0}] + RotateRight[W, {1, 0}] + RotateLeft[W, {0, 1}] + RotateRight[W, {0, 1}] - 4 W)/h^2;
   Kf[W_] := -Exp[-2 W] lap[W];
   stats[W_] := Module[{K = Kf[W], A = Total[Exp[2 W], 2] h^2, ρ}, ρ = Exp[2 W]/A;
     <|"t" -> t, "area" -> A, "energy" -> Total[(RotateLeft[W, {1, 0}] - W)^2 + (RotateLeft[W, {0, 1}] - W)^2, 2], "K2" -> Total[K^2 Exp[2 W], 2] h^2,
       "entropy" -> -Total[ρ Log[ρ], 2] h^2, "kmin" -> Min[K], "maxK" -> Max[Abs[K]], "umax" -> Max[W], "umin" -> Min[W]|>];
   AppendTo[rec, stats[U]]; AppendTo[frames, {0., Kf[U]}]; next = 0.05;
   While[t < 2, With[{dt = 0.2 h^2 Exp[2 Min[U]]}, U = U + dt Exp[-2 U] lap[U]; t += dt]; AppendTo[rec, stats[U]];
    If[t >= next, AppendTo[frames, {t, Kf[U]}]; next += 0.05]];
   AppendTo[frames, {t, Kf[U]}]; <|"rec" -> rec, "frames" -> frames|>];
run = ricciRun[0.3, 0.3 0.83, 32]; rec = run["rec"];
cmpGrid[Join[{cmpRow["run", "steps", 0, Length[rec] - 1] /. {a_, b_, 0, n_, _} :> {a, b, "", n, ""},
    cmpRow["", "max |K| at the end", page["ricci", "maxK"], rec[[-1, "maxK"]]], cmpRow["", "t at the end", page["ricci", "t"], rec[[-1, "t"]]]},
   Flatten[Table[{cmpRow[If[q == "area", which, ""], q, page["ricci", which, q], rec[[If[which == "start", 1, -1], q]]]},
     {which, {"start", "end"}}, {q, {"area", "energy", "entropy", "kmin", "umax", "umin"}}], 2]]]"""),
("Input", r"""rates = Table[With[{p = rec[[k - 1]], q = rec[[k]], dt = rec[[k, "t"]] - rec[[k - 1, "t"]]},
    {q["t"], (q["energy"] - p["energy"])/dt, -(q["K2"] + p["K2"]), (q["entropy"] - p["entropy"])/dt, 2 (q["energy"] + p["energy"])/q["area"]}], {k, 2, Length[rec]}];
late = Select[rates, #[[1]] > 0.2 &];
<|"largest relative gap D′ vs −2∬K²dA (t > 0.2)" -> Max[Abs[(#[[2]] - #[[3]])/#[[3]]] & /@ late],
  "largest relative gap S′ vs 4D/A (t > 0.2)" -> Max[Abs[(#[[4]] - #[[5]])/#[[5]]] & /@ late],
  "area drift, relative" -> (rec[[-1, "area"]] - rec[[1, "area"]])/rec[[1, "area"]],
  "max u never rises, min u and min K never fall" -> And @@ (Differences[#["umax"] & /@ rec] ~Join~ (-Differences[#["umin"] & /@ rec]) ~Join~ (-Differences[#["kmin"] & /@ rec]) // Thread[# <= 10^-12] &),
  "ln 4π²" -> N[Log[4 π^2]]|>"""),
("Text", "What to see: the rates agree to within 0.8% (energy) and 0.4% (entropy) after t = 0.2 (finite differences in time on a 32 × 32 grid); the area drifts by 5 × 10⁻⁴ of itself because the time steps are explicit, while the exact flow keeps it fixed; the maximum principle holds at every one of the steps; the page’s start and end readings agree with Wolfram’s to round-off."),
("Input", r"""With[{D0 = rec[[1, "energy"]], S0 = rec[[1, "entropy"]], Smax = Log[4 π^2]},
 ListLinePlot[{{#["t"], #["energy"]/D0} & /@ rec, {#["t"], (#["entropy"] - S0)/(Smax - S0)} & /@ rec}, PlotStyle -> {orange, blue}, PlotRange -> {0, 1.02},
  AxesLabel -> {"t", "fraction"}, PlotLegends -> {"energy D/D(0)", "entropy: share of the way to ln 4π²"}, ImageSize -> 420]]"""),
("Figure", "Energy falls to 1% of its start while the entropy of the area density climbs most of the way to its flat-metric maximum ln 4π² (the page’s chart “Energy falls, entropy rises”)."),
("Input", r"""kField[{t_, K_}, s_] := ArrayPlot[Reverse[Transpose[K]], ColorFunction -> (kcol[#, s] &), ColorFunctionScaling -> False, Frame -> False,
   PlotLabel -> Row[{"t = ", NumberForm[t, {3, 2}], "   colours ±", NumberForm[s, 3]}], ImageSize -> 200];
Row[{kField[run["frames"][[1]], Max[Abs[run["frames"][[1, 2]]]]], kField[SelectFirst[run["frames"], #[[1]] >= 0.5 &], Max[Abs[SelectFirst[run["frames"], #[[1]] >= 0.5 &][[2]]]]],
   kField[run["frames"][[-1]], Max[Abs[run["frames"][[-1, 2]]]]]}, "  "]"""),
("Figure", "The curvature field at t = 0, 0.5 and 2, each coloured on its own ±max|K| as the page now does, so the pattern stays visible as it shrinks: what survives is the slowest mode, a band in x."),
("Text", "The animator: play the flow; the readout gives t, max|K|, min K, the energy and the entropy at each frame. Choose a fixed colour scale to watch it fade to flat instead."),
("Input", r"""With[{nF = Length[run["frames"]], recT = #["t"] & /@ rec},
 Manipulate[With[{fr = run["frames"][[mF]]}, With[{q = rec[[First[Nearest[recT -> "Index", fr[[1]]]]]]},
    Column[{Legended[kField[fr, If[mScale == "auto", Max[Abs[fr[[2]]]], 1.5]], kLegend[If[mScale == "auto", Max[Abs[fr[[2]]]], 1.5], "K"]],
      Grid[{{"t", q["t"]}, {"max |K|", q["maxK"]}, {"min K", q["kmin"]}, {"energy D", q["energy"]}, {"entropy S", q["entropy"]}, {"area A", q["area"]}}, Alignment -> Left]}]]],
  {{mF, 1, "frame"}, 1, nF, 1, ControlType -> Animator, AnimationRate -> 8}, {{mScale, "auto", "colours"}, {"auto" -> "follow max |K|", "fixed" -> "fixed ±1.5"}}, SaveDefinitions -> True]]"""),

("Section", "5. Where the analogy stops: reaction against diffusion"),
("Text", "Ricci flow is nonlinear, and curvature obeys a reaction–diffusion equation: for the Riemann tensor ∂R/∂t = ΔR + R² + R^♯ (Hamilton), and on a surface exactly K_t = Δ_g K + 2K² (§3). Its model is u_t = Δu + u²: diffusion spreads, the reaction concentrates, and positive data can blow up in finite time."),
("Text", "Worked by hand. For constant data u₀ > 0 the reaction alone, u′ = u², gives u = u₀/(1 − u₀t), infinite at t = 1/u₀. The round unit sphere is this case: g = (1 − 2t)g₀ has K = 1/(1 − 2t), so R = 2K = 2/(1 − 2t) solves R′ = R² with ΔR = 0 and blows up at t = ½, when the sphere vanishes."),
("Input", r"""{Simplify[D[u0/(1 - u0 τ), τ] - (u0/(1 - u0 τ))^2], Simplify[D[2/(1 - 2 τ), τ] - (2/(1 - 2 τ))^2]}"""),
("Text", "The page’s comparison: u_t = u_xx + c u² on a circle of length 2π from 0.6 + 0.4 cos x, with c = 1 (reaction on) and c = 0 (the heat equation)."),
("Input", r"""rdSolve[c_, m_ : 0.6, a_ : 0.4] := Quiet@NDSolveValue[{D[v[τ, x], τ] == D[v[τ, x], {x, 2}] + c v[τ, x]^2, v[0, x] == m + a Cos[x], v[τ, 0] == v[τ, 2 π]}, v, {τ, 0, 4}, {x, 0, 2 π},
    Method -> {"MethodOfLines", "SpatialDiscretization" -> {"TensorProductGrid", "MinPoints" -> 200}}];
maxu[f_, τ_] := Max[Table[f[τ, x], {x, 0, 2 π, 2 π/200}]];
rd1 = rdSolve[1]; rd0 = rdSolve[0]; tEnd = rd1["Domain"][[1, 2]];
tHit = Quiet[τ /. FindRoot[maxu[rd1, τ] == 60, {τ, 0.95 tEnd, 0.5, tEnd}]];
cmpGrid[{cmpRow["u_t = u_xx + u²", "max u reaches 60 at t", page["rd", "blowT"], tHit], {"", "solver stops (blow-up) near t", "", tEnd, ""},
  cmpRow["u_t = u_xx", "max u at t = 4", page["rd", "heatEnd"], maxu[rd0, 4]]}]"""),
("Input", r"""LogPlot[{maxu[rd1, τ], maxu[rd0, τ]}, {τ, 0, Min[2.5, tEnd]}, PlotRange -> {0.3, 60}, PlotStyle -> {orange, blue},
 AxesLabel -> {"t", "max u"}, PlotLegends -> {"u_t = u_xx + u² (reaction wins)", "u_t = u_xx (diffusion only)"}, ImageSize -> 420]"""),
("Text", "What to see: Wolfram’s method of lines reaches 60 at t = 1.316 and stops at the blow-up near t = 1.333; the page’s explicit steps lag slightly and pass 60 at t = 1.325 (both read t ≈ 1.32). Without the reaction both reach 0.6073 at t = 4."),
("Figure", "With the reaction term the maximum blows up in finite time; without it the solution settles to its mean (the page’s reaction–diffusion chart)."),
("Text", "The animator: change the mean m and the ripple a of the initial data m + a cos x and see whether the reaction wins. For small positive data diffusion spreads the heat first, but on a closed circle the mean itself grows like the ODE u′ = u², so every positive start blows up eventually; the time is about 1/m for small ripples."),
("Input", r"""Manipulate[With[{f = rdSolve[1, mM, mA]}, With[{te = f["Domain"][[1, 2]]},
   LogPlot[maxu[f, τ], {τ, 0, Min[te, 6]}, PlotRange -> {0.05, 100}, PlotStyle -> orange, AxesLabel -> {"t", "max u"},
    PlotLabel -> Row[{"blow-up near t = ", NumberForm[te, 3], "   (1/m = ", NumberForm[1/mM, 3], ")"}], ImageSize -> 400]]],
 {{mM, 0.6, "mean m"}, 0.2, 1.5, 0.05, Appearance -> "Labeled"}, {{mA, 0.4, "ripple a"}, 0, 0.6, 0.05, Appearance -> "Labeled"}, SaveDefinitions -> True]"""),
("Text", "Why the torus flattens and the sphere vanishes. On the torus Gauss–Bonnet forces ∬K dA = 0, so positive and negative curvature balance and the reaction cannot win: the flow irons the metric flat (§4). On the sphere the total curvature is 4π > 0 and the reaction wins, but only uniformly: the sphere shrinks while becoming round. Hamilton (1988) and Chow (1991) proved that on any closed surface the normalised flow reaches constant curvature. In three dimensions necks pinch and singularities form; Perelman’s classification of them, and surgery, completed Hamilton’s programme for the Poincaré conjecture."),

("Section", "References"),
("Text", "G. Khan, An Illustrated Introduction to the Ricci Flow, arXiv:2201.04923 (2022), pp. 14–33: the heat equation, curvature, Ricci flow as a geometric heat flow, and its differences from the heat equation. The source of this notebook’s outline."),
("Text", "R. S. Hamilton, Three-manifolds with positive Ricci curvature, J. Differential Geom. 17 (1982) 255–306: introduces Ricci flow. (Not opened for this notebook.)"),
("Text", "R. S. Hamilton, The Ricci flow on surfaces, Contemp. Math. 71 (1988) 237–262: convergence on surfaces. (Not opened.)"),
("Text", "B. Chow, The Ricci flow on the 2-sphere, J. Differential Geom. 33 (1991) 325–334: the sphere without a positivity assumption. (Not opened.)"),
("Text", "G. Perelman, The entropy formula for the Ricci flow and its geometric applications, arXiv:math/0211159 (2002): the monotone functional. (Not opened.)"),
("Text", "P. Li and S.-T. Yau, On the parabolic kernel of the Schrödinger operator, Acta Math. 156 (1986) 153–201: the Li–Yau estimate Khan cites for heat equations on spaces of non-negative Ricci curvature. (Not opened.)"),
("Text", "C. Villani, Optimal Transport, Old and New, Springer (2009), ch. 14: Ricci curvature as the distortion of narrow geodesic cones. (Not opened.)"),
("Text", "© 2026 Computational Classnotes · CC BY-NC-SA 4.0"),
]
