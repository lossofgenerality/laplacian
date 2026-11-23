# Reference content for the Laplacian Lab (version 2) programmer's manual.
TITLE = "Laplacian Lab"
LABNAME = "Laplacian Lab"
SUBTITLE = "Wolfram Language reference for the CCN code behind Laplacian Lab: the Δ notation, the mean-value snippets, the staged derivation laplacianSteps and the LaplacianLabKernel cloud API."
INTRO = "The Δ notation is prepended to every Wolfram cell of the Lab page; the page also rewrites Δ²f, Δ(3)f, Δ^n f and ∇²f into Δ[n]@f before sending, so the examples below use the forms the kernel receives."
REPO = "https://github.com/lossofgenerality/Laplacian-lab"
SITE = "https://lossofgenerality.github.io/Laplacian-lab/"
LAB = "https://lossofgenerality.github.io/Laplacian-lab/"

GUIDES = [
 ("delta", "Δ Notation", "The Δ notation of the notebook: the variables list 𝒶𝓇ℊ𝓈 and its dimension, centre and help symbols, the operator forms Δ[n][f] and Δ[f], and the tensor form 𝜟⊗f. A bare symbol f stands for f[x, y, z].",
  ["𝒶𝓇ℊ𝓈", "𝒹", "𝒞enter", "ℋelp", "lapToExpr", "lapN", "Δ", "𝜟", "CircleTimes"]),
 ("means", "Mean Values and Derivations", "Coefficients of the sphere and ball mean-value series, the staged and checked derivation of Δ from the sphere or ball mean, and the 1/r³ test field of the notes.",
  ["sphere", "ball", "g", "laplacianSteps", "laplacianStepsColumn"]),
 ("kernel", "Cloud Kernel API", "LaplacianLabKernel, the secret-gated Wolfram Cloud API behind the Lab page: Wolfram evaluation and a chat proxy for the Teaching Assistant, with its base64 and chat helpers.",
  ["LaplacianLabKernel", "b64s", "fromB64", "chatCall"]),
]

PRELUDE = '''𝒶𝓇ℊ𝓈 = {x, y, z};
𝒹 := Length[𝒶𝓇ℊ𝓈];
𝒞enter := Symbol[ToString[#] <> "0"] & /@ 𝒶𝓇ℊ𝓈;
ℋelp := {"𝒹" -> 𝒹, "𝒶𝓇ℊ𝓈" -> 𝒶𝓇ℊ𝓈, "𝒞enter" -> 𝒞enter, "Δ" -> "Δ[n][expr]", "𝜟" -> "𝜟⊗expr"};
lapToExpr[g_Symbol] := If[OwnValues[g] === {} && DownValues[g] === {}, g @@ 𝒶𝓇ℊ𝓈, g];
lapToExpr[g_] := g;
lapN[g_, n_Integer?NonNegative] := Nest[Laplacian[#, 𝒶𝓇ℊ𝓈] &, lapToExpr[g], n];
Δ[n_Integer?NonNegative][g_] := lapN[g, n];
Δ[g_] /; ! IntegerQ[g] := lapN[g, 1];
𝜟 = lapOp;
Unprotect[CircleTimes]; CircleTimes[ops : lapOp .., g_] := lapN[g, Length[{ops}]]; Protect[CircleTimes];'''

