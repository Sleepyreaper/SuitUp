"""
suitup/wall.py

Setup mechanics for SuitUp's American Mah Jongg engine. Glavin!

This module owns everything that happens BEFORE the first real turn of
play: assigning table seats via a dealer wind draw, building the four
walls (19 stacks x 2 tiles high each), simulating East's dice roll to
find the break point, and dealing hands so that East ends up with 14
tiles (ready to discard first) while South, West, and North each end
up with 13.

The functions here are engine-facing, not UI-facing: they return plain
dataclasses of tiles and enums. Each public step function also returns
a short, beginner-friendly description string. The web layer collects
these into a guided "here is what just happened and why" walkthrough;
this module never renders HTML or touches request/response objects.

SIMPLIFICATIONS, DOCUMENTED ON PURPOSE:
  - Real-table dealer rotation across an entire session (East passing
    to the next player after a loss) is out of scope here; this module
    only handles selecting the FIRST dealer of a fresh game via a wind
    tile draw, which is the actual beginner-facing ritual the owner
    will perform with their physical Majolica set.
  - Traditional play uses two dice-rolls: one to pick which wall
    breaks, one to pick the break stack within it. For a first release
    we use a single 3-die roll and apply its total to both steps. This
    keeps the code and the on-screen explanation simple for a total
    beginner, while preserving the correct tile counts and the correct
    "East ends up with 14" outcome, which is the part the rules engine
    actually depends on.
  - The last 14 tiles of the live draw order are set aside as a dead
    wall (kong box) for future kong-replacement logic. This module
    only reserves them; it does not consume them.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from .tiles import Tile, Wind, build_standard_set

__all__ = [
    "STACKS_PER_WALL",
    "TILES_PER_STACK",
    "TILES_PER_WALL",
    "DEAD_WALL_SIZE",
    "TURN_ORDER",
    "SeatAssignment",
    "Stack",
    "Wall",
    "DiceRoll",
    "BreakResult",
    "GameSetupState",
    "assign_seats_by_dealer_wind_draw",
    "build_walls",
    "roll_dice",
    "determine_break",
    "deal_tiles",
    "build_game_setup",
]


# --------------------------------------------------------------------------
# Ground-truth wall geometry: a physical American Mah Jongg wall is built
# 19 tiles long by 2 tiles high, per side, for four sides = 152 tiles.
# --------------------------------------------------------------------------
STACKS_PER_WALL: int = 19
TILES_PER_STACK: int = 2
TILES_PER_WALL: int = STACKS_PER_WALL * TILES_PER_STACK  # 38
DEAD_WALL_SIZE: int = 14

# Turn order convention used by this engine: East acts first, then play
# proceeds East -> South -> West -> North -> East, looping. This is the
# convention most beginner-facing American Mah Jongg materials teach at
# the table, and it is what the rest of SuitUp's turn engine expects.
TURN_ORDER: Tuple[Wind, Wind, Wind, Wind] = (
    Wind.EAST,
    Wind.SOUTH,
    Wind.WEST,
    Wind.NORTH,
)


# --------------------------------------------------------------------------
# Dataclasses
# --------------------------------------------------------------------------
@dataclass(frozen=True)
class SeatAssignment:
    """Result of the dealer wind draw: who sits where, who deals first."""

    seat_of_player: Dict[str, Wind]
    player_of_seat: Dict[Wind, str]
    dealer_wind: Wind
    turn_order: Tuple[Wind, Wind, Wind, Wind]
    description: str


@dataclass(frozen=True)
class Stack:
    """One stack of two tiles within a wall.

    ``tiles`` is stored as (bottom, top). Physically the top tile sits
    on the bottom tile and is drawn first, so draw order pulls
    ``tiles[1]`` (top) before ``tiles[0]`` (bottom).
    """

    index: int
    tiles: Tuple[Tile, Tile]

    def draw_order(self) -> Tuple[Tile, Tile]:
        """Return this stack's two tiles in the order they are drawn."""
        bottom, top = self.tiles
        return (top, bottom)


@dataclass(frozen=True)
class Wall:
    """One side's wall: 19 stacks, indexed 0 (right end) to 18 (left end)."""

    wind: Wind
    stacks: Tuple[Stack, ...]

    def tile_count(self) -> int:
        return sum(len(stack.tiles) for stack in self.stacks)


@dataclass(frozen=True)
class DiceRoll:
    """A simulated roll of three six-sided dice."""

    die1: int
    die2: int
    die3: int

    @property
    def total(self) -> int:
        return self.die1 + self.die2 + self.die3


@dataclass(frozen=True)
class BreakResult:
    """Which wall breaks, at which stack, and why (for the beginner UI)."""

    dice_roll: DiceRoll
    broken_wind: Wind
    break_stack_index: int
    description: str


@dataclass(frozen=True)
class GameSetupState:
    """Complete structured setup state handed off to the turn engine."""

    seat_assignment: SeatAssignment
    walls: Dict[Wind, Wall]
    dice_roll: DiceRoll
    break_result: BreakResult
    hands: Dict[Wind, List[Tile]]
    live_wall: List[Tile]
    dead_wall: List[Tile]
    current_turn: Wind
    first_discarder: Wind
    steps: List[Dict[str, str]] = field(default_factory=list)


# --------------------------------------------------------------------------
# Step 1: dealer wind draw and seat assignment
# --------------------------------------------------------------------------
def assign_seats_by_dealer_wind_draw(
    player_ids: List[str],
    rng: Optional[random.Random] = None,
) -> SeatAssignment:
    """Assign each player a seat wind by drawing shuffled wind tiles.

    Four wind tiles (East, South, West, North), one of each, are
    shuffled and dealt one to each player. Whoever draws East becomes
    the dealer and sits East for this game.
    """
    if len(player_ids) != 4:
        raise ValueError(
            "American Mah Jongg is played by exactly four players; "
            "got {0}.".format(len(player_ids))
        )

    rng = rng if rng is not None else random.Random()
    draw_winds: List[Wind] = [Wind.EAST, Wind.SOUTH, Wind.WEST, Wind.NORTH]
    shuffled_players = list(player_ids)
    rng.shuffle(shuffled_players)

    seat_of_player: Dict[str, Wind] = {}
    player_of_seat: Dict[Wind, str] = {}
    for player_id, wind in zip(shuffled_players, draw_winds):
        seat_of_player[player_id] = wind
        player_of_seat[wind] = player_id

    dealer_id = player_of_seat[Wind.EAST]
    description = (
        "Each player drew a wind tile from a shuffled set of East, "
        "South, West, and North. {0} drew East and is the dealer for "
        "this hand; play will proceed East, South, West, North, "
        "looping back to East.".format(dealer_id)
    )

    return SeatAssignment(
        seat_of_player=seat_of_player,
        player_of_seat=player_of_seat,
        dealer_wind=Wind.EAST,
        turn_order=TURN_ORDER,
        description=description,
    )


# --------------------------------------------------------------------------
# Step 2: build four walls of 19 stacks x 2 tiles high
# --------------------------------------------------------------------------
def build_walls(
    tiles: Optional[List[Tile]] = None,
    rng: Optional[random.Random] = None,
) -> Dict[Wind, Wall]:
    """Shuffle all 152 tiles and stack them into four walls of 19x2.

    If ``tiles`` is not supplied, a fresh standard 152-tile set is
    built via ``build_standard_set()`` from ``suitup.tiles``.
    """