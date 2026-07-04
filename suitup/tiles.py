"""
suitup/tiles.py

Foundational tile model for SuitUp's American Mah Jongg engine. Glavin!

Every rules check, every rendered SVG, every AI decision eventually walks
through the identity helpers defined in this module, so the model is kept
small, frozen (immutable), hashable, and deterministically orderable.

PHYSICAL GROUND TRUTH — a commercial American Mah Jongg set (like the
owner's Majolica set) ships with exactly 152 tiles:

    Suits (Dots / Bams / Craks), ranks 1-9, x4 copies each   = 108 tiles
    Winds (East, South, West, North), x4 copies each         =  16 tiles
    Dragons (Red, Green, White a.k.a. "Soap"), x4 copies each=  12 tiles
    Jokers                                                   =   8 tiles
    Flowers                                                  =   8 tiles
    ----------------------------------------------------------------
    TOTAL (full physical American set)                       = 152 tiles

Flowers are real, physical tiles that come in the box, which is why
``build_standard_set()`` returns exactly 152 tiles *by default* — that
matches what a beginner actually has on their table.

What flowers are NOT, by default, is *active in standard scored play*.
In real American Mah Jongg, a flower drawn during the deal is exposed
face-up on the rack and immediately replaced by a draw from the wall —
it never becomes part of a scored hand. The module-level constant
``FLOWERS_ACTIVE_IN_STANDARD_PLAY`` records this so later rules-engine
tasks have one authoritative flag to check, instead of re-deriving the
rule. ``build_standard_set(include_flowers=False)`` is provided for
callers (tests, isolated drills) that want the flower-free 144-tile
core set instead.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, unique
from typing import Dict, List, Optional, Tuple

__all__ = [
    "Kind",
    "Suit",
    "Wind",
    "Dragon",
    "Tile",
    "STANDARD_TILE_COUNT",
    "CORE_TILE_COUNT_NO_FLOWERS",
    "FLOWERS_ACTIVE_IN_STANDARD_PLAY",
    "STANDARD_KIND_COUNTS",
    "build_standard_set",
    "validate_tile_set",
    "self_check",
    "suit_of",
    "rank_of",
    "wind_of",
    "dragon_of",
    "is_joker",
    "is_flower",
    "is_honor",
    "is_suit_tile",
    "display_name",
]


# --------------------------------------------------------------------------
# Constants describing the physical ground truth of an American set.
# --------------------------------------------------------------------------

STANDARD_TILE_COUNT = 152          # full physical set, flowers included
CORE_TILE_COUNT_NO_FLOWERS = 144   # same set with the 8 flowers omitted

# The rules engine (a later module) is expected to treat this as
# authoritative: flowers exist physically in the 152-tile set but are
# swapped out during the deal and excluded from standard hand-building
# unless a teaching drill explicitly opts in.
FLOWERS_ACTIVE_IN_STANDARD_PLAY = False


@unique
class Kind(Enum):
    """The five physical categories of tile in an American set."""

    SUIT = "suit"
    WIND = "wind"
    DRAGON = "dragon"
    JOKER = "joker"
    FLOWER = "flower"


@unique
class Suit(Enum):
    DOTS = "dots"
    BAMS = "bams"
    CRAK