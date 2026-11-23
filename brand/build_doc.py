"""python3 brand/build_doc.py -> CCN-Brand-Strategy.html (self-contained, live 3D Fig. 8) and .pdf"""
import subprocess, re, base64, pathlib
B = pathlib.Path(__file__).resolve().parent
md = B / 'CCN-Brand-Strategy.md'
body = subprocess.run(['pandoc', str(md), '--mathml', '-t', 'html5'], capture_output=True, text=True, check=True).stdout
tok = (B / 'ccn-tokens.css').read_text(encoding='utf-8')
fonts = '\n'.join(l for l in tok.splitlines() if l.startswith('@font-face'))
fonts = re.sub(r'url\((fonts/[^)]+)\)', lambda m: 'url(data:font/woff2;base64,%s)' % base64.b64encode((B / m.group(1)).read_bytes()).decode(), fonts)
css = fonts + '\n' + (B / 'ccn-pdf.css').read_text(encoding='utf-8')
# bold "Fig. n." captions in Orange Ink
body = re.sub(r'<p><strong>(Fig\. \d+\.)</strong>', r'<p class="cap"><strong style="color:#a35206">\1</strong>', body)
def html(live):
    b = body
    for n in range(1, 9):
        b = b.replace('src="img/fig%d.png"' % n, 'src="data:image/png;base64,%s"' % base64.b64encode((B / f'img/fig{n}.png').read_bytes()).decode())
    js = ''
    if live:
        b = re.sub(r'(<figure>\s*)<img src="data:image/png;base64,[^"]+"[^>]*alt="Fig. 8"[^>]*>',
                   r'\1<canvas data-fig3d="ollivier-sphere" aria-label="Rotatable 3D figure: Ollivier sphere"></canvas><div class="fig3d-note">3D: drag to rotate</div>', b)
        js = '<script>%s</script>' % (B.parent / 'tools/series/fig3d.js').read_text(encoding='utf-8')
    screen = ('body{max-width:880px;margin:0 auto;padding:28px 22px 60px}'
              'canvas[data-fig3d]{width:100%;max-width:520px;height:440px;display:block;margin:6px auto;cursor:grab;touch-action:none}'
              '.fig3d-note{text-align:center;font-size:9pt;color:#566273}'
              '.wrap{overflow-x:auto}' if live else '')
    nav = ('<nav style="font-size:10pt;display:flex;gap:14px;margin-bottom:12px"><a href="CCN-Brand-Strategy.pdf">PDF</a>'
           '<a href="https://github.com/lossofgenerality/laplacian/blob/main/brand/CCN-Brand-Strategy.md">Markdown</a><a href="specimen.html">Live specimen</a></nav>') if live else ''
    foot = '<footer style="margin-top:30px;font-size:9pt;color:#566273">© Computational Classnotes · CC BY-NC-SA 4.0</footer>' if live else ''
    b = b.replace('<table>', '<div class="wrap"><table>').replace('</table>', '</table></div>')
    return ('<!DOCTYPE html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
            '<title>CCN Brand Strategy — Computational Classnotes</title><style>%s%s</style></head><body>%s%s%s%s</body></html>\n' % (css, screen, nav, b, foot, js))
(B / 'CCN-Brand-Strategy.html').write_text(html(True), encoding='utf-8')
tmp = pathlib.Path('/tmp/ccn-brand-print.html'); tmp.write_text(html(False), encoding='utf-8')
subprocess.run(['google-chrome', '--headless=new', '--no-sandbox', '--disable-gpu', '--no-pdf-header-footer',
                '--virtual-time-budget=4000', '--print-to-pdf=%s' % (B / 'CCN-Brand-Strategy.pdf'), 'file://' + str(tmp)],
               check=True, capture_output=True)
print('ok')
