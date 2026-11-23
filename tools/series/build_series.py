"""python3 tools/series/build_series.py <module> -> notebooks/series/<NN>-<Name>.nb and .wl"""
import sys, importlib
sys.path.insert(0, '/home/claude/laplacian/tools'); sys.path.insert(0, '/home/claude/laplacian/tools/series')
from build import wl_escape, text_cell, text_plain, number_figures, any_cell
m = importlib.import_module(sys.argv[1])
fn = '/home/claude/laplacian/notebooks/series/' + m.FILE
CS = number_figures(m.CELLS)
cells = ',\n'.join(any_cell(s, t) for s, t in CS)
open(fn + '.nb', 'w', encoding='ascii').write(
    "(* Content-type: application/vnd.wolfram.mathematica *)\n(* %s - Computational Classnotes - CC BY-NC-SA 4.0 *)\n\nNotebook[{\n%s\n},\nWindowTitle -> \"%s\",\nStyleDefinitions -> \"Default.nb\"\n]\n" % (m.TITLE, cells, m.TITLE))
lines = ["(* ::Package:: *)", "", "(* %s *)" % m.TITLE, "(* © 2026 Computational Classnotes · CC BY-NC-SA 4.0 *)", ""]
for s, t in CS:
    if s == 'FigCaption': lines += ["(* ::Text:: *)", "(*%s*)" % text_plain(t.replace('|', ' ')), ""]
    elif s == 'Input': lines += [t, ""]
    elif s in ('Title', 'Section', 'Subsection'): lines += ["(* ::%s:: *)" % s, "(*%s*)" % text_plain(t), ""]
    else: lines += ["(* ::Text:: *)", "(*%s*)" % text_plain(t).replace("(*", "( *").replace("*)", "* )"), ""]
open(fn + '.wl', 'w', encoding='utf-8').write('\n'.join(lines))
print(fn)
