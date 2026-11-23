"""Source of notebooks/lab/Laplacian_Curvature_Lab.nb: the notebook behind every number on the
Laplacian Curvature Lab page. Build: python3 tools/series/build_series.py curvature_lab (from tools/lab_nb on sys.path)."""
import json, re, pathlib

FILE = "Laplacian_Curvature_Lab"
DIR = "/home/claude/laplacian/notebooks/lab/"
TITLE = "Laplacian Curvature Lab — the notebook behind the page"
URL = "https://lossofgenerality.github.io/laplacian/lab/Laplacian_Curvature_Lab.html"

_here = pathlib.Path(__file__).parent
_js = json.loads((_here / "lab_readouts.json").read_text())
_app = (_here / "../../lab/app.js").resolve().read_text(encoding="utf-8")


def _num(x):
    if isinstance(x, bool): return "True" if x else "False"
    if isinstance(x, int): return str(x)
    s = "%.12g" % x
    if "e" in s:
        m, e = s.split("e"); return "%s*^%d" % (m, int(e))
    return s


def _wl(v):
    if isinstance(v, dict): return "<|" + ", ".join('"%s" -> %s' % (k, _wl(x)) for k, x in v.items()) + "|>"
    if isinstance(v, list): return "{" + ", ".join(_wl(x) for x in v) + "}"
    if isinstance(v, str): return '"%s"' % v
    return _num(v)


def page_data(keys=None):
    d = _js if keys is None else {k: _js[k] for k in keys}
    return "page = " + _wl(d) + ";"


def snippet(key):
    """The page's Wolfram snippet exactly as offered (lab/app.js SNIP), script letters as named characters."""
    m = re.search(r"\n  %s: `(.*?)`,?\n(?:  [a-z0-9]+: `|\};)" % key, _app, re.S)
    code = m.group(1)
    return re.sub(r"[\U0001D49C-\U0001D4CF]", lambda c: "\\[Script%s]" % chr(65 + ord(c.group()) - 0x1D4B6) if ord(c.group()) >= 0x1D4B6 else "\\[ScriptCapital%s]" % chr(65 + ord(c.group()) - 0x1D49C), code)


HELPERS = r"""(* page[...] holds the readouts the page computes in the browser (lab/core.js), dumped by tools/lab_nb/js_readouts.js *)
cmpRow[label_, q_, p_, w_] := {label, q, p, w, Abs[p - w]};
cmpGrid[rows_] := Grid[Prepend[Map[If[NumericQ[#] && ! IntegerQ[#], NumberForm[N[#], 7], #] &, rows, {2}],
   Style[#, Bold] & /@ {"", "quantity", "page (JavaScript)", "Wolfram", "|difference|"}],
  Frame -> All, Alignment -> Left, Background -> {None, {1 -> GrayLevel[0.93]}}, FrameStyle -> GrayLevel[0.75]];
(* the page's colour scale: blue negative, near-white zero, CCN orange positive, saturating at ±s *)
kcol[k_?NumericQ, s_] := With[{w = Clip[k/s, {-1, 1}]}, Blend[{RGBColor[0.10, 0.27, 0.75], GrayLevel[0.97], RGBColor[0.96, 0.47, 0.02]}, (1 + Sign[w] Abs[w]^0.55)/2]];
kLegend[s_, label_] := BarLegend[{kcol[#, s] &, {-s, s}}, LegendLabel -> label];
orange = RGBColor[0.96, 0.47, 0.02]; blue = RGBColor[0.10, 0.27, 0.75];"""

