"""Original SVG tile-art generator for SuitUp.

This module is the single source of truth for what a Mah Jongg tile
*looks like* on screen. It contains no external image assets, no
scraped artwork, and no embedded font files -- every tile face is
built at runtime from primitive SVG shapes (rects, circles, paths,
and short `<text>` glyphs rendered with a generic system font stack).
That makes the whole corpus 100% original and trivially regenerable.

Design goals:
    * Small: each tile is a compact viewBox (100x140) so the SVGs are
      tiny and cheap for a browser to render dozens of at once.
    * Crisp: everything is drawn with flat vector primitives, no
      embedded raster images, no external URLs, no webfonts.
    * Consistent: one shared tile "frame" (rounded rect + border)
      is reused for every tile kind, with a suit/kind-specific
      "face" drawn on top of it.
    * Reusable: `render_tile(tile)` is the single public entry point
      the web app should call; it accepts a `suitup.tiles.Tile` and
      returns a ready-to-embed `<svg>...</svg>` string.

Nothing in this module touches the filesystem except the optional
`generate_asset_corpus()` helper, which is only used to pre-render a
static directory of SVGs for the web server to serve as plain files
instead of generating them on every request. Generating the corpus
is a build step, not something this module does implicitly on
import.
"""

from __future__ import annotations

import os
from typing import Iterable, List, Optional

from suitup.tiles import (
    Dragon,
    Suit,
    Tile,
    TileKind,
    Wind,
    build_tile_set,
    is_flower,
    is_honor,
    is_joker,
    is_suited,
    suit_of,
)

# ---------------------------------------------------------------------------
# Shared canvas constants
# ---------------------------------------------------------------------------

TILE_WIDTH: int = 100
TILE_HEIGHT: int = 140
TILE_VIEWBOX: str = f"0 0 {TILE_WIDTH} {TILE_HEIGHT}"

FONT_STACK: str = (
    "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, "
    "Helvetica, Arial, sans-serif"
)

# Base tile "ivory" body and border, shared by every tile kind so the
# whole rack reads as one physical set instead of a grab-bag of styles.
COLOR_BODY: str = "#f6efe0"
COLOR_BODY_SHADOW: str = "#e4d9bf"
COLOR_BORDER: str = "#2b2b2b"

# Suit accent colors (suited tiles).
COLOR_DOTS: str = "#1f6fb2"
COLOR_BAMS: str = "#2e8b57"
COLOR_CRAKS: str = "#b3261e"

# Honor tile accents.
COLOR_WIND: str = "#6b4f9e"
COLOR_DRAGON_RED: str = "#b3261e"
COLOR_DRAGON_GREEN: str = "#2e8b57"
COLOR_DRAGON_WHITE: str = "#3f6fa8"

# Joker / flower accents.
COLOR_JOKER: str = "#c9852c"
COLOR_FLOWER: str = "#d16ba5"

WIND_LABELS = {
    Wind.EAST: "E",
    Wind.SOUTH: "S",
    Wind.WEST: "W",
    Wind.NORTH: "N",
}

DRAGON_COLORS = {
    Dragon.RED: COLOR_DRAGON_RED,
    Dragon.GREEN: COLOR_DRAGON_GREEN,
    Dragon.WHITE: COLOR_DRAGON_WHITE,
}

SUIT_COLORS = {
    Suit.DOTS: COLOR_DOTS,
    Suit.BAMS: COLOR_BAMS,
    Suit.CRAKS: COLOR_CRAKS,
}

SUIT_LETTERS = {
    Suit.DOTS: "D",
    Suit.BAMS: "B",
    Suit.CRAKS: "C",
}

# Classic playing-card style pip layout coordinates (as fractions of
# the pip area) for counts 1-9. Reused for both the "dots" suit
# (circles) and the "bams" suit (stalks), so the two suits read as a
# clear visual pair while still being distinguishable by shape.
_PIP_LAYOUTS = {
    1: [(0.5, 0.5)],
    2: [(0.5, 0.22), (0.5, 0.78)],
    3: [(0.5, 0.18), (0.5, 0.5), (0.5, 0.82)],
    4: [(0.25, 0.25), (0.75, 0.25), (0.25, 0.75), (0.75, 0.75)],
    5: [
        (0.25, 0.25), (0.75, 0.25),
        (0.5, 0.5),
        (0.25, 0.75), (0.75, 0.75),
    ],
    6: [
        (0.25, 0.2), (0.75, 0.2),
        (0.25, 0.5), (0.75, 0.5),
        (0.25, 0.8), (0.75, 0.8),
    ],
    7: [
        (0.25, 0.18), (0.75, 0.18),
        (0.5, 0.38),
        (0.25, 0.6), (0.75, 0.6),
        (0.25, 0.85), (0.75, 0.85),
    ],
    8: [
        (0.25, 0.15), (0.75, 0.15),
        (0.25, 0.38), (0.75, 0.38),
        (0.25, 0.62), (0.75, 0.62),
        (0.25, 0.85), (0.75, 0.85),
    ],
    9: [
        (0.25, 0.15), (0.5, 0.15), (0.75, 0.15),
        (0.25, 0.5), (0.5, 0.5), (0.75, 0.5),
        (0.25, 0.85), (0.5, 0.85), (0.75, 0.85),
    ],
}


