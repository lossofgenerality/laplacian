// Dump every readout the Laplacian Curvature Lab page shows, computed by lab/core.js exactly as lab/app.js does.
// node tools/lab_nb/js_readouts.js > tools/lab_nb/lab_readouts.json
const LC = require('../../lab/core.js');
const out = {};
// surfaces (app.js surfData: 57 x 37 grid, h = 1e-3; total on 160 x 160)
out.surfaces = {};
for (const key of Object.keys(LC.SURFACES)) {
  const S = LC.SURFACES[key], nu = 56, nv = 36; let kmin = Infinity, kmax = -Infinity, hmax = 0;
  for (let i = 0; i <= nu; i++) for (let j = 0; j <= nv; j++) { const q = LC.surfaceKH(S.X, S.U[0] + (S.U[1] - S.U[0]) * i / nu, S.V[0] + (S.V[1] - S.V[0]) * j / nv, 1e-3); kmin = Math.min(kmin, q.K); kmax = Math.max(kmax, q.K); hmax = Math.max(hmax, Math.abs(q.H)); }
  out.surfaces[key] = { kmin, kmax, hmax, total: LC.totalCurvature(S, 160, 160) };
}
// Ricci flow, default bump 0.3 (b = 0.83 a), run to t >= 2
{ const a = 0.3; const S = LC.ricciInit(32, a, a * 0.83); const mk = s => Math.max(...LC.ricciK(s).flat().map(Math.abs));
  const K0 = mk(S); while (S.t < 2) LC.ricciStep(S, 1); const st0 = LC.ricciStats(LC.ricciInit(32, a, a * 0.83)), st1 = LC.ricciStats(S); out.ricci = { a, b: a * 0.83, N: 32, maxK0: K0, t: S.t, maxK: mk(S), totalK: LC.ricciTotalK(S), start: st0, end: st1 }; }
{ const r1 = LC.reactionDiffusion(1), r0 = LC.reactionDiffusion(0); out.rd = { blowT: r1[r1.length - 1][0], blowMax: r1[r1.length - 1][1], heatEnd: r0[r0.length - 1][1] }; }
// curved means: slopes fitted on 0.04 < r < 0.16
{ const rs = []; for (let k = 4; k <= 24; k++) rs.push(2 ** (-k / 4));
  const e = rs.map(r => { const ex = LC.circleMean(r); return [r, Math.abs(ex - LC.approx.flat(r)), Math.abs(ex - LC.approx.curved4(r)), Math.abs(ex - LC.approx.curved6(r))]; });
  const slope = k => { const p = e.filter(r => r[0] > 0.04 && r[0] < 0.16).map(r => [Math.log(r[0]), Math.log(r[k])]), n = p.length, sx = p.reduce((a, q) => a + q[0], 0), sy = p.reduce((a, q) => a + q[1], 0), sxx = p.reduce((a, q) => a + q[0] * q[0], 0), sxy = p.reduce((a, q) => a + q[0] * q[1], 0); return (n * sxy - sx * sy) / (n * sxx - sx * sx); };
  out.means = { slopes: [slope(1), slope(2), slope(3)], pole: LC.POLE }; }
// heat at the default t = 0.05 and at 0.01, 0.1
out.heat = [0.01, 0.05, 0.1].map(t => ({ t, sphere: t * LC.sphereTrace(t), series: 1 + t / 3 + t * t / 15, torus: t * LC.torusTrace(t) }));
// mesh at the four resolutions
out.mesh = [[12, 6], [24, 12], [40, 20], [64, 32]].map(([nu, nv]) => { const M = LC.torusMesh(nu, nv), C = LC.meshCurvature(M); const tot = C.defect.reduce((a, b) => a + b, 0); let err = 0;
  for (let i = 0; i < nu; i++) for (let j = 0; j < nv; j++) { const v = 2 * Math.PI * j / nv; err = Math.max(err, Math.abs(C.K[i * nv + j] - Math.cos(v) / (2 + Math.cos(v)))); }
  return { nu, nv, vertices: M.P.length, defect: tot, err, Kouter: C.K[0] }; });
// graphs: every curvature on every graph
const KF = { lly: [1, (G, a, b) => LC.kappaLLY(G, a, b)], k0: [1, (G, a, b) => LC.kappa0(G, a, b)], be: [0, (G, v) => LC.bakryEmery(G, v)], forman: [1, LC.forman], formanAug: [1, LC.formanAug], res: [2, G => LC.resistanceCurv(G)], stein: [2, G => LC.steinerberger(G)] };
out.graphs = {};
for (const g of ['tree', 'cycle', 'cube', 'complete', 'petersen', 'grid', 'dumbbell']) {
  const G = LC.GRAPHS[g](), sp = LC.normLapSpectrum(G), row = { n: G.n, edges: G.edges.map(([a, b]) => [a + 1, b + 1]), lambda1: sp[1], lambdaMax: sp[sp.length - 1] };
  for (const [k, [kind, f]] of Object.entries(KF)) { const v = kind === 1 ? G.edges.map(([a, b]) => f(G, a, b)) : kind === 0 ? [...Array(G.n).keys()].map(x => f(G, x)) : f(G); row[k] = v; }
  out.graphs[g] = row;
}
// curve shortening: run as the page does (adaptive stable steps, LC.curveFlow) until area < 0.08 A0
out.flows = {};
for (const kind of ['wiggle', 'star', 'bean', 'ellipse']) { const X0 = LC.curveInit(kind), A0 = LC.polyArea(X0); let S = { X: X0, t: 0, L0: LC.perimeter(X0) };
  while (LC.polyArea(S.X) > 0.08 * A0) S = LC.curveFlow(S, 15 * 2e-4);
  out.flows[kind] = { A0, t: S.t, A: LC.polyArea(S.X), rate: (LC.polyArea(S.X) - A0) / S.t, vertices: S.X.length }; }
// Ollivier balls
out.ollivier = [-2, -1, 0, 1, 2].map(K => { const emax = K === 0 ? 1.2 : Math.min(1.2, 0.9 * Math.PI / Math.sqrt(Math.abs(K)) / 2);
  return { K, at005: LC.ollivierBall(K, 0.05, 160) / 0.0025, emax, atmax: LC.ollivierBall(K, emax, 80) / (emax * emax) }; });
console.log(JSON.stringify(out));
