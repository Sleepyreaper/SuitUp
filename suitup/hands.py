"""Winning hands + the win matcher for the SuitUp simulator.

American Mah Jongg hands are exactly 14 tiles and have NO runs/sequences — a hand
is built from exact groups of identical tiles: Pairs (2), Pungs (3), Kongs (4).
A legal win matches one of the hand structures below. Jokers are wild in groups of
3+ (never in a Pair, and a group can never be all jokers).

These are original SuitUp teaching hands — they are NOT the copyrighted National
Mah Jongg League card. For real scored play, use your own current NMJL card.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from suitup.tiles import Tile, is_joker, suit_of

HAND_TILES = 14


@dataclass(frozen=True)
class WinningHand:
    hand_id: str
    name: str
    difficulty: str          # "intro" | "building" | "stretch"
    group_sizes: Tuple[int, ...]   # e.g. (3, 3, 3, 3, 2) — must sum to 14
    single_suit: bool        # all suited tiles must be the SAME suit
    points: int
    teaches: str
    no_jokers: bool = False  # jokers illegal anywhere (Singles & Pairs hands)
    # Optional exact-tile spec: a tuple of (tile identity, group size). When set,
    # the hand requires those SPECIFIC tiles (e.g. NEWS winds), overriding
    # group_sizes/single_suit. Identities look like "wind_north", "dragon_white".
    fixed: Optional[Tuple[Tuple[str, int], ...]] = None

    def describe(self) -> str:
        if self.fixed is not None:
            return " + ".join(f"{_pretty_ident(i)}×{n}" for i, n in self.fixed)
        parts = []
        for s in self.group_sizes:
            parts.append({1: "Single", 2: "Pair", 3: "Pung",
                          4: "Kong", 5: "Quint"}.get(s, f"{s}-group"))
        suit = " (all one suit)" if self.single_suit else ""
        nj = " · no jokers" if self.no_jokers else ""
        return " + ".join(parts) + suit + nj


def _pretty_ident(ident: str) -> str:
    names = {
        "wind_north": "North", "wind_east": "East", "wind_west": "West",
        "wind_south": "South", "dragon_red": "Red", "dragon_green": "Green",
        "dragon_white": "Soap (White)",
    }
    if ident in names:
        return names[ident]
    suit, _, rank = ident.partition("_")
    label = {"dots": "Dot", "bams": "Bam", "craks": "Crak"}.get(suit, suit)
    return f"{rank}-{label}"


# Ordered easiest → hardest. Every group_sizes sums to 14.
WINNING_HANDS: Tuple[WinningHand, ...] = (
    WinningHand("four_pungs", "Four Pungs & a Pair", "intro",
                (3, 3, 3, 3, 2), False, 25,
                "The friendliest hand: four Pungs (three-of-a-kind) plus a Pair."),
    WinningHand("two_kongs_two_pungs", "Two Kongs & Two Pungs", "building",
                (4, 4, 3, 3), False, 35,
                "Two Kongs (four-of-a-kind) and two Pungs — no pair needed."),
    WinningHand("three_kongs", "Three Kongs & a Pair", "building",
                (4, 4, 4, 2), False, 40,
                "Three Kongs and a Pair — collect four-of-a-kinds and lean on jokers."),
    WinningHand("one_suit", "Single-Suit Pungs", "stretch",
                (3, 3, 3, 3, 2), True, 50,
                "Four Pungs and a Pair, ALL in one suit (Dots, Bams, or Craks)."),
    WinningHand("double_quint", "Double Quint", "stretch",
                (5, 5, 4), False, 60,
                "Two Quints (five-of-a-kind) and a Kong. A Quint is impossible "
                "without a Joker — there are only four of each tile."),
    WinningHand("news_soap", "NEWS & Dragons (Singles & Pairs)", "stretch",
                (), False, 75,
                "An original Singles & Pairs hand: the four NEWS winds as singles, "
                "plus dragon and number pairs (Soap = White Dragon = 0). NO jokers "
                "allowed anywhere — the hardest, highest-scoring style.",
                no_jokers=True,
                fixed=(("wind_north", 1), ("wind_east", 1), ("wind_west", 1),
                       ("wind_south", 1), ("dragon_red", 2), ("dragon_green", 2),
                       ("dragon_white", 2), ("dots_2", 2), ("dots_6", 2))),
)

# The simple AI only targets achievable structural hands; the exact-tile /
# no-joker hands are advanced practice targets a human can aim for.
AI_TARGET_HANDS: Tuple[WinningHand, ...] = tuple(
    h for h in WINNING_HANDS if h.fixed is None and not h.no_jokers)


def hand_by_id(hand_id: str) -> Optional[WinningHand]:
    return next((h for h in WINNING_HANDS if h.hand_id == hand_id), None)


def _identity(tile: Tile) -> str:
    """A tile's identity ignoring which physical copy it is (e.g. 'dots_1')."""
    return tile.identifier().rsplit("_c", 1)[0]


