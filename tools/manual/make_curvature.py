import sys, json
sys.path.insert(0, '/home/claude/laplacian/tools'); sys.path.insert(0, '/home/claude/laplacian/tools/manual')
from build import CELLS
from wlparse import statements, lhs_name
import spec_curvature as S
from build_manual import build
from hand_curvature import HAND
defs = {}
for style, text in CELLS:
    if style != 'Input': continue
    for st in statements(text):
        n, k = lhs_name(st)
        if n in S.P and k == 'func' and n not in S.SNIPPET_SOURCES:
            defs.setdefault(n, []).append(st.strip().rstrip(';') + ';')
defs = {k: '\n'.join(v) for k, v in defs.items()}
defs.update(S.SNIPPET_SOURCES)
miss = [n for n in S.P if n not in defs]
print('no source:', miss)
outs = json.load(open('outputs_curvature.json', encoding='utf-8'))
imgs = {k: f'img/{k}.png' for k in ['curvsurf', 'legend', 'edgeplot', 'vertexplot', 'edgepic', 'row']}
print(build(S, defs, outs, imgs, '/home/claude/laplacian/manual.html', 'CCN', HAND))