def _svg_open(extra_class: str = "") -> str:
    """Return the opening `<svg>` tag shared by every tile face."""
    cls = f' class="suitup-tile {extra_class}"'.rstrip() if extra_class else ' class="suitup-tile"'
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{TILE_VIEWBOX}" '
        f'width="{TILE_WIDTH}" height="{TILE_HEIGHT}"{cls} role="img">'
    )


def _tile_frame() -> str:
    """Shared rounded-rect tile body + inner border, drawn under every face."""
    return (
        f'<rect x="1" y="1" width="{TILE_WIDTH - 2}" height="{TILE_HEIGHT - 2}" '
        f'rx="10" ry="10" fill="{COLOR_BODY}" stroke="{COLOR_BORDER}" '
        'stroke-width="2"/>'
        f'<rect x="6" y="6" width="{TILE_WIDTH - 12}" height="{TILE_HEIGHT - 12}" '
        f'rx="6" ry="6" fill="none" stroke="{COLOR_BODY_SHADOW}" stroke-width="1"/>'
    )


def _corner_number(text: str, color: str) -> str:
    """Small index glyph in the top-left corner, like a playing card."""
    return (
        f'<text x="10" y="20" font-family="{FONT_STACK}" font-size="14" '
        f'font-weight="700" fill="{color}">{text}</text>'
    )


def _center_pip_circles(count: int, color: str) -> str:
    """Draw `count` circle pips (used for the Dots suit)."""
    layout = _PIP_LAYOUTS.get(count, _PIP_LAYOUTS[9])
    area_x0, area_y0 = 18.0, 30.0
    area_w, area_h = TILE_WIDTH - 36.0, TILE_HEIGHT - 60.0
    circles: List[str] = []
    for fx, fy in layout:
        cx = area_x0 + fx * area_w
        cy = area_y0 + fy * area_h
        circles.append(
            f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="6.5" fill="{color}" '
            f'stroke="{COLOR_BORDER}" stroke-width="0.75"/>'
        )
    return "".join(circles)


def _center_bam_stalks(count: int, color: str) -> str:
    """Draw `count` bamboo-stalk pips (used for the Bams suit)."""
    layout = _PIP_LAYOUTS.get(count, _PIP_LAYOUTS[9])
    area_x0, area_y0 = 18.0, 30.0
    area_w, area_h = TILE_WIDTH - 36.0, TILE_HEIGHT - 60.0
    stalks: List[str] = []
    for fx, fy in layout:
        cx = area_x0 + fx * area_w
        cy = area_y0 + fy * area_h
        x0 = cx - 3.0
        y0 = cy - 8.0
        stalks.append(
            f'<rect x="{x0:.1f}" y="{y0:.1f}" width="6" height="16" rx="2.5" '
            f'fill="{color}" stroke="{COLOR_BORDER}" stroke-width="0.75"/>'
            f'<line x1="{x0:.1f}" y1="{(cy - 2.5):.1f}" x2="{(x0 + 6):.1f}" '
            f'y2="{(cy - 2.5):.1f}" stroke="{COLOR_BORDER}" stroke-width="0.6"/>'
            f'<line x1="{x0:.1f}" y1="{(cy + 2.5):.1f}" x2="{(x0 + 6):.1f}" '
            f'y2="{(cy + 2.5):.1f}" stroke="{COLOR_BORDER}" stroke-width="0.6"/>'
        )
    return "".join(stalks)


def _center_crak_marks(count: int, color: str) -> str:
    """Draw `count` abstract stroke-pips (used for the Craks suit).

    These are original procedural glyphs (a filled "banner" shape),
    not a rendering of any real Chinese character font, so there is
    no external artwork or typeface being traced or embedded.
    """
    layout = _PIP_LAYOUTS.get(count, _PIP_LAYOUTS[9])
    area_x0, area_y0 = 18.0, 30.0
    area_w, area_h = TILE_WIDTH - 36.0, TILE_HEIGHT - 60.0
    marks: List[str] = []
    for fx, fy in layout:
        cx = area_x0 + fx * area_w
        cy = area_y0 + fy * area_h
        x0 = cx - 6.0
        y0 = cy - 6.0
        marks.append(
            f'<path d="M {x0:.1f} {y0:.1f} L {(x0 + 12):.1f} {y0:.1f} '
            f'L {(x0 + 12):.1f} {(y0 + 8):.1f} L {cx:.1f} {(y0 + 12):.1f} '
            f'L {x0:.1f} {(y0 + 8):.1f} Z" fill="{color}" '
            f'stroke="{COLOR_BORDER}" stroke-width="0.6"/>'
        )
    return "".join(marks)


