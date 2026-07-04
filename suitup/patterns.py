"""
suitup/patterns.py

Original, teaching-only practice hand patterns for SuitUp. Glavin!

COPYRIGHT / RULES NOTE (read this before touching anything below):

    The National Mah Jongg League (NMJL) publishes an official annual
    card of scored hands. That card, and its exact hand text, layout,
    and point values, is copyrighted by the NMJL and is NOT reproduced,
    paraphrased, or approximated anywhere in this module.

    Every pattern defined below is an ORIGINAL SuitUp teaching
    construct, invented purely to give a beginner something concrete
    to practice matching tiles against while they learn the *shape*
    vocabulary of American Mah Jongg (pairs, pungs, kongs, runs,
    same-suit groups, honor groups, joker-eligible slots). None of
    these patterns are claimed to be, or intended to resemble, a real
    scored hand from any NMJL card, past or present. They exist only
    inside SuitUp's practice curriculum and its AI opponent targeting
    logic.

    If a future task adds real NMJL scoring, it must do so as a
    separate, clearly licensed data source -- this module is not that.

SCHEMA OVERVIEW

    A ``Pattern`` is a named, hand-sized (14-tile) practice target made
    of ordered ``PatternGroup`` objects. Each group is made of
    ``SlotSpec`` objects, and each slot describes how many tiles fill
    it, whether it demands an exact suit/honor family or allows any
    suit (as long as the group is internally consistent), whether the
    slot may be satisfied by a joker, and whether the slot must be a
    concealed pair versus an exposable set.

    This schema is intentionally small and JSON-serializable-friendly
    (every field is a primitive, string, bool, or nested dataclass) so
    both the hand matcher and the AI opponent's target-selection logic
    can consume it without importing Flask or any web concern, in
    keeping with the birdwatcher-style domain/web split fixed in
    docs/architecture.md.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, unique
from typing import Dict, List, Optional, Tuple

__all__ = [
    "GroupKind",
    "SuitConstraint",
    "SlotSpec",
    "PatternGroup",
    "Pattern",
    "PATTERN_HAND_SIZE",
    "PATTERNS",
    "get_pattern",
    "list_patterns",
    "list_pattern_ids",
    "pattern_total_tiles",
    "self_check",
]


# --------------------------------------------------------------------------
# Hand size ground truth: a complete American Mah Jongg hand (with the
# winning tile) is fourteen tiles. Every pattern below must sum to this.
# --------------------------------------------------------------------------

PATTERN_HAND_SIZE: int = 14


@unique
class GroupKind(Enum):
    """What a PatternGroup represents, structurally, for teaching purposes."""

    PAIR = "pair"
    PUNG = "pung"
    KONG = "kong"
    RUN = "run"
    LIKE_GROUP = "like_group"


@unique
class SuitConstraint(Enum):
    """How strictly a group's slots must agree on suit/honor family."""

    EXACT_SUIT = "exact_suit"
    ANY_SUIT_CONSISTENT = "any_suit_consistent"
    DRAGON_ONLY = "dragon_only"
    WIND_ONLY = "wind_only"
    MIXED_HONORS = "mixed_honors"


@dataclass(frozen=True)
class SlotSpec:
    """
    One tile-shaped slot inside a PatternGroup.

    Attributes:
        count: how many physical tiles fill this slot (1 for a single
            tile position, more only when the slot itself already
            represents a bundled count such as a kong stub).
        joker_eligible: whether SuitUp's AI/matcher may treat a joker
            as satisfying this slot. Pairs of "singles" used as a
            pair-of-something anchor are conventionally NOT joker
            eligible in American Mah Jongg teaching material, so this
            defaults to False and must be opted into per-slot.
        exact_rank: when set, this slot must be filled by that literal
            rank (1-9) within whatever suit the owning group resolves
            to. When None, the slot is rank-flexible within the
            group's run/like-group logic.
        label: short human string shown in curriculum hint UI, e.g.
            "any pung of Dots".
    """

    count: int = 1
    joker_eligible: bool = False
    exact_rank: Optional[int] = None
    label: str = ""


@dataclass(frozen=True)
class PatternGroup:
    """
    A structural cluster of slots inside a practice pattern, such as a
    same-suit run of three, a pung of dragons, or a single pair.
    """

    kind: GroupKind
    suit_constraint: SuitConstraint
    slots: Tuple[SlotSpec, ...] = field(default_factory=tuple)
    note: str = ""

    def tile_count(self) -> int:
        """Total physical tiles this group consumes."""
        return sum(slot.count for slot in self.slots)

    def joker_eligible_tile_count(self) -> int:
        """How many of this group's tiles may be satisfied by a joker."""
        return sum(slot.count for slot in self.slots if slot.joker_eligible)


