"""
Build a self-contained preview of a page.

    python build-preview.py home
    python build-preview.py covenant-family

Reads  pages/<section>/index.html  +  shared/nspc-base.css
Writes pages/<section>/preview.html

Swaps every Squarespace CDN URL for a local image inlined as a data URI, so the
preview renders offline and inside an Artifact (whose CSP blocks external hosts).

Local images are matched by the PHOTO SLOT comment immediately above each <img>:
a comment naming a file in pages/<section>/images/ wins; otherwise the first
image named worship-hero.* is used as the fallback.
"""
import base64, io, mimetypes, pathlib, re, sys

ROOT = pathlib.Path(__file__).parent


def data_uri(path: pathlib.Path, max_w: int = 1800) -> str:
    """Inline an image, downscaling and re-encoding to JPEG when Pillow is present."""
    try:
        from PIL import Image
        im = Image.open(path)
        im = im.convert("RGB")
        if im.width > max_w:
            im = im.resize((max_w, round(im.height * max_w / im.width)), Image.LANCZOS)
        buf = io.BytesIO()
        im.save(buf, "JPEG", quality=82, optimize=True, progressive=True)
        return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()
    except Exception:
        mime = mimetypes.guess_type(path.name)[0] or "image/png"
        return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode()


def build(section: str) -> pathlib.Path:
    page = ROOT / "pages" / section / "index.html"
    if not page.exists():
        sys.exit(f"no such page: {page}")

    css = (ROOT / "shared" / "nspc-base.css").read_text(encoding="utf-8")
    html = page.read_text(encoding="utf-8")
    imgdir = ROOT / "pages" / section / "images"

    fallback = next((p for p in imgdir.glob("worship-hero.*")), None) if imgdir.exists() else None
    cache: dict[str, str] = {}

    def resolve(name: str) -> str | None:
        if name not in cache:
            p = imgdir / name
            if not p.exists():
                return None
            cache[name] = data_uri(p)
        return cache[name]

    # Walk every <img>, look backwards for a PHOTO SLOT comment naming a local file.
    def swap(m: re.Match) -> str:
        tag = m.group(0)
        before = html[max(0, m.start() - 400):m.start()]
        named = re.findall(r"PHOTO SLOT[^\n]*?([\w\-]+\.(?:jpg|jpeg|png|webp))", before, re.I)
        uri = resolve(named[-1]) if named else None
        if uri is None and fallback is not None:
            uri = cache.setdefault("__fallback__", data_uri(fallback))
        if uri is None:
            return tag
        return re.sub(r'src="[^"]*"', lambda _: f'src="{uri}"', tag, count=1)

    html = re.sub(r"<img\b[^>]*>", swap, html)

    out = ROOT / "pages" / section / "preview.html"
    out.write_text(
        f"<title>NSPC — {section.replace('-', ' ').title()}</title>\n"
        f"<style>\n{css}\n"
        "body{margin:0;background:#FBF8F2}\n"
        ".nspc-sqsp-note{font:600 .7rem/1 'Segoe UI',system-ui,sans-serif;letter-spacing:.16em;"
        "text-transform:uppercase;color:#9A9288;background:#fff;border-bottom:1px solid #E4DDD0;"
        "padding:.85rem 1.5rem;text-align:center}\n"
        "</style>\n"
        "<p class=\"nspc-sqsp-note\">Preview · Squarespace supplies the logo and navigation above this</p>\n"
        + html,
        encoding="utf-8",
    )
    print(f"{out}  ({out.stat().st_size/1048576:.2f} MB)")
    return out


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    for s in sys.argv[1:]:
        build(s)
