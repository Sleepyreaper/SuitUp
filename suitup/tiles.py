"""Canonical tile model for SuitUp.

This module is the single source of truth for what a Mah Jongg tile
"is" across the whole app: the web layer, the rules engine, and the
AI opponents all import from here instead of re-deriving tile facts.

Ground truth counts for a standard NMJL-style 152-tile set (flowers
disabled by default):

    Suited tiles (Dots, Bams, Craks; 1-9; four of each) = 108
    Winds (East, South, West, North; four of each)      = 16
    Dragons (Red, Green, White; four of each)           = 12
    Jokers                                              = 8
    ---------------------------------------------------------
    Standard playing total                              = 144

Flowers/Seasons are optional and OFF by default for standard play.
When explicitly enabled, 8 flower tiles are added on top of the
standard 144, bringing the physical "full box" count to 152 - which
matches a real Majolica-style 152-tile set that includes flowers.

Because flowers are opt-in, `build_tile_set()` defaults to the
144-tile standard playing set and only returns the full 152-tile
physical set when `include_flowers=True` is passed explicitly.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Tuple


class Suit(str, Enum):
    """The three numbered suits used in American Mah Jongg."""

    DOTS = "dots"
    BAMS = "bams"
    CRAKS = "craks"


class Wind(str, Enum):
    """The four wind honor tiles."""

    EAST = "east"
    SOUTH = "south"
    WEST = "west"
    NORTH = "north"


class Dragon(str, Enum):
    """The three dragon honor tiles.

    Traditional suit associations (used for teaching content, not
    required for legality checks here):
        RED   -> associated with Craks
        GREEN -> associated with Bams
        WHITE -> associated with Dots (the "soap"/blank dragon)
    """

    RED = "red"
    GREEN = "green"
    WHITE = "white"


class TileKind(str, Enum):
    """High-level category of a tile, used for dispatch and filtering."""

    SUITED = "suited"
    WIND = "wind"
    DRAGON = "dragon"
    JOKER = "joker"
    FLOWER = "flower"


# Flower/Season labels for the optional 8-tile block. Real physical
# sets vary in artwork; these labels are stable identifiers only.
FLOWER_LABELS: Tuple[str, ...] = (
    "flower_1",
    "flower_2",
    "flower_3",
    "flower_4",
    "season_1",
    "season_2",
    "season_3",
    "season_4",
)


@dataclass(frozen=True)
class Tile:
    """An immutable, hashable representation of a single physical tile.

    Attributes:
        kind: The high-level category (suited, wind, dragon, joker, flower).
        suit: The Suit for suited tiles, else None.
        rank: The numeric rank (1-9) for suited tiles, else None.
        honor: The Wind or Dragon value for honor tiles, else None.
        label: A stable, human-readable label (e.g. "flower_1").
        copy_index: Which physical copy this is (0-based) among
            identical tiles, so four "East" tiles can each get a
            stable, unique identifier for UI/API purposes.
    """

    kind: TileKind
    suit: Optional[Suit]
    rank: Optional[int]
    honor: Optional[object]
    label: Optional[str]
    copy_index: int

    def identifier(self) -> str:
        """Return a stable, serialization-friendly identifier string.

        Format examples:
            "dots_3_c0"      - suited tile, Dots, rank 3, copy 0
            "wind_east_c2"   - honor tile, East wind, copy 2
            "dragon_red_c1"  - honor tile, Red dragon, copy 1
            "joker_c5"       - joker, copy 5
            "flower_flower_1_c0" - flower tile, copy 0

        This identifier is stable across process runs because it is
        derived only from immutable tile facts, never from memory
        addresses or randomization.
        """
        if self.kind is TileKind.SUITED:
            return "{0}_{1}_c{2}".format(self.suit.value, self.rank, self.copy_index)
        if self.kind is TileKind.WIND:
            return "wind_{0}_c{1}".format(self.honor.value, self.copy_index)
        if self.kind is TileKind.DRAGON:
            return "dragon_{0}_c{1}".format(self.honor.value, self.copy_index)
        if self.kind is TileKind.JOKER:
            return "joker_c{0}".format(self.copy_index)
        if self.kind is TileKind.FLOWER:
            return "flower_{0}_c{1}".format(self.label, self.copy_index)
        raise ValueError("Unknown tile kind: {0}".format(self.kind))

    def display_name(self) -> str:
        """Return a human-friendly display name for the curriculum UI."""
        if self.kind is TileKind.SUITED:
            suit_names = {
                Suit.DOTS: "Dot",
                Suit.BAMS: "Bam",
                Suit.CRAKS: "Crak",
            }
            return "{0} {1}".format(self.rank, suit_names[self.suit])
        if self.kind is TileKind.WIND:
            return "{0} Wind".format(self.honor.value.capitalize())
        if self.kind is TileKind.DRAGON:
            return "{0} Dragon".format(self.honor.value.capitalize())
        if self.kind is TileKind.JOKER:
            return "Joker"
        if self.kind is TileKind.FLOWER:
            return self.label.replace("_", " ").title()
        raise ValueError("Unknown tile kind: {0}".format(self.kind))


def is_joker(tile: Tile) -> bool:
    """Return True if the tile is a Joker."""
    return tile.kind is TileKind.JOKER


def is_flower(tile: Tile) -> bool:
    """Return True if the tile is a Flower/Season tile."""
    return tile.kind is TileKind.FLOWER


def is_honor(tile: Tile) -> bool:
    """Return True if the tile is a Wind or Dragon honor tile."""
    return tile.kind in (TileKind.WIND, TileKind.DRAGON)


def is_suited(tile: Tile) -> bool:
    """Return True if the tile is a numbered suited tile (Dots/Bams/Craks)."""
    return tile.kind is TileKind.SUITED


def suit_of(tile: Tile) -> Optional[Suit]:
    """Return the Suit of a suited tile, or None for non-suited tiles.

    Jokers, winds, dragons, and flowers have no suit, so this
    returns None for those kinds rather than raising, since callers
    frequently want to branch on "does this tile belong to a suit"
    without a separate is_suited() check first.
    """
    if tile.kind is TileKind.SUITED:
        return tile.suit
    return None


def _build_suited_tiles() -> List[Tile]:
    """Build the 108 numbered suited tiles: 3 suits x 9 ranks x 4 copies."""
    tiles: List[Tile] = []
    for suit in (Suit.DOTS, Suit.BAMS, Suit.CRAKS):
        for rank in range(1, 10):
            for copy_index in range(4):
                tiles.append(
                    Tile(
                        kind=TileKind.SUITED,
                        suit=suit,
                        rank=rank,
                        honor=None,
                        label=None,
                        copy_index=copy_index,
                    )
                )
    return tiles


def _build_wind_tiles() -> List[Tile]:
    """Build the 16 wind tiles: 4 winds x 4 copies."""
    tiles: List[Tile] = []
    for wind in (Wind.EAST, Wind.SOUTH, Wind.WEST, Wind.NORTH):
        for copy_index in range(4):
            tiles.append(
                Tile(
                    kind=TileKind.WIND,
                    suit=None,
                    rank=None,
                    honor=wind,
                    label=None,
                    copy_index=copy_index,
                )
            )
    return tiles


def _build_dragon_tiles() -> List[Tile]:
    """Build the 12 dragon tiles: 3 dragons x 4 copies."""
    tiles: List[Tile] = []
    for dragon in (Dragon.RED, Dragon.GREEN, Dragon.WHITE):
        for copy_index in range(4):
            tiles.append(
                Tile(
                    kind=TileKind.DRAGON,
                    suit=None,
                    rank=None,
                    honor=dragon,
                    label=None,
                    copy_index=copy_index,
                )
            )
    return tiles


def _build_joker_tiles() -> List[Tile]:
    """Build the 8 joker tiles."""
    tiles: List[Tile] = []
    for copy_index in range(8):
        tiles.append(
            Tile(
                kind=TileKind.JOKER,
                suit=None,
                rank=None,
                honor=None,
                label=None,
                copy_index=copy_index,
            )
        )
    return tiles


def _build_flower_tiles() -> List[Tile]:
    """Build the optional 8 flower/season tiles, one copy each label."""
    tiles: List[Tile] = []
    for label in FLOWER_LABELS:
        tiles.append(
            Tile(
                kind=TileKind.FLOWER,
                suit=None,
                rank=None,
                honor=None,
                label=label,
                copy_index=0,
            )
        )
    return tiles


def build_tile_set(include_flowers: bool = False) -> List[Tile]:
    """Build the canonical tile set.

    Args:
        include_flowers: When False (the default), returns the
            standard 144-tile playing set used for NMJL-style play
            without flowers. When True, also appends the 8 optional
            flower/season tiles, matching a physical 152-tile box
            like the Majolica set referenced in the product brief.

    Returns:
        A list of Tile objects in a deterministic, stable order:
        suited tiles first (Dots, Bams, Craks; rank 1-9; 4 copies
        each), then winds, then dragons, then jokers, then (if
        requested) flowers.

    Raises:
        AssertionError: If the constructed set does not match the
            exact expected counts. This is a deliberate self-check
            so any future edit to the builder functions that breaks
            the canonical counts fails loudly and immediately.
    """
    suited = _build_suited_tiles()
    winds = _build_wind_tiles()
    dragons = _build_dragon_tiles()
    jokers = _build_joker_tiles()

    assert len(suited) == 108, "Expected 108 suited tiles, got {0}".format(len(suited))
    assert len(winds) == 16, "Expected 16 wind tiles, got {0}".format(len(winds))
    assert len(dragons) == 12, "Expected 12 dragon tiles, got {0}".format(len(dragons))
    assert len(jokers) == 8, "Expected 8 joker tiles, got {0}".format(len(jokers))

    tiles: List[Tile] = []
    tiles.extend(suited)
    tiles.extend(winds)
    tiles.extend(dragons)
    tiles.extend(jokers)

    standard_total = len(tiles)
    assert standard_total == 144, "Expected 144-tile standard set, got {0}".format(standard_total)

    if include_flowers:
        flowers = _build_flower_tiles()
        assert len(flowers) == 8, "Expected 8 flower tiles, got {0}".format(len(flowers))
        tiles.extend(flowers)
        full_total = len(tiles)
        assert full_total == 152, "Expected 152-tile full set with flowers, got {0}".format(full_total)

    return tiles


def count_by_kind(tiles: List[Tile]) -> dict:
    """Return a dict mapping TileKind.value -> count for a list of tiles.

    Useful for tests, diagnostics routes, and the curriculum UI when
    explaining set composition to a beginner.
    """
    counts = {kind.value: 0 for kind in TileKind}
    for tile in tiles:
        counts[tile.kind.value] += 1
    return counts


def verify_standard_set(tiles: List[Tile]) -> bool:
    """Verify a tile list matches the standard 144-tile playing set.

    Returns True if the counts match exactly (108 suited, 16 winds,
    12 dragons, 8 jokers, 0 flowers, 144 total). Returns False
    otherwise rather than raising, so callers (e.g. an API health
    check) can report a clean pass/fail without a try/except.
    """
    counts = count_by_kind(tiles)
    if counts[TileKind.SUITED.value] != 108:
        return False
    if counts[TileKind.WIND.value] != 16:
        return False
    if counts[TileKind.DRAGON.value] != 12:
        return False
    if counts[TileKind.JOKER.value] != 8:
        return False
    if counts[TileKind.FLOWER.value] != 0:
        return False
    if len(tiles) != 144:
        return False
    return True


def verify_full_set_with_flowers(tiles: List[Tile]) -> bool:
    """Verify a tile list matches the full 152-tile physical set.

    Same as verify_standard_set() but expects exactly 8 flower tiles
    and a grand total of 152.
    """
    counts = count_by_kind(tiles)
    if counts[TileKind.SUITED.value] != 108:
        return False
    if counts[TileKind.WIND.value] != 16:
        return False
    if counts[TileKind.DRAGON.value] != 12:
        return False
    if counts[TileKind.JOKER.value] != 8:
        return False
    if counts[TileKind.FLOWER.value] != 8:
        return False
    if len(tiles) != 152:
        return False
    return True


# Self-check executed at import time: fail fast if the canonical
# builder ever drifts from the documented ground-truth counts. This
# keeps later modules (rules engine, AI, web layer) safe to assume
# build_tile_set() always returns a legal set.
_STANDARD_SET_SELF_CHECK = build_tile_set(include_flowers=False)
assert verify_standard_set(_STANDARD_SET_SELF_CHECK), "Standard 144-tile set self-check failed"

_FULL_SET_SELF_CHECK = build_tile_set(include_flowers=True)
assert verify_full_set_with_flowers(_FULL_SET_SELF_CHECK), "Full 152-tile set self-check failed"