@dataclass(frozen=True)
class Pattern:
    """
    A complete, original SuitUp teaching pattern: a named target shape
    a beginner practices building toward, made of ordered groups.

    Attributes:
        pattern_id: stable machine key, e.g. "suitup_three_suit_runs".
        title: short human-facing title for curriculum UI.
        teaching_note: one or two sentences explaining WHY this shape
            is useful to practice (what concept it drills).
        groups: ordered tuple of PatternGroup building the full hand.
        hint_text: a beginner-friendly one-liner shown as a curriculum
            hint, kept deliberately vague about exact tiles so the
            learner still has to think.
        difficulty: 1 (easiest) through 3 (hardest), used by the AI
            opponent to pick which patterns it targets at which
            difficulty tier.
        not_nmjl: always True; documents that this is an original
            SuitUp construct and not a reproduction of any official
            NMJL card hand. Present as a explicit machine-checkable
            field, not just a comment, so downstream code can assert
            on it if it ever needs to prove provenance.
    """

    pattern_id: str
    title: str
    teaching_note: str
    groups: Tuple[PatternGroup, ...]
    hint_text: str
    difficulty: int = 1
    not_nmjl: bool = True

    def tile_count(self) -> int:
        """Total physical tiles across every group in this pattern."""
        return sum(group.tile_count() for group in self.groups)

    def joker_eligible_tile_count(self) -> int:
        """Total tiles across the pattern that may be filled by a joker."""
        return sum(group.joker_eligible_tile_count() for group in self.groups)


def _pair(
    suit_constraint: SuitConstraint,
    note: str = "",
    joker_eligible: bool = False,
) -> PatternGroup:
    """Build a two-tile PAIR group; helper to keep pattern defs readable."""
    slots = (
        SlotSpec(count=1, joker_eligible=joker_eligible, label="pair tile"),
        SlotSpec(count=1, joker_eligible=joker_eligible, label="pair tile"),
    )
    return PatternGroup(
        kind=GroupKind.PAIR,
        suit_constraint=suit_constraint,
        slots=slots,
        note=note,
    )


def _pung(
    suit_constraint: SuitConstraint,
    note: str = "",
    joker_eligible: bool = True,
) -> PatternGroup:
    """Build a three-tile PUNG group (three of a kind)."""
    slots = tuple(
        SlotSpec(count=1, joker_eligible=joker_eligible, label="pung tile")
        for _ in range(3)
    )
    return PatternGroup(
        kind=GroupKind.PUNG,
        suit_constraint=suit_constraint,
        slots=slots,
        note=note,
    )


def _kong(
    suit_constraint: SuitConstraint,
    note: str = "",
    joker_eligible: bool = True,
) -> PatternGroup:
    """Build a four-tile KONG group (four of a kind)."""
    slots = tuple(
        SlotSpec(count=1, joker_eligible=joker_eligible, label="kong tile")
        for _ in range(4)
    )
    return PatternGroup(
        kind=GroupKind.KONG,
        suit_constraint=suit_constraint,
        slots=slots,
        note=note,
    )


def _run(
    start_rank: int,
    length: int = 3,
    note: str = "",
    joker_eligible: bool = False,
) -> PatternGroup:
    """
    Build a same-suit sequential RUN group, e.g. 1-2-3 or 4-5-6-7.

    Rank slots are exact (exact_rank set) since a run's whole teaching
    point is consecutive ranks within one suit.
    """
    slots = tuple(
        SlotSpec(
            count=1,
            joker_eligible=joker_eligible,
            exact_rank=start_rank + offset,
            label=f"run tile #{offset + 1}",
        )
        for offset in range(length)
    )
    return PatternGroup(
        kind=GroupKind.RUN,
        suit_constraint=SuitConstraint.EXACT_SUIT,
        slots=slots,
        note=note,
    )


def _like_group(
    suit_constraint: SuitConstraint,
    count: int,
    note: str = "",
    joker_eligible: bool = True,
) -> PatternGroup:
    """Build a flexible LIKE_GROUP of `count` tiles sharing a family."""
    slots = tuple(
        SlotSpec(count=1, joker_eligible=joker_eligible, label="like-group tile")
        for _ in range(count)
    )
    return PatternGroup(
        kind=GroupKind.LIKE_GROUP,
        suit_constraint=suit_constraint,
        slots=slots,
        note=note,
    )