CELLS = [
("Title", TITLE),
("Subtitle", "Every number, check line, figure claim, Wolfram snippet and live readout on the Lab page, regenerated and compared"),
("Text", "© 2026 Computational Classnotes · CC BY-NC-SA 4.0"),
("Text", "The page: " + URL + ". This notebook has one section per section of the page, in the page’s order. Each section restates what the page claims, runs the page’s own Wolfram snippet exactly as the page offers it, recomputes every number the page prints, and sets the value the page computes in the browser (JavaScript, lab/core.js) beside the Wolfram value with their difference. A difference that is not round-off is explained where it appears. Each section then works its main example by hand, the way one would on paper, ending at the same number; redraws every plot the page draws, as numbered figures; and gives the page’s interactive parts as animators (Manipulate), with SaveDefinitions so they work after the notebook is closed and reopened. Evaluate the notebook top to bottom: each section needs §0, and §11 also uses the definitions of §4, §7 and §8."),
("Text", "Conventions are those of the page and of the write-up “The Laplacian and Curvature — Instances and Relationships”: Δ is the Laplace–Beltrami operator, negative semidefinite (Δ = ∂²/∂x² + ∂²/∂y² in the plane); on a graph Δf(v) is the mean of f over the neighbours of v minus f(v), the normalised Laplacian with the same sign."),

("Section", "0. The page’s readouts, and a comparison table"),
("Text", "The association page holds what the page shows at its default settings (and, where the page has a selector, for every choice): it is produced by running lab/core.js under Node exactly as lab/app.js runs it in the browser (tools/lab_nb/js_readouts.js). cmpGrid lays a page value beside the Wolfram value."),
("Input", page_data()),
("Input", HELPERS),

# ------------------------------------------------------------------ 1 surfaces
("Section", "1. Gauss and mean curvature, coloured on six surfaces (page: #surfaces)"),
("Text", "Page claims: K and H computed from the parametrisation; Gauss–Bonnet ∬K dA = 2πχ, so 4π on the sphere and 0 on the torus; on the torus K is positive outside, negative inside and zero on the top and bottom circles. The readouts are the range of K and the largest |H| over the drawn 57 × 37 grid, and ∬K dA over the drawn parameter domain (the page uses finite differences with step 10⁻³ and a 160 × 160 midpoint rule)."),
("Text", "The page’s Wolfram snippet (Gauss and mean curvature, and Gauss–Bonnet on the torus):"),
("Input", snippet("surfaces")),
("Text", "Expected: K = cos v/(2 + cos v) and total 0."),
("Text", "Every surface the page offers, with its parameter domain, recomputed exactly (symbolic K and H, the same 57 × 37 grid, and NIntegrate for the total). The sphere is drawn for 0.02 ≤ v ≤ π − 0.02, so its exact total there is 4π cos 0.02 = 12.5639, not 4π; the saddle, catenoid and pseudosphere are open patches, so their totals depend on the patch."),
("Input", r"""surf = <|"sphere" -> {{Sin[v] Cos[u], Sin[v] Sin[u], Cos[v]}, {0, 2 π}, {0.02, π - 0.02}},
   "cylinder" -> {{Cos[u], Sin[u], v}, {0, 2 π}, {-1, 1}},
   "torus" -> {{(2 + Cos[v]) Cos[u], (2 + Cos[v]) Sin[u], Sin[v]}, {0, 2 π}, {0, 2 π}},
   "saddle" -> {{u, v, u^2 - v^2}, {-1, 1}, {-1, 1}},
   "catenoid" -> {{Cosh[v] Cos[u], Cosh[v] Sin[u], v}, {0, 2 π}, {-1.2, 1.2}},
   "pseudosphere" -> {{Cos[u]/Cosh[v], Sin[u]/Cosh[v], v - Tanh[v]}, {0, 2 π}, {0.08, 3}}|>;
surfRows[key_] := Module[{X, U, V, c, g, Ks, Hs, tot},
   {X, U, V} = surf[key]; c = surfaceCurvatures[X, {u, v}];
   g = Flatten[Table[{U[[1]] + (U[[2]] - U[[1]]) i/56, V[[1]] + (V[[2]] - V[[1]]) j/36}, {i, 0, 56}, {j, 0, 36}], 1];
   Ks = (c["K"] /. {u -> #[[1]], v -> #[[2]]}) & /@ N[g]; Hs = (Abs[c["H"]] /. {u -> #[[1]], v -> #[[2]]}) & /@ N[g];
   tot = Chop[Quiet[NIntegrate[c["K"] c["dA"], {u, U[[1]], U[[2]]}, {v, V[[1]], V[[2]]}, PrecisionGoal -> 10, AccuracyGoal -> 12]], 10^-12];
   {cmpRow[key, "min K", page["surfaces", key, "kmin"], Min[Ks]], cmpRow["", "max K", page["surfaces", key, "kmax"], Max[Ks]],
    cmpRow["", "max |H|", page["surfaces", key, "hmax"], Max[Hs]], cmpRow["", "∬ K dA", page["surfaces", key, "total"], tot]}];
cmpGrid[Join @@ (surfRows /@ Keys[surf])]"""),
("Text", "What to see: the page’s finite differences agree with the exact values to about 5 × 10⁻⁷ (the O(h²) error of step h = 10⁻³), and its totals to the accuracy of a 160 × 160 midpoint rule. The torus total is 0 and the sphere total 4π cos 0.02, as Gauss–Bonnet says for the drawn region."),
("Input", r"""torusK = Simplify[surfaceCurvatures[surf["torus"][[1]], {u, v}]["K"]];
{torusK, Reduce[torusK > 0 && 0 <= v < 2 π, v], Solve[torusK == 0 && 0 <= v < 2 π, v]}"""),
("Text", "K > 0 exactly on the outer half (cos v > 0) and K = 0 on the circles v = π/2 and 3π/2, the top and bottom of the tube, as the page says."),

# ------------------------------------------------------------------ 2 Ricci
("Section", "2. Ricci flow is a heat equation for the conformal factor (page: #ricci)"),
("Text", "Page claims: with g = e^{2u}(dx² + dy²), Ricci flow ∂g/∂t = −2Ric is ∂u/∂t = e^{−2u}Δ₀u = −K; on the flat torus a bumpy metric is ironed out and ∬K dA stays exactly 0."),
("Text", "The page’s snippet (Liouville form of K, and the shrinking sphere):"),
("Input", snippet("ricci")),
("Text", "Expected: {1, −1, 0}: the stereographic sphere has K = 1, the half-plane K = −1, and (1 − 2t)g_{S²} solves ∂g/∂t = −2Ric = −2g."),
("Input", r"""(* the conformal form: g = e^(2w) g0 and ∂g/∂t = −2 K g give ∂w/∂t = −K = e^(−2w) Δ0 w *)
Simplify[(D[Exp[2 w[x, y, t]], t] == -2 (-Exp[-2 w[x, y, t]] (D[w[x, y, t], {x, 2}] + D[w[x, y, t], {y, 2}])) Exp[2 w[x, y, t]]) /.
   Derivative[0, 0, 1][w][x, y, t] -> Exp[-2 w[x, y, t]] (D[w[x, y, t], {x, 2}] + D[w[x, y, t], {y, 2}])]"""),
("Text", "The page’s flow, reproduced step for step: a 32 × 32 periodic grid on [0, 2π)², initial u = a cos x + b sin 2y cos(x + y) with the default bump a = 0.3, b = 0.83a, the five-point Laplacian, and explicit steps dt = 0.2 h² e^{2 min u}, run until t ≥ 2."),
("Input", r"""ricciRun[a_, b_, N_] := Module[{h = 2. π/N, U, lap, Kf, t = 0., K0},
   U = Table[a Cos[i h] + b Sin[2 j h] Cos[i h + j h], {i, 0, N - 1}, {j, 0, N - 1}];
   lap[W_] := (RotateLeft[W, {1, 0}] + RotateRight[W, {1, 0}] + RotateLeft[W, {0, 1}] + RotateRight[W, {0, 1}] - 4 W)/h^2;
   Kf[W_] := -Exp[-2 W] lap[W]; K0 = Max[Abs[Kf[U]]];
   While[t < 2, Do[With[{dt = 0.2 h^2 Exp[2 Min[U]]}, U = U + dt Exp[-2 U] lap[U]; t += dt], {20}]];
   <|"maxK0" -> K0, "t" -> t, "maxK" -> Max[Abs[Kf[U]]], "totalK" -> -Total[lap[U], 2] h^2|>];
rr = ricciRun[0.3, 0.3 0.83, 32];
cmpGrid[{cmpRow["bump 0.3", "max |K| at t = 0", page["ricci", "maxK0"], rr["maxK0"]], cmpRow["", "t at the end", page["ricci", "t"], rr["t"]],
  cmpRow["", "max |K| at the end", page["ricci", "maxK"], rr["maxK"]], cmpRow["", "∬ K dA", page["ricci", "totalK"], rr["totalK"]]}]"""),
("Text", "Note for the proof-reader. The page’s check line used to quote the write-up notebook §10.2 (NDSolve on a 31 × 31 grid: max|K| 4.83 → 0.059 by t = 2). That is a different initial bump and grid, so it did not match the page’s own readout (4.63 → 0.053 by t ≈ 2.11 at the default bump). The page now quotes this section. ∬K dA is 0 to round-off because it is −h²ΣΔ₀u, and a periodic Laplacian sums to zero exactly."),

# ------------------------------------------------------------------ 3 means
("Section", "3. The mean-value origin of Δ, on a curved surface (page: #means)"),
("Text", "Page claims: on a surface of constant curvature K the geodesic-circle mean is M_r f = f + r²Δf/4 + r⁴(Δ²f/64 + KΔf/96) + r⁶(Δ³f/2304 + KΔ²f/1152 + K²Δf/1440) + O(r⁸); for f = eˣ(1 + z)² + yz³ on the unit sphere, at the pole f = 4, Δf = −4, Δ²f = −20, Δ³f = 500; the errors of the flat formula, of + KΔf/96, and of + the r⁶ terms fall with slopes 4, 6 and 8 on log–log axes; and A(r)/πr² = 1 − Kr²/12 + K²r⁴/360 − …"),
("Text", "The page’s snippet: the pole values, and the r⁶ expansion checked exactly (the last entry must be 0):"),
("Input", snippet("means")),
("Text", "The error slopes, recomputed with the exact circle mean (NIntegrate at 30 digits) on the page’s radii r = 2^{−k/4}, k = 4 … 24, fitted on 0.04 < r < 0.16 as the page does:"),
("Input", r"""F0[{x_, y_, z_}] := Exp[x] (1 + z)^2 + y z^3; pole = {4, -4, -20, 500};
cm[r_] := NIntegrate[F0[{Sin[r] Cos[φ], Sin[r] Sin[φ], Cos[r]}], {φ, 0, 2 π}, WorkingPrecision -> 30, PrecisionGoal -> 25]/(2 π);
flat[r_] := pole[[1]] + r^2/4 pole[[2]] + r^4 pole[[3]]/64; c4[r_] := flat[r] + r^4 pole[[2]]/96;
c6[r_] := c4[r] + r^6 (pole[[4]]/2304 + pole[[3]]/1152 + pole[[2]]/1440);
rs = Select[N[2^(-Range[4, 24]/4), 30], 0.04 < # < 0.16 &];
slopes = Table[Coefficient[Fit[{Log[#], Log[Abs[cm[#] - ap[#]]]} & /@ rs, {1, s}, s], s], {ap, {flat, c4, c6}}];
cmpGrid[MapThread[cmpRow[#1, "log–log slope", #2, #3] &, {{"flat formula", "+ KΔf/96 at r^4", "+ r^6 terms"}, page["means", "slopes"], slopes}]]"""),
("Text", "What to see: slopes near 4, 6 and 8. They are not exactly integers because each error still carries its next-order term on this window; the page fits the same window, so page and Wolfram agree closely. The last slope differs in the third decimal (8.005 on the page, 8.000 here) because those errors are near 10⁻¹³, where the page’s double-precision 720-point circle mean starts to show round-off; here the circle mean is computed to 25 digits."),
("Input", r"""(* disc area on a surface of constant curvature K: A(r) = 2π(1 − cos √K r)/K *)
Series[2 π (1 - Cos[Sqrt[K] r])/K/(π r^2), {r, 0, 5}]"""),

# ------------------------------------------------------------------ 4 heat
("Section", "4. Curvature is the first correction to Weyl’s law (page: #heat)"),
("Text", "Page claims: Tr e^{tΔ} ~ (4πt)^{−n/2}(Vol + (t/6)∫S + …) (McKean–Singer). For the unit sphere (eigenvalues l(l + 1), multiplicity 2l + 1, area 4π) the ratio to Weyl’s Area/(4πt), which is t·Tr e^{tΔ}, rises like 1 + t/3 (+ t²/15); the flat square torus of the same area stays at 1. The readouts are at the slider value, default t = 0.05."),
("Text", "The page’s snippet:"),
("Input", snippet("heat")),
("Input", r"""sph[t_] := With[{s = SetPrecision[t, 30]}, s Sum[(2 l + 1) Exp[-l (l + 1) s], {l, 0, 600}]];  (* terms beyond l = 600 are below e^(−1800) for t ≥ 0.005 *)
tor[t_] := t (EllipticTheta[3, 0, Exp[-π t]])^2;  (* side 2√π: eigenvalues π(m² + n²) *)
cmpGrid[Join @@ Table[With[{t = h["t"]}, {cmpRow["t = " <> ToString[t], "sphere t·Tr", h["sphere"], sph[t]],
     cmpRow["", "1 + t/3 + t²/15", h["series"], 1 + t/3 + t^2/15], cmpRow["", "flat torus t·Tr", h["torus"], tor[t]]}], {h, page["heat"]}]]"""),
("Input", r"""(* why the torus line is flat: by Poisson summation θ3(0, e^(−πt)) = t^(−1/2) θ3(0, e^(−π/t)) *)
Table[N[tor[t] - 1, 20], {t, {0.01, 0.05, 0.1, 0.4}}]"""),
("Text", "The torus ratio is θ₃(0, e^{−π/t})² = 1 + 4e^{−π/t} + …: 1 to machine precision for t ≤ 0.1, and 1.0016 at the slider’s end t = 0.4. “Stays at 1” on the page means up to this exponentially small term; on the page’s scale its curve is flat."),

# ------------------------------------------------------------------ 5 Bochner
("Section", "5. Bochner’s formula, and what a curvature bound controls (page: #bochner)"),
("Text", "Page claims: ½Δ|∇f|² = |Hess f|² + ⟨∇f, ∇Δf⟩ + Ric(∇f, ∇f); integrated it gives Lichnerowicz λ₁ ≥ nk; along geodesics the comparison Δr ≤ (n − 1)√k cot(√k r); carré du champ Γ(f) = ½(Δ(f²) − 2fΔf) = |∇f|² and Γ₂(f) = ½ΔΓ(f) − Γ(f, Δf). The readouts at K (default 1, n = 2): Lichnerowicz bound 2K, round sphere λ₁ = 2K, Bonnet–Myers diameter ≤ π/√K, Δr changes sign at π/(2√K); for K ≤ 0, Δr → √|K|."),
("Text", "The page’s snippet: Bochner on S² for an arbitrary function (must return 0):"),
("Input", snippet("bochner")),
("Input", r"""(* on a surface of constant curvature K in geodesic polar coordinates, ds² = dr² + sn(r)² dθ², Δr = sn'(r)/sn(r) *)
sn[K_, r_] := Sin[Sqrt[K] r]/Sqrt[K];
{Simplify[D[sn[K, r], r]/sn[K, r] - Sqrt[K] Cot[Sqrt[K] r], K > 0], Normal[Series[Sqrt[K] Cot[Sqrt[K] r], {K, 0, 0}]],
 Limit[Sqrt[-K] Coth[Sqrt[-K] r], r -> ∞, Assumptions -> K < 0], Reduce[Sqrt[K] Cot[Sqrt[K] r] == 0 && 0 < r < π/Sqrt[K] && K > 0, r]}"""),
("Input", r"""(* round sphere of curvature K: λ1 = 2K, the Lichnerowicz equality case for n = 2; Γ is |∇f|² *)
With[{K = 7/3}, {Min[Select[Table[l (l + 1) K, {l, 0, 4}], # > 0 &]], 2 K}]"""),
("Input", r"""X = {θ, φ}; g = {{1, 0}, {0, Sin[θ]^2}}; Lap[w_] := 1/Sin[θ] (D[Sin[θ] D[w, θ], θ] + D[w, φ, φ]/Sin[θ]);
Simplify[1/2 (Lap[\[ScriptF][θ, φ]^2] - 2 \[ScriptF][θ, φ] Lap[\[ScriptF][θ, φ]]) - (D[\[ScriptF][θ, φ], θ]^2 + D[\[ScriptF][θ, φ], φ]^2/Sin[θ]^2)]"""),

# ------------------------------------------------------------------ 6 mesh
("Section", "6. On a mesh, angle defect is curvature and the cotangent Laplacian is −2Hn (page: #mesh)"),
("Text", "Page claims: (Δf)_i = (1/2A_i) Σ_j (cot α_ij + cot β_ij)(f_j − f_i); the angle defect δ_i = 2π − Σθ_i (a cube corner: 2π − 3·π/2 = π/2); K_i ≈ δ_i/A_i; the defects of a closed mesh add to exactly 2πχ. Fig. 7.1 on the page states: ang[i, j, k] := VectorAngle[P[[j]] − P[[i]], P[[k]] − P[[i]]] is the corner angle at vertex i; 1000 random triangles have angle sum π (error below 10⁻¹⁵); a right triangle gives π/2, π/4, π/4; a flat fan has defect 0, a square-pyramid apex 2π/3, a saddle vertex −0.81 (on z = (x² − y²)/2, eight neighbours on the unit circle). The page’s A_i is the barycentric area (one third of each incident triangle)."),
("Text", "6.1 The checks quoted in the caption of Fig. 7.1:"),
("Input", r"""SeedRandom[7]; angSum[P_] := Module[{ang}, ang[i_, j_, k_] := VectorAngle[P[[j]] - P[[i]], P[[k]] - P[[i]]];
   ang[1, 2, 3] + ang[2, 3, 1] + ang[3, 1, 2]];
<|"right triangle" -> Module[{P = {{0, 0, 0}, {1, 0, 0}, {0, 1, 0}}, ang}, ang[i_, j_, k_] := VectorAngle[P[[j]] - P[[i]], P[[k]] - P[[i]]]; {ang[1, 2, 3], ang[2, 3, 1], ang[3, 1, 2]}],
  "max |angle sum − π|, 1000 random triangles" -> Max[Table[Abs[angSum[RandomReal[{-1, 1}, {3, 3}]] - π], {1000}]],
  "symmetric in j, k" -> Module[{P = RandomReal[1, {3, 3}]}, VectorAngle[P[[2]] - P[[1]], P[[3]] - P[[1]]] == VectorAngle[P[[3]] - P[[1]], P[[2]] - P[[1]]]]|>"""),
("Input", r"""defectAt[apex_, ring_] := 2 π - Total[Table[VectorAngle[ring[[k]] - apex, ring[[Mod[k, Length[ring]] + 1]] - apex], {k, Length[ring]}]];
hex = Table[{Cos[2 π k/6], Sin[2 π k/6], 0}, {k, 0, 5}];
<|"flat fan of six triangles" -> Chop[defectAt[{0, 0, 0}, hex]],
  "square-pyramid apex (unit edges)" -> FullSimplify[defectAt[{0, 0, 1/Sqrt[2]}, {{1, 0, 0}, {0, 1, 0}, {-1, 0, 0}, {0, -1, 0}}/Sqrt[2]]],
  "saddle vertex on z = (x² − y²)/2, eight neighbours on the unit circle" -> N[defectAt[{0, 0, 0}, Table[With[{t = 2 π k/8}, {Cos[t], Sin[t], (Cos[t]^2 - Sin[t]^2)/2}], {k, 0, 7}]]]|>"""),
("Text", "The square-pyramid apex with unit edges has four equilateral corners, so its defect is 2π − 4π/3 = 2π/3. The saddle ring alternates up and down, so the corner angles add to more than 2π and the defect is negative: −0.8054."),
("Text", "6.2 The regular polyhedra, quoted in the write-up §6 and on the page’s lede: every vertex defect, and their total divided by 2π, which is χ = 2."),
("Input", r"""polyDefects[name_] := Module[{P = N[PolyhedronData[name, "VertexCoordinates"]], F = PolyhedronData[name, "FaceIndices"], def},
   def = ConstantArray[2. π, Length[P]];
   Do[Do[With[{i = f[[k]], j = f[[Mod[k, Length[f]] + 1]], l = f[[Mod[k - 2, Length[f]] + 1]]}, def[[i]] -= VectorAngle[P[[j]] - P[[i]], P[[l]] - P[[i]]]], {k, Length[f]}], {f, F}];
   {name, Length[P], Union[Rationalize[def/π, 10^-9]] π, Chop[Total[def]/(2 π), 10^-12]}];
Grid[Prepend[polyDefects /@ {"Tetrahedron", "Cube", "Octahedron", "Dodecahedron", "Icosahedron"}, Style[#, Bold] & /@ {"polyhedron", "vertices", "defect at each vertex", "Σ defect / 2π"}], Frame -> All]"""),
("Text", "6.3 The page’s snippet (angle defect on a 40 × 20 torus mesh; must return 0):"),
("Input", snippet("mesh")),
("Text", "6.4 The readouts at all four resolutions the page offers: vertices, Σ defect, Σ defect/2π and max |K_mesh − K| with K = cos v/(2 + cos v). The mesh, the barycentric area and the cotangent weights below are the page’s (lab/core.js), written in Wolfram Language."),
("Input", r"""meshCurvature[P_, T_] := Module[{nv = Length[P], ang, def, Am},
   ang[i_, j_, k_] := VectorAngle[P[[j]] - P[[i]], P[[k]] - P[[i]]];
   def = ConstantArray[2. π, nv]; Am = ConstantArray[0., nv];
   Do[Module[{a, b, c}, {a, b, c} = tri; def[[a]] -= ang[a, b, c]; def[[b]] -= ang[b, c, a]; def[[c]] -= ang[c, a, b];
     Am[[{a, b, c}]] += Norm[Cross[P[[b]] - P[[a]], P[[c]] - P[[a]]]]/6], {tri, T}];
   <|"defect" -> def, "area" -> Am|>];
torusMesh[nu_, nv_] := Module[{id}, id[i_, j_] := Mod[i, nu] nv + Mod[j, nv] + 1;
   {Flatten[Table[N[{(2 + Cos[2 π j/nv]) Cos[2 π i/nu], (2 + Cos[2 π j/nv]) Sin[2 π i/nu], Sin[2 π j/nv]}], {i, 0, nu - 1}, {j, 0, nv - 1}], 1],
    Flatten[Table[{{id[i, j], id[i + 1, j], id[i + 1, j + 1]}, {id[i, j], id[i + 1, j + 1], id[i, j + 1]}}, {i, 0, nu - 1}, {j, 0, nv - 1}], 2]}];
meshRows[m_] := Module[{P, T, M, Km, Ks},
   {P, T} = torusMesh[m["nu"], m["nv"]]; M = meshCurvature[P, T]; Km = M["defect"]/M["area"];
   Ks = Flatten[Table[N[Cos[2 π j/m["nv"]]/(2 + Cos[2 π j/m["nv"]])], {i, 0, m["nu"] - 1}, {j, 0, m["nv"] - 1}]];
   {cmpRow[ToString[m["nu"]] <> " × " <> ToString[m["nv"]], "vertices", m["vertices"], Length[P]],
    cmpRow["", "Σ defect", m["defect"], Total[M["defect"]]], cmpRow["", "max |Kmesh − K|", m["err"], Max[Abs[Km - Ks]]],
    cmpRow["", "Kmesh at the outer equator (K = 1/3)", m["Kouter"], Km[[1]]]}];
cmpGrid[Join @@ (meshRows /@ page["mesh"])]"""),
("Text", "What to see: the total defect is 0 = 2πχ(torus) at every resolution, to round-off; the pointwise error falls by about 2.6 for each 1.6-fold refinement, i.e. like h², as the barycentric-area estimate does on this regular mesh."),

# ------------------------------------------------------------------ 7 graphs
("Section", "7. Seven graph curvatures, each built from the graph Laplacian (page: #graphs)"),
("Text", "Page claims: the seven graphs (binary tree on 15 vertices, cycle C₆, cube Q₃, complete K₅, Petersen, 5 × 5 grid, dumbbell of two K₅ joined by a path of three edges) and seven curvatures: Lin–Lu–Yau κ_LLY (edges), non-lazy Ollivier κ₀ (edges), Bakry–Émery K_∞ (vertices), Forman F = 4 − d_x − d_y (edges), Forman with triangles F + 3·#triangles (edges), resistance curvature p_i = 1 − ½Σ_{j∼i} ω_ij (vertices) with ω the effective resistance, and Steinerberger curvature w solving Dw = n·1 with D the distance matrix (vertices). The readouts are min, max and mean (the sum for resistance curvature) of the chosen curvature, λ₁ and λ_max of the normalised Laplacian, and the checks λ₁ ≥ min κ_LLY and λ₁ ≥ min K_∞. Vertex numbers below are the page’s, plus one."),
("Text", "The page’s snippet (Lin–Lu–Yau by the Münch–Wojciechowski linear programme, and λ₁ on Q₃):"),
("Input", snippet("graphs")),
("Text", "Expected: {{2/3}, 2/3}. All seven curvatures in Wolfram Language. κ_LLY and κ₀ are computed by optimal transport between the neighbourhood measures (LinearOptimization), K_∞ as the largest K with Γ₂ − KΓ ⪰ 0 on functions on the ball of radius 2 (the quadratic forms are built symbolically from Δ, then the bound is found by bisection on the least eigenvalue), resistance and Steinerberger curvature from pseudoinverses."),
("Input", r"""W1[G_, m1_, m2_] := Module[{s1 = Keys[m1], s2 = Keys[m2], x, vars, d},
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
normSpec[G_] := Module[{A = N@AdjacencyMatrix[G], d}, d = Total[A]; Sort[Eigenvalues[IdentityMatrix[Length[d]] - DiagonalMatrix[d^(-1/2)] . A . DiagonalMatrix[d^(-1/2)]]]];"""),
("Text", "Γ and Γ₂ above are built straight from the definition Γ(f) = ½(Δ(f²) − 2fΔf), Γ₂(f) = ½ΔΓ(f) − Γ(f, Δf) at x, as exact quadratic forms in the values of f on the 2-ball, not copied from the page’s code; only the final bisection is the same idea as the page’s."),
("Input", r"""curvs = <|"lly" -> {"Lin–Lu–Yau κ", "e", κLLYedge}, "k0" -> {"Ollivier κ₀", "e", κ0edge}, "be" -> {"Bakry–Émery K∞", "v", KBE},
   "forman" -> {"Forman", "e", formanE}, "formanAug" -> {"Forman + triangles", "e", formanT}, "res" -> {"resistance p", "all", resistanceP}, "stein" -> {"Steinerberger", "all", steinerbergerW}|>;
graphOf[g_] := Graph[Range[page["graphs", g, "n"]], UndirectedEdge @@@ page["graphs", g, "edges"]];
wlValues[g_, k_] := With[{G = graphOf[g], c = curvs[k]}, Switch[c[[2]], "e", c[[3]][G, #] & /@ page["graphs", g, "edges"], "v", c[[3]][G, #] & /@ VertexList[G], "all", c[[3]][G]]];
graphTable[g_] := Module[{G = graphOf[g], sp = normSpec[graphOf[g]]},
   Join[Join @@ Table[With[{w = N[wlValues[g, k]], p = page["graphs", g, k]},
       {{If[k == "lly", g, ""], curvs[k][[1]] <> ": min", Min[p], Min[w], Abs[Min[p] - Min[w]]},
        {"", "   max", Max[p], Max[w], Abs[Max[p] - Max[w]]},
        {"", "   largest |page − Wolfram| over all " <> If[curvs[k][[2]] == "e", "edges", "vertices"], "", "", Max[Abs[p - w]]}}], {k, Keys[curvs]}],
    {cmpRow["", "λ₁ (normalised)", page["graphs", g, "lambda1"], sp[[2]]], cmpRow["", "λmax", page["graphs", g, "lambdaMax"], sp[[-1]]]}]];
cmpGrid[graphTable["dumbbell"]]"""),
("Text", "The dumbbell is the page’s default graph. The same table for the other six (each takes a few seconds; the linear programmes dominate):"),
("Input", r"""Column[{Style[#, Bold], cmpGrid[graphTable[#]]}, Spacings -> 1] & /@ {"tree", "cycle", "cube", "complete", "petersen", "grid"} // Column"""),
("Text", "The note the page shows under each graph, checked claim by claim:"),
("Input", r"""val[g_, k_] := N[wlValues[g, k]]; edgeIdx[g_, pred_] := Position[page["graphs", g, "edges"], _?pred, {1}, Heads -> False][[All, 1]];
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
     GroupBy[Transpose[{Sort[deg[[#]]] & /@ page["graphs", "grid", "edges"], Rationalize[val["grid", "lly"], 10^-6]}], First -> Last, Union]],
  "dumbbell: κLLY on the three bridge edges" -> Rationalize[val["dumbbell", "lly"][[-3 ;;]], 10^-6]|>"""),
("Text", "Read against the page’s notes, which were corrected on 23 Nov 2026 from this cell: on the tree the interior edges have κ_LLY = −2/3 except the two edges at the root, whose end has degree 2 (−1/3), and the leaf edges have +2/3; on a tree effective resistance equals distance, and Steinerberger curvature is exactly 2n/(n − 1) = 15/7 times resistance curvature (the page’s note says “proportional”, which is right; the inverse distance matrix of a tree is −½L + ττᵀ/(2(n − 1)) with τ = 2 − degree, Graham–Lovász, so D⁻¹1 = τ/(n − 1) and p = τ/2); C₆ is flat for all three; Q₃ has κ_LLY = K_∞ = λ₁ = 2/3 and K₅ has κ_LLY = λ₁ = 5/4, equality cases of λ₁ ≥ κ; Petersen has κ_LLY = 0, κ₀ = −1/3, K_∞ = −1/3 and λ₁ = 2/3. On the grid κ_LLY is 0 on interior edges and along the sides, +1/6 on edges from a side inward and +1/3 on edges at a corner (the page’s note had said the whole boundary is positive). On the dumbbell the two edges joining a clique to the path have κ_LLY = −3/5 and the middle edge of the path has 0 (the note had said all bridge edges are −3/5)."),
("Input", r"""(* the two discrete Lichnerowicz bounds the page ticks, on every graph *)
Table[With[{G = graphOf[g]}, {g, normSpec[G][[2]] >= Min[val[g, "lly"]] - 10^-9, normSpec[G][[2]] >= Min[val[g, "be"]] - 10^-6, Chop[Total[val[g, "res"]] - 1, 10^-9] == 0}], {g, Keys[page["graphs"]]}] //
 Grid[Prepend[#, Style[#, Bold] & /@ {"graph", "λ₁ ≥ min κLLY", "λ₁ ≥ min K∞", "Σ p = 1 (Foster)"}], Frame -> All] &"""),

# ------------------------------------------------------------------ 8 flows
("Section", "8. Mean-curvature flow: a curve rounds itself off (page: #flows)"),
("Text", "Page claims: ∂X/∂t = ΔX = κN; in the plane any embedded curve becomes convex, then round, and shrinks to a point (Gage–Hamilton–Grayson); the area falls at exactly 2π per unit time because ∮κ ds = 2π. The page moves each vertex of a polygon by k(t_f − t_b) with k = 2/(ℓ_f + ℓ_b) (ℓ the edge lengths, t the unit edge directions), the cycle-graph Laplacian weighted by arc length. Since 23 Nov 2026 its time steps are at most 0.2 × (shortest edge)², the stability limit of an explicit heat step; every 20 steps it checks the polygon and resamples it by arc length only when needed: when 160 × (perimeter/initial perimeter) vertices (at least 24) is under 85% of the current count, or when the longest edge exceeds three times the shortest. Each resampling cuts corners and loses a little area, so it is done as rarely as this. Before this the step was a fixed 2 × 10⁻⁴; as the curve shrank its edges fell below that limit, the polygon broke into a zig-zag (“prickly”) at the end, and the mean dA/dt read about −5.6 instead of −2π."),
("Text", "The page’s snippet (exact flows: the round sphere under Ricci flow, and a sphere of radius √(R₀² − 4t) under mean-curvature flow; both residuals 0):"),
("Input", snippet("flows")),
("Text", "The page’s polygon flow in Wolfram Language, run on all four starting curves until the area falls below 8% of its start; the mean dA/dt should be −2π = −6.2832:"),
("Input", r"""curveInit[kind_, n_: 160] := Module[{f = <|"wiggle" -> (1 + 0.35 Cos[3 #] + 0.2 Sin[5 #] &), "star" -> (1 + 0.45 Cos[5 #] &),
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
cmpGrid[Flatten[Table[{cmpRow[k, "mean dA/dt", page["flows", k, "rate"], runs[k, "rate"]], cmpRow["", "t when area < 8%", page["flows", k, "t"], runs[k, "t"]]}, {k, Keys[runs]}], 1]]"""),
("Text", "The page advances its flow in frames of 3 × 10⁻³ (15 × 2 × 10⁻⁴) and stops at the end of the first frame below 8%, so its t is a little later than Wolfram’s, which stops at the first step. Both rates are within about 0.5% of −2π; the small excess is the area lost at each resampling, and the polygon’s own rate between resamplings is −Σ 2 sin(θ_i/2) over its turning angles θ_i, just under 2π. The last polygon of each run, which should be a smooth near-circle:"),
("Input", r"""Row[Table[Graphics[{RGBColor[0.98, 0.56, 0.17], Thickness[0.012], Line[Append[#, First[#]] &[runs[k, "X"]]]}, PlotLabel -> k, ImageSize -> 140, PlotRange -> 0.45], {k, Keys[runs]}], "  "]"""),
("Figure", "The last frame of curve shortening for the four starting curves: smooth near-circles, with no zig-zag."),

# ------------------------------------------------------------------ 9 Ollivier
("Section", "9. Comparing two ball averages measures Ricci curvature (page: #ollivier)"),
("Text", "Page claims: Ollivier’s κ(x, y) = 1 − W₁(μ_x, μ_y)/d(x, y) with μ uniform on ε-balls satisfies κ ≈ ε²Ric(v, v)/(2(n + 2)) = ε²K/8 on a surface; sliding the surface along the geodesic carries one ball onto the other, and a point at distance λ from the geodesic moves δ cos(√K λ), so κ is a plain integral over the ball. The readouts at K (slider −2 … 2, default 1): κ/ε² at ε = 0.05, K/8, and κ/ε² at the largest ε drawn."),
("Text", "The page’s snippet:"),
("Input", snippet("ollivier")),
("Input", r"""κball[K_, ε_?NumericQ] := Which[K == 0, 0, K > 0, With[{R = 1/Sqrt[K]},
     NIntegrate[With[{s = Sin[ρ/R] Sin[α]}, s^2/(1 + Sqrt[1 - s^2])] Sin[ρ/R], {ρ, 0, ε}, {α, 0, 2 π}, PrecisionGoal -> 10]/NIntegrate[Sin[ρ/R] 2 π, {ρ, 0, ε}]],
   True, With[{R = 1/Sqrt[-K]}, -NIntegrate[With[{s = Sinh[ρ/R] Sin[α]}, s^2/(1 + Sqrt[1 + s^2])] Sinh[ρ/R], {ρ, 0, ε}, {α, 0, 2 π}, PrecisionGoal -> 10]/NIntegrate[Sinh[ρ/R] 2 π, {ρ, 0, ε}]]];
cmpGrid[Flatten[Table[{cmpRow["K = " <> ToString[o["K"]], "κ/ε² at ε = 0.05", o["at005"], κball[o["K"], 0.05]/0.05^2], cmpRow["", "K/8", o["K"]/8, o["K"]/8],
     cmpRow["", "κ/ε² at ε = " <> ToString[NumberForm[o["emax"], 3]], o["atmax"], κball[o["K"], o["emax"]]/o["emax"]^2]}, {o, page["ollivier"]}], 1]]"""),
("Text", "Note for the proof-reader. The page’s check line quotes κ/ε² = 0.12496 (sphere), 0 (plane) and −0.12504 (hyperbolic plane) at ε = 0.05 from notebook 07-Ollivier §8. The page’s own readout for K = −1 is −0.12504 (its 160 × 160 midpoint rule), and the converged value above agrees to five figures."),

# ------------------------------------------------------------------ 10 forms + snippets
("Section", "10. Every Laplacian–curvature relationship on one sheet (page: #forms) and the free cell’s other snippets"),
("Text", "The sheet restates formulas checked in the sections above and in the write-up notebook (LaplacianCurvature.nb §2–§10). Two snippets of the page’s free Wolfram cell are not tied to a section above; both must return the stated value."),
("Text", "Yamabe: u⁴ times the flat metric of ℝ³ is the round S³, scalar curvature 6:"),
("Input", snippet("yamabe")),
("Text", "Weitzenböck on S²: Δ_Hodge ω − ∇*∇ω = Ric(ω) = ω for every 1-form df + ⋆dh (must return {0, 0}):"),
("Input", snippet("weitzenbock")),
("Input", r"""(* the ball-volume line of the sheet, n = 2 and n = 3 on spheres of curvature K: Vol B_r = ω_n r^n (1 − S r²/(6(n + 2)) + …), S = n(n − 1)K *)
{Series[2 π (1 - Cos[Sqrt[K] r])/K/(π r^2), {r, 0, 2}], Series[4 π/K^(3/2) (Sqrt[K] r/2 - Sin[2 Sqrt[K] r]/4)/(4/3 π r^3), {r, 0, 2}], {1 - 2 K r^2/(6 4), 1 - 6 K r^2/(6 5)}}"""),

# ------------------------------------------------------------------ 11 quiz
("Section", "11. Self-check: every answer the page marks right (page: #quiz)"),
("Input", r"""tK = Simplify[(Cos[v]/(1 (2 + 1 Cos[v])))];
<|"1. torus K < 0 on the inner half" -> Reduce[tK < 0 && 0 <= v < 2 π, v],
  "1. ∬K dA on the torus" -> Integrate[tK (2 + Cos[v]), {u, 0, 2 π}, {v, 0, 2 π}],
  "2. order at which K enters the circle mean (coefficient of K)" -> (Coefficient[r^2/4 d1 + r^4 (d2/64 + K d1/96) + r^6 (d3/2304 + K d2/1152 + K^2 d1/1440), K] /. {d1 -> 1, d2 -> 1, d3 -> 1} // Expand),
  "3. heat trace t-term on the unit sphere: ratio − 1 ≈ t/3 = (1/6)∫S/Area" -> {N[sph[0.001] - 1, 6], 0.001/3},
  "6. Σ resistance curvature on every graph" -> (Round[Total[val[#, "res"]], 10^-9] & /@ Keys[page["graphs"]]),
  "7. dA/dt for the four curves" -> (runs[#, "rate"] & /@ Keys[runs]),
  "8. ∂u/∂t = −K under 2-D Ricci flow" -> "§2 above"|>"""),
("Text", "Question 4 (Bakry–Émery copies Bochner, Γ₂ ≥ KΓ) and question 5 (the dumbbell’s bridge is negative because its two neighbourhoods barely overlap) are checked in §5 and §7."),
("Text", "© 2026 Computational Classnotes · CC BY-NC-SA 4.0"),
]

