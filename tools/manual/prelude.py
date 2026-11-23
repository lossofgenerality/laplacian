"""Definitions-only prelude of the Curvature notebook, for verifying manual examples."""
import sys, re, json
sys.path.insert(0, '/home/claude/laplacian/tools')
sys.path.insert(0, '/home/claude/laplacian/tools/manual')
from build import CELLS
from wlparse import statements, lhs_name
GLOBALS = {'gS2', '𝓍S2', 'ΔS2', 'graphs', 'dumbbell', 'family', 'torusPos', 'gTor', '𝓍T', 'Ktor', 'ΔT', 'L0', 'surfaces', 'nC', 'Xc', 'λ'}
SKIP = {'R', 'ang', 'Γv', 'Kformulas'}
defs, sources = [], {}
for style, text in CELLS:
    if style != 'Input': continue
    for st in statements(text):
        name, kind = lhs_name(st)
        if not name or name in SKIP: continue
        if kind == 'func' or name in GLOBALS:
            defs.append(st)
            if kind == 'func': sources.setdefault(name, []).append(st)
if __name__ == '__main__':
    print(len(defs), 'definitions;', len(sources), 'functions')
    print(sorted(sources))
    open('/tmp/prelude_curv.wl', 'w', encoding='utf-8').write(';\n'.join(defs) + ';\n')