def _can_fill(counts: Dict[str, int], jokers: int, sizes: List[int]) -> bool:
    """Can the natural-tile counts (+ jokers) be partitioned EXACTLY into groups of
    the given sizes? Each group is one identity; jokers fill only groups of 3+, and
    every group needs at least one natural tile (no all-joker groups)."""
    if not sizes:
        return jokers == 0 and all(v == 0 for v in counts.values())
    size = sizes[0]
    rest = sizes[1:]
    for ident, c in list(counts.items()):
        if c <= 0:
            continue
        max_nat = min(c, size)
        for k in range(max_nat, 0, -1):          # k natural tiles of this identity
            need_joker = size - k
            if need_joker > 0 and size < 3:      # a Pair can't use a joker
                continue
            if need_joker > jokers:
                continue
            counts[ident] -= k
            if _can_fill(counts, jokers - need_joker, rest):
                counts[ident] += k
                return True
            counts[ident] += k
    return False


def matches_hand(tiles: List[Tile], hand: WinningHand) -> bool:
    """True if exactly-14 `tiles` complete `hand` (structure + suit + joker rules)."""
    if len(tiles) != HAND_TILES:
        return False
    jokers = sum(1 for t in tiles if is_joker(t))
    if hand.no_jokers and jokers > 0:
        return False
    if hand.fixed is not None:
        return _matches_fixed(tiles, hand, jokers)
    if hand.single_suit:
        suits = {suit_of(t) for t in tiles if not is_joker(t) and suit_of(t) is not None}
        honors = any(not is_joker(t) and suit_of(t) is None for t in tiles)
        if honors or len(suits) > 1:             # single-suit hands are suited-only, one suit
            return False
    counts: Dict[str, int] = Counter(_identity(t) for t in tiles if not is_joker(t))
    return _can_fill(dict(counts), jokers, sorted(hand.group_sizes, reverse=True))


def _matches_fixed(tiles: List[Tile], hand: WinningHand, jokers: int) -> bool:
    """Match an exact-tile hand: the tiles must partition into the specific
    (identity, size) groups, honoring joker rules (none for singles/pairs)."""
    counts: Dict[str, int] = Counter(_identity(t) for t in tiles if not is_joker(t))
    jok = jokers
    for ident, size in hand.fixed:
        have = counts.get(ident, 0)
        use = min(have, size)
        counts[ident] = have - use
        short = size - use
        if short > 0:
            if size < 3 or hand.no_jokers:       # singles/pairs (or no-joker hand)
                return False
            if short > jok:
                return False
            jok -= short
    return jok == 0 and all(v == 0 for v in counts.values())


def winning_hands_for(tiles: List[Tile]) -> List[WinningHand]:
    """Every defined hand that these 14 tiles complete (usually 0 or 1)."""
    return [h for h in WINNING_HANDS if matches_hand(tiles, hand=h)]


def is_winning(tiles: List[Tile]) -> bool:
    return bool(winning_hands_for(tiles))