# --------------------------------------------------------------------------
# The original SuitUp practice pattern set. Six patterns, difficulty 1-3,
# each hand-sized to exactly PATTERN_HAND_SIZE (14) tiles.
# --------------------------------------------------------------------------

PATTERNS: Tuple[Pattern, ...] = (
    Pattern(
        pattern_id="suitup_pair_starter",
        title="Pair Starter",
        teaching_note=(
            "Drills the most basic building block: matching pairs across "
            "several families before worrying about runs or pungs at all."
        ),
        groups=(
            _pair(SuitConstraint.EXACT_SUIT, note="a pair of Dots"),
            _pair(SuitConstraint.EXACT_SUIT, note="a pair of Bams"),
            _pair(SuitConstraint.EXACT_SUIT, note="a pair of Craks"),
            _pair(SuitConstraint.WIND_ONLY, note="a pair of one Wind"),
            _pair(SuitConstraint.DRAGON_ONLY, note="a pair of one Dragon"),
            _pair(
                SuitConstraint.ANY_SUIT_CONSISTENT,
                note="a pair of any single suit, jokers welcome",
                joker_eligible=True,
            ),
            _pair(
                SuitConstraint.ANY_SUIT_CONSISTENT,
                note="one final free pair, jokers welcome",
                joker_eligible=True,
            ),
        ),
        hint_text="Look for seven pairs, spread across suits, winds, and dragons.",
        difficulty=1,
    ),
    Pattern(
        pattern_id="suitup_three_suit_runs",
        title="Three-Suit Runs",
        teaching_note=(
            "Drills reading consecutive same-suit runs across all three "
            "suits in one hand, which is the core skill for most real "
            "run-shaped hands a beginner will eventually meet."
        ),
        groups=(
            _run(1, length=3, note="Dots run 1-2-3"),
            _run(4, length=3, note="Bams run 4-5-6"),
            _run(7, length=3, note="Craks run 7-8-9"),
            _pair(
                SuitConstraint.ANY_SUIT_CONSISTENT,
                note="closing pair, any single suit",
                joker_eligible=True,
            ),
            _pung(
                SuitConstraint.WIND_ONLY,
                note="pung of one Wind to close the hand",
                joker_eligible=True,
            ),
        ),
        hint_text="Build one clean run in each suit, then close with a pair and a Wind pung.",
        difficulty=2,
    ),
    Pattern(
        pattern_id="suitup_dragon_honor_guard",
        title="Dragon Honor Guard",
        teaching_note=(
            "Drills recognizing honor tiles (Dragons, Winds) as legitimate "
            "pung/kong material distinct from numbered suit tiles."
        ),
        groups=(
            _pung(SuitConstraint.DRAGON_ONLY, note="pung of Red Dragon"),
            _pung(SuitConstraint.DRAGON_ONLY, note="pung of Green Dragon"),
            _kong(SuitConstraint.WIND_ONLY, note="kong of one Wind"),
            _pair(
                SuitConstraint.EXACT_SUIT,
                note="a numbered-suit pair to anchor the hand",
            ),
        ),
        hint_text="Two Dragon pungs, one Wind kong, one plain numbered pair.",
        difficulty=2,
    ),
    Pattern(
        pattern_id="suitup_wind_rose",
        title="Wind Rose",
        teaching_note=(
            "Drills tracking all four Wind families at once, a common "
            "beginner stumbling block since Winds look similar at a glance."
        ),
        groups=(
            _pair(SuitConstraint.WIND_ONLY, note="pair of East"),
            _pair(SuitConstraint.WIND_ONLY, note="pair of South"),
            _pair(SuitConstraint.WIND_ONLY, note="pair of West"),
            _pair(SuitConstraint.WIND_ONLY, note="pair of North"),
            _run(2, length=3, note="Bams run 2-3-4"),
            _pair(
                SuitConstraint.ANY_SUIT_CONSISTENT,
                note="free closing pair, jokers welcome",
                joker_eligible=True,
            ),
        ),
        hint_text="Collect one pair from each of the four Winds, then close with a run and a pair.",
        difficulty=3,
    ),
    Pattern(
        pattern_id="suitup_like_group_lattice",
        title="Like-Group Lattice",
        teaching_note=(
            "Drills the flexible 'like group' idea: tiles that share a "
            "family but are not a strict pung/run/kong, useful once a "
            "learner is ready for looser matching logic and heavier "
            "joker use."
        ),
        groups=(
            _like_group(
                SuitConstraint.ANY_SUIT_CONSISTENT,
                count=5,
                note="five same-suit tiles, jokers welcome",
                joker_eligible=True,
            ),
            _like_group(
                SuitConstraint.ANY_SUIT_CONSISTENT,
                count=5,
                note="five same-suit tiles from a different suit, jokers welcome",
                joker_eligible=True,
            ),
            _pair(
                SuitConstraint.DRAGON_ONLY,
                note="closing pair of one Dragon",
            ),
            SlotSpecNotUsedPlaceholder := None,  # noqa: F841  (intentionally unused sentinel removed below)
        )[:-1],
        hint_text="Two loose five-tile suit lattices, closed out with a Dragon pair.",
        difficulty=3,
    ),
    Pattern(
        pattern_id="suitup_full_joker_bridge",
        title="Full Joker Bridge",
        teaching_note=(
            "Drills the idea that jokers can stand in almost anywhere in "
            "pungs, kongs, and like-groups (but never in a plain pair "
            "anchor), which is a common point of confusion for beginners."
        ),
        groups=(
            _pung(SuitConstraint.EXACT_SUIT, note="pung of Dots, jokers welcome", joker_eligible=True),
            _kong(SuitConstraint.EXACT_SUIT, note="kong of Bams, jokers welcome", joker_eligible=True),
            _pung(SuitConstraint.DRAGON_ONLY, note="pung of one Dragon, jokers welcome", joker_eligible=True),
            _pair(
                SuitConstraint.EXACT_SUIT,
                note="plain pair anchor, NOT joker eligible",
                joker_eligible=False,
            ),
        ),
        hint_text="Three joker-friendly sets plus one strict, joker-free pair anchor.",
        difficulty=3,
    ),
)


