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

def nb():
    cells = []
    for style, text in CELLS:
        cells.append('Cell["%s", "%s"]' % (wl_escape(text), style))
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
    for style, text in CELLS:
        if style == "Input":
            lines += [text, ""]
        elif style in ("Title", "Section", "Subsection"):
            lines += ["(* ::%s:: *)" % ("Title" if style == "Title" else style), "(*%s*)" % text, ""]
        else:
            lines += ["(* ::Text:: *)", "(*%s*)" % text.replace("(*", "( *").replace("*)", "* )"), ""]
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
