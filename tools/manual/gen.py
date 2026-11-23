"""python3 gen.py <spec> <group...>  -> writes /tmp/verify_<tag>.wl and /tmp/verify_<tag>.json (example ids)."""
import sys, re, json, importlib
sys.path.insert(0, '/home/claude/laplacian/tools'); sys.path.insert(0, '/home/claude/laplacian/tools/manual')
from runner import strip, closure, example_code
from wlparse import statements, lhs_name
spec = importlib.import_module(sys.argv[1]); tag = sys.argv[2]; groups = sys.argv[3].split(','); mode = sys.argv[4] if len(sys.argv) > 4 else 'text'
defs = []
if sys.argv[1] == 'spec_curvature':
    from build import CELLS
    GLOBALS = {'gS2', '𝓍S2', 'ΔS2', 'L0'}
    SKIP = {'R', 'ang', 'Γv', 'Kformulas', 'tPC', 'sPC'}
    for style, text in CELLS:
        if style != 'Input': continue
        for st in statements(text):
            n, k = lhs_name(st)
            if n and n not in SKIP and (k == 'func' or n in GLOBALS): defs.append((n, strip(st)))
    for n, src in spec.SNIPPET_SOURCES.items():
        for st in statements(src): defs.append((n, strip(st)))
else:
    for n, src in spec.DEFS: defs.append((n, src))
ids, exprs, alltext = [], [], ''
for name, p in spec.P.items():
    if p['guide'] not in groups: continue
    k = 0
    for sec, exs in p['examples'].items():
        for inp, out in exs:
            k += 1
            isimg = isinstance(out, str) and out.startswith('IMG:')
            if (mode == 'img') != isimg: continue
            ids.append(f'{name}#{k}'); code = example_code(inp, p.get('setup', ''))
            exprs.append(code); alltext += ' ' + code
need = closure(defs, None, alltext)
for a in getattr(spec, 'ALWAYS', []):
    src = dict(defs)[a]
    if src not in need: need.insert(0, src)
need = [x.rstrip().rstrip(';').strip() for x in need]
need = [x for x in need if x]
seen=set(); need=[x for x in need if not (x.startswith('Lap[w_] := 1/Sin') )]
pre = ';\n'.join(need) + ';\n'
if mode == 'img':
    body = '{' + ',\n'.join(exprs) + '}'
else:
    body = 'StringRiffle[MapIndexed[ToString[First[#2]] <> " | " <> # &, {' + ',\n'.join(
        f'Quiet@Check[ToString[TimeConstrained[{e}, 40, "TIMEOUT"], InputForm, CharacterEncoding -> "Unicode", PageWidth -> Infinity], "ERROR"]' for e in exprs) + '}], "\\n"]'
open(f'/tmp/verify_{tag}.wl', 'w', encoding='utf-8').write(pre + body)
json.dump(ids, open(f'/tmp/verify_{tag}.json', 'w', encoding='utf-8'), ensure_ascii=False)
print(len(ids), 'examples,', len(need), 'defs,', len((pre + body).encode()), 'bytes')