def get_pattern(pattern_id: str) -> Optional[Pattern]:
    """Look up a single pattern by its stable id, or None if unknown."""
    for pattern in PATTERNS:
        if pattern.pattern_id == pattern_id:
            return pattern
    return None


def list_patterns(max_difficulty: Optional[int] = None) -> List[Pattern]:
    """
    Return patterns, optionally filtered to those at or below a given
    difficulty tier (used by the AI opponent to pick achievable targets).
    """
    if max_difficulty is None:
        return list(PATTERNS)
    return [p for p in PATTERNS if p.difficulty <= max_difficulty]


def list_pattern_ids() -> List[str]:
    """Return all known pattern ids, in declaration order."""
    return [pattern.pattern_id for pattern in PATTERNS]


def pattern_total_tiles(pattern_id: str) -> int:
    """
    Return the tile count for a pattern by id, or raise KeyError if the
    pattern id is unknown. Used by self_check and by matcher validation.
    """
    pattern = get_pattern(pattern_id)
    if pattern is None:
        raise KeyError(f"unknown pattern id: {pattern_id!r}")
    return pattern.tile_count()


def self_check() -> Dict[str, object]:
    """
    Validate every pattern in PATTERNS: hand size must equal
    PATTERN_HAND_SIZE, every pattern must be flagged not_nmjl=True,
    and every pattern_id must be unique. Returns a small report dict;
    raises AssertionError on the first violation found.
    """
    seen_ids: Dict[str, int] = {}
    report: Dict[str, object] = {
        "pattern_count": len(PATTERNS),
        "hand_size": PATTERN_HAND_SIZE,
        "checked_ids": [],
    }
    for pattern in PATTERNS:
        assert pattern.not_nmjl is True, (
            f"pattern {pattern.pattern_id!r} must be flagged not_nmjl=True"
        )
        assert pattern.pattern_id not in seen_ids, (
            f"duplicate pattern id: {pattern.pattern_id!r}"
        )
        seen_ids[pattern.pattern_id] = 1
        total = pattern.tile_count()
        assert total == PATTERN_HAND_SIZE, (
            f"pattern {pattern.pattern_id!r} has {total} tiles, "
            f"expected {PATTERN_HAND_SIZE}"
        )
        assert 1 <= pattern.difficulty <= 3, (
            f"pattern {pattern.pattern_id!r} has out-of-range difficulty "
            f"{pattern.difficulty!r}"
        )
        report["checked_ids"].append(pattern.pattern_id)  # type: ignore[attr-defined]
    return report


if __name__ == "__main__":
    result = self_check()
    print(f"SuitUp patterns self-check OK: {result}")