HELPERS = {
 "b64s": 'b64s[s_String] := BaseEncode[StringToByteArray[s]];',
 "fromB64": 'fromB64[b_String] := Quiet@Check[ByteArrayToString[BaseDecode[b]], ""];',
 "chatCall": '''chatCall[payload_String, apiKey_String] := Module[{p, model, resp, body, status},
  p = Quiet@Check[ImportByteArray[StringToByteArray[payload], "RawJSON"], $Failed];
  If[! AssociationQ[p] || ! ListQ[p["messages"]], Return[<|"error" -> "bad payload", "status" -> 400|>]];
  model = Replace[p["model"], Except[_String?(StringStartsQ["claude-"])] -> "claude-sonnet-5-5"];
  resp = URLRead[HTTPRequest["https://api.anthropic.com/v1/messages", <|"Method" -> "POST",
      "Headers" -> {"x-api-key" -> apiKey, "anthropic-version" -> "2023-06-01", "content-type" -> "application/json"},
      "Body" -> ExportByteArray[DeleteMissing@<|"model" -> model,
          "max_tokens" -> Clip[Replace[p["max_tokens"], Except[_Integer] -> 1500], {1, 4096}],
          "system" -> p["system"], "messages" -> p["messages"]|>, "RawJSON", "Compact" -> True]|>],
    TimeConstraint -> 110];
  If[FailureQ[resp], Return[<|"error" -> "chat service unreachable", "status" -> 502|>]];
  status = resp["StatusCode"];
  body = Quiet@Check[ImportByteArray[resp["BodyByteArray"], "RawJSON"], <||>];
  If[status === 200 && AssociationQ[body],
   <|"text_b64" -> b64s@StringJoin[Cases[Lookup[body, "content", {}],
        KeyValuePattern[{"type" -> "text", "text" -> t_String}] :> t]],
     "stop_reason" -> Lookup[body, "stop_reason", ""]|>,
   <|"error" -> If[AssociationQ[body], Lookup[Lookup[body, "error", <||>], "message", "chat request failed"], "chat request failed"],
     "status" -> status|>]];''',
}

API_BODY = '''APIFunction[
   {"code" -> "String" -> "", "code_b64" -> "String" -> "", "key" -> "String",
    "mode" -> "String" -> "wolfram", "payload_b64" -> "String" -> ""},
   Module[{b64s, fromB64, chatCall, chat, code},
    __HELPERS__
    chat = Quiet@Check[CloudGet[keyObj], ""];
    chat = If[StringQ[chat], StringTrim[chat], ""];
    Which[
     #key =!= secret,
      Failure["Forbidden", <|"Message" -> "bad key"|>],
     #mode === "chat",
      If[chat === "", <|"error" -> "no chat key stored", "status" -> 503|>,
       chatCall[fromB64[#["payload_b64"]], chat]],
     True,
      code = If[#["code_b64"] =!= "", fromB64[#["code_b64"]], #code];
      Module[{r = TimeConstrained[ToExpression[code], 60, $Aborted], img, txt},
       img = If[FreeQ[r, _Graphics | _Graphics3D | _Image | _Legended], "",
         BaseEncode[ExportByteArray[Rasterize[r, ImageResolution -> 110], "PNG"]]];
       txt = ToString[r /. g : (_Graphics | _Graphics3D | _Image | _Legended) :> "-Graphics-", InputForm];
       <|"text" -> txt, "text_b64" -> b64s[txt], "image" -> img, "chat_ready" -> chat =!= ""|>]
     ]] &,
   "JSON"]'''
_helpers_inline = '\n    '.join(v.replace('\n', '\n    ') for v in HELPERS.values())
API_BODY = API_BODY.replace('__HELPERS__', _helpers_inline)

KERNEL_SOURCE = '''(* Step 1, once, in a signed-in Wolfram Cloud session: store the chat key privately *)
CloudPut["PASTE-THE-CHAT-API-KEY-HERE", "LaplacianLab/apikey", Permissions -> "Private"]

(* Step 2: deploy; the same name keeps the URL *)
With[{keyObj = CloudObject["LaplacianLab/apikey"], secret = "CHOOSE-A-LONG-SECRET"},
 CloudDeploy[
  ''' + API_BODY.replace('\n', '\n ') + ''',
  "LaplacianLabKernel", Permissions -> "Public"]]'''

