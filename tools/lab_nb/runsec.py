"""python3 runsec.py <section number> [<section number>...] -> /tmp/lab_s<..>.wl: §0 cells + the chosen sections' Input cells, each result recorded."""
import sys, re
sys.path.insert(0, '/home/claude/laplacian/tools/lab_nb')
import curvature_lab as m
secs, cur = {}, None
for s, t in m.CELLS:
    if s == 'Section': cur = int(t.split('.')[0]); secs[cur] = []
    elif s == 'Input' and cur is not None: secs[cur].append(t)
want = [int(x) for x in sys.argv[1:]]
keys = {1: ['surfaces'], 2: ['ricci'], 3: ['means'], 4: ['heat'], 5: [], 6: ['mesh'], 7: ['graphs'], 8: ['flows'], 9: ['ollivier'], 10: [], 11: ['graphs', 'flows']}
need = sorted({k for w in want for k in keys[w]})
import os
G = os.environ.get('GR')
if G: m._js = dict(m._js, graphs={g: m._js['graphs'][g] for g in G.split(',')})
if os.environ.get('STRIP'): m._js = dict(m._js, graphs={g: {k: v[k] for k in ('n', 'edges')} for g, v in m._js['graphs'].items()})
CI = os.environ.get('CI')
if CI: secs = {w: [secs[w][int(i) - 1] for i in CI.split(',')] for w in want}
TAIL = os.environ.get('TAIL', '')
parts = [m.page_data(need) if need else 'page = <||>;', m.HELPERS, '$res = {};']
n = 0
for w in want:
    for t in secs[w]:
        n += 1
        parts.append('AppendTo[$res, "%d.%d | " <> Quiet@Check[With[{r = TimeConstrained[(%s), 200, "TIMEOUT"]}, If[!FreeQ[r, _Graphics | _Graphics3D], "GRAPHIC", ToString[r /. {Grid[a_, ___] :> a, NumberForm[x_, _] :> x, Row[{a_, _, b_}] :> {a, b}}, InputForm, CharacterEncoding -> "Unicode", TotalWidth -> 3000]]], "ERROR"]];' % (w, n, t))
if TAIL: parts.append('AppendTo[$res, ToString[(' + TAIL + '), InputForm, CharacterEncoding -> "Unicode"]];')
parts.append('StringRiffle[$res, "\\n"]')
fn = '/tmp/lab_s%s.wl' % '_'.join(map(str, want))
open(fn, 'w', encoding='utf-8').write('\n'.join(parts)); print(fn)