@dataclass
class HandAssessment:
    hand: WinningHand
    placed: int                       # tiles (natural+joker) that fit the structure
    needed: int                       # tiles still required to complete (14 - placed)
    keep_ids: List[str]               # tile identities worth keeping for this hand
    deadwood: List[Tile]              # tiles that do NOT help this hand (discard first)
    wants: List[Tuple[str, int]]      # (identity, how many more of it would help)

    @property
    def completeness(self) -> float:
        return round(self.placed / HAND_TILES, 3)


def _dominant_suit(tiles: List[Tile]) -> Optional[str]:
    counts: Counter = Counter()
    for t in tiles:
        s = suit_of(t)
        if s is not None and not is_joker(t):
            counts[s] += 1
    return counts.most_common(1)[0][0] if counts else None


def assess_hand(tiles: List[Tile], hand: WinningHand) -> HandAssessment:
    """Greedily fit `tiles` to `hand` to gauge closeness and pick deadwood.

    Not an exhaustive solver — a fast heuristic good enough to steer the AI and
    to power the "tiles you still need" tutorial hints.
    """
    jokers = [t for t in tiles if is_joker(t)]
    naturals = [t for t in tiles if not is_joker(t)]

    if hand.fixed is not None:
        return _assess_fixed(tiles, hand, jokers, naturals)

    if hand.single_suit:
        keep_suit = _dominant_suit(naturals)
        usable = [t for t in naturals if suit_of(t) == keep_suit]
    else:
        usable = list(naturals)

    by_ident: Dict[str, List[Tile]] = {}
    for t in usable:
        by_ident.setdefault(_identity(t), []).append(t)
    # Largest natural groups first fill the largest slots.
    ranked = sorted(by_ident.items(), key=lambda kv: len(kv[1]), reverse=True)

    sizes = sorted(hand.group_sizes, reverse=True)
    joker_pool = 0 if hand.no_jokers else len(jokers)
    placed = 0
    keep_ids: List[str] = []
    used_idents = set()
    wants: List[Tuple[str, int]] = []
    idx = 0
    for size in sizes:
        if idx < len(ranked):
            ident, group = ranked[idx]
            idx += 1
            nat = min(len(group), size)
            placed += nat
            keep_ids.append(ident)
            used_idents.add(ident)
            shortfall = size - nat
            if shortfall > 0 and size >= 3:       # jokers may finish a Pung/Kong
                fill = min(shortfall, joker_pool)
                joker_pool -= fill
                placed += fill
                shortfall -= fill
            if shortfall > 0:
                wants.append((ident, shortfall))
        else:
            wants.append(("any", size))           # a whole group still missing

    deadwood = [t for t in tiles
                if not is_joker(t) and _identity(t) not in used_idents]
    return HandAssessment(hand=hand, placed=placed, needed=HAND_TILES - placed,
                          keep_ids=keep_ids, deadwood=deadwood, wants=wants)


def _assess_fixed(tiles, hand, jokers, naturals) -> HandAssessment:
    counts: Counter = Counter(_identity(t) for t in naturals)
    joker_pool = 0 if hand.no_jokers else len(jokers)
    placed = 0
    keep_ids: List[str] = []
    used = set()
    wants: List[Tuple[str, int]] = []
    for ident, size in hand.fixed:
        have = counts.get(ident, 0)
        use = min(have, size)
        placed += use
        keep_ids.append(ident)
        used.add(ident)
        short = size - use
        if short > 0 and size >= 3 and not hand.no_jokers:
            fill = min(short, joker_pool)
            joker_pool -= fill
            placed += fill
            short -= fill
        if short > 0:
            wants.append((ident, short))
    deadwood = [t for t in tiles
                if (is_joker(t) and hand.no_jokers) or
                (not is_joker(t) and _identity(t) not in used)]
    return HandAssessment(hand=hand, placed=placed, needed=HAND_TILES - placed,
                          keep_ids=keep_ids, deadwood=deadwood, wants=wants)


def best_assessment(tiles: List[Tile],
                    hands: Tuple[WinningHand, ...] = WINNING_HANDS) -> HandAssessment:
    """The target hand these tiles are currently closest to completing."""
    return max((assess_hand(tiles, h) for h in hands), key=lambda a: a.placed)

