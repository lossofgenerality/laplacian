const LC = require('./core.js');
const names = ['tree','cycle','cube','complete','petersen','grid','dumbbell'];
for (const nm of names) {
  const G = LC.GRAPHS[nm]();
  const lly = G.edges.map(([a,b]) => LC.kappaLLY(G,a,b)), k0 = G.edges.map(([a,b]) => LC.kappa0(G,a,b));
  const be = [...Array(G.n).keys()].map(v => LC.bakryEmery(G,v));
  const p = LC.resistanceCurv(G), ks = LC.steinerberger(G), sp = LC.normLapSpectrum(G);
  const f = G.edges.map(([a,b]) => LC.formanAug(G,a,b));
  const r = x => Math.round(x*1e4)/1e4;
  console.log(nm.padEnd(9), 'LLY', r(Math.min(...lly)), r(Math.max(...lly)), 'k0', r(Math.min(...k0)), 'BE', r(Math.min(...be)), r(Math.max(...be)), 'Faug', Math.min(...f), 'Σp', r(p.reduce((a,b)=>a+b)), 'minp', r(Math.min(...p)), 'KS', r(Math.min(...ks)), r(Math.max(...ks)), 'λ1', r(sp[1]), 'λmax', r(sp[sp.length-1]));
}
for (const k of Object.keys(LC.SURFACES)) { const S = LC.SURFACES[k]; const q = LC.surfaceKH(S.X, 1.0, (S.V[0]+S.V[1])/2); console.log(k, 'K', q.K.toFixed(5), 'H', q.H.toFixed(5), 'total', LC.totalCurvature(S,120,120).toFixed(4)); }
const M = LC.meshCurvature(LC.torusMesh(40,20)); console.log('mesh Σdefect', M.defect.reduce((a,b)=>a+b).toExponential(2), 'Kouter', M.K[0].toFixed(4), 'exact', (1/3).toFixed(4));
for (const r of [0.4,0.2,0.1,0.05]) { const ex = LC.circleMean(r); console.log('r',r,'err flat',Math.abs(ex-LC.approx.flat(r)).toExponential(3),'c4',Math.abs(ex-LC.approx.curved4(r)).toExponential(3),'c6',Math.abs(ex-LC.approx.curved6(r)).toExponential(3)); }
for (const t of [0.01,0.1]) console.log('heat', t, (t*LC.sphereTrace(t)).toFixed(6), (1+t/3+t*t/15).toFixed(6), (t*LC.torusTrace(t)).toFixed(6));
console.log('ollivier', [1,-1].map(K => (LC.ollivierBall(K,0.05)/0.0025).toFixed(5)));
let X = LC.curveInit('wiggle'); const A0 = LC.polyArea(X); let t=0; for (let k=1;k<=2000;k++){ X = LC.curveStep(X,2e-4); t+=2e-4; if(k%50==0) X = LC.curveResample(X);} console.log('curve dA/dt', ((LC.polyArea(X)-A0)/t).toFixed(4), (-2*Math.PI).toFixed(4));
let S = LC.ricciInit(); const K0 = Math.max(...LC.ricciK(S).flat().map(Math.abs)); while (S.t < 2) LC.ricciStep(S, 20); console.log('ricci maxK', K0.toFixed(3), '->', Math.max(...LC.ricciK(S).flat().map(Math.abs)).toFixed(4), 'totalK', LC.ricciTotalK(S).toExponential(2), 't', S.t.toFixed(3));
