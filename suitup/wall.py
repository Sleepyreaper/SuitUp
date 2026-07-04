"""Table setup mechanics: dealer selection, wall building, the break, and the deal.

American Mah Jongg is played by four seats (East, South, West, North). This module
models the physical setup a beginner sees at the start of every game, kept small and
deterministic (seedable) so the teaching UI can show a real, reproducible table.
"""
from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import List, Optional

from suitup.tiles import Tile, Wind, build_tile_set

SEATS: List[str] = ["East", "South", "West", "North"]
HAND_SIZE = 13          # each player is dealt 13; East effectively starts with 14
WALL_LENGTH = 19        # tiles per wall, stacked 2 high (38 per seat)
WALL_HEIGHT = 2


@dataclass
class DiceRoll:
    die1: int
    die2: int

    @property
    def total(self) -> int:
        return self.die1 + self.die2


@dataclass
class TableSetup:
    """The full result of setting a table up, ready for the Charleston."""
    dealer_index: int                       # 0..3 into SEATS (the seat that drew East)
    dealer_seat: str
    dice: DiceRoll
    hands: dict = field(default_factory=dict)   # seat -> list[Tile] (East has 14)
    wall_remaining: List[Tile] = field(default_factory=list)

    def hand_counts(self) -> dict:
        return {seat: len(tiles) for seat, tiles in self.hands.items()}


def roll_dice(rng: random.Random) -> DiceRoll:
    """Roll two dice. East rolls to decide where the wall is broken."""
    return DiceRoll(rng.randint(1, 6), rng.randint(1, 6))


def choose_dealer(rng: random.Random) -> int:
    """Dealer selection: each player draws a face-down Wind; whoever draws East
    is the first dealer. We model that as a fair random pick of a seat index."""
    return rng.randrange(len(SEATS))


def build_wall(rng: random.Random, include_flowers: bool = False) -> List[Tile]:
    """Build and shuffle the full tile set into a single wall (the four physical
    19x2 walls, concatenated). Deterministic given the rng."""
    tiles = build_tile_set(include_flowers=include_flowers)
    rng.shuffle(tiles)
    return tiles


def deal(rng: Optional[random.Random] = None, seed: Optional[int] = None,
         include_flowers: bool = False) -> TableSetup:
    """Run a complete, reproducible table setup: pick the dealer, roll to break
    the wall, and deal 13 tiles to every seat (East draws one more to reach 14).
    Returns a TableSetup the UI can render tile-by-tile.
    """
    rng = rng or random.Random(seed)
    dealer_index = choose_dealer(rng)
    dice = roll_dice(rng)
    wall = build_wall(rng, include_flowers=include_flowers)

    hands: dict = {seat: [] for seat in SEATS}
    pos = 0
    for _ in range(HAND_SIZE):
        for seat in SEATS:
            hands[seat].append(wall[pos])
            pos += 1
    # East (the dealer's seat for turn purposes) takes the extra 14th tile.
    hands[SEATS[dealer_index]].append(wall[pos])
    pos += 1

    return TableSetup(
        dealer_index=dealer_index,
        dealer_seat=SEATS[dealer_index],
        dice=dice,
        hands=hands,
        wall_remaining=wall[pos:],
    )
