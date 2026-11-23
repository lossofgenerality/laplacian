"""python3 tools/series/build_series.py <module> -> notebooks/series/<NN>-<Name>.nb and .wl"""
import sys, importlib
sys.path.insert(0, '/home/claude/laplacian/tools'); sys.path.insert(0, '/home/claude/laplacian/tools/series')
from build import wl_escape
m = importlib.import_module(sys.argv[1])
fn = '/home/claude/laplacian/notebooks/series/' + m.FILE
cells = ',\n'.join('Cell["%s", "%s"]' % (wl_escape(t), s) for s, t in m.CELLS)
open(fn + '.nb', 'w', encoding='ascii').write(
    "(* Content-type: application/vnd.wolfram.mathematica *)\n(* %s - Computational Classnotes - CC BY-NC-SA 4.0 *)\n\nNotebook[{\n%s\n},\nWindowTitle -> \"%s\",\nStyleDefinitions -> \"Default.nb\"\n]\n" % (m.TITLE, cells, m.TITLE))
lines = ["(* ::Package:: *)", "", "(* %s *)" % m.TITLE, "(* © 2026 Computational Classnotes · CC BY-NC-SA 4.0 *)", ""]
for s, t in m.CELLS:
    if s == 'Input': lines += [t, ""]
    elif s in ('Title', 'Section', 'Subsection'): lines += ["(* ::%s:: *)" % s, "(*%s*)" % t, ""]
    else: lines += ["(* ::Text:: *)", "(*%s*)" % t.replace("(*", "( *").replace("*)", "* )"), ""]
open(fn + '.wl', 'w', encoding='utf-8').write('\n'.join(lines))
print(fn)