STEPS = '''ClearAll[laplacianSteps, laplacianStepsColumn];
Options[laplacianSteps] = {"Region" -> "Sphere", "Function" -> f};
laplacianSteps[d : (_Integer?Positive) : 3, n : (_Integer?Positive) : 2, OptionsPattern[]] /; d <= 7 := Module[
  {fn = OptionValue["Function"], ball = OptionValue["Region"] === "Ball", vars, ctr, f0, series, measure,
   integral, mean, idx, oddIdx, byPower, c2, lap0, factor, scaled, lim},
  vars = Take[{x, y, z, t, u, v, w}, d];
  ctr = Symbol[ToString[#] <> "0"] & /@ vars;
  f0 = fn @@ ctr;
  series = Normal@Series[fn @@ vars, Sequence @@ Transpose[{vars, ctr, ConstantArray[n, d]}]];
  measure = If[ball, Pi^(d/2)/Gamma[d/2 + 1] r^d, 2 Pi^(d/2)/Gamma[d/2] r^(d - 1)];
  integral = If[ball,
    Integrate[series, vars ∈ Ball[ctr, r], Assumptions -> r > 0],
    SurfaceIntegrate[series, vars ∈ Sphere[ctr, r], Assumptions -> r > 0]];
  mean = Expand[integral/measure];
  idx[e_] := Union@Cases[e, Derivative[k__][fn][__] :> {k}, Infinity];
  oddIdx = Select[idx[series], AnyTrue[#, OddQ] &];
  byPower = DeleteCases[Table[k -> Simplify@Coefficient[mean, r, k], {k, 0, d n}], _ -> 0];
  c2 = Simplify@Coefficient[mean, r, 2];
  lap0 = Laplacian[fn @@ vars, vars] /. Thread[vars -> ctr];
  factor = If[ball, 2 (d + 2), 2 d];
  scaled = Expand[factor (mean - f0)/r^2];
  lim = Quiet@Limit[scaled, r -> 0];
  <|
   "region" -> If[ball, "ball", "sphere"],
   "dimension" -> d,
   "Taylor order per variable" -> n,
   "1 Taylor polynomial: terms" -> 1 + Length[idx[series]],
   "2 measure" -> measure,
   "3 odd multi-indices: in series" -> Length[oddIdx],
   "3 odd multi-indices: left after integrating" -> Length[Intersection[oddIdx, idx[mean]]],
   "4 mean by powers of r" -> byPower,
   "4 note" -> If[n < 4,
     "coefficients of r^4 and higher are incomplete at this Taylor order; use n >= 4 for them",
     "coefficients up to r^4 are complete"],
   "5 r^2 coefficient" -> c2,
   "5 check: r^2 coefficient == Δf/" <> ToString[factor] -> Simplify[c2 == lap0/factor],
   "6 factor" -> factor/r^2,
   "6 " <> ToString[factor] <> "(mean - f0)/r^2" -> scaled,
   "6 limit r -> 0" -> lim,
   "6 check: limit == Δf at centre" -> Simplify[lim == lap0]
   |>];
laplacianStepsColumn[steps_Association] := Column[
  KeyValueMap[Row[{Style[#1 <> ":  ", Bold, RGBColor[0.98, 0.56, 0.17]], TraditionalForm[#2]}] &, steps],
  Spacings -> 1.2];'''

SNIP_SPHERE = 'sphere[d_, k_] := 1/(2^k k! Product[d + 2 j, {j, 0, k - 1}]);'
SNIP_BALL = 'ball[d_, k_] := 1/(2^k k! Product[d + 2 j, {j, 1, k}]);'
SNIP_G = 'g[x_, y_, z_] := (x^2 + y^2 + z^2)^(-3/2);'

# Verification definitions: (name, source). kernelAPI is a local, undeployed copy with a demo secret.
DEFS = [("PRELUDE", PRELUDE), ("sphere", SNIP_SPHERE), ("ball", SNIP_BALL), ("g", SNIP_G), ("laplacianSteps", STEPS)] + \
       [(k, v) for k, v in HELPERS.items()] + \
       [("kernelAPI", 'kernelAPI = With[{keyObj = Quiet@CloudObject["LaplacianLab/apikey"], secret = "demo-secret"}, ' + API_BODY + '];')]
ALWAYS = ["PRELUDE"]

