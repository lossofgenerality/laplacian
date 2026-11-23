"""Generate compact Wolfram verification code for groups of manual pages."""
import sys, re, json
sys.path.insert(0, '/home/claude/laplacian/tools'); sys.path.insert(0, '/home/claude/laplacian/tools/manual')
import importlib
from wlparse import statements, lhs_name

def strip(c):
    c = re.sub(r'\(\*.*?\*\)', '', c, flags=re.S)
    return re.sub(r'[ \t]*\n[ \t]*', ' ', c).strip()

def assigned_names(code):
    out = []
    for st in statements(code):
        s = strip(st)
        m = re.match(r'^\{([^}]*)\}\s*=(?!=)', s)
        if m: out += [x.strip() for x in m.group(1).split(',')]; continue
        n, k = lhs_name(st)
        if n and k == 'value': out.append(n)
    return out

def closure(defs, names, text):
    """defs: list of (name, stmt). Return stmts needed by text (transitively), in original order."""
    byname = {}
    for n, s in defs: byname.setdefault(n, []).append(s)
    need, todo = set(), [(text, True)]
    while todo:
        t, top = todo.pop()
        for n in byname:
            if not top and len(n) == 1: continue
            if n not in need and re.search(r'(?<![\w$])' + re.escape(n) + r'(?![\w$])', t):
                need.add(n); todo.extend((s, False) for s in byname[n])
    return [s for n, s in defs if n in need]

def example_code(inp, setup):
    names = sorted(set(assigned_names(setup) + assigned_names(inp)))
    body = (strip(setup) + ' ' if setup else '') + strip(inp)
    body = body.rstrip(';')
    return f'Block[{{{", ".join(names)}}}, {body}]' if names else body
