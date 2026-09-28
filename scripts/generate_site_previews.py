from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
OUT = ASSETS / "previews"
OUT.mkdir(parents=True, exist_ok=True)

ITEMS = [
    ("field-sampling.webp", "field-sampling.webp", 1920, "WEBP", 94),
    ("field-sampling-riverbank.jpg", "field-sampling-riverbank.webp", 1400, "WEBP", 90),
    ("field-camp-aerial.jpg", "field-camp-aerial.webp", 1400, "WEBP", 90),
    ("live-imaging-phoxinus-isetensis.jpg", "live-imaging-phoxinus-isetensis.jpg", 2000, "JPEG", 95),
    ("live-imaging-barbatula-sp.jpg", "live-imaging-barbatula-sp.jpg", 2000, "JPEG", 95),
    ("field-river-landscape-aerial.jpg", "field-river-landscape-aerial.webp", 1400, "WEBP", 90),
    ("field-basecamp-mountains.jpg", "field-basecamp-mountains.webp", 1400, "WEBP", 90),
    ("field-river-meander.jpg", "field-river-meander.webp", 1400, "WEBP", 90),
]

for src_name, dst_name, max_edge, fmt, quality in ITEMS:
    src = ASSETS / src_name
    dst = OUT / dst_name
    with Image.open(src) as im:
        im = ImageOps.exif_transpose(im)
        if max(im.size) > max_edge:
            im.thumbnail((max_edge, max_edge), Image.Resampling.LANCZOS)

        if fmt == "JPEG":
            if im.mode not in ("RGB", "L"):
                im = im.convert("RGB")
            im.save(
                dst,
                format="JPEG",
                quality=quality,
                subsampling=0,
                optimize=True,
                progressive=True,
            )
        elif fmt == "WEBP":
            if im.mode not in ("RGB", "RGBA"):
                im = im.convert("RGB")
            im.save(
                dst,
                format="WEBP",
                quality=quality,
                method=6,
            )
        else:
            raise ValueError(fmt)

        print(f"{src_name}: {src.stat().st_size} -> {dst.stat().st_size} bytes; {im.size}")