SOURCES = {}
SOURCES.update({
 "𝒶𝓇ℊ𝓈": '𝒶𝓇ℊ𝓈 = {x, y, z};   (* typed as \\[ScriptA]\\[ScriptR]\\[ScriptG]\\[ScriptS] *)',
 "𝒹": '𝒹 := Length[𝒶𝓇ℊ𝓈];',
 "𝒞enter": '𝒞enter := Symbol[ToString[#] <> "0"] & /@ 𝒶𝓇ℊ𝓈;',
 "ℋelp": 'ℋelp := {"𝒹" -> 𝒹, "𝒶𝓇ℊ𝓈" -> 𝒶𝓇ℊ𝓈, "𝒞enter" -> 𝒞enter, "Δ" -> "Δ[n][expr]", "𝜟" -> "𝜟⊗expr"};',
 "lapToExpr": 'lapToExpr[g_Symbol] := If[OwnValues[g] === {} && DownValues[g] === {}, g @@ 𝒶𝓇ℊ𝓈, g];\nlapToExpr[g_] := g;',
 "lapN": 'lapN[g_, n_Integer?NonNegative] := Nest[Laplacian[#, 𝒶𝓇ℊ𝓈] &, lapToExpr[g], n];',
 "Δ": 'Δ[n_Integer?NonNegative][g_] := lapN[g, n];\nΔ[g_] /; ! IntegerQ[g] := lapN[g, 1];',
 "𝜟": '𝜟 = lapOp;   (* typed as \\|01d71f *)',
 "CircleTimes": 'Unprotect[CircleTimes]; CircleTimes[ops : lapOp .., g_] := lapN[g, Length[{ops}]]; Protect[CircleTimes];',
 "sphere": SNIP_SPHERE, "ball": SNIP_BALL, "g": SNIP_G,
 "laplacianSteps": STEPS.split('\nlaplacianStepsColumn')[0],
 "laplacianStepsColumn": 'laplacianStepsColumn' + STEPS.split('\nlaplacianStepsColumn')[1],
 "LaplacianLabKernel": KERNEL_SOURCE,
})
SOURCES.update(HELPERS)

P = {}
def page(name, guide, defined, usage, details, examples, see, setup="", kind="Function"):
    P[name] = dict(name=name, guide=guide, defined=defined, usage=usage, details=details, examples=examples, see=see, setup=setup, kind=kind)

PRE = "Lab page: Wolfram cell prelude (WL_PRELUDE)"
page("𝒶𝓇ℊ𝓈", "delta", PRE,
 [("𝒶𝓇ℊ𝓈", "is the list of variables used by Δ, 𝜟 and lapN; initially {x, y, z}."),
  ("𝒶𝓇ℊ𝓈 = vars", "changes the variables, and with them the dimension 𝒹 and the centre 𝒞enter.")],
 ["Typed \\[ScriptA]\\[ScriptR]\\[ScriptG]\\[ScriptS]; the third letter is script g ℊ (U+210A). The look-alike 𝒶𝓇𝓈 is a different, undefined symbol.",
  "A bare symbol f is read as f @@ 𝒶𝓇ℊ𝓈 by lapToExpr."],
 {"Basic Examples": [("𝒶𝓇ℊ𝓈", None)],
  "Scope": [("𝒶𝓇ℊ𝓈 = {x, y, z, t}; Δ[f]", None), ("𝒶𝓇ℊ𝓈 = {x, y}; Δ[x^3 y^3]", None)]},
 ["𝒹", "𝒞enter", "lapToExpr"], kind="Symbol")
page("𝒹", "delta", PRE,
 [("𝒹", "gives the dimension Length[𝒶𝓇ℊ𝓈].")], ["Defined with SetDelayed, so it follows changes of 𝒶𝓇ℊ𝓈."],
 {"Basic Examples": [("𝒹", None)], "Scope": [("𝒶𝓇ℊ𝓈 = {x, y, z, t, u}; 𝒹", None)]},
 ["𝒶𝓇ℊ𝓈", "𝒞enter"], kind="Symbol")
