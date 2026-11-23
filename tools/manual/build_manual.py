"""Generic builder: one standalone HTML programmer's manual in the style of a documentation center.

build(spec, defs, outputs, images, out_path, brand)
  spec     module with TITLE, SUBTITLE, GUIDES, P, REPO, SITE, LAB
  defs     dict name -> source text (Definition section)
  outputs  dict "name#k" -> InputForm text
  images   dict key -> path to PNG
"""
import json, base64, re, html, unicodedata

TRANS = {'κ': 'kappa', 'Δ': 'Delta', 'μ': 'mu', 'Γ': 'Gamma', 'λ': 'lambda', 'ω': 'omega', 'φ': 'phi', 'θ': 'theta',
         '𝒶': 'a', '𝓇': 'r', 'ℊ': 'g', '𝓈': 's', '𝒹': 'd', '𝒞': 'C', 'ℋ': 'H', '𝜟': 'ItalicDelta', '𝓍': 'x', '⊗': 'CircleTimes'}

def slug(name):
    s = ''.join(TRANS.get(c, c) for c in name)
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode()
    return re.sub(r'[^A-Za-z0-9]+', '-', s).strip('-') or 'sym'

def clean_out(o):
    o = re.sub(r'`[0-9.]*(?=\*\^)', '', o)
    o = re.sub(r'`[0-9.]+', '', o)
    return o

def build(spec, defs, outputs, images, out_path, brand):
    pages = {}
    for name, p in spec.P.items():
        exs, k = {}, 0
        for sec, lst in p['examples'].items():
            rows = []
            for inp, out in lst:
                k += 1
                key = f'{name}#{k}'
                if isinstance(out, str) and out.startswith('IMG:'):
                    with open(images[out[4:]], 'rb') as f:
                        rows.append({'in': inp, 'img': 'data:image/png;base64,' + base64.b64encode(f.read()).decode()})
                else:
                    o = outputs.get(key)
                    if o is None: raise SystemExit('missing output ' + key)
                    rows.append({'in': inp, 'out': clean_out(o)})
            exs[sec] = rows
        pages[name] = {'name': name, 'slug': slug(name), 'guide': p['guide'], 'defined': p['defined'], 'kind': p.get('kind', 'Function'),
                       'usage': p['usage'], 'details': p['details'], 'examples': exs, 'see': [s for s in p['see'] if s in spec.P],
                       'source': defs.get(name, '')}
    slugs = [v['slug'] for v in pages.values()]
    assert len(slugs) == len(set(slugs)), 'slug clash'
    for g in spec.GUIDES:
        for f in g[3]: assert f in pages, ('guide lists unknown', f)
    missing = [n for n in pages if not any(n in g[3] for g in spec.GUIDES)]
    assert not missing, missing
    data = {'title': spec.TITLE, 'subtitle': spec.SUBTITLE, 'repo': spec.REPO, 'site': spec.SITE, 'lab': spec.LAB,
            'intro': getattr(spec, 'INTRO', ''), 'labname': getattr(spec, 'LABNAME', spec.TITLE),
            'guides': [{'id': g[0], 'title': g[1], 'desc': g[2], 'fns': g[3]} for g in spec.GUIDES],
            'pages': pages, 'brand': brand}
    js = json.dumps(data, ensure_ascii=False).replace('</', '<\\/')
    doc = TEMPLATE.replace('__TITLE__', html.escape(spec.TITLE + ' — Programmer’s Manual')).replace('__DATA__', js)
    open(out_path, 'w', encoding='utf-8').write(doc)
    return len(pages), len(doc)

