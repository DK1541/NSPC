"""
Regenerate the Squarespace paste file.

    python build-standalone.py

Reads  index.html  +  images/
Writes shared_kitchen_page.html   (images inlined as base64)

Two differences from index.html, both deliberate:

  * images become data URIs, because a Squarespace Code Block cannot reach
    this repo's images/ folder;
  * the PAGES-ONLY robots meta is dropped. That noindex exists to keep the
    GitHub Pages copy from competing with the real page at
    northshorepres.org/shared-kitchen, and must never reach Squarespace.

See HANDOFF.md §6 before changing any color or font in index.html.
"""
import base64, pathlib, re

ROOT = pathlib.Path(__file__).parent
html = (ROOT / "index.html").read_text(encoding="utf-8")

for img in sorted((ROOT / "images").iterdir()):
    mime = "image/png" if img.suffix == ".png" else "image/jpeg"
    uri = f"data:{mime};base64," + base64.b64encode(img.read_bytes()).decode()
    marker = f'src="images/{img.name}"'
    if marker not in html:
        print(f"  unused: {img.name}")
        continue
    html = html.replace(marker, f'src="{uri}"')

html, n = re.subn(r'^.*<!-- PAGES-ONLY -->\n', "", html, flags=re.M)
if n != 1:
    raise SystemExit(f"expected 1 PAGES-ONLY line to strip, found {n}")

if "images/" in html:
    raise SystemExit("an image reference survived — check the filenames")

out = ROOT / "shared_kitchen_page.html"
out.write_text(html, encoding="utf-8")
print(f"  {out.name}  ({out.stat().st_size/1048576:.2f} MB)")
