"""Assemble the Lab pages from template.html + core.js + app.js.

laplacian-curvature-lab.html  - artifact version (Wolfram via the mcp capability, TA via sample)
Laplacian_Curvature_Lab.html  - standalone version (CCN-KEY + LaplacianLabKernel for Wolfram and the TA)
"""
import os, pathlib
d = pathlib.Path(__file__).parent
t = (d / "template.html").read_text(encoding="utf-8")
t = t.replace("/*CORE*/", (d / "core.js").read_text(encoding="utf-8")).replace("/*APP*/", (d / "app.js").read_text(encoding="utf-8"))
(d / "laplacian-curvature-lab.html").write_text(t, encoding="utf-8")
SETTINGS = """<script>
/* ===== Settings =====
   WOLFRAM_URL: the LaplacianLabKernel URL (copy it from your Laplacian Lab version 2 file).
   MODEL: optional; leave "" to use the kernel's default.
   The CCN-KEY is typed into the page, never stored in this file. */
window.LAPLACIAN_LAB_CONFIG = { MODEL: "", WOLFRAM_URL: "%s" };
window.LAB_STANDALONE = true;
</script>
"""
# hosted copy (GitHub Pages) points at TUTUKernel; set CCN_WOLFRAM_URL="" for an empty-settings build
url = os.environ.get("CCN_WOLFRAM_URL", "https://www.wolframcloud.com/obj/ccn2/TUTUKernel")
s = t.replace("<title>Laplacian Curvature Lab</title>", "<title>Laplacian Curvature Lab</title>\n" + SETTINGS % url, 1)
(d / "Laplacian_Curvature_Lab.html").write_text(s, encoding="utf-8")
print("built", len(t.encode()), "and", len(s.encode()), "bytes")