TEMPLATE = r'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
<style>
:root{--ink:#1d1d1f;--muted:#5f6368;--paper:#ffffff;--wash:#f6f5f2;--rule:#dedcd6;--accent:#d4561c;--accent2:#f7a440;--link:#1f5fa8;--code:#fbfaf7;--codeink:#20242a;--in:#9a3f12;--out:#5f6368;--head:#2b2b2e}
*{box-sizing:border-box}
html,body{margin:0;background:var(--paper);color:var(--ink);font:15px/1.55 "Source Sans 3","Segoe UI",Helvetica,Arial,sans-serif}
a{color:var(--link);text-decoration:none}a:hover{text-decoration:underline}
code,pre,.mono{font-family:"Source Code Pro",Menlo,Consolas,"DejaVu Sans Mono",monospace}
header.top{position:sticky;top:0;z-index:10;background:var(--head);color:#fff;display:flex;align-items:center;gap:18px;padding:0 22px;height:52px;box-shadow:0 1px 0 rgba(0,0,0,.2)}
header.top .logo{display:flex;align-items:center;gap:10px;color:#fff;font-weight:600;letter-spacing:.2px;white-space:nowrap}
header.top .logo .mark{width:26px;height:26px;border-radius:5px;background:linear-gradient(135deg,var(--accent),var(--accent2));display:grid;place-items:center;font:700 13px/1 Georgia,serif;color:#fff}
header.top .logo small{font-weight:400;opacity:.7;margin-left:4px}
header.top nav{display:flex;gap:16px;font-size:14px}
header.top nav a{color:#e9e6df}
header.top .search{margin-left:auto;position:relative}
header.top input{width:280px;border:0;border-radius:4px;padding:7px 10px 7px 30px;font:14px inherit;background:#fff;color:var(--ink)}
header.top .search:before{content:"⌕";position:absolute;left:10px;top:4px;color:#777;font-size:17px}
#results{position:absolute;right:0;top:38px;width:420px;max-height:60vh;overflow:auto;background:#fff;color:var(--ink);border:1px solid var(--rule);border-radius:6px;box-shadow:0 8px 28px rgba(0,0,0,.18);display:none}
#results a{display:block;padding:7px 12px;border-bottom:1px solid #f0eee9;color:var(--ink)}#results a:hover,#results a.on{background:#fdf1e8;text-decoration:none}
#results b{font-family:"Source Code Pro",Menlo,monospace;color:var(--accent)}#results span{display:block;font-size:12.5px;color:var(--muted);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.crumbs{background:var(--wash);border-bottom:1px solid var(--rule);font-size:13px;color:var(--muted);padding:7px 22px;display:flex;gap:6px;align-items:center;flex-wrap:wrap}
.crumbs .sep{opacity:.5}
.crumbs .right{margin-left:auto;display:flex;gap:14px}
main{max-width:1020px;margin:0 auto;padding:22px 28px 60px}
.reftype{display:flex;align-items:center;gap:12px;margin:6px 0 2px}
.tag{font:600 11px/1 "Source Sans 3",Arial,sans-serif;letter-spacing:1.6px;text-transform:uppercase;color:var(--accent);border:1px solid var(--accent);padding:4px 7px;border-radius:3px}
.tag.snip{color:#7a4bb0;border-color:#7a4bb0}.tag.api{color:#1f7a58;border-color:#1f7a58}.tag.val{color:#1f5fa8;border-color:#1f5fa8}
h1.sym{font:600 38px/1.15 "Source Code Pro",Menlo,monospace;margin:8px 0 14px;color:#111;word-break:break-all}
.usage{border-top:2px solid var(--accent);border-bottom:1px solid var(--rule);margin:0 0 18px}
.usage .row{display:grid;grid-template-columns:minmax(220px,auto) 1fr;gap:22px;padding:13px 4px;border-bottom:1px solid #eeece7}
.usage .row:last-child{border-bottom:0}
.usage .tpl{font-family:"Source Code Pro",Menlo,monospace;font-size:15px;white-space:nowrap}
.usage .tpl b{font-weight:700}.usage .tpl i{font-family:Georgia,"Times New Roman",serif;font-style:italic;font-size:16px;color:#333}
.usage .txt{color:#333}
details.sec{border-top:1px solid var(--rule);margin:0}
details.sec>summary{list-style:none;cursor:pointer;padding:12px 4px;font:600 19px/1.3 "Source Sans 3",Arial,sans-serif;color:#222;display:flex;align-items:center;gap:10px}
details.sec>summary::-webkit-details-marker{display:none}
details.sec>summary:before{content:"";width:0;height:0;border-left:7px solid var(--accent);border-top:5px solid transparent;border-bottom:5px solid transparent;transition:transform .15s}
details.sec[open]>summary:before{transform:rotate(90deg)}
details.sec>summary .n{font-weight:400;color:var(--muted);font-size:15px}
.detail-list{margin:0 0 16px 22px;padding:0}
.detail-list li{margin:7px 0;padding-left:6px}
details.sub{margin:0 0 6px 18px}
details.sub>summary{list-style:none;cursor:pointer;padding:8px 0;font:600 16px "Source Sans 3",Arial,sans-serif;color:#333;display:flex;gap:9px;align-items:center}
details.sub>summary::-webkit-details-marker{display:none}
details.sub>summary:before{content:"";border-left:6px solid #999;border-top:4px solid transparent;border-bottom:4px solid transparent;transition:transform .15s}
details.sub[open]>summary:before{transform:rotate(90deg)}
details.sub>summary .n{font-weight:400;color:var(--muted);font-size:14px}
.cell{display:grid;grid-template-columns:76px 1fr;gap:0 10px;margin:6px 0 14px 4px}
.cell .lab{font:italic 12.5px/1.9 Georgia,serif;color:var(--in);text-align:right;padding-top:6px;white-space:nowrap}
.cell .lab.o{color:var(--out)}
.cell pre{margin:0;padding:8px 12px;background:var(--code);border:1px solid #ecebe6;border-radius:4px;font-size:13.6px;line-height:1.55;white-space:pre-wrap;word-break:break-word;color:var(--codeink);position:relative}
.cell pre.in{border-left:3px solid var(--accent2)}
.cell pre.out{background:#fff;border-color:#f0efea}
.cell .img{padding:6px 0}.cell .img img{max-width:100%;border:1px solid #f0efea;border-radius:4px;background:#fff}
.copy{position:absolute;right:6px;top:5px;font:11px "Source Sans 3",Arial;background:#fff;border:1px solid var(--rule);color:var(--muted);border-radius:3px;padding:1px 7px;cursor:pointer;opacity:0;transition:opacity .15s}
pre:hover .copy{opacity:1}
pre .fn{color:var(--link);font-weight:600}pre .str{color:#1d7a4a}pre .cmt{color:#8a8a8a;font-style:italic}pre .num{color:#7a3fb0}
.src pre{margin:4px 0 16px;padding:12px 14px;background:#2a2b2f;color:#eee9df;border-radius:5px;font-size:13px;line-height:1.55;white-space:pre-wrap;word-break:break-word}
.src pre .fn{color:#ffb36b}.src pre .str{color:#a8d98a}.src pre .cmt{color:#9a9a9a}.src pre .num{color:#d4b3ff}
.src .note{font-size:13px;color:var(--muted);margin:0 0 4px}
.see{display:flex;flex-wrap:wrap;gap:6px 18px;margin:4px 0 18px 4px;font-family:"Source Code Pro",Menlo,monospace;font-size:14px}
.see a:after{content:"";}
.hist{margin:4px 0 18px 4px;color:#444}
.guides{margin:4px 0 18px 4px}
footer{border-top:1px solid var(--rule);margin-top:34px;padding-top:14px;font-size:12.5px;color:var(--muted);display:flex;justify-content:space-between;flex-wrap:wrap;gap:8px}
/* home & guide */
.hero{background:linear-gradient(120deg,#2b2b2e 0%,#3a3530 60%,#5a3a22 100%);color:#fff;border-radius:8px;padding:30px 32px;margin:0 0 26px}
.hero h1{margin:0 0 6px;font:600 30px/1.2 "Source Sans 3",Arial,sans-serif}
.hero p{margin:0;opacity:.85;max-width:720px}
.hero .meta{margin-top:14px;font-size:13px;opacity:.75}
.hero .meta a{color:#ffd2a8}
.tiles{display:grid;grid-template-columns:repeat(auto-fill,minmax(290px,1fr));gap:16px}
.tile{border:1px solid var(--rule);border-radius:7px;padding:16px 18px;background:#fff;transition:box-shadow .15s,border-color .15s;display:block;color:var(--ink)}
.tile:hover{border-color:var(--accent2);box-shadow:0 4px 16px rgba(212,86,28,.12);text-decoration:none}
.tile h3{margin:0 0 6px;font-size:17px;color:#222}
.tile p{margin:0 0 10px;font-size:13.5px;color:var(--muted)}
.tile .fns{font:12.5px/1.6 "Source Code Pro",Menlo,monospace;color:var(--link)}
.gtitle{font:600 32px/1.2 "Source Sans 3",Arial,sans-serif;margin:8px 0 8px}
.gdesc{color:#333;max-width:820px;margin:0 0 18px}
.glist{border-top:2px solid var(--accent)}
.glist .r{display:grid;grid-template-columns:230px 1fr;gap:18px;padding:9px 4px;border-bottom:1px solid #eeece7}
.glist .r a{font-family:"Source Code Pro",Menlo,monospace;font-weight:600}
.glist .r span{color:#444;font-size:14px}
.idx h2{font:600 20px "Source Sans 3",Arial;border-bottom:1px solid var(--rule);margin:22px 0 8px;padding-bottom:4px;color:var(--accent)}
.idx .cols{columns:3 240px;column-gap:28px}
.idx .cols a{display:block;font-family:"Source Code Pro",Menlo,monospace;font-size:14px;padding:2px 0;break-inside:avoid}
.idx .cols a small{font-family:"Source Sans 3",Arial;color:var(--muted);font-size:12px;margin-left:6px}
.stats{display:flex;gap:26px;margin:0 0 22px;color:var(--muted);font-size:13.5px}
.stats b{display:block;font-size:24px;color:var(--ink)}
/* CCN: always-visible scrollbars (macOS/iPadOS hide overlay scrollbars) + tab-strip arrows */::-webkit-scrollbar{width:11px;height:11px}::-webkit-scrollbar-track{background:rgba(127,127,127,.12);border-radius:8px}::-webkit-scrollbar-thumb{background:rgba(127,127,127,.55);border-radius:8px;border:2px solid transparent;background-clip:padding-box}::-webkit-scrollbar-thumb:hover{background:rgba(212,86,28,.75);background-clip:padding-box}*{scrollbar-width:auto;scrollbar-color:rgba(127,127,127,.6) rgba(127,127,127,.12)}.hs-wrap{position:relative;display:flex;align-items:stretch;min-width:0}.hs-wrap>.hs-strip{flex:1 1 auto;min-width:0}.hs-btn{flex:none;width:30px;border:1px solid rgba(127,127,127,.35);background:inherit;color:inherit;font:600 18px/1 system-ui,sans-serif;cursor:pointer;border-radius:6px;margin:2px 3px 10px;opacity:.85}.hs-btn:hover{opacity:1;border-color:#d4561c;color:#d4561c}.hs-btn[disabled]{opacity:.25;cursor:default}.hs-wrap:not(.hs-over)>.hs-btn{display:none}.hs-wrap:not(.hs-over){display:contents}
@media (max-width:720px){header.top input{width:150px}header.top nav{display:none}.usage .row,.glist .r{grid-template-columns:1fr;gap:4px}.cell{grid-template-columns:1fr}.cell .lab{text-align:left;padding:0}#results{width:300px}h1.sym{font-size:28px}}
@media print{header.top,.crumbs .right,.copy{display:none}details.sec,details.sub{display:block}}
</style>
</head>
<body>
<header class="top">
  <a class="logo" href="#/"><span class="mark">C</span><span id="brandname"></span><small>Documentation</small></a>
  <nav><a href="#/">Home</a><a href="#/index">Index</a><a id="lablink" target="_blank" rel="noopener">Open the Lab ↗</a><a id="repolink" target="_blank" rel="noopener">Source ↗</a></nav>
  <div class="search"><input id="q" placeholder="Search functions…" autocomplete="off" spellcheck="false"><div id="results"></div></div>
</header>
<div class="crumbs" id="crumbs"></div>
<main id="main"></main>
<script id="data" type="application/json">__DATA__</script>
<script>
const D = JSON.parse(document.getElementById('data').textContent);
const P = D.pages, NAMES = Object.keys(P);
const bySlug = {}; NAMES.forEach(n => bySlug[P[n].slug] = n);
const G = {}; D.guides.forEach(g => G[g.id] = g);
document.getElementById('brandname').textContent = D.brand;
document.getElementById('lablink').href = D.lab; document.getElementById('repolink').href = D.repo;
const esc = s => s.replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
function hl(code, self) {
  // tokenise: comments, strings, our names, numbers
  let out = '', i = 0;
  const re = /\(\*[\s\S]*?\*\)|"(?:[^"\\]|\\.)*"|[\p{L}$][\p{L}\p{N}$]*|\d+\.?\d*(?:\*\^-?\d+)?/gu;
  let m;
  while ((m = re.exec(code))) {
    out += esc(code.slice(i, m.index)); const t = m[0]; i = m.index + t.length;
    if (t.startsWith('(*')) out += '<span class="cmt">' + esc(t) + '</span>';
    else if (t[0] === '"') out += '<span class="str">' + esc(t) + '</span>';
    else if (/^\d/.test(t)) out += '<span class="num">' + esc(t) + '</span>';
    else if (P[t] && t !== self && !/^[\p{L}\p{N}$]/u.test(code[m.index - 1] || ' ')) out += '<a class="fn" href="#/ref/' + P[t].slug + '">' + esc(t) + '</a>';
    else if (P[t]) out += '<span class="fn">' + esc(t) + '</span>';
    else out += esc(t);
  }
  return out + esc(code.slice(i));
}
function tpl(t) {
  // name[args] -> bold name, italic argument identifiers
  const m = t.match(/^([^\[]+)(\[[\s\S]*)?$/u);
  if (!m) return esc(t);
  let rest = m[2] || '';
  rest = esc(rest).replace(/(^|[\[\s,{(+−*/^=&;])([\p{L}][\p{L}\p{N}]*)/gu, (a, p, id) => P[id] ? p + '<a href="#/ref/' + P[id].slug + '"><b>' + id + '</b></a>' : (/^(Graph|True|False|All|None|Automatic)$/.test(id) ? p + id : p + '<i>' + id + '</i>'));
  return '<b>' + esc(m[1]) + '</b>' + rest;
}
const SUBRE = /(?<![A-Za-z0-9\u0370-\u03FF])([A-Za-z\u0370-\u03FF])_(\{[^}]*\}|[A-Za-z0-9\u0370-\u03FF½ℝ³²]+)/gu;
const subs = h => h.replace(SUBRE, (m, b, x) => b + '<sub>' + (x[0] === '{' ? x.slice(1, -1) : x) + '</sub>');
function inline(s) {
  return subs(esc(s)).replace(/(^|[\s(“"])([\p{L}][\p{L}\p{N}]*)(?=[\s,.;:)”"]|$)/gu, (a, p, id) => P[id] ? p + '<a class="mono" href="#/ref/' + P[id].slug + '">' + id + '</a>' : a);
}
function copyBtn() { return '<button class="copy" onclick="cp(this)">Copy</button>'; }
window.cp = b => { const t = b.parentNode.getAttribute('data-raw'); navigator.clipboard && navigator.clipboard.writeText(t); b.textContent = 'Copied'; setTimeout(() => b.textContent = 'Copy', 1200); };
function crumbs(parts) {
  document.getElementById('crumbs').innerHTML = '<a href="#/">' + esc(D.title) + '</a>' + parts.map(p => '<span class="sep">›</span>' + (p[1] ? '<a href="' + p[1] + '">' + esc(p[0]) + '</a>' : '<span>' + esc(p[0]) + '</span>')).join('') +
    '<span class="right"><a href="#/index">Function index</a><a href="' + D.lab + '" target="_blank" rel="noopener">' + esc(D.labname) + ' ↗</a></span>';
}
const foot = () => '<footer><span>© Computational Classnotes · CC BY-NC-SA 4.0</span><span>' + esc(D.title) + ' · Programmer’s Manual 1.0 · <a href="' + D.repo + '" target="_blank" rel="noopener">source</a></span></footer>';
function home() {
  crumbs([]);
  let n = NAMES.length, ex = 0; NAMES.forEach(k => Object.values(P[k].examples).forEach(l => ex += l.length));
  let h = '<section class="hero"><h1>' + esc(D.title) + ' · Programmer’s Manual</h1><p>' + esc(D.subtitle) + '</p>' + (D.intro ? '<p style="margin-top:10px">' + esc(D.intro) + '</p>' : '') +
    '<div class="meta">Every function defined in the code base has its own reference page. All examples were evaluated on a Wolfram Language kernel. · <a href="' + D.lab + '" target="_blank" rel="noopener">Open the Lab</a> · <a href="' + D.repo + '" target="_blank" rel="noopener">GitHub</a></div></section>';
  h += '<div class="stats"><div><b>' + n + '</b>reference pages</div><div><b>' + D.guides.length + '</b>guides</div><div><b>' + ex + '</b>verified examples</div></div>';
  h += '<div class="tiles">' + D.guides.map(g => '<a class="tile" href="#/guide/' + g.id + '"><h3>' + esc(g.title) + '</h3><p>' + esc(g.desc) + '</p><div class="fns">' + g.fns.slice(0, 8).map(esc).join(' · ') + (g.fns.length > 8 ? ' · …' : '') + '</div></a>').join('') + '</div>';
  return h + foot();
}
function guide(id) {
  const g = G[id]; if (!g) return notFound();
  crumbs([['Guides', '#/'], [g.title]]);
  let h = '<div class="reftype"><span class="tag val">Guide</span></div><div class="gtitle">' + esc(g.title) + '</div><p class="gdesc">' + inline(g.desc) + '</p><div class="glist">';
  h += g.fns.map(f => '<div class="r"><a href="#/ref/' + P[f].slug + '">' + esc(f) + '</a><span>' + inline(P[f].usage[0][1]) + '</span></div>').join('');
  h += '</div><h3 style="margin:28px 0 8px;font-size:17px">Related Guides</h3><div class="see">' + D.guides.filter(x => x.id !== id).map(x => '<a href="#/guide/' + x.id + '" style="font-family:inherit">' + esc(x.title) + '</a>').join('') + '</div>';
  return h + foot();
}
function ref(name) {
  const p = P[name]; if (!p) return notFound();
  const g = G[p.guide];
  crumbs([[g.title, '#/guide/' + g.id], [name]]);
  const tagc = p.kind.startsWith('Snippet') ? 'snip' : p.kind.startsWith('API') ? 'api' : p.kind.startsWith('Symbol') || p.kind.startsWith('Value') ? 'val' : '';
  let h = '<div class="reftype"><span class="tag ' + tagc + '">' + esc(p.kind) + '</span><span style="font-size:13px;color:var(--muted)">Defined in ' + esc(p.defined) + '</span></div>';
  h += '<h1 class="sym">' + esc(name) + '</h1><div class="usage">' + p.usage.map(u => '<div class="row"><div class="tpl">' + tpl(u[0]) + '</div><div class="txt">' + inline(u[1]) + '</div></div>').join('') + '</div>';
  if (p.details.length) h += '<details class="sec"><summary>Details and Options</summary><ul class="detail-list">' + p.details.map(d => '<li>' + inline(d) + '</li>').join('') + '</ul></details>';
  let total = 0; Object.values(p.examples).forEach(l => total += l.length);
  h += '<details class="sec" open><summary>Examples <span class="n">(' + total + ')</span></summary>';
  let n = 0, first = true;
  for (const [sec, rows] of Object.entries(p.examples)) {
    h += '<details class="sub"' + (first ? ' open' : '') + '><summary>' + esc(sec) + ' <span class="n">(' + rows.length + ')</span></summary>'; first = false;
    for (const r of rows) {
      n++;
      h += '<div class="cell"><div class="lab">In[' + n + ']:=</div><pre class="in" data-raw="' + esc(r.in) + '">' + hl(r.in, name) + copyBtn() + '</pre></div>';
      if (r.img) h += '<div class="cell"><div class="lab o">Out[' + n + ']=</div><div class="img"><img alt="Output of example ' + n + '" src="' + r.img + '"></div></div>';
      else h += '<div class="cell"><div class="lab o">Out[' + n + ']=</div><pre class="out" data-raw="' + esc(r.out) + '">' + hl(r.out, name) + copyBtn() + '</pre></div>';
    }
    h += '</details>';
  }
  h += '</details>';
  if (p.source) h += '<details class="sec src"><summary>Definition</summary><p class="note">CCN source, as defined in ' + esc(p.defined) + '.</p><pre>' + hl(p.source, name) + '</pre></details>';
  if (p.see.length) h += '<details class="sec" open><summary>See Also</summary><div class="see">' + p.see.map(s => '<a href="#/ref/' + P[s].slug + '">' + esc(s) + '</a>').join('<span style="color:#bbb">·</span>') + '</div></details>';
  h += '<details class="sec" open><summary>Related Guides</summary><div class="guides">▪ <a href="#/guide/' + g.id + '">' + esc(g.title) + '</a></div></details>';
  h += '<details class="sec" open><summary>History</summary><div class="hist">Introduced in 2026 (1.0)</div></details>';
  return h + foot();
}
function index() {
  crumbs([['Function index']]);
  const groups = {};
  NAMES.slice().sort((a, b) => a.localeCompare(b, 'en', {sensitivity: 'base'})).forEach(n => { let c = n.normalize('NFKD')[0].toUpperCase(); if (!/[A-Z]/.test(c)) c = 'Symbols'; (groups[c] = groups[c] || []).push(n); });
  let h = '<div class="gtitle">Function index</div><p class="gdesc">All ' + NAMES.length + ' reference pages, alphabetically.</p><div class="idx">';
  Object.keys(groups).sort((a, b) => a === 'Symbols' ? 1 : b === 'Symbols' ? -1 : a.localeCompare(b)).forEach(c => h += '<h2>' + c + '</h2><div class="cols">' + groups[c].map(n => '<a href="#/ref/' + P[n].slug + '">' + esc(n) + '<small>' + esc(G[P[n].guide].title) + '</small></a>').join('') + '</div>');
  return h + '</div>' + foot();
}
function notFound() { crumbs([['Not found']]); return '<p>Page not found. <a href="#/">Home</a></p>' + foot(); }
function route() {
  const h = location.hash.replace(/^#\/?/, ''); let html;
  if (!h) html = home();
  else if (h.startsWith('ref/')) html = ref(bySlug[h.slice(4)]);
  else if (h.startsWith('guide/')) html = guide(h.slice(6));
  else if (h === 'index') html = index();
  else html = notFound();
  document.getElementById('main').innerHTML = html; window.scrollTo(0, 0);
  const t = h.startsWith('ref/') && bySlug[h.slice(4)];
  document.title = (t ? t + ' — ' : '') + D.title + ' Programmer’s Manual';
}
window.addEventListener('hashchange', route); route();
// search
const q = document.getElementById('q'), R = document.getElementById('results'); let sel = 0, hits = [];
function search() {
  const s = q.value.trim().toLowerCase(); if (!s) { R.style.display = 'none'; return; }
  hits = NAMES.map(n => { const ln = n.toLowerCase(), sl = P[n].slug.toLowerCase(); let sc = ln === s || sl === s ? 0 : ln.startsWith(s) || sl.startsWith(s) ? 1 : ln.includes(s) || sl.includes(s) ? 2 : (P[n].usage.map(u => u[1]).join(' ') + ' ' + P[n].details.join(' ')).toLowerCase().includes(s) ? 3 : 9; return [sc, n]; })
    .filter(x => x[0] < 9).sort((a, b) => a[0] - b[0] || a[1].length - b[1].length).slice(0, 14).map(x => x[1]);
  sel = 0;
  R.innerHTML = hits.length ? hits.map((n, i) => '<a href="#/ref/' + P[n].slug + '" class="' + (i === sel ? 'on' : '') + '"><b>' + esc(n) + '</b><span>' + esc(P[n].usage[0][1]) + '</span></a>').join('') : '<a><span>No matches</span></a>';
  R.style.display = 'block';
}
q.addEventListener('input', search);
q.addEventListener('keydown', e => {
  if (e.key === 'ArrowDown' || e.key === 'ArrowUp') { e.preventDefault(); sel = (sel + (e.key === 'ArrowDown' ? 1 : -1) + hits.length) % hits.length; [...R.children].forEach((a, i) => a.classList.toggle('on', i === sel)); }
  if (e.key === 'Enter' && hits[sel]) { location.hash = '#/ref/' + P[hits[sel]].slug; R.style.display = 'none'; q.blur(); }
  if (e.key === 'Escape') { R.style.display = 'none'; q.blur(); }
});
R.addEventListener('click', () => { R.style.display = 'none'; q.value = ''; });
document.addEventListener('click', e => { if (!e.target.closest('.search')) R.style.display = 'none'; });
document.addEventListener('keydown', e => { if (e.key === '/' && document.activeElement !== q) { e.preventDefault(); q.focus(); } });
</script>
</body>
</html>
'''
