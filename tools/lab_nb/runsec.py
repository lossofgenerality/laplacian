"""python3 runsec.py <section number> [...] -> /tmp/lab_s<..>.wl: the toolkit, the chosen sections' Input cells
and (PN=1) their Production Notes tables, each result recorded. Env: CI cell indices, GR graph subset, STRIP, TAIL."""
import sys, os
sys.path.insert(0, '/home/claude/laplacian/tools/lab_nb')
import curvature_lab as m
PNMAP = {'PN 1': 1, 'PN 2': 2, 'PN 3': 3, 'PN 4': 4, 'PN 5': 6, 'PN 6': 7, 'PN 7': 8, 'PN 8': 9}
secs, pns, cur, curpn = {}, {}, None, None
for s, t in m.CELLS:
    if s == 'Section':
        cur = int(t.split('.')[0]) if t[0].isdigit() else 'PN'; curpn = None
        if cur != 'PN': secs[cur] = []
    elif s == 'Subsection' and cur == 'PN':
        curpn = PNMAP.get(t.split('.')[0]); pns.setdefault(curpn, [])
    elif s == 'Input' and cur not in (None, 'PN', 0): secs[cur].append(t)
    elif s == 'Input' and cur == 'PN' and curpn: pns[curpn].append(t)
want = [int(x) for x in sys.argv[1:]]
keys = {1: ['surfaces'], 2: ['ricci'], 3: ['means'], 4: ['heat'], 5: [], 6: ['mesh'], 7: ['graphs'], 8: ['flows'], 9: ['ollivier'], 10: [], 11: []}
need = sorted({k for w in want for k in keys[w]})
G = os.environ.get('GR')
if G: m._js = dict(m._js, graphs={g: m._js['graphs'][g] for g in G.split(',')})
if os.environ.get('STRIP'): m._js = dict(m._js, graphs={g: {k: v[k] for k in ('n', 'edges')} for g, v in m._js['graphs'].items()})
CI = os.environ.get('CI')
if CI: secs = {w: [secs[w][int(i) - 1] for i in CI.split(',')] for w in want}
PN = os.environ.get('PN')
TAIL = os.environ.get('TAIL', '')
tk = m.TOOLKIT.replace('ClearAll["Global`*"];  (* start from a clean kernel *)', '')
parts = [tk, '$res = {};']
n = 0
def add(w, t):
    global n; n += 1
    parts.append('AppendTo[$res, "%s.%d | " <> Quiet@Check[With[{r = TimeConstrained[(%s), 200, "TIMEOUT"]}, If[!FreeQ[r, _Graphics | _Graphics3D], "GRAPHIC", ToString[r /. {Grid[a_, ___] :> a, NumberForm[x_, _] :> x, Row[{a_, _, b_}] :> {a, b}}, InputForm, CharacterEncoding -> "Unicode", TotalWidth -> 3000]]], "ERROR"]];' % (w, n, t))
for w in want:
    for t in secs[w]: add(w, t)
if PN:
    parts += [m.page_data(need) if need else 'page = <||>;', m.PN_HELPERS]
    for w in want:
        for t in pns.get(w, []): add('PN%d' % w, t)
if TAIL: parts.append('AppendTo[$res, ToString[(' + TAIL + '), InputForm, CharacterEncoding -> "Unicode"]];')
parts.append('StringRiffle[$res, "\\n"]')
fn = '/tmp/lab_s%s.wl' % '_'.join(map(str, want))
open(fn, 'w', encoding='utf-8').write('\n'.join(parts)); print(fn)
