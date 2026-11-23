"""python3 runcheck.py module -> /tmp/<module>_run.wl: all Input cells in order, each cell's result recorded (graphics as their head)."""
import sys, importlib
sys.path.insert(0, '/home/claude/laplacian/tools/series')
m = importlib.import_module(sys.argv[1])
ins = [t for s, t in m.CELLS if s == 'Input']
sel = [int(x) for x in sys.argv[2].split(',')] if len(sys.argv) > 2 else list(range(1, len(ins) + 1))
tag = sys.argv[3] if len(sys.argv) > 3 else ''
parts = ['$res = {};']
for i in sel:
    t = ins[i - 1]
    parts.append('AppendTo[$res, ToString[' + str(i) + '] <> " | " <> Quiet@Check[With[{r = TimeConstrained[(' + t + '), 120, "TIMEOUT"]}, '
                 'If[!FreeQ[r, _Graphics | _Graphics3D | _Legended | _Graph], "GRAPHIC " <> ToString[Head[r]], ToString[r /. Grid[a_, ___] :> a, InputForm, CharacterEncoding -> "Unicode"]]], "ERROR"]];')
parts.append('StringRiffle[$res, "\\n"]')
open(f'/tmp/{sys.argv[1]}{tag}_run.wl', 'w', encoding='utf-8').write('\n'.join(parts))
print(len(ins))