page("𝒞enter", "delta", PRE,
 [("𝒞enter", "gives the centre point {x0, y0, z0}: each variable of 𝒶𝓇ℊ𝓈 with 0 appended.")],
 ["Matches the centre used by laplacianSteps."],
 {"Basic Examples": [("𝒞enter", None)],
  "Scope": [("Δ[x^2 y + z^3] /. Thread[𝒶𝓇ℊ𝓈 -> 𝒞enter]", None)]},
 ["𝒶𝓇ℊ𝓈", "laplacianSteps"], kind="Symbol")
page("ℋelp", "delta", PRE,
 [("ℋelp", "gives a short summary of the Δ notation: the dimension, the variables, the centre and the two operator forms.")], [],
 {"Basic Examples": [("ℋelp", None)]}, ["Δ", "𝜟", "𝒶𝓇ℊ𝓈"], kind="Symbol")
page("lapToExpr", "delta", PRE,
 [("lapToExpr[f]", "gives f @@ 𝒶𝓇ℊ𝓈 when f is a symbol with no values, so that a bare f means f[x, y, z]."),
  ("lapToExpr[expr]", "gives expr unchanged for anything else.")],
 ["A symbol that already has a definition, such as h[x_, y_, z_] := …, is left as it is."],
 {"Basic Examples": [("lapToExpr[f]", None), ("lapToExpr[x^2 + y]", None)],
  "Possible Issues": [("h[x_, y_, z_] := x^2 y z; {lapToExpr[h], Δ[h], Δ[h[x, y, z]]}", None)]},
 ["lapN", "Δ", "𝒶𝓇ℊ𝓈"])
page("lapN", "delta", PRE,
 [("lapN[f, n]", "gives the n-th power of the Laplacian in the variables 𝒶𝓇ℊ𝓈 applied to f.")],
 ["f goes through lapToExpr first; n is a non-negative integer.", "Δ[n][f], Δ[f] and 𝜟⊗…⊗f all call lapN."],
 {"Basic Examples": [("lapN[f, 1]", None), ("lapN[x^4 + y^2 z^2, 2]", None)],
  "Properties & Relations": [("lapN[f, 0]", None), ("Simplify[lapN[f, 2] - Laplacian[Laplacian[f[x, y, z], {x, y, z}], {x, y, z}]]", None)]},
 ["Δ", "CircleTimes", "lapToExpr"])
page("Δ", "delta", PRE,
 [("Δ[f]", "gives the Laplacian of f in the variables 𝒶𝓇ℊ𝓈."),
  ("Δ[n][f]", "gives the n-th power Δⁿf.")],
 ["On the Lab page Δf, Δ²f, Δ(2)f, Δ^2 f, Δ2f and ∇²f are rewritten to Δ[1]@f or Δ[2]@f before the code is sent.",
  "In outputs the page shows Derivative[a, b, c][f] as f^(a,b,c)."],
 {"Basic Examples": [("Δ[f]", None), ("Δ[2][x^2 y^2 z^2]", None)],
  "Scope": [("Δ[1/Sqrt[x^2 + y^2 + z^2]] // Simplify", None)],
  "Properties & Relations": [("Δ[2][f] - Δ[Δ[f]]", None)],
  "Possible Issues": [("Δ[3]", None)]},
 ["lapN", "𝜟", "CircleTimes", "laplacianSteps"])
page("𝜟", "delta", PRE,
 [("𝜟", "is the operator symbol of the tensor notation; it evaluates to the inert symbol lapOp."),
  ("𝜟⊗f", "gives Δf; 𝜟⊗𝜟⊗f gives Δ²f.")],
 ["Typed \\|01d71f (mathematical italic capital delta), distinct from Δ.", "The products are handled by the CircleTimes rule."],
 {"Basic Examples": [("𝜟", None), ("𝜟⊗f", None)]},
 ["CircleTimes", "Δ"], kind="Symbol")
