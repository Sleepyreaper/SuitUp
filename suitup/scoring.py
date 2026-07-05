"""Payment-based scoring for the SuitUp simulator, following how American Mah
Jongg is actually settled at the table.

Each hand has a value (SuitUp uses its own hand values, in the same 25-75 range as
a real card). When someone declares Mah Jongg, the other players PAY the winner:

* Self-pick (you drew your own winning tile from the wall): all three losers pay
  DOUBLE the hand value.
* Won on a discard: the player who threw the winning tile pays DOUBLE; the other
  two losers pay the single value.
* Jokerless (no jokers anywhere in the hand): the whole payout DOUBLES again.

This mirrors standard NMJL settlement (you'd swap coins/chips). It is a teaching
model, not the copyrighted card, but the mechanics are the real ones.
"""
from __future__ import annotations

from typing import Dict, List, Optional

from suitup.hands import WinningHand
from suitup.tiles import Tile, is_joker


def settle_win(hand: WinningHand, tiles: List[Tile], winner_index: int,
               self_drawn: bool, discarder_index: Optional[int],
               seats: int = 4) -> dict:
    """Compute what each loser pays the winner. Returns a full, explainable
    breakdown that the UI can render as the settlement."""
    value = hand.points
    jokers_used = sum(1 for t in tiles if is_joker(t))
    jokerless = jokers_used == 0
    joker_mult = 2 if jokerless else 1

    payments: Dict[int, int] = {}
    lines: List[dict] = []
    for i in range(seats):
        if i == winner_index:
            continue
        if self_drawn:
            factor = 2                       # everyone pays double on a self-pick
            reason = "self-pick x2"
        elif discarder_index is not None and i == discarder_index:
            factor = 2                       # thrower of the winning tile pays double
            reason = "threw winning tile x2"
        else:
            factor = 1
            reason = "x1"
        amount = value * factor * joker_mult
        payments[i] = amount
        lines.append({"seat_index": i, "amount": amount, "reason": reason})

    total = sum(payments.values())
    return {
        "hand_id": hand.hand_id,
        "hand_name": hand.name,
        "value": value,
        "jokers_used": jokers_used,
        "jokerless": jokerless,
        "self_drawn": self_drawn,
        "payments": payments,             # loser index -> amount paid to winner
        "lines": lines,
        "total": total,                   # what the winner collects
    }
