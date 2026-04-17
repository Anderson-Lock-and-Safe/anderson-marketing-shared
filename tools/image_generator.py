#!/usr/bin/env python3
"""
Local-only branded tile generator (Pillow fallback to Canva).

Produces consistent, on-brand social graphics when Canva templates aren't
available or the agent wants a no-network option. Renders tip cards, stat
cards, numbered lists, before/after splits, and Q&A cards as 1080x1080
(IG feed), 1080x1350 (IG portrait), or 1080x1920 (IG reel/story) PNGs.

Reads brand tokens from brand/style_guide.md (YAML front-matter) so the
same tokens drive both Canva and local renders. Tokens include:
    primary_hex, secondary_hex, dark_hex, light_blue_hex, lighter_blue_hex,
    gray_hex, light_gray_hex, lightest_gray_hex, background_hex,
    text_hex, text_light_hex, cta_red_hex,
    display_font_family (Burlingame Pro), headline_font_family (FS Silas Slab),
    body_font_family (Sans Beam), plus *_alt free-font fallbacks
    (Saira, Zilla Slab, Lexend).

Fonts: falls back to Google-font alternatives, then system fonts if the
branded families aren't installed.

Usage:
    python tools/image_generator.py tip-card --headline "Key control is a chain of custody" \\
        --body "Every duplicate key is a signature you owe someone." \\
        --size 1080x1080 --out out.png

    python tools/image_generator.py stat-card --stat "60+" \\
        --label "Years securing Phoenix businesses" --out out.png

    python tools/image_generator.py before-after --before in/before.jpg \\
        --after in/after.jpg --label "Rekey for a new property manager" --out out.png

    python tools/image_generator.py qa-card --question "When should you rekey?" \\
        --answer "Any time keys stop being accounted for." --out out.png

    python tools/image_generator.py numbered-list --title "3 signs you need a master key overhaul" \\
        --items "Keys nobody can account for" "Terminated staff never returning keys" \\
        "Vendors holding old building keys" --out out.png

All subcommands accept --size, --watermark / --no-watermark, --palette {dark|light}.
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Tuple

try:
    from PIL import Image, ImageDraw, ImageFont, ImageFilter
except ImportError:
    print("Pillow not installed. Run: .venv/bin/pip install Pillow", file=sys.stderr)
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent
STYLE_GUIDE = ROOT / "brand" / "style_guide.md"
BRAND_DIR = ROOT / "brand"


# ---------- brand tokens ----------


_DEFAULTS = {
    "primary_hex": "#0045DB",       # Primary Blue (Pantone 286 C)
    "secondary_hex": "#0F2CC9",     # Secondary Blue (Pantone Blue 072 C)
    "dark_hex": "#141A2E",          # Deep Navy (Pantone 289 C) — body text on light
    "light_blue_hex": "#6C95F5",    # Mid Blue (Pantone 2727 C)
    "lighter_blue_hex": "#BBDAFF",  # Sky Blue (Pantone 278 C)
    "gray_hex": "#838D96",          # Gray (Pantone 4137 C)
    "light_gray_hex": "#C1CCD3",    # Light Gray (Pantone 7543 C)
    "lightest_gray_hex": "#DFE8ED", # Lightest Gray (Pantone 5455 C)
    "background_hex": "#FFFFFF",
    "text_hex": "#141A2E",
    "text_light_hex": "#FFFFFF",
    "cta_red_hex": "#EF3333",       # CTA buttons only
    "display_font_family": "Burlingame Pro",
    "display_font_alt": "Saira",
    "headline_font_family": "FS Silas Slab",
    "headline_font_alt": "Zilla Slab",
    "body_font_family": "Sans Beam",
    "body_font_alt": "Lexend",
    "brand_name": "Anderson Lock & Safe",
    "tagline": "Securing Arizona Since 1966",
}


def _parse_frontmatter(text: str) -> dict:
    """Simple YAML-ish front-matter parser — supports scalar key: value pairs."""
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not m:
        return {}
    out: dict[str, str] = {}
    for line in m.group(1).splitlines():
        line = line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        k, v = line.split(":", 1)
        out[k.strip()] = v.strip().strip('"').strip("'")
    return out


def load_brand() -> dict:
    tokens = dict(_DEFAULTS)
    if STYLE_GUIDE.exists():
        parsed = _parse_frontmatter(STYLE_GUIDE.read_text())
        tokens.update(parsed)
    return tokens


# ---------- color + font helpers ----------


def _hex_to_rgb(h: str) -> Tuple[int, int, int]:
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


_HOME = Path.home()

_FONT_CANDIDATES = {
    # Display / headline — Burlingame Pro → Saira (free alt) → system bold
    "display": [
        str(_HOME / "Library/Fonts/BurlingamePro-Bold.ttf"),
        str(_HOME / "Library/Fonts/BurlingamePro-Regular.ttf"),
        "/Library/Fonts/BurlingamePro-Bold.ttf",
        str(_HOME / "Library/Fonts/Saira-Bold.ttf"),
        str(_HOME / "Library/Fonts/Saira-SemiBold.ttf"),
        "/System/Library/Fonts/HelveticaNeue.ttc",
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/Library/Fonts/Arial Bold.ttf",
    ],
    # Headline slab — FS Silas Slab → Zilla Slab (free alt) → system
    "headline": [
        str(_HOME / "Library/Fonts/FSSilasSlab-Bold.otf"),
        str(_HOME / "Library/Fonts/FSSilasSlab-Regular.otf"),
        str(_HOME / "Library/Fonts/ZillaSlab-Bold.ttf"),
        str(_HOME / "Library/Fonts/ZillaSlab-SemiBold.ttf"),
        "/System/Library/Fonts/HelveticaNeue.ttc",
        "/System/Library/Fonts/Helvetica.ttc",
    ],
    # Body — Sans Beam → Lexend (free alt) → system
    "body": [
        str(_HOME / "Library/Fonts/SansBeam-Regular.ttf"),
        str(_HOME / "Library/Fonts/SansBeam-Light.ttf"),
        str(_HOME / "Library/Fonts/Lexend-Regular.ttf"),
        str(_HOME / "Library/Fonts/Lexend-Light.ttf"),
        "/System/Library/Fonts/HelveticaNeue.ttc",
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/Library/Fonts/Arial.ttf",
    ],
}


def load_font(kind: str, size: int) -> ImageFont.ImageFont:
    for path in _FONT_CANDIDATES[kind]:
        if Path(path).exists():
            try:
                return ImageFont.truetype(path, size=size)
            except Exception:
                continue
    return ImageFont.load_default()


# ---------- layout primitives ----------


def _wrap_text(draw: ImageDraw.ImageDraw, text: str, font, max_width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for w in words:
        test = f"{current} {w}".strip()
        if draw.textlength(test, font=font) <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = w
    if current:
        lines.append(current)
    return lines


def _draw_wrapped(
    draw: ImageDraw.ImageDraw,
    text: str,
    font,
    x: int,
    y: int,
    max_width: int,
    line_spacing: int = 10,
    fill=(0, 0, 0),
    anchor: str = "la",
) -> int:
    lines = _wrap_text(draw, text, font, max_width)
    ascent, descent = font.getmetrics()
    line_h = ascent + descent
    for i, line in enumerate(lines):
        draw.text((x, y + i * (line_h + line_spacing)), line, font=font, fill=fill, anchor=anchor)
    return y + len(lines) * (line_h + line_spacing)


def _parse_size(spec: str) -> Tuple[int, int]:
    if "x" not in spec:
        raise ValueError(f"invalid size: {spec}")
    w, h = spec.lower().split("x", 1)
    return int(w), int(h)


def _watermark(draw: ImageDraw.ImageDraw, W: int, H: int, brand: dict, fill) -> None:
    font = load_font("display", int(H * 0.022))
    txt = brand["brand_name"]
    draw.text((W // 2, H - int(H * 0.045)), txt, font=font, fill=fill, anchor="mm")


# ---------- tile renderers ----------


def _canvas(W: int, H: int, brand: dict, palette: str) -> Tuple[Image.Image, ImageDraw.ImageDraw]:
    bg = _hex_to_rgb(brand["background_hex"] if palette == "light" else brand["primary_hex"])
    img = Image.new("RGB", (W, H), bg)
    return img, ImageDraw.Draw(img)


def render_tip_card(args, brand: dict) -> Image.Image:
    W, H = _parse_size(args.size)
    palette = args.palette
    img, draw = _canvas(W, H, brand, palette)
    fg = _hex_to_rgb(brand["text_hex"] if palette == "light" else brand["text_light_hex"])
    accent = _hex_to_rgb(brand["secondary_hex"])

    # Eyebrow / header band
    eyebrow_font = load_font("display", int(H * 0.025))
    draw.rectangle([0, 0, W, int(H * 0.08)], fill=accent)
    draw.text(
        (W // 2, int(H * 0.04)),
        (args.eyebrow or "COMMERCIAL SECURITY TIP").upper(),
        font=eyebrow_font,
        fill=_hex_to_rgb(brand["primary_hex"]),
        anchor="mm",
    )

    # Headline
    headline_font = load_font("display", int(H * 0.075))
    margin = int(W * 0.08)
    y = int(H * 0.18)
    y = _draw_wrapped(
        draw,
        args.headline,
        headline_font,
        margin,
        y,
        W - 2 * margin,
        line_spacing=8,
        fill=fg,
    )

    # Body
    if args.body:
        body_font = load_font("body", int(H * 0.038))
        y += int(H * 0.045)
        _draw_wrapped(
            draw,
            args.body,
            body_font,
            margin,
            y,
            W - 2 * margin,
            line_spacing=10,
            fill=fg,
        )

    # Watermark
    if not args.no_watermark:
        _watermark(draw, W, H, brand, fill=accent)
    return img


def render_stat_card(args, brand: dict) -> Image.Image:
    W, H = _parse_size(args.size)
    palette = args.palette
    img, draw = _canvas(W, H, brand, palette)
    fg = _hex_to_rgb(brand["text_hex"] if palette == "light" else brand["text_light_hex"])
    accent = _hex_to_rgb(brand["secondary_hex"])

    # Giant stat
    stat_font = load_font("display", int(H * 0.28))
    draw.text((W // 2, int(H * 0.40)), args.stat, font=stat_font, fill=accent, anchor="mm")

    # Label
    label_font = load_font("body", int(H * 0.045))
    margin = int(W * 0.08)
    _draw_wrapped(
        draw,
        args.label,
        label_font,
        W // 2,
        int(H * 0.62),
        W - 2 * margin,
        line_spacing=10,
        fill=fg,
        anchor="ma",
    )
    if not args.no_watermark:
        _watermark(draw, W, H, brand, fill=accent)
    return img


def render_qa_card(args, brand: dict) -> Image.Image:
    W, H = _parse_size(args.size)
    palette = args.palette
    img, draw = _canvas(W, H, brand, palette)
    fg = _hex_to_rgb(brand["text_hex"] if palette == "light" else brand["text_light_hex"])
    accent = _hex_to_rgb(brand["secondary_hex"])
    margin = int(W * 0.08)

    # Q:
    label_font = load_font("display", int(H * 0.045))
    draw.text((margin, int(H * 0.13)), "Q.", font=label_font, fill=accent, anchor="la")
    qfont = load_font("display", int(H * 0.062))
    y = _draw_wrapped(
        draw,
        args.question,
        qfont,
        margin + int(W * 0.08),
        int(H * 0.13),
        W - 2 * margin - int(W * 0.08),
        line_spacing=6,
        fill=fg,
    )

    # A:
    y += int(H * 0.06)
    draw.text((margin, y), "A.", font=label_font, fill=accent, anchor="la")
    afont = load_font("body", int(H * 0.045))
    _draw_wrapped(
        draw,
        args.answer,
        afont,
        margin + int(W * 0.08),
        y,
        W - 2 * margin - int(W * 0.08),
        line_spacing=10,
        fill=fg,
    )
    if not args.no_watermark:
        _watermark(draw, W, H, brand, fill=accent)
    return img


def render_numbered_list(args, brand: dict) -> Image.Image:
    W, H = _parse_size(args.size)
    palette = args.palette
    img, draw = _canvas(W, H, brand, palette)
    fg = _hex_to_rgb(brand["text_hex"] if palette == "light" else brand["text_light_hex"])
    accent = _hex_to_rgb(brand["secondary_hex"])
    margin = int(W * 0.08)

    title_font = load_font("display", int(H * 0.058))
    y = int(H * 0.12)
    y = _draw_wrapped(
        draw,
        args.title,
        title_font,
        margin,
        y,
        W - 2 * margin,
        line_spacing=8,
        fill=fg,
    )
    y += int(H * 0.06)

    num_font = load_font("display", int(H * 0.085))
    item_font = load_font("body", int(H * 0.038))
    row_h = int(H * 0.14)
    for i, item in enumerate(args.items[:5], start=1):
        draw.text(
            (margin, y + row_h // 2),
            f"{i:02d}",
            font=num_font,
            fill=accent,
            anchor="lm",
        )
        _draw_wrapped(
            draw,
            item,
            item_font,
            margin + int(W * 0.14),
            y + row_h // 2 - int(H * 0.025),
            W - 2 * margin - int(W * 0.14),
            line_spacing=8,
            fill=fg,
        )
        y += row_h

    if not args.no_watermark:
        _watermark(draw, W, H, brand, fill=accent)
    return img


def render_before_after(args, brand: dict) -> Image.Image:
    W, H = _parse_size(args.size)
    palette = args.palette
    bg = _hex_to_rgb(brand["primary_hex"])
    img = Image.new("RGB", (W, H), bg)

    half_h = (H - int(H * 0.14)) // 2
    top_area = (0, int(H * 0.07), W, int(H * 0.07) + half_h)
    bot_area = (0, int(H * 0.07) + half_h, W, int(H * 0.07) + 2 * half_h)

    def _place(img_path: str, box):
        src = Image.open(img_path).convert("RGB")
        bw = box[2] - box[0]
        bh = box[3] - box[1]
        src_ratio = src.width / src.height
        box_ratio = bw / bh
        if src_ratio > box_ratio:
            new_h = bh
            new_w = int(src_ratio * new_h)
        else:
            new_w = bw
            new_h = int(new_w / src_ratio)
        resized = src.resize((new_w, new_h), Image.LANCZOS)
        ox = box[0] - (new_w - bw) // 2
        oy = box[1] - (new_h - bh) // 2
        img.paste(resized, (ox, oy))

    _place(args.before, top_area)
    _place(args.after, bot_area)

    draw = ImageDraw.Draw(img)
    # labels
    label_font = load_font("display", int(H * 0.03))
    accent = _hex_to_rgb(brand["secondary_hex"])
    for text, y in (("BEFORE", int(H * 0.09)), ("AFTER", int(H * 0.09) + half_h)):
        pad_x = int(W * 0.025)
        pad_y = int(H * 0.012)
        bbox = draw.textbbox((0, 0), text, font=label_font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        x0 = int(W * 0.04)
        draw.rectangle([x0, y, x0 + tw + 2 * pad_x, y + th + 2 * pad_y], fill=accent)
        draw.text(
            (x0 + pad_x, y + pad_y),
            text,
            font=label_font,
            fill=_hex_to_rgb(brand["primary_hex"]),
            anchor="la",
        )

    # caption bar
    caption_font = load_font("body", int(H * 0.028))
    if args.label:
        _draw_wrapped(
            draw,
            args.label,
            caption_font,
            int(W * 0.05),
            int(H * 0.93),
            W - int(W * 0.10),
            line_spacing=6,
            fill=_hex_to_rgb(brand["text_light_hex"]),
        )

    if not args.no_watermark:
        _watermark(draw, W, H, brand, fill=accent)
    return img


# ---------- main ----------


def main() -> int:
    p = argparse.ArgumentParser(description="Branded tile generator")
    sub = p.add_subparsers(dest="cmd", required=True)

    def add_common(parser):
        parser.add_argument("--size", default="1080x1080", help="WIDTHxHEIGHT")
        parser.add_argument("--palette", choices=["dark", "light"], default="dark")
        parser.add_argument("--no-watermark", action="store_true")
        parser.add_argument("--out", required=True)

    p_tip = sub.add_parser("tip-card")
    p_tip.add_argument("--headline", required=True)
    p_tip.add_argument("--body", default="")
    p_tip.add_argument("--eyebrow", default="")
    add_common(p_tip)
    p_tip.set_defaults(func=lambda a, b: render_tip_card(a, b))

    p_stat = sub.add_parser("stat-card")
    p_stat.add_argument("--stat", required=True)
    p_stat.add_argument("--label", required=True)
    add_common(p_stat)
    p_stat.set_defaults(func=lambda a, b: render_stat_card(a, b))

    p_qa = sub.add_parser("qa-card")
    p_qa.add_argument("--question", required=True)
    p_qa.add_argument("--answer", required=True)
    add_common(p_qa)
    p_qa.set_defaults(func=lambda a, b: render_qa_card(a, b))

    p_list = sub.add_parser("numbered-list")
    p_list.add_argument("--title", required=True)
    p_list.add_argument("--items", nargs="+", required=True)
    add_common(p_list)
    p_list.set_defaults(func=lambda a, b: render_numbered_list(a, b))

    p_ba = sub.add_parser("before-after")
    p_ba.add_argument("--before", required=True)
    p_ba.add_argument("--after", required=True)
    p_ba.add_argument("--label", default="")
    add_common(p_ba)
    p_ba.set_defaults(func=lambda a, b: render_before_after(a, b))

    args = p.parse_args()
    brand = load_brand()
    img = args.func(args, brand)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, format="PNG", optimize=True)
    print(f"wrote {out} ({img.size[0]}x{img.size[1]})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
