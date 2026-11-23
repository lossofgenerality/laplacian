// Laplacian Curvature Lab — computational core (no DOM).
// © 2026 Computational Classnotes · CC BY-NC-SA 4.0
const LC = (() => {
  const PI = Math.PI;

  // ---------- linear algebra ----------
  function jacobiEig(Ain) { // symmetric matrix -> {values, vectors (columns)}
    const n = Ain.length, A = Ain.map(r => r.slice()), V = A.map((r, i) => r.map((_, j) => (i === j ? 1 : 0)));
    for (let sweep = 0; sweep < 100; sweep++) {
      let off = 0;
      for (let p = 0; p < n; p++) for (let q = p + 1; q < n; q++) off += A[p][q] * A[p][q];
      if (off < 1e-22) break;
      for (let p = 0; p < n; p++) for (let q = p + 1; q < n; q++) {
        if (Math.abs(A[p][q]) < 1e-300) continue;
        const th = (A[q][q] - A[p][p]) / (2 * A[p][q]);
        const t = Math.sign(th || 1) / (Math.abs(th) + Math.sqrt(th * th + 1));
        const c = 1 / Math.sqrt(t * t + 1), s = t * c;
        for (let k = 0; k < n; k++) { const akp = A[k][p], akq = A[k][q]; A[k][p] = c * akp - s * akq; A[k][q] = s * akp + c * akq; }
        for (let k = 0; k < n; k++) { const apk = A[p][k], aqk = A[q][k]; A[p][k] = c * apk - s * aqk; A[q][k] = s * apk + c * aqk; }
        for (let k = 0; k < n; k++) { const vkp = V[k][p], vkq = V[k][q]; V[k][p] = c * vkp - s * vkq; V[k][q] = s * vkp + c * vkq; }
      }
    }
    return { values: A.map((r, i) => r[i]), vectors: V };
  }
  const minEig = M => Math.min(...jacobiEig(M).values);
  function pinvSym(M, tol = 1e-9) {
    const { values, vectors } = jacobiEig(M), n = M.length, P = M.map(r => r.map(() => 0));
    values.forEach((l, k) => { if (Math.abs(l) > tol) for (let i = 0; i < n; i++) for (let j = 0; j < n; j++) P[i][j] += vectors[i][k] * vectors[j][k] / l; });
    return P;
  }

  // ---------- graphs ----------
  function makeGraph(n, edges, pos) {
    const adj = Array.from({ length: n }, () => []);
    edges.forEach(([a, b]) => { adj[a].push(b); adj[b].push(a); });
    const dist = adj.map((_, s) => { const d = Array(n).fill(Infinity); d[s] = 0; const q = [s]; while (q.length) { const v = q.shift(); for (const w of adj[v]) if (d[w] === Infinity) { d[w] = d[v] + 1; q.push(w); } } return d; });
    return { n, edges, adj, dist, pos };
  }
  const ring = (k, r = 1, ph = -PI / 2, cx = 0, cy = 0) => Array.from({ length: k }, (_, i) => [cx + r * Math.cos(ph + 2 * PI * i / k), cy + r * Math.sin(ph + 2 * PI * i / k)]);
  const GRAPHS = {
    tree: () => { const e = []; for (let i = 1; i < 8; i++) { e.push([i - 1, 2 * i - 1], [i - 1, 2 * i]); } const pos = []; for (let i = 0; i < 15; i++) { const lv = Math.floor(Math.log2(i + 1)), k = i + 1 - 2 ** lv; pos.push([(k + 0.5) / 2 ** lv * 2 - 1, -0.9 + lv * 0.6]); } return makeGraph(15, e, pos); },
    cycle: () => makeGraph(6, Array.from({ length: 6 }, (_, i) => [i, (i + 1) % 6]), ring(6)),
    cube: () => { const e = []; for (let i = 0; i < 8; i++) for (let b = 0; b < 3; b++) { const j = i ^ (1 << b); if (i < j) e.push([i, j]); } const pos = Array.from({ length: 8 }, (_, i) => { const x = i & 1, y = (i >> 1) & 1, z = (i >> 2) & 1; return [(x - 0.5) * 1.3 + (z - 0.5) * 0.6, (y - 0.5) * 1.3 + (z - 0.5) * 0.45]; }); return makeGraph(8, e, pos); },
    complete: () => { const e = []; for (let i = 0; i < 5; i++) for (let j = i + 1; j < 5; j++) e.push([i, j]); return makeGraph(5, e, ring(5)); },
    petersen: () => { const e = []; for (let i = 0; i < 5; i++) { e.push([i, (i + 1) % 5], [i, i + 5], [i + 5, ((i + 2) % 5) + 5]); } return makeGraph(10, e, ring(5).concat(ring(5, 0.5))); },
    grid: () => { const e = [], pos = []; for (let i = 0; i < 5; i++) for (let j = 0; j < 5; j++) { const v = 5 * i + j; pos.push([(j - 2) * 0.45, (i - 2) * 0.45]); if (j < 4) e.push([v, v + 1]); if (i < 4) e.push([v, v + 5]); } return makeGraph(25, e, pos); },
    dumbbell: () => { const e = []; for (let i = 0; i < 5; i++) for (let j = i + 1; j < 5; j++) { e.push([i, j], [i + 7, j + 7]); } e.push([4, 5], [5, 6], [6, 7]); const L = ring(5, 0.38, 0, -1.05, 0), R = ring(5, 0.38, PI, 1.05, 0); const pos = L.concat([[-0.25, 0], [0.25, 0]], R); return makeGraph(12, e, pos); }
  };

  // min-cost flow with integer supplies: super source -> sources -> sinks -> super sink, successive shortest paths
  function transportCost(supply, demand, cost) {
    const m = supply.length, n = demand.length, N = m + n + 2, S = 0, T = N - 1, E = [], g = Array.from({ length: N }, () => []);
    const add = (u, v, cap, c) => { g[u].push(E.length); E.push({ v, cap, c }); g[v].push(E.length); E.push({ v: u, cap: 0, c: -c }); };
    supply.forEach((a, i) => add(S, 1 + i, a, 0));
    demand.forEach((b, j) => add(1 + m + j, T, b, 0));
    for (let i = 0; i < m; i++) for (let j = 0; j < n; j++) add(1 + i, 1 + m + j, 1e18, cost[i][j]);
    let total = 0;
    for (;;) {
      const d = Array(N).fill(Infinity), pe = Array(N).fill(-1); d[S] = 0;
      for (let it = 0; it < N; it++) { let ch = false; for (let u = 0; u < N; u++) if (d[u] < Infinity) for (const k of g[u]) { const e = E[k]; if (e.cap > 0 && d[u] + e.c < d[e.v] - 1e-12) { d[e.v] = d[u] + e.c; pe[e.v] = k; ch = true; } } if (!ch) break; }
      if (d[T] === Infinity) break;
      let f = Infinity; for (let v = T; v !== S; v = E[pe[v] ^ 1].v) f = Math.min(f, E[pe[v]].cap);
      for (let v = T; v !== S; v = E[pe[v] ^ 1].v) { E[pe[v]].cap -= f; E[pe[v] ^ 1].cap += f; }
      total += f * d[T];
    }
    return total;
  }
  function ollivier(G, x, y, alpha) { // alpha = 1/2 (lazy) or 0
    const dx = G.adj[x].length, dy = G.adj[y].length;
    const mu = (v, d, other) => { const m = new Map(); if (alpha > 0) m.set(v, dx * dy); for (const w of G.adj[v]) m.set(w, (m.get(w) || 0) + (alpha > 0 ? other : other)); return m; };
    // alpha=1/2: total mass 2*dx*dy, centre dx*dy, each neighbour of x gets dy (dx of them), of y gets dx
    // alpha=0: total mass dx*dy, each neighbour of x gets dy, of y gets dx
    const mx = mu(x, dx, dy), my = mu(y, dy, dx);
    const A = [...mx.keys()], B = [...my.keys()];
    const cost = A.map(p => B.map(q => G.dist[p][q]));
    const tot = (alpha > 0 ? 2 : 1) * dx * dy;
    return 1 - transportCost(A.map(k => mx.get(k)), B.map(k => my.get(k)), cost) / tot;
  }
  const kappaLLY = (G, x, y) => 2 * ollivier(G, x, y, 0.5);
  const kappa0 = (G, x, y) => ollivier(G, x, y, 0);
  const forman = (G, x, y) => 4 - G.adj[x].length - G.adj[y].length;
  const formanAug = (G, x, y) => forman(G, x, y) + 3 * G.adj[x].filter(w => G.adj[y].includes(w)).length;

  function bakryEmery(G, x) {
    const B = [...new Set([x, ...G.adj[x], ...G.adj[x].flatMap(w => G.adj[w])])], idx = new Map(B.map((v, i) => [v, i])), n = B.length;
    const lap = (f, v) => G.adj[v].reduce((s, w) => s + f[idx.get(w)], 0) / G.adj[v].length - f[idx.get(v)];
    const gam = (f, v) => 0.5 * G.adj[v].reduce((s, w) => s + (f[idx.get(w)] - f[idx.get(v)]) ** 2, 0) / G.adj[v].length;
    const q1 = f => gam(f, x);
    const q2 = f => { const dx = G.adj[x].length; const gN = G.adj[x].reduce((s, w) => s + gam(f, w), 0) / dx; const cross = G.adj[x].reduce((s, w) => s + (f[idx.get(w)] - f[idx.get(x)]) * (lap(f, w) - lap(f, x)), 0) / dx; return 0.5 * (gN - gam(f, x)) - 0.5 * cross; };
    const mat = q => { const e = i => B.map((_, k) => (k === i ? 1 : 0)); const M = []; for (let i = 0; i < n; i++) { M.push([]); for (let j = 0; j < n; j++) { if (i === j) M[i].push(q(e(i))); else { const s = e(i).map((v, k) => v + e(j)[k]); M[i].push((q(s) - q(e(i)) - q(e(j))) / 2); } } } return M; };
    const M1 = mat(q1), M2 = mat(q2);
    let lo = -10, hi = 10;
    for (let it = 0; it < 50; it++) { const mid = (lo + hi) / 2; const D = M2.map((r, i) => r.map((v, j) => v - mid * M1[i][j])); if (minEig(D) >= -1e-9) lo = mid; else hi = mid; }
    return Math.floor(lo * 1e6) / 1e6;
  }
  function resistanceCurv(G) {
    const L = G.adj.map((nb, i) => G.adj.map((_, j) => (i === j ? nb.length : nb.includes(j) ? -1 : 0)));
    const P = pinvSym(L);
    const om = (i, j) => P[i][i] + P[j][j] - 2 * P[i][j];
    return G.adj.map((nb, i) => 1 - 0.5 * nb.reduce((s, j) => s + om(i, j), 0));
  }
  function steinerberger(G) { const P = pinvSym(G.dist); return P.map(r => r.reduce((s, v) => s + v * G.n, 0)); }
  function normLapSpectrum(G) {
    const d = G.adj.map(a => a.length);
    const M = G.adj.map((nb, i) => G.adj.map((_, j) => (i === j ? 1 : nb.includes(j) ? -1 / Math.sqrt(d[i] * d[j]) : 0)));
    return jacobiEig(M).values.sort((a, b) => a - b);
  }

  // ---------- surfaces (finite differences) ----------
  const SURFACES = {
    sphere: { name: "Sphere", X: (u, v) => [Math.sin(v) * Math.cos(u), Math.sin(v) * Math.sin(u), Math.cos(v)], U: [0, 2 * PI], V: [0.02, PI - 0.02], chi: 2 },
    cylinder: { name: "Cylinder", X: (u, v) => [Math.cos(u), Math.sin(u), v], U: [0, 2 * PI], V: [-1, 1] },
    torus: { name: "Torus (R = 2, r = 1)", X: (u, v) => [(2 + Math.cos(v)) * Math.cos(u), (2 + Math.cos(v)) * Math.sin(u), Math.sin(v)], U: [0, 2 * PI], V: [0, 2 * PI], chi: 0 },
    saddle: { name: "Saddle z = x² − y²", X: (u, v) => [u, v, u * u - v * v], U: [-1, 1], V: [-1, 1] },
    catenoid: { name: "Catenoid", X: (u, v) => [Math.cosh(v) * Math.cos(u), Math.cosh(v) * Math.sin(u), v], U: [0, 2 * PI], V: [-1.2, 1.2] },
    pseudosphere: { name: "Pseudosphere", X: (u, v) => [Math.cos(u) / Math.cosh(v), Math.sin(u) / Math.cosh(v), v - Math.tanh(v)], U: [0, 2 * PI], V: [0.08, 3] }
  };
  const sub = (a, b) => a.map((x, i) => x - b[i]), dot = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
  const cross = (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
  function surfaceKH(X, u, v, h = 1e-4) {
    const p = X(u, v), xu = X(u + h, v), xd = X(u - h, v), yu = X(u, v + h), yd = X(u, v - h);
    const Xu = sub(xu, xd).map(c => c / (2 * h)), Xv = sub(yu, yd).map(c => c / (2 * h));
    const Xuu = xu.map((c, i) => (c - 2 * p[i] + xd[i]) / (h * h)), Xvv = yu.map((c, i) => (c - 2 * p[i] + yd[i]) / (h * h));
    const pp = X(u + h, v + h), pm = X(u + h, v - h), mp = X(u - h, v + h), mm = X(u - h, v - h);
    const Xuv = pp.map((c, i) => (c - pm[i] - mp[i] + mm[i]) / (4 * h * h));
    const N0 = cross(Xu, Xv), nn = Math.hypot(...N0), n = N0.map(c => c / nn);
    const E = dot(Xu, Xu), F = dot(Xu, Xv), Gm = dot(Xv, Xv), L = dot(Xuu, n), M = dot(Xuv, n), Nn = dot(Xvv, n), W = E * Gm - F * F;
    return { K: (L * Nn - M * M) / W, H: (E * Nn - 2 * F * M + Gm * L) / (2 * W), dA: Math.sqrt(W), p, n };
  }
  function totalCurvature(S, nu = 200, nv = 200) {
    let s = 0; const du = (S.U[1] - S.U[0]) / nu, dv = (S.V[1] - S.V[0]) / nv;
    for (let i = 0; i < nu; i++) for (let j = 0; j < nv; j++) { const q = surfaceKH(S.X, S.U[0] + (i + 0.5) * du, S.V[0] + (j + 0.5) * dv, 1e-3); s += q.K * q.dA * du * dv; }
    return s;
  }

  // ---------- torus mesh ----------
  function torusMesh(nu, nv, R = 2, r = 1) {
    const P = [], T = [], id = (i, j) => ((i + nu) % nu) * nv + ((j + nv) % nv);
    for (let i = 0; i < nu; i++) for (let j = 0; j < nv; j++) { const u = 2 * PI * i / nu, v = 2 * PI * j / nv; P.push([(R + r * Math.cos(v)) * Math.cos(u), (R + r * Math.cos(v)) * Math.sin(u), r * Math.sin(v)]); }
    for (let i = 0; i < nu; i++) for (let j = 0; j < nv; j++) T.push([id(i, j), id(i + 1, j), id(i + 1, j + 1)], [id(i, j), id(i + 1, j + 1), id(i, j + 1)]);
    return { P, T, nu, nv, R, r };
  }
  function meshCurvature({ P, T }) {
    const n = P.length, defect = Array(n).fill(2 * PI), area = Array(n).fill(0), LX = P.map(() => [0, 0, 0]);
    const ang = (i, j, k) => { const a = sub(P[j], P[i]), b = sub(P[k], P[i]); return Math.acos(Math.max(-1, Math.min(1, dot(a, b) / Math.hypot(...a) / Math.hypot(...b)))); };
    for (const [a, b, c] of T) {
      const A = ang(a, b, c), B = ang(b, c, a), C = ang(c, a, b);
      defect[a] -= A; defect[b] -= B; defect[c] -= C;
      const add = (i, j, w) => { for (let k = 0; k < 3; k++) { LX[i][k] += w * (P[j][k] - P[i][k]); LX[j][k] += w * (P[i][k] - P[j][k]); } };
      add(b, c, 0.5 / Math.tan(A)); add(c, a, 0.5 / Math.tan(B)); add(a, b, 0.5 / Math.tan(C));
      const ar = Math.hypot(...cross(sub(P[b], P[a]), sub(P[c], P[a]))) / 6; area[a] += ar; area[b] += ar; area[c] += ar;
    }
    return { defect, area, K: defect.map((d, i) => d / area[i]), H: LX.map((v, i) => Math.hypot(...v) / area[i] / 2) };
  }

  // ---------- curved mean value (test function e^x (1+z)^2 + y z^3 on S²) ----------
  const F0 = (x, y, z) => Math.exp(x) * (1 + z) ** 2 + y * z ** 3;
  const POLE = { f: 4, d1: -4, d2: -20, d3: 500 };
  function circleMean(r, n = 720) { let s = 0; for (let k = 0; k < n; k++) { const p = 2 * PI * (k + 0.5) / n; s += F0(Math.sin(r) * Math.cos(p), Math.sin(r) * Math.sin(p), Math.cos(r)); } return s / n; }
  const approx = {
    flat: r => POLE.f + r * r / 4 * POLE.d1 + r ** 4 * POLE.d2 / 64,
    curved4: r => approx.flat(r) + r ** 4 * POLE.d1 / 96,
    curved6: r => approx.curved4(r) + r ** 6 * (POLE.d3 / 2304 + POLE.d2 / 1152 + POLE.d1 / 1440)
  };
  const discRatio = (K, r) => (Math.abs(K) < 1e-9 ? 1 : K > 0 ? 2 * (1 - Math.cos(Math.sqrt(K) * r)) / (K * r * r) : 2 * (Math.cosh(Math.sqrt(-K) * r) - 1) / (-K * r * r));
  const lapDist = (K, r) => (Math.abs(K) < 1e-9 ? 1 / r : K > 0 ? Math.sqrt(K) / Math.tan(Math.sqrt(K) * r) : Math.sqrt(-K) / Math.tanh(Math.sqrt(-K) * r));

  // ---------- heat traces ----------
  const sphereTrace = t => { let s = 0; for (let l = 0; l < 3000; l++) { const term = (2 * l + 1) * Math.exp(-l * (l + 1) * t); s += term; if (term < 1e-16 && l > 10) break; } return s; };
  const torusTrace = t => { let s = 0; for (let m = -400; m <= 400; m++) s += Math.exp(-PI * m * m * t); return s * s; }; // side 2√π, area 4π

  // ---------- Ollivier curvature of ε-balls on a surface of curvature K ----------
  function ollivierBall(K, eps, n = 120) {
    if (Math.abs(K) < 1e-12) return 0;
    const R = 1 / Math.sqrt(Math.abs(K)); let num = 0, den = 0;
    for (let i = 0; i < n; i++) for (let j = 0; j < n; j++) {
      const rho = eps * (i + 0.5) / n, al = 2 * PI * (j + 0.5) / n;
      if (K > 0) { const s = Math.sin(rho / R) * Math.sin(al), w = Math.sin(rho / R); num += (s * s / (1 + Math.sqrt(1 - s * s))) * w; den += w; }
      else { const s = Math.sinh(rho / R) * Math.sin(al), w = Math.sinh(rho / R); num -= (s * s / (1 + Math.sqrt(1 + s * s))) * w; den += w; }
    }
    return num / den;
  }

  // ---------- curve shortening ----------
  function curveInit(kind, n = 160) {
    const f = { wiggle: t => 1 + 0.35 * Math.cos(3 * t) + 0.2 * Math.sin(5 * t), star: t => 1 + 0.45 * Math.cos(5 * t), ellipse: t => 1 / Math.sqrt(Math.cos(t) ** 2 / 1.6 + Math.sin(t) ** 2 * 1.6), bean: t => 1 + 0.5 * Math.cos(2 * t) * Math.sin(t) + 0.25 * Math.cos(3 * t) }[kind];
    return Array.from({ length: n }, (_, k) => { const t = 2 * PI * k / n, r = f(t); return [r * Math.cos(t), r * Math.sin(t)]; });
  }
  function curveStep(X, dt) {
    const n = X.length;
    return X.map((p, i) => { const a = X[(i + n - 1) % n], b = X[(i + 1) % n]; const fw = [b[0] - p[0], b[1] - p[1]], bw = [p[0] - a[0], p[1] - a[1]]; const lf = Math.hypot(...fw), lb = Math.hypot(...bw); const k = 2 / (lf + lb); return [p[0] + dt * k * (fw[0] / lf - bw[0] / lb), p[1] + dt * k * (fw[1] / lf - bw[1] / lb)]; });
  }
  function curveResample(X, nOut) {
    const n = nOut || X.length, c = X.concat([X[0]]), s = [0]; for (let i = 1; i < c.length; i++) s.push(s[i - 1] + Math.hypot(c[i][0] - c[i - 1][0], c[i][1] - c[i - 1][1]));
    const L = s[s.length - 1], out = []; let k = 0;
    for (let i = 0; i < n; i++) { const q = L * i / n; while (s[k + 1] < q) k++; const t = (q - s[k]) / (s[k + 1] - s[k] || 1); out.push([c[k][0] + t * (c[k + 1][0] - c[k][0]), c[k][1] + t * (c[k + 1][1] - c[k][1])]); }
    return out;
  }
  // Advance the flow by time T with stable steps: dt ≤ 0.2·(shortest edge)², and as the curve shrinks
  // resample it with edges about 1/40 of its initial perimeter (between 24 and 160 vertices) so the steps stay usable.
  const perimeter = X => X.reduce((s, p, i) => { const q = X[(i + 1) % X.length]; return s + Math.hypot(q[0] - p[0], q[1] - p[1]); }, 0);
  function curveFlow(state, T) {
    let { X, t, L0 } = state, done = 0, k = 0;
    while (done < T - 1e-15) {
      let h = Infinity; for (let i = 0; i < X.length; i++) { const q = X[(i + 1) % X.length]; h = Math.min(h, Math.hypot(q[0] - X[i][0], q[1] - X[i][1])); }
      const dt = Math.min(T - done, 0.2 * h * h);
      X = curveStep(X, dt); done += dt; k++;
      if (k % 20 === 0) X = curveResample(X, Math.max(24, Math.min(160, Math.round(160 * perimeter(X) / L0))));
    }
    return { X, t: t + done, L0, steps: (state.steps || 0) + k };
  }
  const polyArea = X => Math.abs(X.reduce((s, p, i) => { const q = X[(i + 1) % X.length]; return s + p[0] * q[1] - q[0] * p[1]; }, 0)) / 2;

  // ---------- 2-D Ricci flow on the flat torus (conformal factor) ----------
  function ricciInit(N = 32, a = 0.3, b = 0.25) { const h = 2 * PI / N, u = []; for (let i = 0; i < N; i++) { u.push([]); for (let j = 0; j < N; j++) u[i].push(a * Math.cos(i * h) + b * Math.sin(2 * j * h) * Math.cos(i * h + j * h)); } return { u, N, h, t: 0 }; }
  function ricciLap(S) { const { u, N, h } = S; return u.map((r, i) => r.map((v, j) => (u[(i + 1) % N][j] + u[(i + N - 1) % N][j] + u[i][(j + 1) % N] + u[i][(j + N - 1) % N] - 4 * v) / (h * h))); }
  function ricciK(S) { const L = ricciLap(S); return S.u.map((r, i) => r.map((v, j) => -Math.exp(-2 * v) * L[i][j])); }
  function ricciStep(S, steps = 1) {
    for (let s = 0; s < steps; s++) {
      const L = ricciLap(S); let umin = Infinity; S.u.forEach(r => r.forEach(v => (umin = Math.min(umin, v))));
      const dt = 0.2 * S.h * S.h * Math.exp(2 * umin);
      S.u = S.u.map((r, i) => r.map((v, j) => v + dt * Math.exp(-2 * v) * L[i][j])); S.t += dt;
    }
    return S;
  }
  const ricciTotalK = S => ricciLap(S).flat().reduce((a, b) => a - b, 0) * S.h * S.h; // ∬K dA = −∬Δ₀u

  return { jacobiEig, pinvSym, GRAPHS, kappaLLY, kappa0, forman, formanAug, bakryEmery, resistanceCurv, steinerberger, normLapSpectrum,
    SURFACES, surfaceKH, totalCurvature, torusMesh, meshCurvature, circleMean, approx, POLE, discRatio, lapDist, sphereTrace, torusTrace,
    ollivierBall, curveInit, curveStep, curveResample, curveFlow, perimeter, polyArea, ricciInit, ricciStep, ricciK, ricciTotalK };
})();
if (typeof module !== "undefined") module.exports = LC;
