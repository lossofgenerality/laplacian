{
// ===================== helpers =====================
const $ = id => document.getElementById(id);
const fmt = (x, d = 4) => (x === undefined || x === null || Number.isNaN(x)) ? "—" : Math.abs(x) < 1e-12 ? "0" : Number(x.toFixed(d)).toString();
const isDark = () => { const t = document.documentElement.dataset.theme; return t === "dark" || (t !== "light" && matchMedia("(prefers-color-scheme: dark)").matches); };
const NEG = [46, 92, 199], POS = [250, 143, 43];
function kcol(k, s) {
  const mid = isDark() ? [52, 60, 72] : [244, 244, 244], t = Math.max(-1, Math.min(1, k / s));
  const a = t < 0 ? NEG : POS, w = Math.abs(t);
  return `rgb(${a.map((c, i) => Math.round(mid[i] + (c - mid[i]) * w)).join(",")})`;
}
const probe = document.createElement("i"); probe.style.display = "none"; document.body.appendChild(probe);
const css = v => { probe.style.color = `var(${v})`; return getComputedStyle(probe).color; };
function fit(cv) { const r = cv.getBoundingClientRect(), d = devicePixelRatio || 1; cv.width = Math.max(1, r.width * d); cv.height = Math.max(1, r.height * d); const c = cv.getContext("2d"); c.setTransform(d, 0, 0, d, 0, 0); return { c, W: r.width, H: r.height }; }
const watchers = [];
function onSize(el, fn) { const ro = new ResizeObserver(() => fn()); ro.observe(el); watchers.push(ro); }

// generic line plot
function plot(cv, o) {
  const { c, W, H } = fit(cv); c.clearRect(0, 0, W, H);
  const ink = css("--ink") || "#222", soft = css("--soft") || "#777", line = css("--line") || "#ddd";
  const small = W < 420, L = small ? 44 : 58, R = 12, T = o.title ? 26 : 12, B = 34;
  const tx = v => (o.xlog ? Math.log10(v) : v), ty = v => (o.ylog ? Math.log10(Math.max(v, 1e-300)) : v);
  const [x0, x1] = (o.xr || [0, 1]).map(tx), [y0, y1] = (o.yr || [0, 1]).map(ty);
  const X = v => L + (tx(v) - x0) / (x1 - x0) * (W - L - R), Y = v => T + (1 - (ty(v) - y0) / (y1 - y0)) * (H - T - B);
  c.font = "12px IBM Plex Sans, sans-serif"; c.fillStyle = soft; c.strokeStyle = line; c.lineWidth = 1;
  const ticks = (a, b, log) => { if (log) { const out = []; for (let e = Math.ceil(a); e <= Math.floor(b); e++) out.push(10 ** e); return out; } const step = 10 ** Math.floor(Math.log10((b - a) / 4 || 1)), m = (b - a) / step > 8 ? 2 * step : step; const out = []; for (let v = Math.ceil(a / m) * m; v <= b + 1e-9; v += m) out.push(+v.toFixed(10)); return out; };
  const lab = (v, log) => (log ? (v >= 1e-2 && v <= 1e3 ? String(v) : "1e" + Math.round(Math.log10(v))) : String(+v.toFixed(3)));
  ticks(x0, x1, o.xlog).forEach(v => { const x = X(v); c.beginPath(); c.moveTo(x, T); c.lineTo(x, H - B); c.stroke(); if (!small || true) { c.textAlign = "center"; c.fillText(lab(v, o.xlog), x, H - B + 15); } });
  ticks(y0, y1, o.ylog).forEach(v => { const y = Y(v); c.beginPath(); c.moveTo(L, y); c.lineTo(W - R, y); c.stroke(); c.textAlign = "right"; c.fillText(lab(v, o.ylog), L - 6, y + 4); });
  c.textAlign = "center"; c.fillText(o.xlabel || "", L + (W - L - R) / 2, H - 4);
  c.save(); c.translate(12, T + (H - T - B) / 2); c.rotate(-Math.PI / 2); c.fillText(o.ylabel || "", 0, 0); c.restore();
  if (o.title) { c.fillStyle = ink; c.textAlign = "left"; c.font = "600 13px IBM Plex Sans, sans-serif"; c.fillText(o.title, L, 16); }
  c.save(); c.beginPath(); c.rect(L, T, W - L - R, H - T - B); c.clip();
  (o.series || []).forEach(s => {
    c.strokeStyle = s.color; c.fillStyle = s.color; c.lineWidth = s.width || 2; c.setLineDash(s.dash ? [5, 4] : []);
    if (s.dots) s.pts.forEach(([a, b]) => { c.beginPath(); c.arc(X(a), Y(b), 3, 0, 7); c.fill(); });
    else { c.beginPath(); s.pts.forEach(([a, b], i) => (i ? c.lineTo(X(a), Y(b)) : c.moveTo(X(a), Y(b)))); c.stroke(); }
  });
  (o.vlines || []).forEach(v => { c.setLineDash([3, 3]); c.strokeStyle = soft; c.lineWidth = 1; c.beginPath(); c.moveTo(X(v), T); c.lineTo(X(v), H - B); c.stroke(); });
  c.restore(); c.setLineDash([]);
  if (o.series && o.series.some(s => s.label)) {
    let yy = T + 8; c.font = "12px IBM Plex Sans, sans-serif"; c.textAlign = "left";
    o.series.filter(s => s.label).forEach(s => { const w = c.measureText(s.label).width; const x = W - R - w - 26; c.fillStyle = css("--panel") || "#fff"; c.globalAlpha = 0.85; c.fillRect(x - 4, yy - 9, w + 30, 16); c.globalAlpha = 1; c.strokeStyle = s.color; c.lineWidth = 2; c.setLineDash(s.dash ? [4, 3] : []); c.beginPath(); c.moveTo(x, yy - 1); c.lineTo(x + 18, yy - 1); c.stroke(); c.setLineDash([]); c.fillStyle = ink; c.fillText(s.label, x + 22, yy + 3); yy += 17; });
  }
}

// 3-D painter for coloured triangles
function render3D(cv, tris, view, opts = {}) {
  const { c, W, H } = fit(cv); c.clearRect(0, 0, W, H);
  const { yaw, pitch } = view, cy = Math.cos(yaw), sy = Math.sin(yaw), cp = Math.cos(pitch), sp = Math.sin(pitch);
  const rot = p => { const x = cy * p[0] - sy * p[1], y = sy * p[0] + cy * p[1]; return [x, cp * y - sp * p[2], sp * y + cp * p[2]]; };
  const pts = tris.map(t => ({ v: t.v.map(rot), col: t.col }));
  let mx = 1e-9; pts.forEach(t => t.v.forEach(p => (mx = Math.max(mx, Math.abs(p[0]), Math.abs(p[2])))));
  const s = Math.min(W, H) * 0.46 / mx, ox = W / 2, oy = H / 2;
  pts.forEach(t => (t.z = (t.v[0][1] + t.v[1][1] + t.v[2][1]) / 3)); pts.sort((a, b) => b.z - a.z);
  const light = [0.3, -0.75, 0.6], ln = Math.hypot(...light);
  for (const t of pts) {
    const [a, b, d] = t.v, u = [b[0] - a[0], b[1] - a[1], b[2] - a[2]], w = [d[0] - a[0], d[1] - a[1], d[2] - a[2]];
    const n = [u[1] * w[2] - u[2] * w[1], u[2] * w[0] - u[0] * w[2], u[0] * w[1] - u[1] * w[0]], nn = Math.hypot(...n) || 1;
    const sh = 0.62 + 0.38 * Math.abs((n[0] * light[0] + n[1] * light[1] + n[2] * light[2]) / nn / ln);
    const m = t.col.match(/\d+/g).map(Number).map(v => Math.round(v * sh));
    c.fillStyle = `rgb(${m.join(",")})`; c.strokeStyle = opts.wire ? "rgba(90,100,115,0.35)" : c.fillStyle; c.lineWidth = opts.wire ? 0.5 : 0.6;
    c.beginPath(); c.moveTo(ox + s * a[0], oy - s * a[2]); c.lineTo(ox + s * b[0], oy - s * b[2]); c.lineTo(ox + s * d[0], oy - s * d[2]); c.closePath(); c.fill(); c.stroke();
  }
}
function dragView(cv, view, redraw) {
  let last = null;
  cv.addEventListener("pointerdown", e => { last = [e.clientX, e.clientY]; cv.setPointerCapture(e.pointerId); });
  cv.addEventListener("pointermove", e => { if (!last) return; view.yaw += (e.clientX - last[0]) * 0.01; view.pitch = Math.max(-1.5, Math.min(1.5, view.pitch + (e.clientY - last[1]) * 0.01)); last = [e.clientX, e.clientY]; redraw(); });
  cv.addEventListener("pointerup", () => (last = null)); cv.addEventListener("pointercancel", () => (last = null));
}
const reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;

// ===================== routing =====================
const sections = [...document.querySelectorAll("main > section")];
const inits = {}, started = new Set();
let current = "map";
$("nav").innerHTML = sections.map(s => `<a href="#${s.id}" data-id="${s.id}">${s.dataset.title}</a>`).join("");
function show(id) {
  if (!sections.some(s => s.id === id)) id = "map";
  current = id;
  sections.forEach(s => (s.hidden = s.id !== id));
  document.querySelectorAll("#nav a").forEach(a => (a.getAttribute("aria-current") === "page" && a.removeAttribute("aria-current"), a.dataset.id === id && a.setAttribute("aria-current", "page")));
  const i = sections.findIndex(s => s.id === id), p = sections[i - 1], n = sections[i + 1];
  $("pager").innerHTML = (p ? `<a href="#${p.id}"><span>Previous</span>${p.dataset.title}</a>` : "<span></span>") + (n ? `<a href="#${n.id}" style="text-align:right"><span>Next</span>${n.dataset.title}</a>` : "<span></span>");
  if (!started.has(id) && inits[id]) { started.add(id); try { inits[id](); } catch (e) { console.error(e); } }
  if (window.MathJax && MathJax.typesetPromise) MathJax.typesetPromise([sections[i]]).catch(() => {});
  const na = document.querySelector(`#nav a[data-id="${id}"]`), nv = $("nav"); if (na) nv.scrollLeft = na.offsetLeft - nv.clientWidth / 2 + na.clientWidth / 2;
  window.scrollTo(0, 0);
}
addEventListener("hashchange", () => show(location.hash.slice(1)));

// ===================== 1. map =====================
const ROWS = [
  ["surfaces", "Gauss curvature", "K = −e^(−2u) Δ₀u", "graphs", "Gauss–Bonnet sums", "angle defect · resistance · Higuchi"],
  ["surfaces", "Mean curvature", "ΔX = −2H n", "mesh", "Cotangent Laplacian", "ΔXᵢ ≈ −2Hᵢ nᵢ on meshes"],
  ["means", "Ball and circle means", "r⁴(Δ²f/64 + KΔf/96)", "graphs", "Ollivier / Lin–Lu–Yau", "compare neighbour means"],
  ["bochner", "Bochner formula", "Γ₂ = |Hess f|² + Ric", "graphs", "Bakry–Émery CD(K, N)", "Γ₂ ≥ KΓ + (Δf)²/N"],
  ["bochner", "Weitzenböck splitting", "Δ<tspan baseline-shift=\"sub\" font-size=\"72%\">Hodge</tspan> = ∇*∇ + Ric", "graphs", "Forman curvature", "4 − d<tspan baseline-shift=\"sub\" font-size=\"72%\">x</tspan> − d<tspan baseline-shift=\"sub\" font-size=\"72%\">y</tspan> + 3·triangles"],
  ["heat", "Heat trace, spectrum", "S/6 in Tr e^(tΔ); λ₁ ≥ nk", "graphs", "Graph spectral bounds", "λ₁ ≥ κ, λ₁ ≥ K"]
];
function drawMap() {
  const svg = $("mapsvg"), W = svg.clientWidth || 760, small = W < 640;
  const bw = small ? (W - 40) / 2 : 300, gap = small ? 16 : W - 2 * bw - 48, x1 = 16, x2 = x1 + bw + gap, bh = 48, top = 34;
  let h = `<text x="${x1}" y="20" font-size="12" font-weight="600" fill="var(--soft)">SMOOTH</text><text x="${x2}" y="20" font-size="12" font-weight="600" fill="var(--soft)">DISCRETE</text>`;
  ROWS.forEach((r, i) => {
    const y = top + i * (bh + 10), hi = i === 2;
    const box = (x, sec, a, b) => `<a href="#${sec}"><rect x="${x}" y="${y}" width="${bw}" height="${bh}" rx="8" fill="${hi ? "var(--tint)" : "var(--panel)"}" stroke="${hi ? "var(--acc)" : "var(--line)"}" stroke-width="${hi ? 2 : 1}"/><text x="${x + 10}" y="${y + 20}" font-size="${small ? 11.5 : 13.5}" font-weight="600" fill="var(--ink)">${a}</text><text x="${x + 10}" y="${y + 37}" font-size="${small ? 10.5 : 12}" fill="var(--soft)">${b}</text></a>`;
    h += box(x1, r[0], r[1], r[2]) + box(x2, r[3], r[4], r[5]);
    h += `<path d="M${x1 + bw + 2} ${y + bh / 2}H${x2 - 6}" stroke="var(--soft)" stroke-width="1.2"/><path d="M${x2 - 10} ${y + bh / 2 - 4}L${x2 - 3} ${y + bh / 2}L${x2 - 10} ${y + bh / 2 + 4}z" fill="var(--soft)"/>`;
  });
  const yb = top + 6 * (bh + 10);
  h += `<a href="#ollivier"><rect x="${x1}" y="${yb}" width="${x2 + bw - x1}" height="36" rx="8" fill="var(--bg)" stroke="var(--line)"/><text x="${(x1 + x2 + bw) / 2}" y="${yb + 23}" text-anchor="middle" font-size="${small ? 11 : 13}" fill="var(--ink)">Point clouds and ε-balls: graph Laplacians converge to Δ and Ollivier curvature to Ric</text></a>`;
  svg.setAttribute("viewBox", `0 0 ${W} ${yb + 44}`); svg.parentElement.style.minHeight = `${(yb + 44) * (svg.clientWidth / W || 1)}px`;
  svg.innerHTML = h;
}
inits.map = () => {
  drawMap(); onSize($("mapsvg").parentElement, drawMap);
  $("tiles").innerHTML = sections.slice(1).map(s => `<a class="tile" href="#${s.id}"><b>${s.dataset.title}</b><span>${s.querySelector("h2")?.textContent || ""}</span></a>`).join("");
};

// ===================== 2. surfaces =====================
const SV = { yaw: 0.6, pitch: 0.45 };
let surfKey = "torus", surfQ = "K", surfCache = {};
function surfData(key) {
  if (surfCache[key]) return surfCache[key];
  const S = LC.SURFACES[key], nu = 56, nv = 36, grid = [];
  for (let i = 0; i <= nu; i++) { grid.push([]); for (let j = 0; j <= nv; j++) { const u = S.U[0] + (S.U[1] - S.U[0]) * i / nu, v = S.V[0] + (S.V[1] - S.V[0]) * j / nv; grid[i].push(LC.surfaceKH(S.X, u, v, 1e-3)); } }
  let kmin = Infinity, kmax = -Infinity, hmax = 0; grid.flat().forEach(q => { kmin = Math.min(kmin, q.K); kmax = Math.max(kmax, q.K); hmax = Math.max(hmax, Math.abs(q.H)); });
  return (surfCache[key] = { S, grid, nu, nv, kmin, kmax, hmax, total: LC.totalCurvature(S, 160, 160) });
}
function drawSurf() {
  const d = surfData(surfKey), tris = [];
  const col = q => (surfQ === "K" ? kcol(q.K, 1) : kcol(Math.abs(q.H), 1));
  for (let i = 0; i < d.nu; i++) for (let j = 0; j < d.nv; j++) {
    const a = d.grid[i][j], b = d.grid[i + 1][j], c = d.grid[i + 1][j + 1], e = d.grid[i][j + 1];
    const cl = col({ K: (a.K + c.K) / 2, H: (a.H + c.H) / 2 });
    tris.push({ v: [a.p, b.p, c.p], col: cl }, { v: [a.p, c.p, e.p], col: cl });
  }
  render3D($("surfcv"), tris, SV, { wire: false });
  const chi = d.S.chi;
  $("surfread").innerHTML = `<dt>K range</dt><dd>${fmt(d.kmin)} … ${fmt(d.kmax)}</dd><dt>max |H|</dt><dd>${fmt(d.hmax)}</dd><dt>∬ K dA</dt><dd>${fmt(d.total, 4)}</dd><dt>∬ K dA / 2π</dt><dd>${fmt(d.total / (2 * Math.PI), 4)}</dd>`;
  $("surfcheck").textContent = chi !== undefined ? `Closed surface: ∬K dA/2π = ${fmt(d.total / (2 * Math.PI), 3)}, Euler characteristic χ = ${chi}.` : `Open surface: ∬K dA depends on the patch drawn; Gauss–Bonnet adds a boundary term.`;
}
inits.surfaces = () => {
  $("surfsel").innerHTML = Object.entries(LC.SURFACES).map(([k, s]) => `<option value="${k}" ${k === surfKey ? "selected" : ""}>${s.name}</option>`).join("");
  $("surfsel").onchange = e => { surfKey = e.target.value; drawSurf(); };
  $("surfq").onchange = e => { surfQ = e.target.value; drawSurf(); };
  dragView($("surfcv"), SV, drawSurf); onSize($("surfcv"), drawSurf);
};

// ===================== 3. Ricci flow =====================
let RS = null, ricciTimer = 0, ricciHist = [];
function ricciReset() { RS = LC.ricciInit(32, +$("riccia").value, +$("riccia").value * 0.83); ricciHist = [[0, maxAbs(LC.ricciK(RS))]]; drawRicci(); }
const maxAbs = M => Math.max(...M.flat().map(Math.abs));
function drawRicci() {
  const { c, W, H } = fit($("riccicv")), K = LC.ricciK(RS), N = RS.N, s = Math.min(W, H) * 0.92, ox = (W - s) / 2, oy = (H - s) / 2, cell = s / N;
  c.clearRect(0, 0, W, H);
  for (let i = 0; i < N; i++) for (let j = 0; j < N; j++) { c.fillStyle = kcol(K[i][j], 1.5); c.fillRect(ox + i * cell, oy + (N - 1 - j) * cell, cell + 0.6, cell + 0.6); }
  c.strokeStyle = css("--line"); c.strokeRect(ox, oy, s, s);
  const mk = maxAbs(K);
  $("ricciread").innerHTML = `<dt>t</dt><dd>${fmt(RS.t, 3)}</dd><dt>max |K|</dt><dd>${fmt(mk, 4)}</dd><dt>∬ K dA</dt><dd>${fmt(LC.ricciTotalK(RS), 10)}</dd>`;
  plot($("riccichart"), { xr: [0, 2], yr: [0.01, 10], ylog: true, xlabel: "t", ylabel: "max |K|", series: [{ pts: ricciHist, color: POSc() }] });
}
const POSc = () => "rgb(250,143,43)", NEGc = () => (isDark() ? "rgb(111,151,255)" : "rgb(46,92,199)");
function ricciRun() {
  if (ricciTimer) { cancelAnimationFrame(ricciTimer); ricciTimer = 0; $("ricciplay").textContent = "Run"; return; }
  $("ricciplay").textContent = "Pause";
  const tick = () => { LC.ricciStep(RS, reduced ? 200 : 12); ricciHist.push([RS.t, maxAbs(LC.ricciK(RS))]); drawRicci(); if (RS.t < 2) ricciTimer = requestAnimationFrame(tick); else { ricciTimer = 0; $("ricciplay").textContent = "Run"; } };
  ricciTimer = requestAnimationFrame(tick);
}
inits.ricci = () => { ricciReset(); $("ricciplay").onclick = ricciRun; $("riccireset").onclick = () => { if (ricciTimer) ricciRun(); ricciReset(); }; $("riccia").oninput = () => { if (ricciTimer) ricciRun(); ricciReset(); }; onSize($("riccicv"), drawRicci); };

// ===================== 4. curved means =====================
let meansData = null;
function drawMeans() {
  if (!meansData) {
    const rs = []; for (let k = 4; k <= 24; k++) rs.push(2 ** (-k / 4));
    const e = rs.map(r => { const ex = LC.circleMean(r); return [r, Math.abs(ex - LC.approx.flat(r)), Math.abs(ex - LC.approx.curved4(r)), Math.abs(ex - LC.approx.curved6(r))]; });
    const slope = k => { const pts = e.filter(r => r[0] > 0.04 && r[0] < 0.16).map(r => [Math.log(r[0]), Math.log(r[k])]), n = pts.length, sx = pts.reduce((a, p) => a + p[0], 0), sy = pts.reduce((a, p) => a + p[1], 0), sxx = pts.reduce((a, p) => a + p[0] * p[0], 0), sxy = pts.reduce((a, p) => a + p[0] * p[1], 0); return (n * sxy - sx * sy) / (n * sxx - sx * sx); };
    meansData = { e, slopes: [slope(1), slope(2), slope(3)] };
  }
  const { e, slopes } = meansData;
  plot($("meanscv"), { xlog: true, ylog: true, xr: [0.01, 0.6], yr: [1e-14, 1e-2], xlabel: "r", ylabel: "|error|", series: [
    { pts: e.map(r => [r[0], r[1]]), color: "rgb(130,138,150)", label: "flat formula (K = 0)" },
    { pts: e.map(r => [r[0], r[2]]), color: POSc(), label: "+ KΔf/96" },
    { pts: e.map(r => [r[0], r[3]]), color: NEGc(), label: "+ r⁶ terms" }] });
  $("meansread").innerHTML = `<dt>flat formula</dt><dd>${fmt(slopes[0], 2)}</dd><dt>+ KΔf/96 at r⁴</dt><dd>${fmt(slopes[1], 2)}</dd><dt>+ r⁶ curvature terms</dt><dd>${fmt(slopes[2], 2)}</dd>`;
}
function drawDisc() {
  const K = +$("discK").value; $("discKv").textContent = `K = ${K}`;
  const pts = K => Array.from({ length: 120 }, (_, i) => { const r = 0.02 + 2.98 * i / 119; return [r, LC.discRatio(K, r)]; });
  plot($("disccv"), { xr: [0, 3], yr: [0, 2], xlabel: "r", ylabel: "A(r)/πr²", series: [{ pts: pts(0), color: "rgb(130,138,150)", dash: true, label: "K = 0" }, { pts: pts(K), color: K >= 0 ? POSc() : NEGc(), label: `K = ${K}` }] });
}
inits.means = () => { drawMeans(); drawDisc(); $("discK").oninput = drawDisc; onSize($("meanscv"), drawMeans); onSize($("disccv"), drawDisc); };

// ===================== 5. heat =====================
let heatPts = null;
function drawHeat() {
  if (!heatPts) heatPts = Array.from({ length: 160 }, (_, i) => { const t = 0.004 + 0.4 * i / 159; return [t, t * LC.sphereTrace(t), t * LC.torusTrace(t)]; });
  const t = +$("heatt").value;
  plot($("heatcv"), { xr: [0, 0.4], yr: [0.98, 1.16], xlabel: "t", ylabel: "Tr e^{tΔ} ÷ (Area/4πt)", vlines: [t], series: [
    { pts: heatPts.map(p => [p[0], p[1]]), color: POSc(), label: "unit sphere, K = 1" },
    { pts: heatPts.map(p => [p[0], 1 + p[0] / 3 + p[0] ** 2 / 15]), color: css("--ink"), dash: true, width: 1.5, label: "1 + t/3 + t²/15" },
    { pts: heatPts.map(p => [p[0], p[2]]), color: NEGc(), label: "flat torus, same area" }] });
  $("heatread").innerHTML = `<dt>sphere</dt><dd>${fmt(t * LC.sphereTrace(t), 6)}</dd><dt>1 + t/3 + t²/15</dt><dd>${fmt(1 + t / 3 + t * t / 15, 6)}</dd><dt>flat torus</dt><dd>${fmt(t * LC.torusTrace(t), 6)}</dd><dt>difference ≈ t/3</dt><dd>${fmt(t * LC.sphereTrace(t) - t * LC.torusTrace(t), 6)}</dd>`;
}
inits.heat = () => { drawHeat(); $("heatt").oninput = drawHeat; onSize($("heatcv"), drawHeat); };

// ===================== 6. Bochner =====================
function drawBoch() {
  const K = +$("bochK").value; $("bochKv").textContent = `K = ${K}`;
  const rmax = 3.2, pts = k => Array.from({ length: 300 }, (_, i) => { const r = 0.05 + (rmax - 0.05) * i / 299; return [r, LC.lapDist(k, r)]; }).filter(p => Math.abs(p[1]) < 50);
  plot($("bochcv"), { xr: [0, rmax], yr: [-3, 5], xlabel: "r", ylabel: "Δr", series: [{ pts: pts(0), color: "rgb(130,138,150)", dash: true, label: "K = 0: 1/r" }, { pts: pts(K), color: K >= 0 ? POSc() : NEGc(), label: `K = ${K}` }] });
  const rd = [`<dt>Ric ≥ K, n = 2</dt><dd>K = ${K}</dd>`];
  if (K > 0) rd.push(`<dt>Lichnerowicz λ₁ ≥ nK</dt><dd>${fmt(2 * K, 3)}</dd><dt>round sphere λ₁ = 2K</dt><dd>${fmt(2 * K, 3)} (equality)</dd><dt>Bonnet–Myers diam ≤ π/√K</dt><dd>${fmt(Math.PI / Math.sqrt(K), 3)}</dd><dt>Δr changes sign at r</dt><dd>${fmt(Math.PI / (2 * Math.sqrt(K)), 3)}</dd>`);
  else rd.push(`<dt>Lichnerowicz</dt><dd>no bound for K ≤ 0</dd><dt>Δr → √|K| as r → ∞</dt><dd>${fmt(Math.sqrt(-K), 3)}</dd>`);
  $("bochread").innerHTML = rd.join("");
}
inits.bochner = () => { drawBoch(); $("bochK").oninput = drawBoch; onSize($("bochcv"), drawBoch); };

// ===================== 7. mesh =====================
const MV = { yaw: 0.5, pitch: 0.6 };
let meshState = null;
function meshBuild() {
  const [nu, nv] = $("meshres").value.split(",").map(Number), M = LC.torusMesh(nu, nv), C = LC.meshCurvature(M);
  meshState = { M, C, nu, nv };
}
function drawMesh() {
  if (!meshState) meshBuild();
  const { M, C, nu, nv } = meshState, q = $("meshq").value, vals = q === "K" ? C.K : C.H;
  render3D($("meshcv"), M.T.map(t => ({ v: t.map(i => M.P[i]), col: kcol((vals[t[0]] + vals[t[1]] + vals[t[2]]) / 3, q === "K" ? 1 : 0.7) })), MV, { wire: true });
  const tot = C.defect.reduce((a, b) => a + b, 0);
  let err = 0; for (let i = 0; i < nu; i++) for (let j = 0; j < nv; j++) { const v = 2 * Math.PI * j / nv, k = Math.cos(v) / (2 + Math.cos(v)); err = Math.max(err, Math.abs(C.K[i * nv + j] - k)); }
  $("meshread").innerHTML = `<dt>vertices</dt><dd>${M.P.length}</dd><dt>Σ angle defect</dt><dd>${fmt(tot, 12)}</dd><dt>Σ defect / 2π (= χ)</dt><dd>${fmt(tot / (2 * Math.PI), 10)}</dd><dt>max |K<sub>mesh</sub> − K|</dt><dd>${fmt(err, 4)}</dd>`;
  const pts = [], sm = []; for (let j = 0; j < nv; j++) pts.push([2 * Math.PI * j / nv, C.K[j]]); for (let k = 0; k <= 120; k++) { const v = 2 * Math.PI * k / 120; sm.push([v, Math.cos(v) / (2 + Math.cos(v))]); }
  plot($("meshchart"), { xr: [0, 2 * Math.PI], yr: [-1.1, 0.5], xlabel: "v (around the tube)", ylabel: "K", series: [{ pts: sm, color: css("--ink"), width: 1.5, label: "smooth cos v/(2 + cos v)" }, { pts, color: POSc(), dots: true, label: "mesh defect/area" }] });
}
inits.mesh = () => { $("meshres").onchange = () => { meshBuild(); drawMesh(); }; $("meshq").onchange = drawMesh; dragView($("meshcv"), MV, drawMesh); onSize($("meshcv"), drawMesh); };

// ===================== 8. graphs =====================
const KINFO = {
  lly: { s: 1.25, edge: true, f: (G, a, b) => LC.kappaLLY(G, a, b), name: "Lin–Lu–Yau κ" },
  k0: { s: 1, edge: true, f: (G, a, b) => LC.kappa0(G, a, b), name: "Ollivier κ₀" },
  be: { s: 1, edge: false, f: (G, v) => LC.bakryEmery(G, v), name: "Bakry–Émery K∞" },
  forman: { s: 6, edge: true, f: (G, a, b) => LC.forman(G, a, b), name: "Forman" },
  formanAug: { s: 6, edge: true, f: (G, a, b) => LC.formanAug(G, a, b), name: "Forman + triangles" },
  res: { s: 0.3, edge: false, all: G => LC.resistanceCurv(G), name: "resistance p" },
  stein: { s: 1.5, edge: false, all: G => LC.steinerberger(G), name: "Steinerberger K" }
};
const NOTES = {
  tree: "Interior edges have κ<sub>LLY</sub> = −2/3 (the two neighbourhoods do not overlap); leaf edges +2/3, because a leaf sees only its parent. On a tree, resistance equals distance, so resistance and Steinerberger curvature are exactly proportional.",
  cycle: "Flat: Lin–Lu–Yau, Ollivier and Bakry–Émery are all 0 on C₆ — the discrete circle has no curvature.",
  cube: "κ<sub>LLY</sub> = K<sub>BE</sub> = 2/3 = λ₁: the cube is an equality case of both discrete Lichnerowicz bounds.",
  complete: "Every pair shares three neighbours, so mass can stay put: κ<sub>LLY</sub> = 5/4 = λ₁, another equality case.",
  petersen: "Girth 5 and 3-regular: κ<sub>LLY</sub> = 0, κ₀ = −1/3 and K<sub>BE</sub> = 2/d − 1 = −1/3, yet λ₁ = 2/3 is large.",
  grid: "Zero curvature inside, as on ℤ²; the boundary carries positive Lin–Lu–Yau curvature and the corners the most.",
  dumbbell: "The bridge is a bottleneck: its edges are negative (κ<sub>LLY</sub> = −3/5) while the cliques are positive. This is the negative curvature behind over-squashing in graph networks."
};
let gKey = "dumbbell", kKey = "lly";
function graphValues(G, k) {
  const I = KINFO[k];
  if (I.edge) return G.edges.map(([a, b]) => I.f(G, a, b));
  if (I.all) return I.all(G);
  return [...Array(G.n).keys()].map(v => I.f(G, v));
}
function drawGraph() {
  const G = LC.GRAPHS[gKey](), I = KINFO[kKey], vals = graphValues(G, kKey), svg = $("graphsvg");
  const W = svg.clientWidth || 600, H = svg.clientHeight || 340, xs = G.pos.map(p => p[0]), ys = G.pos.map(p => p[1]);
  const [x0, x1, y0, y1] = [Math.min(...xs), Math.max(...xs), Math.min(...ys), Math.max(...ys)], pad = 34;
  const sc = Math.min((W - 2 * pad) / (x1 - x0 || 1), (H - 2 * pad) / (y1 - y0 || 1));
  const P = G.pos.map(([x, y]) => [W / 2 + (x - (x0 + x1) / 2) * sc, H / 2 + (y - (y0 + y1) / 2) * sc]);
  const r = Math.max(6, Math.min(14, sc * 0.09));
  let h = "";
  G.edges.forEach(([a, b], i) => { const col = I.edge ? kcol(vals[i], I.s) : "var(--line)"; h += `<line x1="${P[a][0]}" y1="${P[a][1]}" x2="${P[b][0]}" y2="${P[b][1]}" stroke="${col}" stroke-width="${I.edge ? 6 : 2}" stroke-linecap="round" tabindex="0" data-v="edge ${a}–${b}: ${fmt(vals[i], 4)}"><title>edge ${a}–${b}: ${fmt(vals[i], 4)}</title></line>`; });
  P.forEach((p, v) => { const col = I.edge ? "var(--soft)" : kcol(vals[v], I.s); h += `<circle cx="${p[0]}" cy="${p[1]}" r="${I.edge ? r * 0.55 : r}" fill="${col}" stroke="var(--ink)" stroke-opacity=".35" tabindex="0" data-v="vertex ${v}: ${I.edge ? "degree " + G.adj[v].length : fmt(vals[v], 4)}"><title>vertex ${v}</title></circle>`; });
  svg.setAttribute("viewBox", `0 0 ${W} ${H}`); svg.innerHTML = h;
  const sp = LC.normLapSpectrum(G), mn = Math.min(...vals), mx = Math.max(...vals), mean = vals.reduce((a, b) => a + b, 0) / vals.length;
  const lly = Math.min(...G.edges.map(([a, b]) => LC.kappaLLY(G, a, b))), be = Math.min(...[...Array(G.n).keys()].map(v => LC.bakryEmery(G, v)));
  $("gread").innerHTML = `<dt>${I.name}: min</dt><dd>${fmt(mn)}</dd><dt>max</dt><dd>${fmt(mx)}</dd><dt>${kKey === "res" ? "sum" : "mean"}</dt><dd>${fmt(kKey === "res" ? mean * vals.length : mean)}</dd><dt>λ₁ (normalised)</dt><dd>${fmt(sp[1])}</dd><dt>λ_max</dt><dd>${fmt(sp[sp.length - 1])}</dd><dt id="gpick">selected</dt><dd id="gpickv">—</dd>`;
  $("gcheck").innerHTML = `λ₁ = ${fmt(sp[1])} ≥ min κ<sub>LLY</sub> = ${fmt(lly)} ${sp[1] >= lly - 1e-9 ? "✓" : "✗"} · λ₁ ≥ min K<sub>BE</sub> = ${fmt(be)} ${sp[1] >= be - 1e-6 ? "✓" : "✗"}${kKey === "res" ? ` · Σp = ${fmt(mean * vals.length, 10)} (always 1)` : ""}`;
  $("gnote").innerHTML = NOTES[gKey];
  svg.querySelectorAll("[data-v]").forEach(el => { const f = () => { $("gpickv").textContent = el.dataset.v; }; el.addEventListener("pointerenter", f); el.addEventListener("focus", f); el.addEventListener("click", f); });
  window.__labState = { graph: gKey, curvature: I.name, min: mn, max: mx, lambda1: sp[1] };
}
inits.graphs = () => { $("gsel").onchange = e => { gKey = e.target.value; drawGraph(); }; $("ksel").onchange = e => { kKey = e.target.value; drawGraph(); }; onSize($("graphsvg").parentElement, drawGraph); };

// ===================== 9. curve shortening =====================
let CX = null, CA0 = 0, Ct = 0, Chist = [], Cframe = 0, Csteps = 0;
function flowReset() { CX = LC.curveInit($("flowsel").value); CA0 = LC.polyArea(CX); Ct = 0; Csteps = 0; Chist = [[0, CA0]]; drawFlow(); }
function drawFlow() {
  const { c, W, H } = fit($("flowcv")); c.clearRect(0, 0, W, H);
  const s = Math.min(W, H) / 3.4, ox = W / 2, oy = H / 2;
  c.strokeStyle = css("--line"); c.setLineDash([3, 3]); const init = LC.curveInit($("flowsel").value); c.beginPath(); init.forEach((p, i) => (i ? c.lineTo(ox + s * p[0], oy - s * p[1]) : c.moveTo(ox + s * p[0], oy - s * p[1]))); c.closePath(); c.stroke(); c.setLineDash([]);
  c.strokeStyle = POSc(); c.lineWidth = 3; c.beginPath(); CX.forEach((p, i) => (i ? c.lineTo(ox + s * p[0], oy - s * p[1]) : c.moveTo(ox + s * p[0], oy - s * p[1]))); c.closePath(); c.stroke();
  const A = LC.polyArea(CX), rate = Ct > 0 ? (A - CA0) / Ct : NaN;
  $("flowread").innerHTML = `<dt>t</dt><dd>${fmt(Ct, 3)}</dd><dt>area</dt><dd>${fmt(A, 4)}</dd><dt>mean dA/dt</dt><dd>${fmt(rate, 3)}</dd><dt>−2π</dt><dd>${fmt(-2 * Math.PI, 3)}</dd><dt>vertices</dt><dd>${CX.length}</dd>`;
  plot($("flowchart"), { xr: [0, Math.max(0.1, CA0 / (2 * Math.PI))], yr: [0, CA0 * 1.05], xlabel: "t", ylabel: "area", series: [{ pts: [[0, CA0], [CA0 / (2 * Math.PI), 0]], color: css("--soft"), dash: true, width: 1.5, label: "slope −2π" }, { pts: Chist, color: POSc(), label: "polygon" }] });
}
function flowRun() {
  if (Cframe) { cancelAnimationFrame(Cframe); Cframe = 0; $("flowplay").textContent = "Run"; return; }
  $("flowplay").textContent = "Pause";
  const tick = () => {
    for (let k = 0; k < (reduced ? 200 : 15); k++) { CX = LC.curveStep(CX, 2e-4); Ct += 2e-4; Csteps++; if (Csteps % 50 === 0) CX = LC.curveResample(CX); }
    Chist.push([Ct, LC.polyArea(CX)]); drawFlow();
    if (LC.polyArea(CX) > 0.08 * CA0) Cframe = requestAnimationFrame(tick); else { Cframe = 0; $("flowplay").textContent = "Run"; }
  };
  Cframe = requestAnimationFrame(tick);
}
inits.flows = () => { flowReset(); $("flowplay").onclick = flowRun; $("flowreset").onclick = () => { if (Cframe) flowRun(); flowReset(); }; $("flowsel").onchange = () => { if (Cframe) flowRun(); flowReset(); }; onSize($("flowcv"), drawFlow); };

// ===================== 10. Ollivier on manifolds =====================
function drawOll() {
  const K = +$("ollK").value; $("ollKv").textContent = `K = ${K}`;
  const emax = K === 0 ? 1.2 : Math.min(1.2, 0.9 * Math.PI / Math.sqrt(Math.abs(K)) / 2), pts = [];
  for (let i = 1; i <= 40; i++) { const e = emax * i / 40; pts.push([e, LC.ollivierBall(K, e, 80) / (e * e)]); }
  const yl = Math.max(0.05, Math.abs(K) / 8 * 1.6); plot($("ollcv"), { xr: [0, emax], yr: [-yl, yl], xlabel: "ε", ylabel: "κ / ε²", series: [{ pts: [[0, K / 8], [emax, K / 8]], color: css("--soft"), dash: true, width: 1.5, label: "K/8" }, { pts, color: K >= 0 ? POSc() : NEGc(), label: `K = ${K}` }] });
  const e0 = 0.05;
  $("ollread").innerHTML = `<dt>κ/ε² at ε = 0.05</dt><dd>${fmt(LC.ollivierBall(K, e0, 160) / (e0 * e0), 5)}</dd><dt>K/8</dt><dd>${fmt(K / 8, 5)}</dd><dt>κ/ε² at ε = ${fmt(emax, 2)}</dt><dd>${fmt(pts[pts.length - 1][1], 5)}</dd>`;
}
inits.ollivier = () => { drawOll(); $("ollK").oninput = drawOll; onSize($("ollcv"), drawOll); };

// ===================== 11. reference =====================
const FORMS = [
  ["Gauss curvature (Liouville)", "\\(K=-e^{-2u}\\Delta_0u\\)", "angle defect; resistance and Higuchi Gauss–Bonnet", "surfaces"],
  ["Mean curvature", "\\(\\Delta_gX=-2H\\mathbf n\\)", "cotangent Laplacian of positions", "mesh"],
  ["Curved mean value", "\\(M_rf=f+\\tfrac{r^2}4\\Delta f+r^4(\\tfrac{\\Delta^2f}{64}+\\tfrac{K\\Delta f}{96})+\\dots\\)", "Ollivier / Lin–Lu–Yau", "means"],
  ["Disc and ball volumes", "\\(\\mathrm{Vol}B_r=\\omega_nr^n(1-\\tfrac{Sr^2}{6(n+2)}+\\dots)\\)", "volume growth of graphs", "means"],
  ["Heat trace", "\\((4\\pi t)^{-n/2}(\\mathrm{Vol}+\\tfrac t6\\int S+\\dots)\\)", "graph heat kernels, Li–Yau (CDE)", "heat"],
  ["Bochner", "\\(\\tfrac12\\Delta|\\nabla f|^2=|\\mathrm{Hess}f|^2+\\langle\\nabla f,\\nabla\\Delta f\\rangle+\\mathrm{Ric}\\)", "Bakry–Émery \\(\\Gamma_2\\ge K\\Gamma\\)", "bochner"],
  ["Lichnerowicz", "\\(\\mathrm{Ric}\\ge(n-1)k\\Rightarrow\\lambda_1\\ge nk\\)", "\\(\\lambda_1\\ge\\kappa\\), \\(\\lambda_1\\ge K\\)", "graphs"],
  ["Laplacian comparison", "\\(\\Delta r\\le(n-1)\\sqrt k\\cot\\sqrt k r\\)", "Münch–Wojciechowski comparison", "bochner"],
  ["Weitzenböck", "\\(\\Delta_{\\mathrm{Hodge}}=\\nabla^*\\nabla+\\mathrm{Ric}\\)", "Forman curvature", "graphs"],
  ["Ricci flow (2-D)", "\\(\\partial_tu=e^{-2u}\\Delta_0u=-K\\)", "discrete Ricci flows on graphs", "ricci"],
  ["Mean-curvature flow", "\\(\\partial_tX=\\Delta X\\), \\(dA/dt=-2\\pi\\)", "cycle-graph Laplacian on a polygon", "flows"],
  ["Ollivier on manifolds", "\\(\\kappa\\approx\\varepsilon^2\\mathrm{Ric}/(2(n+2))\\)", "Lin–Lu–Yau on graphs", "ollivier"],
  ["Yamabe", "\\(\\tilde S=u^{-\\frac{n+2}{n-2}}(-\\tfrac{4(n-1)}{n-2}\\Delta u+Su)\\)", "—", "wolfram"],
  ["Point-cloud limit", "\\((\\text{mean}_t-f)/t\\to\\Delta f\\)", "Belkin–Niyogi", "wolfram"]
];
inits.forms = () => { $("formtable").querySelector("tbody").innerHTML = FORMS.map(r => `<tr><td>${r[0]}</td><td class="math">${r[1]}</td><td>${r[2]}</td><td><a href="#${r[3]}">${sections.find(s => s.id === r[3]).dataset.title}</a></td></tr>`).join(""); if (window.MathJax && MathJax.typesetPromise) MathJax.typesetPromise([$("formtable")]).catch(() => {}); };

// ===================== 12. quiz =====================
const QUIZ = [
  ["On the torus of revolution, where is the Gauss curvature negative?", ["on the inner half, facing the hole", "on the outer half", "nowhere: a torus is flat"], 0, "K = cos v/(r(R + r cos v)) is negative where cos v < 0, the inner half; its integral is 0 = 2πχ."],
  ["At which order in r does curvature first enter the geodesic-circle mean?", ["r²", "r⁴", "r⁶"], 1, "The r² term is Δf/4 in every geometry; K first appears as KΔf/96 at r⁴."],
  ["The heat-trace coefficient that hears curvature is", ["the leading Weyl term", "the t-term, (1/6)∫S", "the t²-term only"], 1, "Tr e^{tΔ} ~ (4πt)^{−n/2}(Vol + (t/6)∫S + …); for surfaces ∫S = 4πχ."],
  ["Bakry–Émery curvature on graphs copies which smooth identity?", ["Gauss–Bonnet", "the Bochner formula, Γ₂ ≥ KΓ", "Liouville's equation"], 1, "Γ₂(f) = |Hess f|² + Ric(∇f, ∇f) is Bochner's formula in Γ-calculus."],
  ["Why is Lin–Lu–Yau curvature negative on the dumbbell's bridge?", ["its endpoints share many neighbours", "the two neighbourhoods barely overlap, so mass must travel far", "bridges always have curvature −1"], 1, "Optimal transport between the two neighbourhood measures is expensive across a bottleneck."],
  ["What does resistance curvature always sum to on a connected graph?", ["0", "1", "the number of edges"], 1, "Foster's theorem Σ<sub>edges</sub> ω = n − 1 gives Σ p<sub>i</sub> = 1, a discrete Gauss–Bonnet theorem."],
  ["Under curve shortening, the enclosed area changes at rate", ["−2π, for every embedded curve", "−(perimeter)", "0"], 0, "dA/dt = −∮κ ds = −2π, independent of the curve."],
  ["Under 2-D Ricci flow in conformal form, ∂u/∂t equals", ["Δ₀u", "−K", "H"], 1, "∂u/∂t = e^{−2u}Δ₀u = −K: positive curvature shrinks, negative expands."]
];
let quizScore = {};
inits.quiz = () => {
  $("quizlist").innerHTML = QUIZ.map((q, i) => `<li><div>${q[0]}</div>${q[1].map((a, j) => `<button data-q="${i}" data-a="${j}">${a}</button>`).join("")}<div class="muted" id="qf${i}"></div></li>`).join("");
  $("quizlist").addEventListener("click", e => { const b = e.target.closest("button"); if (!b) return; const i = +b.dataset.q, j = +b.dataset.a, ok = j === QUIZ[i][2]; quizScore[i] = ok; $("qf" + i).innerHTML = `<span class="${ok ? "ok" : "no"}">${ok ? "Right." : "Not quite."}</span> ${QUIZ[i][3]}`; $("quizscore").textContent = `${Object.values(quizScore).filter(Boolean).length} of ${QUIZ.length} right so far.`; });
  $("quizscore").textContent = "Pick an answer to see the reasoning.";
};

// ===================== Wolfram cells =====================
const SNIP = {
  surfaces: `(* Gauss and mean curvature of an embedded surface, and Gauss–Bonnet on the torus *)
surfaceCurvatures[pos_, 𝓍_] := Module[{Xu, Xv, nn, E1, F1, G1, L1, M1, N1},
  Xu = D[pos, 𝓍[[1]]]; Xv = D[pos, 𝓍[[2]]]; nn = Cross[Xu, Xv]/Sqrt[Cross[Xu, Xv] . Cross[Xu, Xv]];
  {E1, F1, G1} = {Xu . Xu, Xu . Xv, Xv . Xv};
  {L1, M1, N1} = {D[pos, 𝓍[[1]], 𝓍[[1]]] . nn, D[pos, 𝓍[[1]], 𝓍[[2]]] . nn, D[pos, 𝓍[[2]], 𝓍[[2]]] . nn};
  <|"K" -> Simplify[(L1 N1 - M1^2)/(E1 G1 - F1^2)], "H" -> Simplify[(E1 N1 - 2 F1 M1 + G1 L1)/(2 (E1 G1 - F1^2))], "dA" -> Simplify[Sqrt[E1 G1 - F1^2]]|>];
t = surfaceCurvatures[{(2 + Cos[v]) Cos[u], (2 + Cos[v]) Sin[u], Sin[v]}, {u, v}];
{t["K"], Integrate[Simplify[t["K"] t["dA"], 0 < v < 2 π], {u, 0, 2 π}, {v, 0, 2 π}]}`,
  ricci: `(* Liouville form of Gauss curvature, and the shrinking sphere under Ricci flow *)
Kconformal[w_] := Simplify[-Exp[-2 w] (D[w, {x, 2}] + D[w, {y, 2}])];
{Kconformal[Log[2/(1 + x^2 + y^2)]], Kconformal[Log[1/y]], Simplify[D[(1 - 2 t) {{1, 0}, {0, Sin[θ]^2}}, t] + 2 {{1, 0}, {0, Sin[θ]^2}}]}`,
  means: `(* circle mean on S² of f = e^x(1+z)^2 + y z^3, exact to r^6 *)
F0[{x_, y_, z_}] := Exp[x] (1 + z)^2 + y z^3;
ext = F0[{x, y, z}/Sqrt[x^2 + y^2 + z^2]];
ΔS2amb[h_] := Simplify[(x^2 + y^2 + z^2) Laplacian[h, {x, y, z}]];
L1 = ΔS2amb[ext]; L2 = ΔS2amb[L1]; L3 = ΔS2amb[L2]; atPole[h_] := h /. {x -> 0, y -> 0, z -> 1};
circleMean = Integrate[Normal@Series[F0[{Sin[r] Cos[φ], Sin[r] Sin[φ], Cos[r]}], {r, 0, 6}], {φ, 0, 2 π}]/(2 π);
formula = atPole[ext] + r^2/4 atPole[L1] + r^4 (atPole[L2]/64 + atPole[L1]/96) + r^6 (atPole[L3]/2304 + atPole[L2]/1152 + atPole[L1]/1440);
{atPole /@ {ext, L1, L2, L3}, Simplify[Expand[circleMean - formula]]}`,
  heat: `(* heat trace of the unit sphere against 1 + t/3 + t^2/15 *)
heatTrace[t_?NumericQ] := Sum[(2 j + 1) Exp[-j (j + 1) t], {j, 0, 2000}];
Table[{t, t heatTrace[t], 1 + t/3 + t^2/15}, {t, {0.1, 0.03, 0.01}}]`,
  bochner: `(* Bochner formula on S² for an arbitrary function *)
X = {θ, φ}; g = {{1, 0}, {0, Sin[θ]^2}}; gi = Inverse[g];
Γ = Table[1/2 Sum[gi[[i, l]] (D[g[[l, j]], X[[k]]] + D[g[[l, k]], X[[j]]] - D[g[[j, k]], X[[l]]]), {l, 2}], {i, 2}, {j, 2}, {k, 2}];
Lap[w_] := 1/Sqrt[Det[g]] Sum[D[Sqrt[Det[g]] gi[[i, j]] D[w, X[[j]]], X[[i]]], {i, 2}, {j, 2}];
g2[w_] := Sum[gi[[i, j]] D[w, X[[i]]] D[w, X[[j]]], {i, 2}, {j, 2}];
Hs[w_] := Table[D[w, X[[i]], X[[j]]] - Sum[Γ[[k, i, j]] D[w, X[[k]]], {k, 2}], {i, 2}, {j, 2}];
f = 𝒻[θ, φ];
Simplify[1/2 Lap[g2[f]] - (Tr[gi . Hs[f] . gi . Hs[f]] + Sum[gi[[i, j]] D[f, X[[i]]] D[Lap[f], X[[j]]], {i, 2}, {j, 2}] + g2[f])]`,
  mesh: `(* angle defect on a torus mesh: total is exactly 0 = 2πχ *)
torusPos = {(2 + Cos[v]) Cos[u], (2 + Cos[v]) Sin[u], Sin[v]}; {nu, nv} = {40, 20};
idx[i_, j_] := Mod[i, nu] nv + Mod[j, nv] + 1;
P = Flatten[Table[N[torusPos /. {u -> 2 π i/nu, v -> 2 π j/nv}], {i, 0, nu - 1}, {j, 0, nv - 1}], 1];
T = Flatten[Table[{{idx[i, j], idx[i + 1, j], idx[i + 1, j + 1]}, {idx[i, j], idx[i + 1, j + 1], idx[i, j + 1]}}, {i, 0, nu - 1}, {j, 0, nv - 1}], 2];
ang[i_, j_, k_] := VectorAngle[P[[j]] - P[[i]], P[[k]] - P[[i]]];
defect = ConstantArray[2. π, Length[P]];
Do[{a, b, c} = tr; defect[[a]] -= ang[a, b, c]; defect[[b]] -= ang[b, c, a]; defect[[c]] -= ang[c, a, b], {tr, T}];
Chop[Total[defect], 10^-9]`,
  graphs: `(* Lin–Lu–Yau curvature (Münch–Wojciechowski LP) and the spectral gap *)
nbr[G_, v_] := AdjacencyList[G, v]; Δg[G_, f_][v_] := Mean[f /@ nbr[G, v]] - f[v];
κLLY[G_, {x_, y_}] := Module[{S, vars, f, cons}, S = Union[{x, y}, nbr[G, x], nbr[G, y]];
  vars = Table[Unique["f"], {Length[S]}]; f = AssociationThread[S -> vars];
  cons = Flatten[{f[y] - f[x] == 1, f[x] == 0, Table[With[{d = GraphDistance[G, S[[i]], S[[j]]]}, {f[S[[i]]] - f[S[[j]]] <= d, f[S[[j]]] - f[S[[i]]] <= d}], {i, Length[S]}, {j, i + 1, Length[S]}]}];
  LinearOptimization[Δg[G, f][x] - Δg[G, f][y], cons, vars, "PrimalMinimumValue"]];
G = HypercubeGraph[3]; A = N@AdjacencyMatrix[G]; d = Total[A];
{Union[κLLY[G, #] & /@ (List @@@ EdgeList[G])], Sort[Eigenvalues[IdentityMatrix[8] - DiagonalMatrix[d^(-1/2)] . A . DiagonalMatrix[d^(-1/2)]]][[2]]}`,
  flows: `(* exact flows: Ricci flow on the round sphere, mean-curvature flow of a sphere *)
{Simplify[D[Sqrt[R0^2 - 4 t], t] + 2/Sqrt[R0^2 - 4 t]], Simplify[D[(1 - 2 t) {{1, 0}, {0, Sin[θ]^2}}, t] + 2 {{1, 0}, {0, Sin[θ]^2}}]}`,
  ollivier: `(* Ollivier curvature of ε-balls: κ/ε² → K/8 on S² and H² *)
κS2[ε_?NumericQ] := NIntegrate[With[{s = Sin[ρ] Sin[α]}, s^2/(1 + Sqrt[1 - s^2])] Sin[ρ], {ρ, 0, ε}, {α, 0, 2 π}]/(2 π (1 - Cos[ε]));
κH2[ε_?NumericQ] := -NIntegrate[With[{s = Sinh[ρ] Sin[α]}, s^2/(1 + Sqrt[1 + s^2])] Sinh[ρ], {ρ, 0, ε}, {α, 0, 2 π}]/(2 π (Cosh[ε] - 1));
Table[{ε, κS2[ε]/ε^2, κH2[ε]/ε^2}, {ε, {0.05, 0.2, 0.8}}]`,
  yamabe: `(* Yamabe: u^4 times the flat metric of R^3 is the round S^3, scalar curvature 6 *)
uY = (2/(1 + x^2 + y^2 + z^2))^(1/2); Simplify[-8 uY^-5 Laplacian[uY, {x, y, z}]]`,
  weitzenbock: `(* Weitzenböck on S²: Hodge Laplacian ω − ∇*∇ω = Ric(ω) = ω for every 1-form df + ⋆dh *)
X = {θ, φ}; g = {{1, 0}, {0, Sin[θ]^2}}; gi = Inverse[g];
Γ = Table[1/2 Sum[gi[[i, l]] (D[g[[l, j]], X[[k]]] + D[g[[l, k]], X[[j]]] - D[g[[j, k]], X[[l]]]), {l, 2}], {i, 2}, {j, 2}, {k, 2}];
Lap[w_] := 1/Sin[θ] (D[Sin[θ] D[w, θ], θ] + D[w, φ, φ]/Sin[θ]);
rough[ω_] := Module[{T, TT}, T = Table[D[ω[[i]], X[[j]]] - Sum[Γ[[k, i, j]] ω[[k]], {k, 2}], {i, 2}, {j, 2}];
  TT = Table[D[T[[i, j]], X[[k]]] - Sum[Γ[[m, k, i]] T[[m, j]] + Γ[[m, k, j]] T[[i, m]], {m, 2}], {i, 2}, {j, 2}, {k, 2}];
  Table[-Sum[gi[[j, k]] TT[[i, j, k]], {j, 2}, {k, 2}], {i, 2}]];
d1[w_] := {D[w, θ], D[w, φ]}; star[{a_, b_}] := {-b/Sin[θ], a Sin[θ]};
ω = d1[𝒻[θ, φ]] + star[d1[𝒽[θ, φ]]];
Simplify[d1[-Lap[𝒻[θ, φ]]] + star[d1[-Lap[𝒽[θ, φ]]]] - (rough[ω] + ω)]`
};
const SNIPNAMES = { surfaces: "Gauss and mean curvature", ricci: "Liouville and Ricci flow", means: "curved mean value", heat: "heat trace", bochner: "Bochner on S²", weitzenbock: "Weitzenböck on S²", mesh: "torus mesh defect", graphs: "Lin–Lu–Yau and λ₁", flows: "exact flows", ollivier: "Ollivier on S² and H²", yamabe: "Yamabe" };
let MCP = null, SAMPLE = null, capsChecked = false;
const STANDALONE = !!window.LAB_STANDALONE, CFG = window.LAPLACIAN_LAB_CONFIG || {};
let WL_KEY = "", kernelOK = false, chatReady = false;
const b64enc = s => { const b = new TextEncoder().encode(s); let t = ""; for (let i = 0; i < b.length; i += 0x8000) t += String.fromCharCode.apply(null, b.subarray(i, i + 0x8000)); return btoa(t); };
const b64dec = s => { const t = atob(s), b = new Uint8Array(t.length); for (let i = 0; i < t.length; i++) b[i] = t.charCodeAt(i); return new TextDecoder().decode(b); };
async function kernelPost(params) {
  if (!CFG.WOLFRAM_URL) throw { code: "no_url", message: "Set WOLFRAM_URL in the settings block at the top of this file." };
  if (!WL_KEY) throw { code: "no_key", message: "Enter your CCN-KEY and press Connect (Wolfram Language section)." };
  let res;
  try { res = await fetch(CFG.WOLFRAM_URL, { method: "POST", body: new URLSearchParams({ key: WL_KEY, ...params }) }); }
  catch (e) { throw { code: "network", message: "Could not reach CCN's Wolfram Cloud kernel." }; }
  let j = null; try { j = await res.json(); } catch (e) {}
  if (!j || (j.Success === false) || (!res.ok && !j.error)) throw { code: "rejected", message: "The kernel refused the request. Check the CCN-KEY." };
  return j;
}
const capStatus = () => ($("status").textContent = STANDALONE ? (kernelOK ? `CCN Cloud connected${chatReady ? " · TA ready" : " · TA unavailable (no chat key on the kernel)"}` : "Not connected: enter your CCN-KEY in the Wolfram Language section") : MCP ? "Wolfram kernel connected" : capsChecked ? "Wolfram cells need the Wolfram connector (open this page in Claude)" : "");
if (STANDALONE) { capsChecked = true; setTimeout(capStatus, 0); }
else if (window.claude && claude.use) {
  claude.use("mcp").then(m => { MCP = m; capsChecked = true; capStatus(); }).catch(() => { capsChecked = true; capStatus(); });
  claude.use("sample").then(s => { SAMPLE = s; $("askstate").textContent = s ? "" : "The TA needs this page to be open in Claude."; }).catch(() => {});
} else { capsChecked = true; setTimeout(() => { capStatus(); $("askstate").textContent = "The TA needs this page to be open in Claude."; }, 0); }
function wlError(e) {
  const c = e && e.code;
  if (c === "no_url" || c === "no_key" || c === "network" || c === "rejected") return e.message;
  if (c === "server_not_connected") return "Add the Wolfram connector in claude.ai Settings → Connectors, then run again.";
  if (c === "needs_reauth") return "Reconnect Wolfram in claude.ai Settings → Connectors.";
  if (c === "not_in_manifest") return "Wolfram is turned off for this page in this view.";
  if (c === "selection_required") return "Choose which Wolfram connector to use when claude.ai asks, then run again.";
  if (c === "tool_error") return "The kernel reported an error: " + (e.message || "");
  if (c === "server_unavailable") return "The Wolfram service did not answer in time. Run again in a moment.";
  return "The Wolfram call failed (" + (c || "unknown") + "): " + (e && e.message || "");
}
async function runWolfram(code) {
  if (STANDALONE) {
    const j = await kernelPost({ code_b64: b64enc(code), mode: "wolfram" });
    const text = j.text_b64 ? b64dec(j.text_b64) : (j.text || "");
    return { text, imgs: j.image ? [`data:image/png;base64,${j.image}`] : [] };
  }
  if (!MCP) throw { code: "not_granted", message: "No Wolfram connector in this view." };
  const r = await MCP.callTool("Wolfram", "WolframLanguageEvaluator", { code }, { cache: false });
  const text = [], imgs = [];
  (r.content || []).forEach(b => { if (b.type === "text") text.push(b.text); else if (b.type === "image") imgs.push(`data:${b.mimeType};base64,${b.data}`); });
  if (!text.length && typeof r.payload === "string") text.push(r.payload);
  return { text: text.join("\n").replace(/Symbol::undefined2:[^\n]*\n?/g, "").replace(/General::messages:[^\n]*\n?/g, ""), imgs };
}
function mountCell(el, key) {
  el.classList.add("card"); el.style.marginTop = "18px";
  el.innerHTML = `<h3>Wolfram Language${SNIPNAMES[key] ? " · " + SNIPNAMES[key] : ""}</h3><textarea spellcheck="false" aria-label="Wolfram Language code"></textarea><div class="controls"><button class="primary">Evaluate</button><button>Copy</button><button>Ask the TA about this</button><span class="muted"></span></div><div class="out"></div>`;
  const ta = el.querySelector("textarea"), [run, copy, ask] = el.querySelectorAll("button"), st = el.querySelector(".muted"), out = el.querySelector(".out");
  ta.value = SNIP[key] || SNIP.surfaces;
  run.onclick = async () => {
    st.textContent = "Evaluating…"; run.disabled = true; out.innerHTML = "";
    try { const r = await runWolfram(ta.value); out.innerHTML = `<pre></pre>${r.imgs.map(s => `<img alt="Wolfram output" src="${s}">`).join("")}`; out.querySelector("pre").textContent = r.text || "(no text output)"; st.textContent = ""; }
    catch (e) { st.textContent = wlError(e); }
    run.disabled = false;
  };
  copy.onclick = () => navigator.clipboard?.writeText(ta.value).then(() => (st.textContent = "Copied."), () => (st.textContent = "Copy is blocked here; select the code instead."));
  ask.onclick = () => { askContext = `The student is looking at this Wolfram cell (${SNIPNAMES[key] || key}):\n${ta.value}\nOutput shown: ${out.textContent.slice(0, 1500)}`; location.hash = "ask"; $("askq").focus(); };
  return ta;
}
document.querySelectorAll(".wl").forEach(el => { const ta = mountCell(el, el.dataset.key); if (el.dataset.key === "free") { $("wlsnip").innerHTML = Object.keys(SNIP).map(k => `<option value="${k}">${SNIPNAMES[k]}</option>`).join(""); $("wlsnip").onchange = e => (ta.value = SNIP[e.target.value]); } });

// ===================== Ask the TA =====================
let askContext = "", history = [];
const BRIEF = `You are the teaching assistant of the Laplacian Curvature Lab (Computational Classnotes). Explain clearly and precisely, at the level of a strong undergraduate or graduate student, using the lab's conventions: Δ = div grad (negative semidefinite); on graphs Δf(x) = mean of f over neighbours − f(x); λ are eigenvalues of the normalised Laplacian.
Facts verified in the companion notebook (github.com/lossofgenerality/laplacian):
- K = −e^{−2u}Δ₀u (Liouville); ΔX = −2H n; torus R=2,r=1: K = cos v/(2+cos v), H = (1+cos v)/(2+cos v), ∬K dA = 0; sphere ∬K dA = 4π.
- Constant-curvature circle mean M_r f = f + r²Δf/4 + r⁴(Δ²f/64 + KΔf/96) + r⁶(Δ³f/2304 + KΔ²f/1152 + K²Δf/1440); error slopes of flat / +K term / +r⁶ terms are 4, 6, 8. A(r)/πr² = 1 − Kr²/12 + K²r⁴/360.
- Heat trace of S²: t·Tr e^{tΔ} = 1 + t/3 + t²/15 + …; flat torus of equal area stays at 1.
- Bochner verified on S² and on the torus; Lichnerowicz λ₁ ≥ nk with equality on S² (λ₁ = 2); Δr = cot r, 1/r, coth r.
- Cotangent Laplacian; angle defect sums to 2πχ exactly.
- Graphs (min over edges/vertices): K5 κ_LLY 5/4, κ₀ 3/4, K_BE 7/8, λ₁ 5/4; Q3 2/3, 0, 2/3, λ₁ 2/3; Petersen 0, −1/3, −1/3, λ₁ 2/3; C6 all 0, λ₁ 1/2; binary tree interior edges −2/3, leaf edges +2/3; dumbbell bridge −3/5. Resistance curvature p<sub>i</sub> = 1 − ½Σω<sub>ij</sub> sums to 1 (Foster). On trees resistance and Steinerberger curvature are proportional.
- λ₁ ≥ κ_LLY, λ₁ ≥ K_BE, λ_max ≤ 2 − κ₀ hold on all test graphs.
- Weitzenböck Δ_Hodge = ∇*∇ + Ric verified on S²; 2-D Ricci flow ∂u/∂t = e^{−2u}Δ₀u = −K; curve shortening dA/dt = −2π; Ollivier on ε-balls κ → ε²K/8 = ε²Ric/(2(n+2)); Yamabe in R³ S̃ = −8u^{−5}Δu, u = (2/(1+r²))^{1/2} gives S̃ = 6.
Use the run_wolfram tool when a computation would settle a question; the kernel is stateless, so send complete code. Keep answers focused; use plain text with simple notation (no LaTeX delimiters). If something is not established, say so.`;
const TOOLS = [{ name: "run_wolfram", description: "Evaluate Wolfram Language code on a stateless Wolfram kernel and return the text output.", inputSchema: { type: "object", properties: { code: { type: "string", description: "Complete Wolfram Language code" } }, required: ["code"] },
  execute: async ({ code }) => { const r = await runWolfram(code); lastCode.push(code); return (r.text || "(no text output)").slice(0, 4000); } }];
let lastCode = [];
function addMsg(role, text, codes) {
  const d = document.createElement("div"); d.className = "msg " + role; d.textContent = text;
  (codes || []).forEach(c => { const det = document.createElement("details"); det.innerHTML = "<summary>Wolfram code the TA ran</summary><pre></pre>"; det.querySelector("pre").textContent = c; d.appendChild(det); });
  $("chat").appendChild(d); $("chat").scrollTop = $("chat").scrollHeight; return d;
}
const RUN_NOTE = `\nTo run Wolfram Language, reply with only <run_wolfram>complete code</run_wolfram> and nothing else; the page runs it on the kernel and sends you the output, then you answer. Use it at most twice per question.`;
async function askStandalone(q, d, ctx) {
  if (!kernelOK) { d.textContent = "Connect with your CCN-KEY first (Wolfram Language section)."; return; }
  if (!chatReady) { d.textContent = "The kernel has no chat key stored, so the TA is unavailable. Store one with CloudPut on your Wolfram Cloud."; return; }
  const msgs = history.slice(-8).concat([{ role: "user", content: `${ctx}\n\nQuestion: ${q}` }]), codes = [];
  for (let round = 0; round < 3; round++) {
    const payload = { model: CFG.MODEL || undefined, max_tokens: 1500, system: BRIEF + RUN_NOTE, messages: msgs };
    const j = await kernelPost({ mode: "chat", payload_b64: b64enc(JSON.stringify(payload)) });
    if (j.error) { d.textContent = "The TA could not answer: " + j.error + (j.status ? ` (status ${j.status})` : ""); return; }
    const text = b64dec(j.text_b64 || ""), m = text.match(/<run_wolfram>([\s\S]*?)<\/run_wolfram>/);
    if (m && round < 2) {
      d.textContent = "Running Wolfram code…"; codes.push(m[1].trim());
      let out; try { const r = await runWolfram(m[1].trim()); out = (r.text || "(no text output)").slice(0, 4000); } catch (e) { out = "Error: " + wlError(e); }
      msgs.push({ role: "assistant", content: text }, { role: "user", content: "Wolfram output:\n" + out + "\nNow answer the question." });
      continue;
    }
    d.textContent = text.replace(/<run_wolfram>[\s\S]*?<\/run_wolfram>/g, "").trim();
    codes.forEach(c => { const det = document.createElement("details"); det.innerHTML = "<summary>Wolfram code the TA ran</summary><pre></pre>"; det.querySelector("pre").textContent = c; d.appendChild(det); });
    history.push({ role: "user", content: q }, { role: "assistant", content: d.firstChild ? d.firstChild.textContent : text });
    return;
  }
}
async function ask() {
  const q = $("askq").value.trim(); if (!q) return;
  if (STANDALONE) {
    $("askq").value = ""; addMsg("user", q); const d = addMsg("ta", "Thinking…");
    const state = window.__labState ? `Current graph bench state: ${JSON.stringify(window.__labState)}.` : "";
    $("asksend").disabled = true;
    try { await askStandalone(q, d, `Bench the student came from: ${$("askctx").dataset.from || "none"}. ${state}\n${askContext}`); }
    catch (e) { d.textContent = wlError(e); }
    $("asksend").disabled = false; askContext = ""; return;
  }
  if (!SAMPLE) { $("askstate").textContent = "The TA needs this page to be open in Claude."; return; }
  $("askq").value = ""; addMsg("user", q); const d = addMsg("ta", "Thinking…"); lastCode = [];
  const state = window.__labState ? `Current graph bench state: ${JSON.stringify(window.__labState)}.` : "";
  const ctx = `Bench the student came from: ${$("askctx").dataset.from || "none"}. ${state}\n${askContext}`;
  history.push({ role: "user", content: `${BRIEF}\n\n${ctx}\n\nQuestion: ${q}` });
  $("asksend").disabled = true;
  try {
    const r = await SAMPLE(history.slice(-8), { tools: MCP ? TOOLS : undefined, cache: false, onText: ({ text }) => (d.textContent = text) });
    d.textContent = r.text; lastCode.forEach(c => { const det = document.createElement("details"); det.innerHTML = "<summary>Wolfram code the TA ran</summary><pre></pre>"; det.querySelector("pre").textContent = c; d.appendChild(det); });
    history[history.length - 1].content = q; history.push({ role: "assistant", content: r.text });
  } catch (e) { d.textContent = e && e.code === "not_granted" ? "The TA is not available in this view." : e && e.code === "rate_limited" ? "Too many questions at once; wait a moment." : "The TA could not answer: " + (e && e.message || "unknown error"); history.pop(); }
  $("asksend").disabled = false; askContext = "";
}
let lastBench = "map";
addEventListener("hashchange", () => { const id = location.hash.slice(1); if (id === "ask") { $("askctx").dataset.from = lastBench; $("askctx").textContent = `Asking from: ${sections.find(s => s.id === lastBench)?.dataset.title || "the lab"}.`; } else if (sections.some(s => s.id === id)) lastBench = id; });
$("asksend").onclick = ask; $("askq").addEventListener("keydown", e => { if (e.key === "Enter" && (e.metaKey || e.ctrlKey)) ask(); });

// ===================== standalone: CCN-KEY =====================
if (STANDALONE) {
  const card = document.createElement("div"); card.className = "card"; card.style.margin = "16px 0";
  card.innerHTML = `<h3>Connect to CCN Cloud</h3><p class="muted">Wolfram cells and the TA run on CCN's Wolfram Cloud kernel. Enter your CCN-KEY and press Connect.</p>
   <div class="controls"><label for="wl-key">CCN-KEY</label><input id="wl-key" type="password" autocomplete="off" spellcheck="false" style="min-height:40px;padding:6px 10px;font:inherit;font-size:16px;border:1px solid var(--line);border-radius:8px;background:var(--panel);color:var(--ink);width:min(100%,320px)">
   <button class="primary" id="wl-connect">Connect</button><label><input type="checkbox" id="wl-remember"> Remember on this device</label><span class="muted" id="wl-state"></span></div>`;
  const wsec = $("wolfram"); wsec.insertBefore(card, wsec.querySelector(".controls"));
  try { const k = localStorage.getItem("ccn-key"); if (k) { $("wl-key").value = k; $("wl-remember").checked = true; } } catch (e) {}
  const connect = async () => {
    WL_KEY = $("wl-key").value.trim(); $("wl-state").textContent = "Connecting…";
    try {
      const j = await kernelPost({ code_b64: b64enc("$VersionNumber"), mode: "wolfram" });
      kernelOK = true; chatReady = j.chat_ready === true || j.chat_ready === "True";
      $("wl-state").textContent = `Connected · Wolfram ${j.text_b64 ? b64dec(j.text_b64) : j.text}${chatReady ? " · TA ready" : " · no chat key on the kernel"}`;
      try { if ($("wl-remember").checked) localStorage.setItem("ccn-key", WL_KEY); else localStorage.removeItem("ccn-key"); } catch (e) {}
    } catch (e) { kernelOK = false; chatReady = false; $("wl-state").textContent = wlError(e); }
    capStatus(); $("askstate").textContent = kernelOK ? (chatReady ? "" : "The kernel has no chat key stored.") : "Connect with your CCN-KEY (Wolfram Language section).";
  };
  $("wl-connect").onclick = connect; $("wl-key").addEventListener("keydown", e => { if (e.key === "Enter") connect(); });
  $("askstate").textContent = "Connect with your CCN-KEY (Wolfram Language section).";
  $("status").style.cursor = "pointer"; $("status").onclick = () => (location.hash = "wolfram");
  if ($("wl-key").value) setTimeout(connect, 0);
}

// ===================== write-ups and notebooks (Curvature from the Laplacian series) =====================
const SERIES_BASE = "https://lossofgenerality.github.io/laplacian/";
const SERIES_REPO = "https://github.com/lossofgenerality/laplacian/blob/main/";
const READ = {
  ollivier: [["07-ollivier", "07-Ollivier", "Ollivier Curvature"]],
  graphs: [["07-ollivier", "07-Ollivier", "Ollivier and Lin–Lu–Yau curvature"]],
};
for (const [id, items] of Object.entries(READ)) {
  const sec = document.getElementById(id); if (!sec) continue;
  const box = document.createElement("div"); box.className = "readmore";
  box.innerHTML = items.map(([doc, nb, title]) => `<span class="rm-title">${title}</span>` +
    `<a href="${SERIES_BASE}docs/series/${doc}.html" target="_blank" rel="noopener">Read the write-up</a>` +
    `<a href="${SERIES_BASE}docs/series/${doc}.pdf" target="_blank" rel="noopener">PDF</a>` +
    `<a href="${SERIES_BASE}notebooks/series/${nb}.nb" download>Open the notebook (.nb)</a>`).join("<br>");
  const lede = sec.querySelector(".lede"); (lede || sec.querySelector("h2")).after(box);
}

// ===================== start =====================
show(location.hash.slice(1) || "map");
addEventListener("load", () => requestAnimationFrame(() => window.scrollTo(0, 0)));
}
