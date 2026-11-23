# "Worked by Hand" sections for the Laplacian Programmable Lab manual.
HAND = {
"𝒶𝓇ℊ𝓈": [
 "With 𝒶𝓇ℊ𝓈 = {x, y, z, t}, a bare f means f[x, y, z, t], and Δ adds one unrepeated second derivative per variable.",
 "Δf = f_{xx} + f_{yy} + f_{zz} + f_{tt}: four terms — Out[2].",
 "With 𝒶𝓇ℊ𝓈 = {x, y}: Δ(x³y³) = 6xy³ + 6x³y — Out[3]."],
"𝒹": [
 "𝒹 is Length[𝒶𝓇ℊ𝓈]: {x, y, z} has 3 entries — Out[1].",
 "After 𝒶𝓇ℊ𝓈 = {x, y, z, t, u}: 5 — Out[2]."],
"𝒞enter": [
 "Append “0” to each variable name: x → x0, y → y0, z → z0 — Out[1].",
 "Δ(x²y + z³) = 2y + 6z; at the centre 2y0 + 6z0 — Out[2]."],
"ℋelp": [
 "ℋelp just collects 𝒹 = 3, 𝒶𝓇ℊ𝓈 = {x, y, z}, 𝒞enter = {x0, y0, z0} and the two operator templates — Out[1]."],
"lapToExpr": [
 "f has no definitions, so lapToExpr[f] = f @@ 𝒶𝓇ℊ𝓈 = f[x, y, z] — Out[1]. An expression such as x² + y is returned unchanged — Out[2].",
 "h[x_, y_, z_] := x² y z gives h DownValues, so lapToExpr[h] stays the bare symbol h, and Δ[h] differentiates a constant: 0.",
 "Δ[h[x, y, z]] = Δ(x²yz) = 2yz. Together {h, 0, 2yz} — Out[3]."],
"lapN": [
 "lapN[f, 1] is one Laplacian of f[x, y, z]: f_{xx} + f_{yy} + f_{zz} — Out[1].",
 "Δ(x⁴ + y²z²) = 12x² + 2z² + 2y²; Δ again: 24 + 4 + 4 = 32 — Out[2].",
 "lapN[f, 0] applies no Laplacian: f[x, y, z] — Out[3]."],
"Δ": [
 "Δ[f] = f_{xx} + f_{yy} + f_{zz} — Out[1].",
 "Δ(x²y²z²) = 2y²z² + 2x²z² + 2x²y²; Δ again: (4z² + 4y²) + (4z² + 4x²) + (4y² + 4x²) = 8x² + 8y² + 8z² — Out[2].",
 "For r = |X| in ℝ³, Δ rᵖ = p(p + 1) rᵖ⁻²; p = −1 gives 0, so 1/r is harmonic — Out[3]."],
"𝜟": [
 "𝜟 evaluates to the inert symbol lapOp — Out[1].",
 "𝜟⊗f is CircleTimes[lapOp, f], which the extension rule turns into lapN[f, 1] = f_{xx} + f_{yy} + f_{zz} — Out[2]."],
"CircleTimes": [
 "𝜟⊗𝜟⊗f has two lapOp factors, so it is lapN[f, 2] = Δ[2][f]; the difference is 0 — Out[1].",
 "𝜟⊗(x² + y² + z²)² = Δ r⁴ = 4 · 5 · r² = 20r², which Laplacian writes as 8x² + 8y² + 8z² + 12(x² + y² + z²) — Out[2].",
 "a⊗b has no lapOp factor, so the rule does not fire: a ⊗ b — Out[3]."],
"sphere": [
 "sphere[d, k] = 1/(2ᵏ k! d(d + 2)…(d + 2k − 2)).",
 "d = 3: k = 1 → 1/(2 · 3) = 1/6; k = 2 → 1/(4 · 2 · 3 · 5) = 1/120; k = 3 → 1/(8 · 6 · 3 · 5 · 7) = 1/5040.",
 "{1, 1/6, 1/120, 1/5040, 1/362880} — Out[1]: the series of sinh r/r, the sphere mean of e^{x}."],
"ball": [
 "ball[d, k] = 1/(2ᵏ k! (d + 2)(d + 4)…(d + 2k)).",
 "d = 3: k = 1 → 1/(2 · 5) = 1/10; k = 2 → 1/(4 · 2 · 5 · 7) = 1/280.",
 "{1, 1/10, 1/280, 1/15120, 1/1330560} — Out[1]. Shifting d by 2 turns the ball product into the sphere product, so ball[d, k] = sphere[d + 2, k] — Out[3]."],
"g": [
 "g(1, 1, 1) = (1 + 1 + 1)^{−3/2} = 3^{−3/2} = 1/(3√3) — Out[1].",
 "With r = |X|, Δ rᵖ = p(p + 1) rᵖ⁻². For p = −3: (−3)(−2) r⁻⁵ = 6/r⁵ — Out[2]."],
"laplacianSteps": [
 "Taylor-expand f to order 2 at the centre and average over the sphere of radius r in ℝ³. Odd monomials average to 0 (Out[6] counts 0 left).",
 "The mean of (x − x0)² over the sphere is r²/3, and the same for y, z; mixed terms vanish. So mean = f0 + (r²/3)(½)(f_{xx} + f_{yy} + f_{zz}) = f0 + r²Δf/6.",
 "Hence 6(mean − f0)/r² → Δf at the centre: both checks are True — Out[1], and the limit is f^{(0,0,2)} + f^{(0,2,0)} + f^{(2,0,0)} — Out[2].",
 "In the plane the circle has length 2πr — Out[4]; the ball factor is 2(d + 2) = 8 — Out[3]."],
"laplacianStepsColumn": [
 "For d = 2, n = 2 the steps give measure 2πr, r² coefficient Δf/4 = ¼(f^{(0,2)} + f^{(2,0)}), and limit Δf.",
 "The column shows exactly these three rows, labelled in CCN orange — Out[1]."],
"LaplacianLabKernel": [
 "The request carries the right key and plain code, so the kernel evaluates Expand[(x + y)³] = x³ + 3x²y + 3xy² + y³.",
 "text_b64 is the base64 of those ASCII bytes; no graphics, so image is \"\"; no chat key is stored, so chat_ready is False — Out[1].",
 "A wrong key stops at the first Which test: Failure[\"Forbidden\"] — Out[4]. Chat mode with no stored key returns status 503 — Out[5]."],
"b64s": [
 "UTF-8 of “Δf = 0”: Δ = CE 94, then 66 20 3D 20 30 — seven bytes.",
 "Groups of three bytes → four 6-bit digits: CE 94 66 → z p R m; 20 3D 20 → I D 0 g; 30 → M A, padded ==.",
 "“zpRmID0gMA==” — Out[1]."],
"fromB64": [
 "Reverse the digits of “zpRmID0gMA==”: z p R m I D 0 g M A → bytes CE 94 66 20 3D 20 30.",
 "Decoded as UTF-8: “Δf = 0” — Out[1]. Text that is not base64 fails inside Check and gives \"\" — Out[2]."],
"chatCall": [
 "The payload {\"model\": \"claude-sonnet-5-5\"} is valid JSON but has no messages list.",
 "The first test fails before any network request, so the reply is <|\"error\" → \"bad payload\", \"status\" → 400|> — Out[1]."],
}
