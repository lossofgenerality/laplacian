"""Build the site search index for both Labs, both manuals and every write-up.

python3 tools/build_search.py   ->  search-index.json (and search.html, which loads it)
Run after any write-up, manual or Lab rebuild. Reads ../laplacian-lab for the Programmable Lab.
"""
import re, json, html, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
LAB2 = ROOT.parent / 'laplacian-lab'
SITE = 'https://lossofgenerality.github.io/laplacian/'
SITE2 = 'https://lossofgenerality.github.io/Laplacian-lab/'


def text(h):
    h = re.sub(r'<(script|style|svg|annotation)[^>]*>.*?</\1>', ' ', h, flags=re.S)
    h = re.sub(r'<(br|p|li|tr|div|h\d)[^>]*>', ' ', h)
    h = re.sub(r'<[^>]+>', '', h)
    return re.sub(r'\s+', ' ', html.unescape(h)).strip()


entries = []


def add(source, title, section, url, body):
    body = body.strip()
    if body:
        entries.append({'s': source, 't': title, 'h': section, 'u': url, 'x': body})


# 1. Write-ups (pandoc HTML): one entry per h2/h3 section
def writeup(path, url):
    s = path.read_text(encoding='utf-8')
    title = text(re.search(r'<h1[^>]*>(.*?)</h1>', s, re.S).group(1))
    body = s[s.index('</h1>'):]
    parts = re.split(r'(<h[23][^>]*id="[^"]*"[^>]*>.*?</h[23]>)', body, flags=re.S)
    add('Write-up', title, 'Introduction', url, text(parts[0])[:4000])
    for i in range(1, len(parts), 2):
        hid = re.search(r'id="([^"]*)"', parts[i]).group(1)
        add('Write-up', title, text(parts[i]), url + '#' + hid, text(parts[i + 1])[:6000])


writeup(ROOT / 'docs/laplacian-curvature.html', SITE + 'docs/laplacian-curvature.html')
for p in sorted((ROOT / 'docs/series').glob('[0-9][0-9]-*.html')):
    writeup(p, SITE + 'docs/series/' + p.name)


# 1b. Glossary: one entry per term
g = (ROOT / 'docs/glossary.html').read_text(encoding='utf-8')
for m in re.finditer(r'<section class="g" id="([^"]+)"><h2>(.*?)</h2><p>(.*?)</p>', g, re.S):
    add('Glossary', 'Glossary', text(m.group(2)), SITE + 'docs/glossary.html#' + m.group(1), text(m.group(3)))


# 2. Manuals: one entry per reference page and per guide
def manual(path, base, name):
    s = path.read_text(encoding='utf-8')
    d = json.loads(re.search(r'<script id="data" type="application/json">(.*?)</script>', s, re.S).group(1).replace('<\\/', '</'))
    for g in d['guides']:
        add('Manual', name, 'Guide: ' + g['title'], base + '#/guide/' + g['id'], g.get('desc', ''))
    for slug, pg in d['pages'].items():
        bits = [' '.join(u) for u in pg.get('usage', [])] + pg.get('details', [])
        for sec in pg.get('examples', {}).values():
            for ex in sec:
                bits.append(ex.get('in', '')); bits.append(ex.get('text', '') or '')
        hand = pg.get('hand') or []
        if isinstance(hand, dict):
            hand = [hand.get('title', '')] + list(hand.get('steps', []))
        bits += [h if isinstance(h, str) else ' '.join(map(str, h)) for h in hand]
        add('Manual', name, pg['name'], base + '#/ref/' + slug, text(' '.join(map(str, bits)))[:6000])


manual(ROOT / 'manual.html', SITE + 'manual.html', 'Laplacian Curvature Lab manual')
if (LAB2 / 'manual.html').exists():
    manual(LAB2 / 'manual.html', SITE2 + 'manual.html', 'Laplacian Programmable Lab manual')


# 3. Labs: one entry per bench / section
def lab(path, base, name, prefix=''):
    s = path.read_text(encoding='utf-8')
    # menu labels: <a href="#id" ...><span class="n">5</span><span>Label</span></a>
    menu = {m.group(1): (m.group(2), text(m.group(3))) for m in
            re.finditer(r'<a href="#([a-z0-9-]+)"[^>]*><span class="n">([^<]*)</span><span>(.*?)</span></a>', s)}
    for k, m in enumerate(re.finditer(r'<section([^>]*)id="([a-z0-9-]+)"([^>]*)>(.*?)</section>', s, re.S), 1):
        attrs, sid, inner = m.group(1) + m.group(3), m.group(2), m.group(4)
        hid = sid[len(prefix):]
        hm = re.search(r'<h[12][^>]*>(.*?)</h[12]>', inner, re.S)
        inner_h = text(hm.group(1)) if hm else ''
        num, label = menu.get(hid, (str(k), ''))
        if not label:
            dt = re.search(r'data-title="([^"]*)"', attrs)
            label = html.unescape(dt.group(1)) if dt else hid
        head = (num + '. ' if num and num.strip().isdigit() else '') + label + (' — ' + inner_h if inner_h and inner_h != label else '')
        add('Lab', name, head, base + '#' + hid, text(inner)[:6000])


lab(ROOT / 'lab/Laplacian_Curvature_Lab.html', SITE + 'lab/Laplacian_Curvature_Lab.html', 'Laplacian Curvature Lab')
if (LAB2 / 'index.html').exists():
    lab(LAB2 / 'index.html', SITE2, 'Laplacian Programmable Lab', prefix='m-')

(ROOT / 'search-index.json').write_text(json.dumps(entries, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')
print(len(entries), 'entries;', sum(len(e['x']) for e in entries) // 1000, 'k characters')
