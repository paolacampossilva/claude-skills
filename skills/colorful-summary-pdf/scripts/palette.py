"""Generate an evenly-spaced, muted color palette for a colorful-summary-pdf document.

Usage:
    python palette.py <section_count> [--start-hue 5] [--sat 55] [--light 40]

Prints one line per section as:
    <index> <accent_hex> <tint_hex> <tint2_hex>

- accent_hex: the section's main color (headings, borders, chips, table headers)
- tint_hex:   a ~7% tint of accent over white, for .callout backgrounds
- tint2_hex:  a ~4% tint of accent over white, for zebra-striped table rows

Hues are spaced evenly around the color wheel starting at --start-hue, which
keeps every section visually distinct while still reading as one coherent
"rainbow progression" (useful as a legend/index and matches the topic order).
Saturation and lightness are kept moderate on purpose (default 55% / 40%) so
colors stay legible as text and background tints rather than looking like a
neon UI kit.
"""

import argparse
import colorsys


def hsl_to_hex(h_deg: float, s_pct: float, l_pct: float) -> str:
    """Convert HSL (hue in degrees, saturation/lightness in percent) to #RRGGBB."""
    h = (h_deg % 360) / 360
    s = s_pct / 100
    l = l_pct / 100
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return f"{round(r * 255):02X}{round(g * 255):02X}{round(b * 255):02X}"


def tint(hex_color: str, pct: float) -> str:
    """Mix hex_color with white. pct=1.0 keeps the full color, pct=0 gives white."""
    r, g, b = (int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
    r = round(r * pct + 255 * (1 - pct))
    g = round(g * pct + 255 * (1 - pct))
    b = round(b * pct + 255 * (1 - pct))
    return f"{r:02X}{g:02X}{b:02X}"


def build_palette(count: int, start_hue: float = 5, sat: float = 55, light: float = 40):
    step = 360 / count
    palette = []
    for i in range(count):
        hue = start_hue + i * step
        accent = hsl_to_hex(hue, sat, light)
        palette.append({
            "index": i + 1,
            "accent": accent,
            "tint": tint(accent, 0.07),
            "tint2": tint(accent, 0.04),
        })
    return palette


def main():
    parser = argparse.ArgumentParser(description="Generate a section color palette.")
    parser.add_argument("count", type=int, help="number of sections/topics")
    parser.add_argument("--start-hue", type=float, default=5)
    parser.add_argument("--sat", type=float, default=55)
    parser.add_argument("--light", type=float, default=40)
    args = parser.parse_args()

    palette = build_palette(args.count, args.start_hue, args.sat, args.light)
    for entry in palette:
        print(f"{entry['index']} {entry['accent']} {entry['tint']} {entry['tint2']}")

    gradient_stops = ", ".join(f"#{entry['accent']}" for entry in palette)
    print(f"\n/* gradient for .toc-rule */\nlinear-gradient(180deg, {gradient_stops})")


if __name__ == "__main__":
    main()