page("CircleTimes", "delta", PRE,
 [("𝜟⊗…⊗𝜟⊗f", "with k copies of 𝜟 gives lapN[f, k].")],
 ["CCN extension of the built-in CircleTimes: one rule for lapOp factors, other uses of ⊗ are untouched."],
 {"Basic Examples": [("𝜟⊗𝜟⊗f - Δ[2][f]", None), ("𝜟⊗(x^2 + y^2 + z^2)^2", None)],
  "Possible Issues": [("a⊗b", None)]},
 ["𝜟", "lapN"], kind="Function (extension)")

page("sphere", "means", "Lab snippet: Theorem 5.4",
 [("sphere[d, k]", "gives the coefficient of r^{2k} Δᵏf in the mean of f over the sphere of radius r in ℝᵈ: 1/(2ᵏ k! d(d + 2)…(d + 2k − 2)).")], [],
 {"Basic Examples": [("Table[sphere[3, k], {k, 0, 4}]", None)],
  "Properties & Relations": [("Simplify[sphere[d, 1] == 1/(2 d)]", None)]},
 ["ball", "laplacianSteps"])
page("ball", "means", "Lab snippet: Theorem 5.4",
 [("ball[d, k]", "gives the coefficient of r^{2k} Δᵏf in the mean of f over the ball of radius r in ℝᵈ: 1/(2ᵏ k! (d + 2)(d + 4)…(d + 2k)).")], [],
 {"Basic Examples": [("Table[ball[3, k], {k, 0, 4}]", None)],
  "Properties & Relations": [("Simplify[ball[d, 1] == 1/(2 (d + 2))]", None), ("Union@Flatten@Table[ball[d, k] == sphere[d + 2, k], {d, 1, 6}, {k, 0, 4}]", None)]},
 ["sphere", "laplacianSteps"])
page("g", "means", "Lab snippet: §7.5.1 check",
 [("g[x, y, z]", "gives the field 1/r³ = (x² + y² + z²)^(−3/2) used in the §7.5.1 normalisation check.")],
 ["Its Laplacian is 6/r⁵, so the sphere-mean limit with the Theorem 3.1 normalisation is finite."],
 {"Basic Examples": [("g[1, 1, 1]", None)],
  "Properties & Relations": [("Simplify[Laplacian[g[x, y, z], {x, y, z}]]", None)]},
 ["sphere", "Δ"])
page("laplacianSteps", "means", "Laplacian Lab notebook code (staged derivation)",
 [("laplacianSteps[]", "derives Δf at a point from the mean of f over a small sphere in ℝ³, with Taylor order 2, and returns every stage with its checks."),
  ("laplacianSteps[d, n]", "works in dimension d ≤ 7 with Taylor order n in each variable."),
  ("laplacianSteps[d, n, \"Region\" -> \"Ball\"]", "uses the ball mean instead of the sphere mean.")],
 ["Stages: Taylor polynomial, measure, vanishing of odd multi-indices, mean by powers of r, the r² coefficient against Δf/(2d) (sphere) or Δf/(2(d + 2)) (ball), and the limit of the scaled difference.",
  "n = 2 is enough for the r² coefficient and the limit; the r⁴ coefficient needs n ≥ 4.",
  "Option \"Function\" (default f) names the function being averaged."],
 {"Basic Examples": [("Select[laplacianSteps[], BooleanQ]", None), ("laplacianSteps[][\"6 limit r -> 0\"]", None)],
  "Scope": [("Select[laplacianSteps[2, 2, \"Region\" -> \"Ball\"], BooleanQ]", None), ("laplacianSteps[2, 2][\"2 measure\"]", None)],
  "Options": [("laplacianSteps[2, 2, \"Function\" -> u][\"6 limit r -> 0\"]", None)],
  "Properties & Relations": [("laplacianSteps[3, 2][\"3 odd multi-indices: left after integrating\"]", None)]},
 ["laplacianStepsColumn", "sphere", "ball", "Δ"])
page("laplacianStepsColumn", "means", "Laplacian Lab notebook code (staged derivation)",
 [("laplacianStepsColumn[steps]", "typesets the Association returned by laplacianSteps as a column of labelled stages in TraditionalForm.")], [],
 {"Basic Examples": [("laplacianStepsColumn[KeyTake[laplacianSteps[2, 2], {\"2 measure\", \"5 r^2 coefficient\", \"6 limit r -> 0\"}]]", "IMG:stepscol")]},
 ["laplacianSteps"])

