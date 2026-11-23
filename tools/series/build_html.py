"""python3 tools/series/build_html.py docs/series/07-ollivier.md [more.md] -> .html next to each md (MathML, rotatable 3D figures)."""
import sys, subprocess, re, pathlib
JS = pathlib.Path('/home/claude/laplacian/tools/series/fig3d.js').read_text(encoding='utf-8')
CSS = pathlib.Path('/home/claude/laplacian/tools/pdf-style.css').read_text(encoding='utf-8')
SCREEN = '''
body{max-width:860px;margin:0 auto;padding:28px 22px 60px;background:#fff}
img{max-width:100%;height:auto}
canvas[data-fig3d]{width:100%;max-width:520px;height:440px;display:block;margin:6px auto;cursor:grab;touch-action:none}
.fig3d-note{text-align:center;font-size:9pt;color:#666;margin-top:-2px}
nav.wtop{font-size:10pt;margin-bottom:14px;display:flex;gap:14px;flex-wrap:wrap}
nav.wtop a{color:rgb(212,86,28)}
@media print{canvas[data-fig3d]{display:none}.fig3d-fallback{display:block!important}}
'''
FIG3D = {'img/ollivier-sphere.png': 'ollivier-sphere', 'img/be-sphere.png': 'be-sphere'}
for md in sys.argv[1:]:
    p = pathlib.Path(md)
    body = subprocess.run(['pandoc', str(p), '--mathml', '-t', 'html5'], capture_output=True, text=True, check=True).stdout
    title = re.search(r'^# (.+)$', p.read_text(encoding='utf-8'), re.M).group(1)
    for src, key in FIG3D.items():
        body = re.sub(r'<img src="%s"[^>]*>' % re.escape(src),
                      '<canvas data-fig3d="%s" aria-label="Rotatable 3D figure"></canvas><img class="fig3d-fallback" style="display:none" src="%s" alt="">'
                      '<div class="fig3d-note">3D: drag to rotate</div>' % (key, src), body)
    pdf = p.with_suffix('.pdf').name
    nav = '<nav class="wtop"><a href="%s">PDF</a><a href="https://github.com/lossofgenerality/laplacian/blob/main/%s">Markdown</a><a href="https://lossofgenerality.github.io/laplacian/lab/Laplacian_Curvature_Lab.html">Laplacian Curvature Lab</a><a href="https://lossofgenerality.github.io/laplacian/docs/series/">All write-ups</a><a href="https://lossofgenerality.github.io/laplacian/search.html">Search</a><a href="https://lossofgenerality.github.io/laplacian/docs/glossary.html">Glossary</a></nav>' % (pdf, str(p).replace('/home/claude/laplacian/', ''))
    html = ('<!DOCTYPE html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
            '<title>%s — Computational Classnotes</title><style>%s%s</style></head><body>%s%s'
            '<footer style="margin-top:30px;font-size:9pt;color:#666">© 2026 Computational Classnotes · CC BY-NC-SA 4.0</footer><script>%s</script></body></html>\n'
            % (title, CSS, SCREEN, nav, body, JS))
    out = p.with_suffix('.html'); out.write_text(html, encoding='utf-8'); print(out)
