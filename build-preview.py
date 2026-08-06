"""
Build self-contained previews.

    python build-preview.py                     every page
    python build-preview.py home                one page
    python build-preview.py ministries/worship  a sub-page

Reads  pages/<path>/index.html
       shared/nspc-base.css  shared/nspc-chrome.css  shared/header.html  shared/footer.html
Writes pages/<path>/preview.html

Images are inlined as data URIs so previews render offline and inside an
Artifact, whose CSP blocks external hosts. Local files in the page's images/
folder win; a Squarespace CDN URL with no local counterpart is left alone.
"""
import base64, io, mimetypes, pathlib, re, sys

ROOT = pathlib.Path(__file__).parent
PAGES = ROOT / "pages"
SHARED = ROOT / "shared"


def data_uri(path: pathlib.Path, max_w: int = 1700) -> str:
    try:
        from PIL import Image
        im = Image.open(path).convert("RGB")
        if im.width > max_w:
            im = im.resize((max_w, round(im.height * max_w / im.width)), Image.LANCZOS)
        buf = io.BytesIO()
        im.save(buf, "JPEG", quality=80, optimize=True, progressive=True)
        return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()
    except Exception:
        mime = mimetypes.guess_type(path.name)[0] or "image/png"
        return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode()


def build(rel: str) -> pathlib.Path | None:
    page = PAGES / rel / "index.html"
    if not page.exists():
        print(f"  skip (no index.html): {rel}")
        return None

    html = page.read_text(encoding="utf-8")
    imgdir = PAGES / rel / "images"
    slug = pathlib.Path(rel).name
    cache: dict[str, str] = {}

    def local(name: str):
        if name not in cache:
            p = imgdir / name
            if not p.exists():
                return None
            cache[name] = data_uri(p)
        return cache[name]

    def swap(m: re.Match) -> str:
        tag = m.group(0)
        src = re.search(r'src="([^"]*)"', tag)
        if not src:
            return tag
        val = src.group(1)

        # a PHOTO SLOT comment just above may name a specific local file
        before = html[max(0, m.start() - 400):m.start()]
        named = re.findall(r"PHOTO SLOT[^\n]*?([\w\-]+\.(?:jpg|jpeg|png|webp))", before, re.I)

        uri = None
        for cand in (named[-1] if named else None, pathlib.Path(val).name, "hero.jpg"):
            if cand:
                uri = local(cand)
                if uri:
                    break
        return tag.replace(val, uri) if uri else tag

    html = re.sub(r"<img\b[^>]*>", swap, html)

    css = (SHARED / "nspc-base.css").read_text(encoding="utf-8")
    chrome = (SHARED / "nspc-chrome.css").read_text(encoding="utf-8")
    header = (SHARED / "header.html").read_text(encoding="utf-8")
    footer = (SHARED / "footer.html").read_text(encoding="utf-8")

    # the header/footer logo is a remote Squarespace URL — inline it if we have it
    logo = ROOT / "pages" / "home" / "images" / "logo.png"
    if logo.exists():
        uri = data_uri(logo, 400)
        header = re.sub(r'src="https://images\.squarespace-cdn\.com[^"]*"', f'src="{uri}"', header)
        footer = re.sub(r'src="https://images\.squarespace-cdn\.com[^"]*"', f'src="{uri}"', footer)

    title = slug.replace("-", " ").title()
    out = PAGES / rel / "preview.html"
    out.write_text(
        f"<title>NSPC — {title}</title>\n"
        f'<script>document.documentElement.setAttribute("data-page","{slug}");</script>\n'
        f"<style>\n{css}\n{chrome}\n"
        "body{margin:0;background:#FDF9F0}\n"
        "</style>\n"
        f"{header}\n{html}\n{footer}\n",
        encoding="utf-8",
    )
    print(f"  {out.relative_to(ROOT)}  ({out.stat().st_size/1048576:.2f} MB)")
    return out


def all_pages():
    return sorted(str(p.parent.relative_to(PAGES)).replace("\\", "/")
                  for p in PAGES.glob("**/index.html"))


if __name__ == "__main__":
    targets = sys.argv[1:] or all_pages()
    print(f"building {len(targets)} preview(s)")
    for t in targets:
        build(t.strip("/"))
