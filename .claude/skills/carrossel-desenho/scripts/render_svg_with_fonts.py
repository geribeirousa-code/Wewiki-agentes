#!/usr/bin/env python3
"""
Render SVG carousel slides to PNG using Playwright + Chromium.
Loads real font files (Lufga + Chalkiez) via @font-face so the
browser renders exactly the declared font-family in the SVG.

Usage:
    python3 render_svg_with_fonts.py --svg slide-1-blueprint.svg --output slide-1.png [--size 1080]
"""

import argparse
import base64
import re
import sys
from pathlib import Path

FONTS_BASE = Path(__file__).resolve().parents[4] / ".agents/skills/carrossel-opiniao/fonts/bowlgreen"

LUFGA_DIR = FONTS_BASE
CHALKIEZ_DIR = FONTS_BASE

# Lufga weights to preload (regular + bold + extrabold + black)
LUFGA_FACES = [
    ("Lufga", "400", "normal", "Lufga-400.otf"),
    ("Lufga", "500", "normal", "Lufga-500.otf"),
    ("Lufga", "600", "normal", "Lufga-600.otf"),
    ("Lufga", "700", "normal", "Lufga-700.otf"),
    ("Lufga", "800", "normal", "Lufga-800.otf"),
    ("Lufga", "900", "normal", "Lufga-900.otf"),
]

CHALKIEZ_FACES = [
    ("Chalkiez", "400", "normal", "Chalkiez-400.otf"),
]


def font_to_data_uri(font_path: Path) -> str:
    data = font_path.read_bytes()
    b64 = base64.b64encode(data).decode()
    ext = font_path.suffix.lower()
    mime = "font/otf" if ext == ".otf" else "font/ttf"
    return f"data:{mime};base64,{b64}"


def build_font_face_css() -> str:
    rules = []
    for family, weight, style, filename in LUFGA_FACES:
        path = LUFGA_DIR / filename
        if not path.exists():
            continue
        uri = font_to_data_uri(path)
        rules.append(
            f"@font-face {{ font-family: '{family}'; font-weight: {weight}; "
            f"font-style: {style}; src: url('{uri}'); }}"
        )
    for family, weight, style, filename in CHALKIEZ_FACES:
        path = CHALKIEZ_DIR / filename
        if not path.exists():
            continue
        uri = font_to_data_uri(path)
        rules.append(
            f"@font-face {{ font-family: '{family}'; font-weight: {weight}; "
            f"font-style: {style}; src: url('{uri}'); }}"
        )
    return "\n".join(rules)


def render_svg(svg_path: Path, output_path: Path, size: int = 1080) -> None:
    svg_content = svg_path.read_text(encoding="utf-8")

    # Patch font-family in SVG style attr to put Lufga first for body,
    # keeping Chalkiez for elements that explicitly declare it.
    # The SVG already has 'Chalkiez','Lufga' in its global font-family;
    # we just need the browser to honour it with the real files loaded.

    font_css = build_font_face_css()

    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
{font_css}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: {size}px; height: {size}px; overflow: hidden; background: transparent; }}
svg {{ width: {size}px; height: {size}px; display: block; }}
</style>
</head>
<body>
{svg_content}
</body>
</html>"""

    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": size, "height": size})
        page.set_content(html, wait_until="networkidle")
        # Wait for fonts to be ready
        page.evaluate("document.fonts.ready")
        page.screenshot(path=str(output_path), clip={"x": 0, "y": 0, "width": size, "height": size})
        browser.close()

    print(f"[output] Saved: {output_path} ({output_path.stat().st_size // 1024}KB)")


def main():
    parser = argparse.ArgumentParser(description="Render SVG slide with real fonts via Playwright")
    parser.add_argument("--svg", required=True, help="SVG blueprint file path")
    parser.add_argument("--output", "-o", required=True, help="Output PNG path")
    parser.add_argument("--size", type=int, default=1080, help="Output size in pixels (default: 1080)")
    args = parser.parse_args()

    svg_path = Path(args.svg)
    output_path = Path(args.output)

    if not svg_path.exists():
        print(f"ERROR: SVG not found: {svg_path}", file=sys.stderr)
        sys.exit(1)

    print(f"[svg] Rendering {svg_path.name} at {args.size}x{args.size}px with real fonts...")
    render_svg(svg_path, output_path, args.size)


if __name__ == "__main__":
    main()
