"""The Charleston — American Mah Jongg's signature tile-passing ritual.

Before play begins, players pass unwanted tiles to improve everyone's starting
hands. This module describes the exact, ordered pass sequence for the teaching UI
and enforces the one hard rule beginners always trip on: you may NEVER pass a
Joker (or a Flower) during the Charleston.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List

from suitup.tiles import Tile, is_flower, is_joker

TILES_PER_PASS = 3


@dataclass
class CharlestonStep:
    order: int
    phase: str          # "first", "second", or "courtesy"
    direction: str      # "right", "across", "left", or "opposite"
    count: int          # tiles passed this step
    mandatory: bool
    blind_allowed: bool
    note: str


def can_pass_tile(tile: Tile) -> bool:
    """Jokers and Flowers may never be passed in the Charleston."""
    return not is_joker(tile) and not is_flower(tile)


def illegal_pass_tiles(tiles: List[Tile]) -> List[Tile]:
    """Return any tiles in the proposed pass that are not allowed (jokers/flowers)."""
    return [t for t in tiles if not can_pass_tile(t)]


def validate_pass(tiles: List[Tile], expected_count: int = TILES_PER_PASS) -> List[str]:
    """Return a list of human-readable problems with a proposed pass (empty = OK)."""
    problems: List[str] = []
    if len(tiles) != expected_count:
        problems.append(f"You must pass exactly {expected_count} tiles (you selected {len(tiles)}).")
    for t in illegal_pass_tiles(tiles):
        problems.append(f"You cannot pass {t.display_name()} — Jokers and Flowers stay in your hand.")
    return problems


def charleston_sequence(second_charleston: bool = True,
                        courtesy: bool = True) -> List[CharlestonStep]:
    """The ordered Charleston steps a beginner walks through.

    First Charleston (mandatory): right, across, left.
    Second Charleston (optional, by table agreement): left, across, right.
    Courtesy pass (optional): 1-3 tiles with the player opposite you.
    """
    steps: List[CharlestonStep] = []
    order = 1

    first = [
        ("right", "Pass 3 tiles to the player on your RIGHT."),
        ("across", "Pass 3 tiles ACROSS the table. (A 'blind pass' is allowed here — "
                   "you may pass tiles you just received without looking.)"),
        ("left", "Pass 3 tiles to the player on your LEFT."),
    ]
    for direction, note in first:
        steps.append(CharlestonStep(order, "first", direction, TILES_PER_PASS,
                                    mandatory=True, blind_allowed=(direction == "across"),
                                    note=note))
        order += 1

    if second_charleston:
        second = [
            ("left", "Pass 3 tiles to your LEFT."),
            ("across", "Pass 3 tiles ACROSS (blind pass allowed)."),
            ("right", "Pass 3 tiles to your RIGHT."),
        ]
        for direction, note in second:
            steps.append(CharlestonStep(order, "second", direction, TILES_PER_PASS,
                                        mandatory=False, blind_allowed=(direction == "across"),
                                        note=note))
            order += 1

    if courtesy:
        steps.append(CharlestonStep(
            order, "courtesy", "opposite", 0, mandatory=False, blind_allowed=False,
            note="Optional courtesy pass: you and the player OPPOSITE you may agree to "
                 "swap 1, 2, or 3 tiles (both pass the same number)."))

    return steps
