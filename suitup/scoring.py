"""Simplified, teaching-friendly scoring for the SuitUp simulator.

Real American Mah Jongg scores from the NMJL card value printed next to each hand
(and doubles for jokerless / self-picked wins). SuitUp uses its own original hands,
so we score by the hand's difficulty plus small, easy-to-explain bonuses. This is
meant to teach the *idea* of scoring, not to reproduce any copyrighted card values.
"""
from __future__ import annotations

from typing import List, Optional

from suitup.hands import WinningHand
from suitup.tiles import Tile, is_joker

SELF_DRAW_BONUS = 10        # you completed the hand off your own drawn tile
JOKERLESS_BONUS = 10        # you used no jokers at all


def score_win(hand: WinningHand, concealed_and_exposed: List[Tile],
              self_drawn: bool) -> dict:
    """Return a scoring breakdown for a winning hand."""
    base = hand.points
    jokers_used = sum(1 for t in concealed_and_exposed if is_joker(t))
    bonuses = []
    total = base
    if self_drawn:
        total += SELF_DRAW_BONUS
        bonuses.append({"label": "Self-drawn (picked your own winning tile)",
                        "points": SELF_DRAW_BONUS})
    if jokers_used == 0:
        total += JOKERLESS_BONUS
        bonuses.append({"label": "Jokerless (no jokers used)",
                        "points": JOKERLESS_BONUS})
    return {
        "hand_id": hand.hand_id,
        "hand_name": hand.name,
        "base": base,
        "bonuses": bonuses,
        "jokers_used": jokers_used,
        "total": total,
    }