page("LaplacianLabKernel", "kernel", "Wolfram Cloud deployment (CCN account)",
 [("POST https://www.wolframcloud.com/obj/ccn2/LaplacianLabKernel", "with form fields key, code_b64 (or code) and mode = \"wolfram\" evaluates the code and returns JSON {text, text_b64, image, chat_ready}."),
  ("… mode = \"chat\", payload_b64", "sends the JSON payload (model, max_tokens, system, messages) to the chat service with the key stored privately in the cloud, and returns {text_b64, stop_reason} or {error, status}.")],
 ["A deployed APIFunction with public permissions, gated by a deploy secret: requests whose key differs get Failure[\"Forbidden\"].",
  "The chat key is read with CloudGet from the private object LaplacianLab/apikey and is never returned.",
  "Text travels as base64 of UTF-8 so that Δ, 𝜟 and θ survive the JSON format.",
  "Graphics results come back as a base64 PNG in image, and as \"-Graphics-\" in text.",
  "The examples call kernelAPI, a local, undeployed copy of the same APIFunction built with the demo secret \"demo-secret\"; it has no chat key, so chat_ready is False."],
 {"Basic Examples": [("kernelAPI[<|\"key\" -> \"demo-secret\", \"code\" -> \"Expand[(x + y)^3]\"|>]", None)],
  "Scope": [("kernelAPI[<|\"key\" -> \"demo-secret\", \"code_b64\" -> b64s[\"Laplacian[x^2 y^2, {x, y}]\"]|>][\"text\"]", None),
            ("kernelAPI[<|\"key\" -> \"demo-secret\", \"code\" -> \"Plot[Sin[x], {x, 0, 6}]\"|>][\"text\"]", None)],
  "Possible Issues": [("kernelAPI[<|\"key\" -> \"wrong\", \"code\" -> \"1 + 1\"|>]", None),
                      ("kernelAPI[<|\"key\" -> \"demo-secret\", \"mode\" -> \"chat\", \"payload_b64\" -> b64s[\"{}\"]|>]", None)]},
 ["b64s", "fromB64", "chatCall"], kind="API Function")
page("b64s", "kernel", "LaplacianLabKernel (local helper)",
 [("b64s[s]", "gives the base64 encoding of the UTF-8 bytes of the string s.")],
 ["The page decodes with atob and TextDecoder, which gives back the same characters."],
 {"Basic Examples": [("b64s[\"Δf = 0\"]", None)],
  "Properties & Relations": [("fromB64[b64s[\"𝜟⊗f, θ, ∂\"]]", None)]},
 ["fromB64", "LaplacianLabKernel"])
page("fromB64", "kernel", "LaplacianLabKernel (local helper)",
 [("fromB64[b]", "decodes the base64 string b to a UTF-8 string, or gives \"\" when b is not valid base64.")], [],
 {"Basic Examples": [("fromB64[\"zpRmID0gMA==\"]", None)],
  "Possible Issues": [("fromB64[\"not base64!\"]", None)]},
 ["b64s", "LaplacianLabKernel"])
page("chatCall", "kernel", "LaplacianLabKernel (local helper)",
 [("chatCall[payload, apiKey]", "sends the JSON string payload to the chat service with apiKey and gives <|\"text_b64\" -> …, \"stop_reason\" -> …|>, or <|\"error\" -> …, \"status\" -> …|>.")],
 ["payload must be a JSON object with a messages list; model must start with claude- (otherwise claude-sonnet-5-5 is used), and max_tokens is clipped to 1–4096 (default 1500).",
  "Only the text blocks of the reply are kept."],
 {"Basic Examples": [("chatCall[\"{\\\"model\\\": \\\"claude-sonnet-5-5\\\"}\", \"unused\"]", None)],
  "Possible Issues": [("chatCall[\"not json\", \"unused\"]", None)]},
 ["LaplacianLabKernel", "b64s"])