# ====================================================================== additions of 23 Nov 2026:
# worked by hand, every plot the page draws, and the page's interactive parts as animators
EXTRA = {}
EXTRA[1] = [
("Subsection", "1.1 Worked by hand: the torus"),
("Text", "Take X(u, v) = ((2 + cos v) cos u, (2 + cos v) sin u, sin v). Then X_u = (2 + cos v)(−sin u, cos u, 0) and X_v = (−sin v cos u, −sin v sin u, cos v), so E = X_u·X_u = (2 + cos v)², F = X_u·X_v = 0, G = X_v·X_v = 1, and dA = √(EG − F²) du dv = (2 + cos v) du dv."),
("Text", "The unit normal is n = X_u × X_v/|X_u × X_v| = (cos v cos u, cos v sin u, sin v), pointing out of the tube. Second derivatives: X_uu = −(2 + cos v)(cos u, sin u, 0), X_uv = sin v (sin u, −cos u, 0), X_vv = −(cos v cos u, cos v sin u, sin v). So L = X_uu·n = −(2 + cos v) cos v, M = X_uv·n = 0, N = X_vv·n = −1."),
("Text", "Gauss curvature: K = (LN − M²)/(EG − F²) = (2 + cos v) cos v/(2 + cos v)² = cos v/(2 + cos v). Mean curvature: H = (EN − 2FM + GL)/(2(EG − F²)) = (−(2 + cos v)² − (2 + cos v) cos v)/(2(2 + cos v)²) = −(1 + cos v)/(2 + cos v). (The sign of H follows the outward normal; the page shows |H|.)"),
("Text", "Readings: on the outer equator v = 0, K = 1/3 and |H| = 2/3; on the inner equator v = π, K = 1/(−1)… that is cos π/(2 + cos π) = −1, and H = 0; on the top and bottom circles v = ±π/2, K = 0. These are exactly the page’s max K = 0.3333, min K = −1.0000 and max |H| = 0.6667 for the torus. Total: ∬K dA = ∫₀^{2π}∫₀^{2π} [cos v/(2 + cos v)](2 + cos v) dv du = 2π ∫₀^{2π} cos v dv = 0 = 2πχ(torus)."),
("Text", "How the other five follow: the sphere gives K = 1 everywhere, so ∬K dA over 0.02 ≤ v ≤ π − 0.02 is 2π ∫ sin v dv = 4π cos 0.02 = 12.5639; the cylinder has L = −1, N = 0, so K = 0 and |H| = 1/2; the catenoid is minimal (H = 0) with K = −1/cosh⁴v; the pseudosphere has K = −1. The table in §1 is these formulas evaluated on the page’s grid."),
("Subsection", "1.2 The picture the page draws, and its animator"),
("Input", r"""surfPlot[key_, q_] := Module[{X, U, V, c, f},
   {X, U, V} = surf[key]; c = surfaceCurvatures[X, {u, v}]; f = If[q == "K", c["K"], Abs[c["H"]]];
   ParametricPlot3D[X, {u, U[[1]], U[[2]]}, {v, V[[1]], V[[2]]}, ColorFunction -> Function[{x, y, z, uu, vv}, kcol[f /. {u -> uu, v -> vv}, 1]],
    ColorFunctionScaling -> False, Mesh -> None, PlotPoints -> 40, Boxed -> False, Axes -> False, Lighting -> "Neutral", PlotLabel -> key, ImageSize -> 230]];
Legended[Grid[Partition[surfPlot[#, "K"] & /@ Keys[surf], 3]], kLegend[1, "K"]]"""),
("Figure", "The six surfaces of the page coloured by Gauss curvature K on the page’s scale: blue negative, near-white zero, orange positive, saturating at |K| = 1. The torus is orange outside and blue inside; the catenoid and pseudosphere are blue throughout."),
("Text", "The animator: pick the surface and the quantity, and drag the picture to turn it, as on the page."),
("Input", r"""Manipulate[Legended[surfPlot[key, q], kLegend[1, If[q == "K", "K", "|H|"]]],
 {{key, "torus", "surface"}, Keys[surf]}, {{q, "K", "colour by"}, {"K" -> "Gauss curvature K", "H" -> "mean curvature |H|"}}, SaveDefinitions -> True]"""),
]
EXTRA[2] = [
("Subsection", "2.1 Worked by hand"),
("Text", "Stereographic sphere. With u = log(2/(1 + r²)), r² = x² + y², write u = log 2 − log(1 + r²). For a radial function the flat Laplacian is Δ₀ = d²/dr² + (1/r) d/dr, and for log(1 + r²) it gives 2(1 − r²)/(1 + r²)² + 2/(1 + r²) = 4/(1 + r²)². So Δ₀u = −4/(1 + r²)², e^{−2u} = (1 + r²)²/4, and K = −e^{−2u}Δ₀u = 1."),
("Text", "Half-plane. u = log(1/y) = −log y: Δ₀u = 1/y², e^{−2u} = y², K = −y²·(1/y²) = −1."),
("Text", "Shrinking sphere. The round metric g₀ on S² has Ric = g₀. Try g(t) = c(t) g₀: Ricci curvature does not change under constant scaling, so Ric(g(t)) = g₀ and Ricci flow ∂g/∂t = −2Ric reads c′ g₀ = −2 g₀, so c = 1 − 2t: the sphere shrinks to a point at t = 1/2."),
("Text", "Why ∬K dA stays 0 on the page. With dA = e^{2u} dx dy, K dA = −Δ₀u dx dy, and the integral of a Laplacian over the flat torus is 0. On the 32 × 32 grid the five-point Laplacian sums to exactly 0 over a periodic grid (each value enters once with +4 and four times with −1), so the page reads 0 to round-off, about 10⁻¹⁵."),
("Text", "Why max|K| falls. ∂u/∂t = e^{−2u}Δ₀u is a heat equation for u; a single Fourier mode a cos x decays like e^{−t}, and K ≈ −Δ₀u for small u, so max|K| falls by about e² ≈ 7.4 between t = 0 and t = 2 for the slowest mode, and faster for the sin 2y cos(x + y) part. Here 4.63 → 0.053 is a factor 87 because the bump is not small at first (e^{−2u} amplifies the start)."),
("Subsection", "2.2 The plots the page draws, and its animator"),
("Input", r"""ricciHistory[a_, b_, N_] := Module[{h = 2. π/N, U, lap, Kf, t = 0., hist = {}, frames = {}, next = 0.},
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
    kField[rh["frames"][[1]]], kField[SelectFirst[rh["frames"], #[[1]] >= 0.5 &]], kField[rh["frames"][[-1]]]}, "  "], kLegend[1.5, "K"]]"""),
("Figure", "Ricci flow on the flat torus at the default bump 0.3: max|K| on a log scale against t (the page’s chart), and the curvature field at t = 0, 0.5 and the end, on the page’s colour scale (saturating at |K| = 1.5)."),
("Text", "The animator plays the flow frame by frame (every 0.05 in t); press the play button."),
("Input", r"""Manipulate[Legended[kField[rh["frames"][[i]]], kLegend[1.5, "K"]], {{i, 1, "frame"}, 1, Length[rh["frames"]], 1, ControlType -> Animator, AnimationRate -> 8}, SaveDefinitions -> True]"""),
]
EXTRA[3] = [
("Subsection", "3.1 Worked by hand: Δf = −4 at the pole from the circle mean"),
("Text", "Near the north pole write x = sin r cos φ, y = sin r sin φ, z = cos r. To order r²: x ≈ r cos φ, y ≈ r sin φ, z ≈ 1 − r²/2. Then eˣ ≈ 1 + x + x²/2, (1 + z)² ≈ (2 − r²/2)² ≈ 4 − 2r², and yz³ ≈ y. So f ≈ (1 + x + x²/2)(4 − 2r²) + y ≈ 4 + 4x + 2x² − 2r² + y."),
("Text", "Average over the circle (over φ): the means of x and y are 0 and the mean of x² is r²/2. So M_r f ≈ 4 + 2·r²/2 − 2r² = 4 − r². The expansion says M_r f = f + (r²/4)Δf + …, so f = 4 and Δf/4 = −1: Δf = −4 at the pole, the snippet’s second value."),
("Text", "Why the flat formula has slope 4. The flat formula keeps f + r²Δf/4 + r⁴Δ²f/64 and misses the curvature term r⁴KΔf/96 = r⁴(1)(−4)/96 = −r⁴/24. So its error is about r⁴/24 for small r: at r = 0.1 that is 4.17 × 10⁻⁶ (the page reads 3.97 × 10⁻⁶; the r⁶ terms account for the rest). Adding KΔf/96 leaves the r⁶ terms, r⁶(500/2304 − 20/1152 − 4/1440) = 0.1969 r⁶: slope 6. Adding those leaves r⁸: slope 8."),
("Text", "Disc area. On the unit sphere the geodesic disc of radius r has area 2π(1 − cos r), so A/πr² = 2(1 − cos r)/r² = 1 − r²/12 + r⁴/360 − …; for curvature K replace r by √K r and divide by K: 1 − Kr²/12 + K²r⁴/360, the formula on the page."),
("Subsection", "3.2 The plots the page draws, and its animator"),
("Input", r"""rsAll = N[2^(-Range[4, 24]/4), 30];
errs = Table[With[{e = cm[r]}, {r, Abs[e - flat[r]], Abs[e - c4[r]], Abs[e - c6[r]]}], {r, rsAll}];
ListLogLogPlot[{errs[[All, {1, 2}]], errs[[All, {1, 3}]], errs[[All, {1, 4}]]}, Joined -> True, PlotMarkers -> Automatic,
 PlotStyle -> {GrayLevel[0.5], orange, blue}, AxesLabel -> {"r", "|error|"}, ImageSize -> 420,
 PlotLegends -> {"flat formula (K = 0)", "+ K Δf/96", "+ r^6 terms"}]"""),
("Figure", "Errors of the three approximations to the exact circle mean of f = eˣ(1 + z)² + yz³ on the unit sphere, on log–log axes (the page’s chart). The lines have slopes 4, 6 and 8. With the circle mean at 30 digits the blue line keeps falling below 10⁻¹³, where the page’s double precision flattens it."),
("Input", r"""discRatio[K_, r_] := Which[K == 0, 1, K > 0, 2 (1 - Cos[Sqrt[K] r])/(K r^2), True, 2 (Cosh[Sqrt[-K] r] - 1)/(-K r^2)];
Plot[{1, discRatio[1, r], discRatio[-1, r]}, {r, 0.02, 3}, PlotRange -> {0, 2}, PlotStyle -> {Directive[GrayLevel[0.5], Dashed], orange, blue},
 AxesLabel -> {"r", "A(r)/π r^2"}, PlotLegends -> {"K = 0", "K = 1", "K = −1"}, ImageSize -> 380]"""),
("Figure", "Area of a geodesic disc divided by the flat area πr², for K = 1, 0 and −1 (the page’s disc-area chart)."),
("Input", r"""Manipulate[Plot[{1, discRatio[K, r]}, {r, 0.02, 3}, PlotRange -> {0, 2}, PlotStyle -> {Directive[GrayLevel[0.5], Dashed], If[K >= 0, orange, blue]},
  AxesLabel -> {"r", "A(r)/π r^2"}, PlotLabel -> Row[{"K = ", K, ":  1 − K r²/12 + K² r⁴/360 − …"}], ImageSize -> 380], {{K, 1}, -1, 1, 0.1, Appearance -> "Labeled"}, SaveDefinitions -> True]"""),
]
EXTRA[4] = [
("Subsection", "4.1 Worked by hand: 1 + t/3 + t²/15 from the eigenvalues"),
("Text", "Put x = l + ½. Then (2l + 1) = 2x and l(l + 1) = x² − ¼, so Tr e^{tΔ} = Σ_{l≥0} g(l + ½) with g(x) = 2x e^{−(x² − ¼)t} = 2 e^{t/4} x e^{−x²t}."),
("Text", "A sum over half-integers is the integral plus corrections at the end point (the midpoint Euler–Maclaurin formula): Σ_{l≥0} g(l + ½) = ∫₀^∞ g dx + g′(0)/24 − 7g‴(0)/5760 + … Here ∫₀^∞ 2x e^{−x²t} dx = 1/t, g′(0) = 2e^{t/4} and g‴(0) = −12t e^{t/4}. So Tr e^{tΔ} = e^{t/4}(1/t + 1/12 + 7t/480 + …)."),
("Text", "Multiply by t and expand e^{t/4} = 1 + t/4 + t²/32 + …: t·Tr = (1 + t/4 + t²/32)(1 + t/12 + 7t²/480) = 1 + (1/4 + 1/12) t + (1/32 + 1/48 + 7/480) t² = 1 + t/3 + t²/15. The t/3 is McKean–Singer’s (t/6)∫S/Area with S = 2 (the scalar curvature of the unit sphere): (t/6)(2·4π)/(4π) = t/3."),
("Text", "The flat square torus of area 4π has side 2√π and eigenvalues π(m² + n²), so Tr e^{tΔ} = θ₃(0, e^{−πt})², and the Jacobi identity θ₃(0, e^{−πt}) = t^{−1/2} θ₃(0, e^{−π/t}) gives t·Tr = θ₃(0, e^{−π/t})² = 1 + 4e^{−π/t} + …: no t-term, because the torus is flat. At the default t = 0.05 the page reads 1.016835 for the sphere and 1.000000 for the torus, and 1 + t/3 + t²/15 = 1.016833."),
("Subsection", "4.2 The plot the page draws, and its animator"),
("Input", r"""sphM[t_?NumericQ] := t Sum[(2 l + 1) Exp[-l (l + 1) t], {l, 0, 400}];
heatPlot[tt_] := Show[Plot[{sphM[t], 1 + t/3 + t^2/15, tor[t]}, {t, 0.004, 0.4}, PlotRange -> {0.98, 1.16}, AxesLabel -> {"t", "t Tr e^(tΔ)"},
    PlotStyle -> {orange, Directive[Black, Dashed], blue}, PlotLegends -> {"unit sphere, K = 1", "1 + t/3 + t^2/15", "flat torus, same area"}, ImageSize -> 420],
   Graphics[{GrayLevel[0.5], Line[{{tt, 0.98}, {tt, 1.16}}]}]];
heatPlot[0.05]"""),
("Figure", "The heat trace divided by Weyl’s Area/(4πt) for the unit sphere and for a flat torus of the same area, against 1 + t/3 + t²/15 (the page’s chart; the grey line is the default t = 0.05)."),
("Input", r"""Manipulate[Column[{heatPlot[t], Grid[{{"sphere", NumberForm[sphM[t], 7]}, {"1 + t/3 + t²/15", NumberForm[1 + t/3 + t^2/15, 7]}, {"flat torus", NumberForm[tor[t], 7]},
     {"difference ≈ t/3", NumberForm[sphM[t] - tor[t], 7]}}, Alignment -> Left]}], {{t, 0.05}, 0.005, 0.4, 0.005, Appearance -> "Labeled"}, SaveDefinitions -> True]"""),
]
EXTRA[5] = [
("Subsection", "5.1 Worked by hand: Bochner for f = z on the unit sphere"),
("Text", "Take f = z = cos θ. It is a first spherical harmonic, so Δf = −2f. Its gradient on the sphere has |∇f|² = sin²θ = 1 − z²."),
("Text", "Left side. z² = (z² − 1/3) + 1/3 and z² − 1/3 is a second harmonic (eigenvalue −6), so Δ(z²) = −6(z² − 1/3) = −6z² + 2, and ½Δ|∇f|² = ½Δ(1 − z²) = 3z² − 1."),
("Text", "Right side. The Hessian of the restriction of a linear function to the unit sphere is −f·g, so |Hess f|² = 2z² (two directions, each −z). ⟨∇f, ∇Δf⟩ = ⟨∇f, −2∇f⟩ = −2(1 − z²). Ric = g on the unit sphere, so Ric(∇f, ∇f) = 1 − z². Sum: 2z² − 2 + 2z² + 1 − z² = 3z² − 1, equal to the left side."),
("Text", "Lichnerowicz with equality. Integrate Bochner over the sphere: ∫½Δ|∇f|² = 0, so 0 = ∫|Hess f|² − ∫(Δf)² + ∫Ric(∇f, ∇f). For an eigenfunction Δf = −λf, and |Hess f|² ≥ (Δf)²/n, which gives λ ≥ n k when Ric ≥ (n − 1)k; on S² (n = 2, k = 1) that is λ₁ ≥ 2, and f = z attains it because its Hessian is a multiple of g. For curvature K the page’s readout: λ₁ ≥ 2K, the round sphere has λ₁ = 2K, diameter ≤ π/√K (Bonnet–Myers), and Δr = √K cot(√K r) changes sign at r = π/(2√K)."),
("Subsection", "5.2 The plot the page draws, and its animator"),
("Input", r"""lapDist[K_, r_] := Which[K == 0, 1/r, K > 0, Sqrt[K] Cot[Sqrt[K] r], True, Sqrt[-K] Coth[Sqrt[-K] r]];
Plot[{lapDist[0, r], lapDist[1, r], lapDist[-1, r]}, {r, 0.05, 3.2}, PlotRange -> {-3, 5}, AxesLabel -> {"r", "Δr"},
 PlotStyle -> {Directive[GrayLevel[0.5], Dashed], orange, blue}, PlotLegends -> {"K = 0: 1/r", "K = 1: cot r", "K = −1: coth r"}, ImageSize -> 400]"""),
("Figure", "Laplacian of the distance function on surfaces of constant curvature K = 1, 0, −1 (the page’s chart): positive curvature makes Δr smaller than the flat 1/r and negative at r > π/2; negative curvature keeps it above √|K|."),
("Input", r"""Manipulate[Column[{Plot[{lapDist[0, r], lapDist[K, r]}, {r, 0.05, 3.2}, PlotRange -> {-3, 5}, AxesLabel -> {"r", "Δr"},
    PlotStyle -> {Directive[GrayLevel[0.5], Dashed], If[K >= 0, orange, blue]}, ImageSize -> 400],
   If[K > 0, Grid[{{"Lichnerowicz λ₁ ≥ nK", 2 K}, {"round sphere λ₁ = 2K", 2 K}, {"Bonnet–Myers diam ≤ π/√K", N[π/Sqrt[K]]}, {"Δr changes sign at r", N[π/(2 Sqrt[K])]}}, Alignment -> Left],
    Grid[{{"Lichnerowicz", "no bound for K ≤ 0"}, {"Δr → √|K| as r → ∞", N[Sqrt[-K]]}}, Alignment -> Left]]}],
 {{K, 1}, -1, 2, 0.1, Appearance -> "Labeled"}, SaveDefinitions -> True]"""),
]
EXTRA[6] = [
("Subsection", "6.5 Worked by hand"),
("Text", "Corner angles of the right triangle P₁ = (0, 0, 0), P₂ = (1, 0, 0), P₃ = (0, 1, 0). At P₁ the edges are (1, 0, 0) and (0, 1, 0): dot product 0, angle π/2. At P₂ they are (−1, 1, 0) and (−1, 0, 0): cos = 1/(√2·1), angle π/4; likewise π/4 at P₃. Sum π."),
("Text", "Cube corner: three squares meet, each with corner angle π/2, so δ = 2π − 3π/2 = π/2; eight corners give 4π = 2π·2. Icosahedron vertex: five equilateral triangles, δ = 2π − 5π/3 = π/3; twelve vertices give 4π. Square-pyramid apex with unit edges: four equilateral corners, δ = 2π − 4π/3 = 2π/3."),
("Text", "Torus mesh at the outer equator (v = 0) and the barycentric area. A vertex of the 40 × 20 mesh touches six triangles; its area A_i is one third of their total, about one mesh cell: (2π·3/40)(2π/20) = 0.148. Its six corner angles add to slightly less than 2π because the surface is convex there; the defect is about K A_i = (1/3)(0.148) = 0.049, and the page’s ratio defect/area at that vertex is 0.3352 against the smooth 1/3."),
("Text", "Why the total is exactly 0. Summing δ_i = 2π − Σθ over all V vertices gives 2πV − πF (each of the F triangles contributes π). Every triangle has three edges and every edge two triangles, so E = 3F/2, and 2πV − πF = 2π(V − E + F) = 2πχ. For the torus mesh V = 800, E = 2400, F = 1600, so χ = 0."),
("Subsection", "6.6 The plots the page draws, and its animator"),
("Input", r"""meshPicture[{nu_, nv_}] := Module[{P, T, M, Km}, {P, T} = torusMesh[nu, nv]; M = meshCurvature[P, T]; Km = M["defect"]/M["area"];
   Legended[Graphics3D[{EdgeForm[GrayLevel[0.4, 0.5]], Table[{kcol[Mean[Km[[tr]]], 1], Polygon[P[[tr]]]}, {tr, T}]}, Boxed -> False, Lighting -> "Neutral",
     PlotLabel -> Row[{nu, " × ", nv, ":  Σ defect = ", NumberForm[Chop[Total[M["defect"]], 10^-9], 3]}], ImageSize -> 360], kLegend[1, "defect/area"]]];
{P40, T40} = torusMesh[40, 20]; M40 = meshCurvature[P40, T40];
Row[{meshPicture[{40, 20}], Show[Plot[Cos[v]/(2 + Cos[v]), {v, 0, 2 π}, PlotStyle -> Black, AxesLabel -> {"v (around the tube)", "K"}],
    ListPlot[Table[{2 π j/20, (M40["defect"]/M40["area"])[[j + 1]]}, {j, 0, 19}], PlotStyle -> Directive[orange, PointSize[0.02]]], PlotRange -> {-1.1, 0.5}, ImageSize -> 340]}]"""),
("Figure", "The 40 × 20 torus mesh coloured by angle defect divided by vertex area, and that ratio around the tube (orange dots) against the smooth K = cos v/(2 + cos v) (black): the page’s two pictures."),
("Input", r"""ListLogLogPlot[{2 π/#[[2]], #[[3]]} & /@ ({#["nu"], #["nv"], #["err"]} & /@ page["mesh"]), Joined -> True, PlotMarkers -> Automatic, PlotStyle -> orange,
 AxesLabel -> {"edge length 2π/nv", "max |Kmesh − K|"}, PlotLabel -> Row[{"fitted slope ", NumberForm[Coefficient[Fit[Log[{2 π/#["nv"], #["err"]}] & /@ page["mesh"], {1, s}, s], s], 3]}], ImageSize -> 380]"""),
("Figure", "Largest error of the mesh curvature against the mesh size for the four resolutions: slope about 2, second-order convergence."),
("Input", r"""Manipulate[meshPicture[res], {{res, {40, 20}, "resolution"}, {{12, 6} -> "12 × 6", {24, 12} -> "24 × 12", {40, 20} -> "40 × 20", {64, 32} -> "64 × 32"}}, SaveDefinitions -> True]"""),
]
EXTRA[7] = [
("Subsection", "7.1 Worked by hand"),
("Text", "Lin–Lu–Yau on an edge xy of K₅. With idleness ½, μ_x puts ½ on x and ⅛ on each of its four neighbours; μ_y the same around y. The three other vertices get ⅛ from both, so nothing moves there. At x, μ_x has ½ and μ_y has ⅛: an excess of ⅜, which must go to y (where μ_y has ½ and μ_x ⅛), distance 1. So W₁ = ⅜, κ_{1/2} = 1 − ⅜ = ⅝ and κ_LLY = 2κ_{1/2} = 5/4. Non-lazy: μ_x is ¼ on y and on the three others, μ_y ¼ on x and on the three others; ¼ moves from y to x, W₁ = ¼, κ₀ = ¾."),
("Text", "Forman on K₅: F = 4 − d_x − d_y = 4 − 4 − 4 = −4; each edge lies in three triangles, so F + 3·3 = 5. On C₆: F = 4 − 2 − 2 = 0, and no triangles."),
("Text", "Resistance curvature on C₆. Between neighbours the cycle is a resistor of 1 in parallel with one of 5, so ω = 5/6. Then p = 1 − ½(5/6 + 5/6) = 1/6 at every vertex, and Σp = 6·(1/6) = 1. Steinerberger on C₆: the distances from a vertex are 1, 1, 2, 2, 3, which add to 9; by symmetry w is constant, so 9w = n = 6 and w = 2/3."),
("Text", "Spectral gap of Petersen. Its adjacency eigenvalues are 3, 1 (five times) and −2 (four times); the normalised Laplacian 1 − A/3 has eigenvalues 0, 2/3, 5/3. So λ₁ = 2/3 and λ_max = 5/3, as the page reads. On the cube, adjacency eigenvalues 3, 1, −1, −3 give λ₁ = 1 − 1/3 = 2/3 = κ_LLY = K_∞: the equality case."),
("Text", "Tree root edge. The root has degree 2 and its child degree 3, with no common neighbour and no 4-cycle, so the tree formula κ_LLY = 2/d_x + 2/d_y − 2 gives 2/2 + 2/3 − 2 = −1/3; an interior edge between two vertices of degree 3 gives 2/3 + 2/3 − 2 = −2/3; a leaf edge 2/3 + 2/1 − 2 = 2/3. The dumbbell edge from a clique vertex (degree 5) to the path (degree 2): 2/5 + 2/2 − 2 = −3/5; the middle path edge (degrees 2 and 2) is 0."),
("Subsection", "7.2 The pictures the page draws, and its animator"),
("Input", r"""kScale = <|"lly" -> 1.25, "k0" -> 1, "be" -> 1, "forman" -> 6, "formanAug" -> 6, "res" -> 0.3, "stein" -> 1.5|>;
graphPicture[g_, k_] := Module[{G = graphOf[g], vals = N[wlValues[g, k]], e = UndirectedEdge @@@ page["graphs", g, "edges"], s = kScale[k]},
   If[curvs[k][[2]] == "e",
    Graph[G, EdgeStyle -> Thread[e -> (Directive[kcol[#, s], AbsoluteThickness[5]] & /@ vals)], VertexStyle -> GrayLevel[0.6], VertexSize -> 0.2, PlotLabel -> g, ImageSize -> 190],
    Graph[G, VertexStyle -> Thread[VertexList[G] -> (kcol[#, s] & /@ vals)], VertexSize -> 0.35, EdgeStyle -> GrayLevel[0.7], PlotLabel -> g, ImageSize -> 190]]];
Legended[Grid[Partition[graphPicture[#, "lly"] & /@ Keys[page["graphs"]], 4, 4, 1, ""]], kLegend[1.25, Subscript["κ", "LLY"]]]"""),
("Figure", "The seven graphs of the page with every edge coloured by its Lin–Lu–Yau curvature (the page’s default curvature): the tree and the dumbbell’s bridge are blue, the cube and K₅ orange, C₆ and Petersen white."),
("Input", r"""Legended[Grid[Partition[graphPicture[#, "be"] & /@ Keys[page["graphs"]], 4, 4, 1, ""]], kLegend[1, Subscript["K", "∞"]]]"""),
("Figure", "The same graphs with every vertex coloured by its Bakry–Émery curvature K_∞."),
("Text", "The animator: pick a graph and a curvature, as on the page; the readout gives min, max, mean (sum for resistance curvature) and the spectral bounds the page ticks."),
("Input", r"""Manipulate[With[{w = N[wlValues[g, k]], sp = normSpec[graphOf[g]]},
  Column[{Legended[graphPicture[g, k], kLegend[kScale[k], curvs[k][[1]]]],
    Grid[{{"min", Min[w]}, {"max", Max[w]}, {If[k == "res", "sum", "mean"], If[k == "res", Total[w], Mean[w]]}, {"λ₁ (normalised)", sp[[2]]}, {"λmax", sp[[-1]]},
      {"λ₁ ≥ min κLLY", sp[[2]] >= Min[N[wlValues[g, "lly"]]] - 10^-9}}, Alignment -> Left]}]],
 {{g, "dumbbell", "graph"}, Keys[page["graphs"]]}, {{k, "lly", "curvature"}, Thread[Keys[curvs] -> curvs[[All, 1]]]}, SaveDefinitions -> True]"""),
]
EXTRA[8] = [
("Subsection", "8.1 Worked by hand"),
("Text", "Why the area falls at 2π. For a closed embedded plane curve moving by ∂X/∂t = κN (N the inward normal), the area changes by dA/dt = −∮κ ds, and ∮κ ds is the total turning of the tangent, 2π for any simple closed curve (Hopf’s Umlaufsatz). So A(t) = A₀ − 2πt, independent of the shape, and the curve vanishes at t = A₀/2π: 3.3934/2π = 0.540 for the wiggly start."),
("Text", "The polygon’s rate. Vertex i moves by k(t_f − t_b) with k = 2/(ℓ_f + ℓ_b), where t_b, t_f are the unit directions of the edges into and out of it. The area swept per unit time near vertex i is that velocity’s inward component times (ℓ_f + ℓ_b)/2, which is |t_f − t_b| = 2 sin(θ_i/2), θ_i the turning angle. So dA/dt = −Σ 2 sin(θ_i/2), slightly less than Σθ_i = 2π; for a regular 160-gon it is −320 sin(π/160) = −6.2828 against −2π = −6.2832."),
("Text", "Sphere under mean-curvature flow. A sphere of radius R has H = 1/R (the mean of the two principal curvatures) and ΔX = −2H n, so dR/dt = −2/R, R dR = −2 dt and R² = R₀² − 4t: the snippet’s √(R₀² − 4t), with residual 0."),
("Subsection", "8.2 The plots the page draws, and its animator"),
("Input", r"""Row[{ListLinePlot[Table[runs[k, "hist"], {k, Keys[runs]}], PlotStyle -> {orange, blue, Darker[Green], Purple}, PlotLegends -> Keys[runs],
    Epilog -> {Dashed, GrayLevel[0.5], Line[{{0, runs["wiggle", "A0"]}, {runs["wiggle", "A0"]/(2 π), 0}}]}, AxesLabel -> {"t", "area"}, ImageSize -> 360],
   Graphics[{Table[{Opacity[0.25 + 0.75 j/6], orange, Line[Append[#, First[#]] &[runs["wiggle", "frames"][[Round[1 + (Length[runs["wiggle", "frames"]] - 1) j/6]]]]]}, {j, 0, 6}]},
    PlotLabel -> "wiggly start, seven moments", ImageSize -> 260]}]"""),
("Figure", "Area against time for the four starting curves, with the line of slope −2π from the wiggly start (dashed), and the wiggly curve at seven moments: it becomes convex, then round, and shrinks to a point."),
("Input", r"""Manipulate[With[{fr = runs[kind, "frames"]}, Graphics[{Dashed, GrayLevel[0.6], Line[Append[#, First[#]] &[fr[[1]]]], Dashing[{}], orange, Thickness[0.008],
    Line[Append[#, First[#]] &[fr[[Min[i, Length[fr]]]]]]}, PlotRange -> 1.6, ImageSize -> 380,
   PlotLabel -> Row[{"area ", NumberForm[polyArea[fr[[Min[i, Length[fr]]]]], 4], ",  vertices ", Length[fr[[Min[i, Length[fr]]]]]}]]],
 {{kind, "wiggle", "start"}, Keys[runs]}, {{i, 1, "frame"}, 1, Max[Length[runs[#, "frames"]] & /@ Keys[runs]], 1, ControlType -> Animator, AnimationRate -> 10}, SaveDefinitions -> True]"""),
]
EXTRA[9] = [
("Subsection", "9.1 Worked by hand: κ ≈ ε²K/8"),
("Text", "Slide the surface a distance δ along the geodesic from x to y. A point of the ball at distance λ from the geodesic moves δ cos(√K λ) ≈ δ(1 − Kλ²/2) on a surface of curvature K (geodesics at distance λ converge or spread like cos √K λ). This sliding carries μ_x onto μ_y, and for small balls it is the optimal plan, so W₁(μ_x, μ_y) ≈ δ(1 − K⟨λ²⟩/2), with ⟨λ²⟩ the mean of λ² over the ball."),
("Text", "In polar coordinates (ρ, α) about x, λ = ρ|sin α|, and the mean of ρ² sin²α over a flat disc of radius ε is (ε²/2)(1/2) = ε²/4. So W₁ ≈ δ(1 − Kε²/8), and κ = 1 − W₁/δ ≈ Kε²/8: 0.125 for the unit sphere. The page’s κ/ε² at ε = 0.05 is 0.12496 = 1/8 − 0.000039; the correction is of order ε², from the curvature of the ball itself."),
("Subsection", "9.2 The plot the page draws, and its animator"),
("Input", r"""(* the same integral as κball at plotting accuracy (six digits), on twelve values of ε *)
κfast[K_, ε_?NumericQ] := Which[K == 0, 0, K > 0, With[{R = 1/Sqrt[K]},
     Quiet@NIntegrate[With[{s = Sin[ρ/R] Sin[α]}, s^2/(1 + Sqrt[1 - s^2])] Sin[ρ/R], {ρ, 0, ε}, {α, 0, 2 π}, PrecisionGoal -> 6]/(2 π R (1 - Cos[ε/R]))],
   True, With[{R = 1/Sqrt[-K]}, -Quiet@NIntegrate[With[{s = Sinh[ρ/R] Sin[α]}, s^2/(1 + Sqrt[1 + s^2])] Sinh[ρ/R], {ρ, 0, ε}, {α, 0, 2 π}, PrecisionGoal -> 6]/(2 π R (Cosh[ε/R] - 1))]];
ollPlot[K_] := With[{emax = If[K == 0, 1.2, Min[1.2, 0.9 π/Sqrt[Abs[K]]/2]]},
   ListLinePlot[Table[{e, κfast[K, e]/e^2}, {e, emax/12, emax, emax/12}], PlotStyle -> If[K >= 0, orange, blue], PlotRange -> {-Max[0.05, 1.6 Abs[K]/8], Max[0.05, 1.6 Abs[K]/8]},
    Epilog -> {Dashed, GrayLevel[0.5], Line[{{0, K/8}, {emax, K/8}}]}, AxesLabel -> {"ε", "κ/ε^2"}, PlotLabel -> Row[{"K = ", K}], ImageSize -> 300]];
Row[{ollPlot[1], ollPlot[0], ollPlot[-1]}]"""),
("Figure", "Ollivier curvature of ε-balls divided by ε², against ε, for K = 1, 0 and −1 (the page’s chart); the dashed line is K/8."),
("Input", r"""Manipulate[ollPlot[K], {{K, 1}, -2, 2, 0.25, Appearance -> "Labeled"}, SaveDefinitions -> True]"""),
]

def _merge(cells, extra):
    out, cur = [], None
    for st, tx in cells:
        if st == 'Section':
            if cur in extra: out += extra[cur]
            cur = int(tx.split('.')[0])
        if st == 'Text' and tx.startswith('© 2026') and cur == 11:
            pass
        out.append((st, tx))
    return out

CELLS = _merge(CELLS, EXTRA)