def render_suited(suit: Suit, number: int) -> str:
    """Render a numbered suit tile (Dots / Bams / Craks 1-9)."""
    color = SUIT_COLORS[suit]
    letter = SUIT_LETTERS[suit]
    body = _svg_open("suit")
    body += _tile_frame()
    body += _corner_number(f"{number}{letter}", color)
    if suit is Suit.DOTS:
        body += _center_pip_circles(number, color)
    elif suit is Suit.BAMS:
        body += _center_bam_stalks(number, color)
    else:
        body += _center_crak_marks(number, color)
    body += "</svg>"
    return body


def render_wind(wind: Wind) -> str:
    """Render a wind honor tile (E/S/W/N) as a colored roundel."""
    letter = WIND_LABELS[wind]
    body = _svg_open("wind")
    body += _tile_frame()
    body += (
        f'<circle cx="{TILE_WIDTH / 2}" cy="{TILE_HEIGHT / 2}" r="28" '
        f'fill="none" stroke="{COLOR_WIND}" stroke-width="4"/>'
        f'<text x="{TILE_WIDTH / 2}" y="{TILE_HEIGHT / 2 + 12}" '
        f'font-family="{FONT_STACK}" font-size="36" font-weight="800" '
        f'text-anchor="middle" fill="{COLOR_WIND}">{letter}</text>'
    )
    body += "</svg>"
    return body


def render_dragon(dragon: Dragon) -> str:
    """Render a dragon honor tile (Red/Green/White).

    Red and Green dragons get a filled emblem in their color; the
    White Dragon (the traditional "soap" tile) is rendered as an
    empty framed rectangle, matching how it is physically blank.
    """
    color = DRAGON_COLORS[dragon]
    body = _svg_open("dragon")
    body += _tile_frame()
    if dragon is Dragon.WHITE:
        body += (
            f'<rect x="26" y="{TILE_HEIGHT / 2 - 22}" width="{TILE_WIDTH - 52}" '
            f'height="44" rx="6" fill="none" stroke="{color}" stroke-width="4"/>'
        )
    else:
        body += (
            f'<rect x="26" y="{TILE_HEIGHT / 2 - 22}" width="{TILE_WIDTH - 52}" '
            f'height="44" rx="6" fill="{color}" stroke="{COLOR_BORDER}" '
            'stroke-width="2"/>'
            f'<path d="M 34 {TILE_HEIGHT / 2} L {TILE_WIDTH / 2} '
            f'{TILE_HEIGHT / 2 - 14} L {TILE_WIDTH - 34} {TILE_HEIGHT / 2} '
            f'L {TILE_WIDTH / 2} {TILE_HEIGHT / 2 + 14} Z" fill="{COLOR_BODY}"/>'
        )
    body += "</svg>"
    return body


def render_joker() -> str:
    """Render the Joker tile: a rainbow banner with a starburst."""
    body = _svg_open("joker")
    body += _tile_frame()
    stripes = ["#e05252", "#e0a552", "#d6c94a", "#57a65a", "#3f7fb0", "#7d5db0"]
    stripe_h = 8
    top = 26
    for i, color in enumerate(stripes):
        y = top + i * stripe_h
        body += (
            f'<rect x="16" y="{y}" width="{TILE_WIDTH - 32}" height="{stripe_h - 1}" '
            f'fill="{color}"/>'
        )
    body += (
        f'<text x="{TILE_WIDTH / 2}" y="{TILE_HEIGHT - 22}" '
        f'font-family="{FONT_STACK}" font-size="16" font-weight="800" '
        f'text-anchor="middle" fill="{COLOR_JOKER}">JOKER</text>'
    )
    body += "</svg>"
    return body


_FLOWER_ORDER = ("flower_1", "flower_2", "flower_3", "flower_4",
                 "season_1", "season_2", "season_3", "season_4")
_FLOWER_PALETTE = ("#d16ba5", "#e0736b", "#e0a552", "#57a65a",
                   "#5aa6a0", "#5a86c0", "#8d6bd0", "#c05a97")


def render_flower(label: str) -> str:
    """Render a Flower/Season bonus tile: a six-petal blossom whose colour and
    F/S mark vary by label. All flowers are interchangeable in American play."""
    idx = _FLOWER_ORDER.index(label) if label in _FLOWER_ORDER else 0
    color = _FLOWER_PALETTE[idx % len(_FLOWER_PALETTE)]
    cx = TILE_WIDTH / 2
    cy = TILE_HEIGHT / 2 - 6
    body = _svg_open("flower")
    body += _tile_frame()
    for k in range(6):
        body += (
            f'<ellipse cx="{cx}" cy="{cy - 17}" rx="9" ry="17" fill="{color}" '
            f'opacity="0.9" transform="rotate({k * 60} {cx} {cy})"/>'
        )
    body += (
        f'<circle cx="{cx}" cy="{cy}" r="10" fill="#f2d24a" '
        f'stroke="{COLOR_BORDER}" stroke-width="1"/>'
    )
    mark = ("S" if label.startswith("season") else "F") + label[-1]
    body += (
        f'<text x="{cx}" y="{TILE_HEIGHT - 18}" font-family="{FONT_STACK}" '
        f'font-size="18" font-weight="800" text-anchor="middle" '
        f'fill="{color}">{mark}</text>'
    )
    body += "</svg>"
    return body