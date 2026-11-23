"""Build LaplacianCurvature.nb and LaplacianCurvature.wl from cells.py."""
import json, sys
from cells import CELLS as BASE
from additions import ADD

def merged():
    out, sec = [], 0
    for style, text in BASE:
        if style == "Section":
            if sec in ADD:
                out += ADD[sec]
            sec = int(text.split(".")[0])
        out.append((style, text))
    if sec in ADD:
        out += ADD[sec]
    return out

CELLS = merged()

def wl_escape(s):
    out = []
    for ch in s:
        o = ord(ch)
        if ch == '\\':
            out.append('\\\\')
        elif ch == '"':
            out.append('\\"')
        elif ch == '\n':
            out.append('\\n')
        elif o > 0xFFFF:
            out.append('\\|%06x' % o)
        elif o > 127:
            out.append('\\:%04x' % o)
        else:
            out.append(ch)
    return ''.join(out)


import re as _re
_SUB = _re.compile(r'([A-Za-z\u0370-\u03FF\u2200-\u22FF\u1D00-\u1DBF\u2100-\u214F]+)_(\{[^}]*\}|[A-Za-z0-9\u0370-\u03FF\u2070-\u209F\u00B2\u00B3\u00B9\u00BD\u211D]+)')

def sub_parts(text):
    """Split prose into plain strings and (base, subscript) pairs for X_Y and X_{Y}."""
    out, i = [], 0
    for m in _SUB.finditer(text):
        out.append(text[i:m.start()]); sb = m.group(2)
        out.append((m.group(1), sb[1:-1] if sb.startswith('{') else sb)); i = m.end()
    out.append(text[i:])
    return [p for p in out if p != '']

def text_cell(text, style):
    parts = sub_parts(text)
    if all(isinstance(p, str) for p in parts):
        return 'Cell["%s", "%s"]' % (wl_escape(text), style)
    items = []
    for p in parts:
        if isinstance(p, str): items.append('"%s"' % wl_escape(p))
        else: items.append('Cell[BoxData[SubscriptBox["%s", "%s"]]]' % (wl_escape(p[0]), wl_escape(p[1])))
    return 'Cell[TextData[{%s}], "%s"]' % (', '.join(items), style)

def text_plain(text):
    """For .wl comments: linear-syntax subscripts."""
    return ''.join(p if isinstance(p, str) else '\\!\\(\\*SubscriptBox[\\(%s\\), \\(%s\\)]\\)' % p for p in sub_parts(text))

import re as _re2
_FIG = _re2.compile(r'\b(Plot|Plot3D|ListPlot|ListLinePlot|ListLogPlot|ListLogLogPlot|LogLogPlot|ParametricPlot3D|ParametricPlot|Graphics3D|Graphics|BarChart|Legended|GraphicsRow|GraphicsGrid|Show|curvatureSurface|edgeCurvaturePlot|vertexCurvaturePlot|edgePicture|planPicture|row|Row|ArrayPlot|DensityPlot|ListDensityPlot|Histogram|Grid)\[')
def is_figure(code):
    import sys as _s; _s.path.insert(0, '/home/claude/laplacian/tools/manual')
    from wlparse import statements
    st = statements(code); last = (st[-1] if st else '').strip()
    if not last or last.endswith(';') or last.startswith('<|') or last.startswith('Dataset') or last.startswith('Grid[Prepend'): return False
    return bool(_FIG.search(last))

def number_figures(cells):
    """Explicit ('Figure', caption) cells become numbered captions; with none, every figure Input gets 'Fig. n'."""
    explicit = any(s == 'Figure' for s, _ in cells)
    out, n = [], 0
    for s, t in cells:
        if s == 'Figure':
            n += 1; out.append(('FigCaption', 'Fig. %d.|%s' % (n, t)))
        else:
            out.append((s, t))
            if not explicit and s == 'Input' and is_figure(t):
                n += 1; out.append(('FigCaption', 'Fig. %d.|' % n))
    return out

def caption_cell(t):
    num, cap = t.split('|', 1)
    items = ['StyleBox["%s", FontWeight -> "Bold", FontColor -> RGBColor[0.83, 0.34, 0.11]]' % wl_escape(num + (' ' if cap else ''))]
    for p in sub_parts(cap) if cap else []:
        items.append('"%s"' % wl_escape(p) if isinstance(p, str) else 'Cell[BoxData[SubscriptBox["%s", "%s"]]]' % (wl_escape(p[0]), wl_escape(p[1])))
    return 'Cell[TextData[{%s}], "Text"]' % ', '.join(items)

def any_cell(style, text):
    if style == 'Input': return 'Cell["%s", "Input"]' % wl_escape(text)
    if style == 'FigCaption': return caption_cell(text)
    return text_cell(text, style)

def nb():
    cells = []
    for style, text in number_figures(CELLS):
        cells.append(any_cell(style, text))
    body = ",\n".join(cells)
    return ("(* Content-type: application/vnd.wolfram.mathematica *)\n"
            "(* The Laplacian and Curvature - Computational Classnotes - CC BY-NC-SA 4.0 *)\n\n"
            "Notebook[{\n" + body + "\n},\n"
            "WindowTitle -> \"The Laplacian and Curvature\",\n"
            "StyleDefinitions -> \"Default.nb\"\n]\n")

def wl():
    lines = ["(* ::Package:: *)", "",
             "(* The Laplacian and Curvature — instances and relationships, computed *)",
             "(* © 2026 Computational Classnotes · CC BY-NC-SA 4.0 *)", ""]
    for style, text in number_figures(CELLS):
        if style == "FigCaption":
            lines += ["(* ::Text:: *)", "(*%s*)" % text_plain(text.replace('|', ' ')), ""]
        elif style == "Input":
            lines += [text, ""]
        elif style in ("Title", "Section", "Subsection"):
            lines += ["(* ::%s:: *)" % ("Title" if style == "Title" else style), "(*%s*)" % text_plain(text), ""]
        else:
            lines += ["(* ::Text:: *)", "(*%s*)" % text_plain(text).replace("(*", "( *").replace("*)", "* )"), ""]
    return "\n".join(lines)

def chunks():
    """Input cells grouped by section, for testing."""
    secs, cur = [], None
    for style, text in CELLS:
        if style == "Section":
            cur = [text, []]; secs.append(cur)
        elif style == "Input" and cur:
            cur[1].append(text)
    return secs

if __name__ == "__main__":
    out = sys.argv[1]
    open(out + "/LaplacianCurvature.nb", "w", encoding="ascii").write(nb())
    open(out + "/LaplacianCurvature.wl", "w", encoding="utf-8").write(wl())
    json.dump(chunks(), open(out + "/chunks.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    print("ok")
