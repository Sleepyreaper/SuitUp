"""Charleston state machine for American Mah Jongg (SuitUp).

The Charleston is the ritual tile-passing phase that happens before play
begins. This module implements it as a pure, deterministic state machine so
it can be driven interactively from the web UI or headlessly from tests and
the AI opponent.

Phase sequence:
    FIRST_RIGHT -> FIRST_ACROSS -> FIRST_LEFT -> DECIDE_SECOND
      -> (if all four players vote to continue)
         SECOND_LEFT -> SECOND_ACROSS -> SECOND_RIGHT -> COURTESY -> COMPLETE
      -> (if any player votes to stop)
         COURTESY -> COMPLETE

Rules encoded here:
    * The first Charleston is mandatory: exactly 3 tiles pass right, then
      3 across, then 3 left.
    * After the first Charleston, all four players vote on whether to do
      the optional second Charleston. It only happens if every player
      agrees; otherwise the table proceeds straight to the courtesy pass.
    * The second Charleston mirrors the first in reverse order: left,
      across, right -- again exactly 3 tiles per pass.
    * Jokers and flowers can never be passed, in either Charleston or the
      courtesy pass.
    * Blind passes (passing 3 tiles without looking at what you're giving
      away) are only permitted during the second Charleston.
    * The courtesy pass is optional and happens only between seats directly
      across from one another (the two "opposite" pairs at a 4-player
      table). Each side of a pair privately proposes a count from 0 to 3;
      the pass only actually happens if both sides propose the same
      nonzero count. Mismatched or zero counts mean no tiles move for
      that pair.

Seating convention used throughout this module: four seats numbered
0-3 arranged clockwise around the table. "Right" means the next seat
clockwise, "left" means the previous seat clockwise, and "across" means
the seat two positions away (only meaningful for exactly 4 players).
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum, unique
from typing import Dict, List, Optional, Tuple

from suitup.tiles import Tile, TileKind

NUM_PLAYERS = 4
CHARLESTON_PASS_SIZE = 3
COURTESY_MIN_TILES = 0
COURTESY_MAX_TILES = 3

# The two opposite-seat pairs that negotiate the courtesy pass.
COURTESY_PAIRS: Tuple[Tuple[int, int], ...] = ((0, 2), (1, 3))

_UNPASSABLE_KINDS = (TileKind.JOKER, TileKind.FLOWER)


class CharlestonRuleViolation(ValueError):
    """Raised when a caller attempts an illegal pass, vote, or transition."""


@unique
class PassDirection(Enum):
    RIGHT = "right"
    ACROSS = "across"
    LEFT = "left"


@unique
class CharlestonPhase(Enum):
    FIRST_RIGHT = "first_right"
    FIRST_ACROSS = "first_across"
    FIRST_LEFT = "first_left"
    DECIDE_SECOND = "decide_second"
    SECOND_LEFT = "second_left"
    SECOND_ACROSS = "second_across"
    SECOND_RIG