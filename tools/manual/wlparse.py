"""Split Wolfram Language code into top-level statements and pick out definitions."""
import re

def statements(code):
    out, depth, i, start, n = [], 0, 0, 0, len(code)
    while i < n:
        c = code[i]
        if c == '"':
            i += 1
            while i < n and code[i] != '"':
                i += 2 if code[i] == '\\' else 1
        elif code.startswith('(*', i):
            j = code.find('*)', i + 2); i = (j + 1) if j >= 0 else n
        elif c in '[({':
            depth += 1
        elif c in '])}':
            depth -= 1
        elif depth == 0 and (c == ';' or (c == '\n' and not code[i - 1:i].strip() in ('', ',') and not re.match(r'\s*[\]\)\}]', code[i + 1:i + 40] or ''))):
            # newline ends a statement only when the next line does not continue it
            seg = code[start:i].strip()
            if c == '\n':
                nxt = code[i + 1:].lstrip(' ')
                if nxt[:1] in ('', ) or re.match(r'[\-\+\*/&|=<>.@,]', nxt[:1] or 'x') or seg.endswith(('=', ':=', '->', '&&', '||', ',', '+', '-', '*', '/', '@', '//')):
                    i += 1; continue
            if seg: out.append(seg)
            start = i + 1
        i += 1
    seg = code[start:].strip()
    if seg: out.append(seg)
    return out

def strip_comments(s):
    return re.sub(r'\(\*.*?\*\)', '', s, flags=re.S).strip()

def lhs_name(stmt):
    s = strip_comments(stmt)
    m = re.match(r'^(?:ClearAll\[.*?\];\s*)?([^\s\[\]=;(){},."@]+)\s*(\[[\s\S]*?\])?\s*(:=|=)(?!=)', s)
    if not m: return None, None
    return m.group(1), ('func' if m.group(2) else 'value')
