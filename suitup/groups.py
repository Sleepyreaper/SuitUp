"""Group recognition — the building blocks of every American Mah Jongg hand.

American Mah Jongg has no runs; legal hands are made of exact groups: Pairs (2),
Pungs (3), Kongs (4), and Quints (5) of the SAME tile. Jokers are wild in groups
of 3 or more, but never in a Pair (or as a single). These helpers let the teaching
UI check a beginner's selection and explain why it is or isn't a valid group.
"""
from __future__ import annotations

from typing import List

from suitup.tiles import Tile, is_joker

GROUP_SIZES = {2: "Pair", 3: "Pung", 4: "Kong", 5: "Quint"}


def _non_joker_key(tile: Tile) -> str:
    """A comparable identity for a tile ignoring which physical copy it is."""
    return tile.identifier().rsplit("_c", 1)[0]


def group_name(size: int) -> str:
    return GROUP_SIZES.get(size, f"{size}-tile group")


def is_valid_group(tiles: List[Tile]) -> bool:
    """True if the tiles form a legal Pair/Pung/Kong/Quint under joker rules."""
    n = len(tiles)
    if n not in GROUP_SIZES:
        return False
    jokers = [t for t in tiles if is_joker(t)]
    naturals = [t for t in tiles if not is_joker(t)]
    if n == 2:  # a Pair may not contain a joker
        return not jokers and _non_joker_key(naturals[0]) == _non_joker_key(naturals[1])
    if not naturals:  # a group of 3+ can't be all jokers
        return False
    key = _non_joker_key(naturals[0])
    return all(_non_joker_key(t) == key for t in naturals)


def describe_group(tiles: List[Tile]) -> str:
    """A short, beginner-friendly explanation of a selected group."""
    n = len(tiles)
    if n not in GROUP_SIZES:
        return (f"{n} tiles isn't a legal group — American Mah Jongg groups are "
                f"Pairs (2), Pungs (3), Kongs (4), or Quints (5).")
    if is_valid_group(tiles):
        jokers = sum(1 for t in tiles if is_joker(t))
        extra = f" (using {jokers} joker{'s' if jokers != 1 else ''})" if jokers else ""
        natural = next((t for t in tiles if not is_joker(t)), None)
        of = f" of {natural.display_name()}" if natural else ""
        return f"✓ Valid {group_name(n)}{of}{extra}."
    if n == 2 and any(is_joker(t) for t in tiles):
        return "✗ A Pair cannot use a Joker — you need two identical natural tiles."
    return f"✗ Not a valid {group_name(n)} — the natural tiles must all be the same."
