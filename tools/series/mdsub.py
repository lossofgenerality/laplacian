"""Convert prose pseudo-subscripts X_Y / X_{Y} in markdown to inline LaTeX, outside $..$, $$..$$ and `code`."""
import re, sys
G = {'κ': r'\kappa', 'μ': r'\mu', 'Δ': r'\Delta', 'Σ': r'\Sigma', 'λ': r'\lambda', 'ω': r'\omega', 'α': r'\alpha', 'β': r'\beta',
     'ε': r'\varepsilon', 'ρ': r'\rho', 'π': r'\pi', 'lim': r'\lim', 'Γ': r'\Gamma', 'θ': r'\theta', 'φ': r'\varphi'}
SUBMAP = {'½': '1/2', 'ℝ³': r'\mathbb{R}^3', 'S²': 'S^2', 'j~i': r'j\sim i', 'α→1': r'\alpha\to 1'}
def tex_sub(s):
    if s in SUBMAP: return SUBMAP[s]
    if re.fullmatch(r'[A-Za-z]{3,}|[A-Z]{2,}[a-z]*', s): return r'\mathrm{%s}' % s
    return ''.join(G.get(c, c) + (' ' if c in G else '') for c in s).strip()
TOK = re.compile(r'([A-Za-zͰ-Ͽ]+|Δ|Σ)_(\{[^}]*\}|[A-Za-z0-9Ͱ-Ͽ½]+(?:³|²)?)')
XS = re.compile(r'([A-Za-z\u0370-\u03FF])ₓ')
def conv(seg):
    def f(m):
        b, s = m.group(1), m.group(2)
        s = s[1:-1] if s.startswith('{') else s
        base = G.get(b, b)
        return '$%s_{%s}$' % (base, tex_sub(s))
    seg = TOK.sub(f, seg)
    return XS.sub(lambda m: '$%s_{x}$' % G.get(m.group(1), m.group(1)), seg)
def process(text):
    parts = re.split(r'(\$\$.*?\$\$|\$[^$\n]+\$|`[^`]*`|\]\([^)]*\))', text, flags=re.S)
    return ''.join(p if i % 2 else conv(p) for i, p in enumerate(parts))
if __name__ == '__main__':
    for f in sys.argv[1:]:
        s = open(f, encoding='utf-8').read(); t = process(s)
        open(f, 'w', encoding='utf-8').write(t)
        print(f, sum(1 for _ in TOK.finditer(s)) )
