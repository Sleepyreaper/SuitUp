"""A small, teaching-oriented AI opponent + practice hand.

This is intentionally simple and rules-honest: it plays legal moves so a beginner
can practice the FLOW of a turn (draw, then discard) against bots at three levels.
It is not a competitive engine — its job is to make the mechanics tangible.
"""
from __future__ import annotations

import random
from collections import Counter
from typing import List, Optional

from suitup.tiles import Tile, is_joker

LEVELS = {
    1: "Beginner — keeps pairs, discards obvious singles at random.",
    2: "Improver — keeps pairs and jokers, discards the least-connected tile.",
    3: "Sharp — like Improver, but also avoids discarding a tile it has seen little of.",
}


def _key(tile: Tile) -> str:
    return tile.identifier().rsplit("_c", 1)[0]


def _counts(hand: List[Tile]) -> Counter:
    return Counter(_key(t) for t in hand if not is_joker(t))


def choose_discard(hand: List[Tile], level: int = 1,
                   seen: Optional[Counter] = None,
                   rng: Optional[random.Random] = None) -> Tile:
    """Pick a tile to discard from `hand` at the given AI level. Never discards a
    Joker. Returns the chosen Tile (which the caller removes from the hand)."""
    rng = rng or random.Random()
    candidates = [t for t in hand if not is_joker(t)] or list(hand)
    counts = _counts(hand)

    if level <= 1:
        singles = [t for t in candidates if counts[_key(t)] == 1]
        return rng.choice(singles or candidates)

    # Level 2 & 3: score by how connected a tile is (more copies in hand = keep).
    seen = seen or Counter()

    def score(t: Tile) -> tuple:
        in_hand = counts[_key(t)]
        seen_out = seen[_key(t)] if level >= 3 else 0
        # Lower score = better discard candidate. Fewer-in-hand first; at level 3,
        # break ties by discarding tiles already widely seen (safer / less useful).
        return (in_hand, -seen_out, rng.random())

    return min(candidates, key=score)


def bot_take_turn(hand: List[Tile], wall: List[Tile], level: int,
                  seen: Optional[Counter] = None,
                  rng: Optional[random.Random] = None) -> dict:
    """A bot draws the top wall tile (if any) then discards one. Mutates hand and
    wall in place. Returns a small record of what happened for the UI log."""
    rng = rng or random.Random()
    drew = None
    if wall:
        drew = wall.pop(0)
        hand.append(drew)
    discard = choose_discard(hand, level=level, seen=seen, rng=rng)
    hand.remove(discard)
    return {"drew": drew.display_name() if drew else None,
            "discarded": discard.display_name(),
            "discard_tile": discard}
