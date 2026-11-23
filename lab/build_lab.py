"""Assemble laplacian-curvature-lab.html from template.html + core.js + app.js."""
import pathlib
d = pathlib.Path(__file__).parent
t = (d / "template.html").read_text(encoding="utf-8")
t = t.replace("/*CORE*/", (d / "core.js").read_text(encoding="utf-8")).replace("/*APP*/", (d / "app.js").read_text(encoding="utf-8"))
(d / "laplacian-curvature-lab.html").write_text(t, encoding="utf-8")
print(len(t.splitlines()), "lines,", len(t.encode()), "bytes")
