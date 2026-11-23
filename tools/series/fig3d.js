/* CCN rotatable 3D figures for the HTML write-ups (no libraries). © Computational Classnotes · CC BY-NC-SA 4.0 */
(function () {
  const ORANGE = [250, 143, 43], BLUE = [46, 92, 199];
  const mix = (a, b, t) => a.map((v, i) => Math.round(v + (b[i] - v) * t));
  const rot = (p, ax, ay) => { // rotate about y (ay) then x (ax)
    let [x, y, z] = p; const cy = Math.cos(ay), sy = Math.sin(ay);
    [x, z] = [cy * x + sy * z, -sy * x + cy * z];
    const cx = Math.cos(ax), sx = Math.sin(ax);
    [y, z] = [cx * y - sx * z, sx * y + cx * z];
    return [x, y, z];
  };
  const rz = (p, t) => [Math.cos(t) * p[0] - Math.sin(t) * p[1], Math.sin(t) * p[0] + Math.cos(t) * p[1], p[2]];
  // points of the eps-ball around (1,0,0): spherical cap, Fibonacci sampling
  function capPoints(eps, n) {
    const out = [], c = Math.cos(eps);
    for (let i = 0; i < n; i++) {
      const u = 1 - (1 - c) * (i + 0.5) / n, a = i * Math.PI * (3 - Math.sqrt(5)), s = Math.sqrt(1 - u * u);
      out.push([u, s * Math.cos(a), s * Math.sin(a)]); // axis = +x
    }
    return out.map(p => [p[0], p[1], p[2]]).map(p => [p[0], p[2], p[1]]).map(p => [p[0], p[1], p[2]]);
  }
  function ollivierSphere(cv) {
    const delta = 0.7, eps = 0.42, pts = capPoints(eps, 90).map(p => [p[0], p[1], p[2]]);
    // ball centred at x=(1,0,0) on the equator z=0; geodesic = equator; rotation about z by delta
    const ball = pts.map(p => [p[0], p[2], p[1]]); // keep z as latitude direction
    let ax = 0.45, ay = 0.0, drag = null;
    const ctx = cv.getContext('2d');
    function draw() {
      const dpr = window.devicePixelRatio || 1, W = cv.clientWidth, H = cv.clientHeight;
      cv.width = W * dpr; cv.height = H * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      const R = Math.min(W, H) * 0.42, cx = W / 2, cy = H / 2 + 6;
      const P = q => { const v = rz(q, -delta / 2), r = rot([v[1], v[2], v[0]], ax, ay); return [cx + R * r[0], cy - R * r[1], r[2]]; };
      ctx.clearRect(0, 0, W, H);
      const g = ctx.createRadialGradient(cx - R * 0.35, cy - R * 0.35, R * 0.1, cx, cy, R);
      g.addColorStop(0, '#fbfaf7'); g.addColorStop(1, '#d9d6cf');
      ctx.fillStyle = g; ctx.beginPath(); ctx.arc(cx, cy, R, 0, 2 * Math.PI); ctx.fill();
      const seg = (pts3, style, width, dash) => { // polyline, faint when behind
        for (let i = 0; i + 1 < pts3.length; i++) {
          const a = P(pts3[i]), b = P(pts3[i + 1]); const front = a[2] + b[2] > 0;
          ctx.strokeStyle = style; ctx.globalAlpha = front ? 1 : 0.18; ctx.lineWidth = width; ctx.setLineDash(dash || []);
          ctx.beginPath(); ctx.moveTo(a[0], a[1]); ctx.lineTo(b[0], b[1]); ctx.stroke();
        }
        ctx.globalAlpha = 1; ctx.setLineDash([]);
      };
      // meridians/parallels
      for (let k = 0; k < 12; k++) { const t = k * Math.PI / 6; seg(Array.from({length: 49}, (_, i) => { const s = -Math.PI / 2 + i * Math.PI / 48; return [Math.cos(s) * Math.cos(t), Math.cos(s) * Math.sin(t), Math.sin(s)]; }), '#bdb8ae', 0.6); }
      for (const la of [-60, -30, 30, 60]) { const s = la * Math.PI / 180; seg(Array.from({length: 73}, (_, i) => { const t = i * Math.PI / 36; return [Math.cos(s) * Math.cos(t), Math.cos(s) * Math.sin(t), Math.sin(s)]; }), '#bdb8ae', 0.6); }
      // geodesic (equator) and cap boundaries
      seg(Array.from({length: 81}, (_, i) => { const t = -0.4 + i * (delta + 0.8) / 80; return [Math.cos(t), Math.sin(t), 0]; }), '#333', 2.2);
      const circ = c => Array.from({length: 73}, (_, i) => { const t = i * Math.PI / 36; return rz([Math.cos(eps), Math.sin(eps) * Math.cos(t), Math.sin(eps) * Math.sin(t)], c); }).map(p => [p[0], p[1], p[2]]);
      seg(circ(0).map(p => [p[0], p[1], p[2]]), '#222', 1.4); seg(circ(delta), '#222', 1.4);
      // arrows: each point slides along its latitude circle by delta; colour = cos(lambda)
      for (const p of ball) {
        const lam = Math.asin(Math.max(-1, Math.min(1, p[2]))), t = (Math.cos(lam) - Math.cos(eps)) / (1 - Math.cos(eps));
        const col = 'rgb(' + mix(BLUE, ORANGE, t).join(',') + ')';
        const path = Array.from({length: 13}, (_, i) => rz(p, delta * i / 12));
        seg(path, col, 1.3);
        const a = P(path[11]), b = P(path[12]);
        if (b[2] > 0) { const ang = Math.atan2(b[1] - a[1], b[0] - a[0]); ctx.fillStyle = col; ctx.beginPath(); ctx.moveTo(b[0], b[1]); ctx.lineTo(b[0] - 6 * Math.cos(ang - 0.4), b[1] - 6 * Math.sin(ang - 0.4)); ctx.lineTo(b[0] - 6 * Math.cos(ang + 0.4), b[1] - 6 * Math.sin(ang + 0.4)); ctx.fill(); }
      }
      // centres
      for (const [q, lab] of [[[1, 0, 0], 'x'], [rz([1, 0, 0], delta), 'y']]) {
        const s = P(q); if (s[2] < 0) continue; ctx.fillStyle = '#000'; ctx.beginPath(); ctx.arc(s[0], s[1], 4, 0, 2 * Math.PI); ctx.fill();
        ctx.font = 'bold 15px DejaVu Sans, sans-serif'; ctx.fillText(lab, s[0] + 7, s[1] + 16);
      }
    }
    const pos = e => e.touches ? [e.touches[0].clientX, e.touches[0].clientY] : [e.clientX, e.clientY];
    const down = e => { drag = pos(e); e.preventDefault(); };
    const move = e => { if (!drag) return; const p = pos(e); ay += (p[0] - drag[0]) * 0.01; ax += (p[1] - drag[1]) * 0.01; ax = Math.max(-1.5, Math.min(1.5, ax)); drag = p; draw(); e.preventDefault(); };
    cv.addEventListener('mousedown', down); addEventListener('mousemove', move); addEventListener('mouseup', () => drag = null);
    cv.addEventListener('touchstart', down, {passive: false}); cv.addEventListener('touchmove', move, {passive: false}); cv.addEventListener('touchend', () => drag = null);
    addEventListener('resize', draw); draw();
  }
  // Bakry–Émery: slack of CD(1,2) on the unit sphere for g = z + (x^2 - y^2); slack = 8 - 8 sin^2 t + sin^4 t (1 + cos 4p)
  function beSphere(cv) {
    const ctx = cv.getContext('2d'); let ax = 0.35, ay = -0.6, drag = null;
    const W0 = [247, 247, 247], O = [250, 143, 43], D = [163, 82, 6];
    const col = v => { const u = Math.max(0, Math.min(1, v / 8)); return u < 0.5 ? mix(W0, O, u * 2) : mix(O, D, (u - 0.5) * 2); };
    const slack = (t, p) => { const s = Math.sin(t) ** 2; return 8 - 8 * s + s * s * (1 + Math.cos(4 * p)); };
    const pt = (t, p) => [Math.sin(t) * Math.cos(p), Math.sin(t) * Math.sin(p), Math.cos(t)];
    const NT = 36, NP = 72;
    function draw() {
      const dpr = window.devicePixelRatio || 1, W = cv.clientWidth, H = cv.clientHeight;
      cv.width = W * dpr; cv.height = H * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0); ctx.clearRect(0, 0, W, H);
      const R = Math.min(W, H) * 0.40, cx = W / 2, cy = H / 2;
      const P = q => { const r = rot([q[1], q[2], q[0]], ax, ay); return [cx + R * r[0], cy - R * r[1], r[2]]; };
      const quads = [];
      for (let i = 0; i < NT; i++) for (let j = 0; j < NP; j++) {
        const t0 = Math.PI * i / NT, t1 = Math.PI * (i + 1) / NT, p0 = 2 * Math.PI * j / NP, p1 = 2 * Math.PI * (j + 1) / NP;
        const c = [P(pt(t0, p0)), P(pt(t1, p0)), P(pt(t1, p1)), P(pt(t0, p1))], z = (c[0][2] + c[1][2] + c[2][2] + c[3][2]) / 4;
        if (z < -0.05) continue;
        quads.push([z, c, slack((t0 + t1) / 2, (p0 + p1) / 2)]);
      }
      quads.sort((a, b) => a[0] - b[0]);
      for (const [z, c, v] of quads) {
        const k = 0.78 + 0.22 * Math.max(0, z), rgb = col(v).map(x => Math.round(x * k + 255 * 0 * (1 - k)));
        ctx.fillStyle = ctx.strokeStyle = 'rgb(' + rgb.join(',') + ')'; ctx.lineWidth = 0.6;
        ctx.beginPath(); ctx.moveTo(c[0][0], c[0][1]); for (let n = 1; n < 4; n++) ctx.lineTo(c[n][0], c[n][1]); ctx.closePath(); ctx.fill(); ctx.stroke();
      }
      // equator, faint behind
      for (let i = 0; i < 120; i++) { const a = P(pt(Math.PI / 2, i * Math.PI / 60)), b = P(pt(Math.PI / 2, (i + 1) * Math.PI / 60));
        if (a[2] + b[2] < 0) continue; ctx.strokeStyle = '#566273'; ctx.lineWidth = 1; ctx.beginPath(); ctx.moveTo(a[0], a[1]); ctx.lineTo(b[0], b[1]); ctx.stroke(); }
      // the four zeros
      for (let k = 0; k < 4; k++) { const s = P(pt(Math.PI / 2, Math.PI / 4 + k * Math.PI / 2)); if (s[2] < 0) continue;
        ctx.fillStyle = '#17202b'; ctx.beginPath(); ctx.arc(s[0], s[1], 4.5, 0, 2 * Math.PI); ctx.fill(); }
      // legend
      const lx = W - 34, ly = cy - R * 0.8, lh = R * 1.6;
      for (let i = 0; i < 60; i++) { ctx.fillStyle = 'rgb(' + col(8 * (1 - i / 60)).join(',') + ')'; ctx.fillRect(lx, ly + lh * i / 60, 12, lh / 60 + 1); }
      ctx.strokeStyle = '#566273'; ctx.strokeRect(lx, ly, 12, lh); ctx.fillStyle = '#17202b'; ctx.font = '12px IBM Plex Sans, DejaVu Sans, sans-serif';
      ctx.fillText('8', lx - 12, ly + 8); ctx.fillText('0', lx - 12, ly + lh); ctx.fillText('slack', lx - 22, ly - 8);
    }
    const pos = e => e.touches ? [e.touches[0].clientX, e.touches[0].clientY] : [e.clientX, e.clientY];
    const down = e => { drag = pos(e); e.preventDefault(); };
    const move = e => { if (!drag) return; const p = pos(e); ay += (p[0] - drag[0]) * 0.01; ax += (p[1] - drag[1]) * 0.01; ax = Math.max(-1.5, Math.min(1.5, ax)); drag = p; draw(); e.preventDefault(); };
    cv.addEventListener('mousedown', down); addEventListener('mousemove', move); addEventListener('mouseup', () => drag = null);
    cv.addEventListener('touchstart', down, {passive: false}); cv.addEventListener('touchmove', move, {passive: false}); cv.addEventListener('touchend', () => drag = null);
    addEventListener('resize', draw); draw();
  }
  const FIGS = { 'ollivier-sphere': ollivierSphere, 'be-sphere': beSphere };
  document.querySelectorAll('canvas[data-fig3d]').forEach(cv => { const f = FIGS[cv.dataset.fig3d]; if (f) f(cv); });
})();
