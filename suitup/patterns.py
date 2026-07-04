"""Original teaching-only practice hand patterns for SuitUp.

This module is intentionally NOT a reproduction of any National Mah
Jongg League (NMJL) card. The NMJL publishes a new card every year and
its exact hand text, point values, and specific number/suit
combinations are that organization's copyrighted material. SuitUp does
not ship, embed, or approximate that card.

Instead, this module defines a small set of ORIGINAL, generic
"practice patterns" used only to teach the *mechanics* of building a
Mah Jongg hand: how many groups a hand needs, how pairs/pungs/kongs/
quints/runs work, how jokers can substitute into certain group slots,
and how suit relationships between groups (same suit vs. any suit vs.
honors) shape a hand. These practice patterns are deliberately simple,
clearly labeled as SuitUp originals, and are structured as data so both
the rules-matching code and the AI planner can consume them
generically.

A hand in American Mah Jongg is built from 14 tiles arranged into a
fixed number of "groups" (with exactly one pair among them, in the
common case). Real play always requires the player's own current NMJL
card. SuitUp's practice patterns exist only to teach that group/pair
structure and joker mechanics in a low-stakes, guided way.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Tuple

from suitup.tiles import Suit


DISCLAIMER: str = (
    "These are SuitUp original practice patterns for teaching hand "
    "structure and joker mechanics only. They are not National Mah "
    "Jongg League (NMJL) card content. Real scored play requires your "
    "own current NMJL card."
)


class GroupType(str, Enum):
    """The kinds of tile groups a practice pattern slot can require."""

    PAIR = "pair"
    PUNG = "pung"
    KONG = "kong"
    QUINT = "quint"
    RUN = "run"


class SuitRelation(str, Enum):
    """How a group slot's suit relates to the other slots in a pattern."""

    ANY_SUIT = "any_suit"
    SAME_AS_PATTERN = "same_as_pattern"
    DISTINCT_PER_SLOT = "distinct_per_slot"
    HONOR_ONLY = "honor_only"


class Difficulty(str, Enum):
    """Beginner-facing difficulty label for a practice pattern."""

    INTRO = "intro"
    BUILDING = "building"
    STRETCH = "stretch"


@dataclass(frozen=True)
class GroupSlot:
    """One structural slot within a practice pattern.

    A pattern is a list of GroupSlot entries. Each slot says what kind
    of group goes there (pair, pung, kong, quint, run), how big it is,
    whether jokers may substitute into it, and how its suit relates to
    the rest of the pattern.
    """

    group_type: GroupType
    size: int
    joker_eligible: bool
    suit_relation: SuitRelation
    honor_only: bool = False
    label: str = ""

    def describe(self) -> str:
        """Return a short human-readable description of this slot."""
        joker_note = "jokers ok" if self.joker_eligible else "no jokers"
        honor_note = "honors only" if self.honor_only else "numbered or honor"
        base = self.label if self.label else self.group_type.value
        return "{0} ({1} tiles, {2}, {3})".format(
            base, self.size, joker_note, honor_note
        )


@dataclass(frozen=True)
class PracticePattern:
    """An original SuitUp practice pattern for teaching hand structure."""

    pattern_id: str
    display_name: str
    difficulty: Difficulty
    explanation: str
    group_slots: Tuple[GroupSlot, ...]
    requires_pair: bool = True
    disclaimer: str = DISCLAIMER

    def total_tiles(self) -> int:
        """Return the total tile count required to complete this pattern."""
        return sum(slot.size for slot in self.group_slots)

    def slot_count(self) -> int:
        """Return how many group slots this pattern defines."""
        return len(self.group_slots)

    def joker_eligible_slots(self) -> List[GroupSlot]:
        """Return only the slots where jokers may be used."""
        eligible = []
        for slot in self.group_slots:
            if slot.joker_eligible:
                eligible.append(slot)
        return eligible

    def summary(self) -> str:
        """Return a compact multi-line teaching summary of this pattern."""
        lines = [
            "{0} ({1})".format(self.display_name, self.difficulty.value),
            self.explanation,
        ]
        for index, slot in enumerate(self.group_slots, start=1):
            lines.append("  slot {0}: {1}".format(index, slot.describe()))
        lines.append(self.disclaimer)
        return "\n".join(lines)


def _pair_slot(label: str, joker_eligible: bool = True) -> GroupSlot:
    """Build a standard pair slot used across several practice patterns."""
    return GroupSlot(
        group_type=GroupType.PAIR,
        size=2,
        joker_eligible=joker_eligible,
        suit_relation=SuitRelation.SAME_AS_PATTERN,
        honor_only=False,
        label=label,
    )


def _pung_slot(label: str, suit_relation: SuitRelation) -> GroupSlot:
    """Build a standard three-of-a-kind (pung) slot."""
    return GroupSlot(
        group_type=GroupType.PUNG,
        size=3,
        joker_eligible=True,
        suit_relation=suit_relation,
        honor_only=False,
        label=label,
    )


def _kong_slot(label: str, suit_relation: SuitRelation) -> GroupSlot:
    """Build a standard four-of-a-kind (kong) slot."""
    return GroupSlot(
        group_type=GroupType.KONG,
        size=4,
        joker_eligible=True,
        suit_relation=suit_relation,
        honor_only=False,
        label=label,
    )


def _run_slot(label: str, suit_relation: SuitRelation) -> GroupSlot:
    """Build a standard three-tile consecutive-run slot."""
    return GroupSlot(
        group_type=GroupType.RUN,
        size=3,
        joker_eligible=False,
        suit_relation=suit_relation,
        honor_only=False,
        label=label,
    )


def _honor_pung_slot(label: str) -> GroupSlot:
    """Build a pung slot restricted to honor tiles (winds/dragons)."""
    return GroupSlot(
        group_type=GroupType.PUNG,
        size=3,
        joker_eligible=True,
        suit_relation=SuitRelation.HONOR_ONLY,
        honor_only=True,
        label=label,
    )


PRACTICE_TRIPLE_STEP: PracticePattern = PracticePattern(
    pattern_id="practice_triple_step",
    display_name="Triple Step (SuitUp original)",
    difficulty=Difficulty.INTRO,
    explanation=(
        "A gentle first pattern: one pair plus three pungs, all in the "
        "same suit. Teaches counting to fourteen tiles and how jokers "
        "can fill in for any tile in a pung."
    ),
    group_slots=(
        _pair_slot("center pair"),
        _pung_slot("pung one", SuitRelation.SAME_AS_PATTERN),
        _pung_slot("pung two", SuitRelation.SAME_AS_PATTERN),
        _pung_slot("pung three", SuitRelation.SAME_AS_PATTERN),
    ),
    requires_pair=True,
)


PRACTICE_RUN_LADDER: PracticePattern = PracticePattern(
    pattern_id="practice_run_ladder",
    display_name="Run Ladder (SuitUp original)",
    difficulty=Difficulty.BUILDING,
    explanation=(
        "Two consecutive-number runs of three plus one pung plus a "
        "pair, all in one suit. Teaches that runs cannot use jokers "
        "while pairs and pungs can, so players must plan which tiles "
        "to keep in hand versus which to expose."
    ),
    group_slots=(
        _pair_slot("anchor pair"),
        _run_slot("run one", SuitRelation.SAME_AS_PATTERN),
        _run_slot("run two", SuitRelation.SAME_AS_PATTERN),
        _pung_slot("closing pung", SuitRelation.SAME_AS_PATTERN),
    ),
    requires_pair=True,
)


PRACTICE_HONOR_GUARD: PracticePattern = PracticePattern(
    pattern_id="practice_honor_guard",
    display_name="Honor Guard (SuitUp original)",
    difficulty=Difficulty.BUILDING,
    explanation=(
        "One honor pung (winds or dragons), two numbered pungs in "
        "different suits, and a pair. Teaches the distinction between "
        "honor tiles and numbered suits, and how a pattern can mix "
        "both categories across its slots."
    ),
    group_slots=(
        _pair_slot("keeper pair"),
        _honor_pung_slot("honor pung"),
        _pung_slot("numbered pung one", SuitRelation.DISTINCT_PER_SLOT),
        _pung_slot("numbered pung two", SuitRelation.DISTINCT_PER_SLOT),
    ),
    requires_pair=True,
)


PRACTICE_QUAD_STACK: PracticePattern = PracticePattern(
    pattern_id="practice_quad_stack",
    display_name="Quad Stack (SuitUp original)",
    difficulty=Difficulty.STRETCH,
    explanation=(
        "A pair plus two pungs plus one kong, mixing suits freely. "
        "Teaches that a kong uses four tiles instead of three, so the "
        "beginner must recount their fourteen-tile target and see how "
        "an exposed kong changes hand shape and draw order."
    ),
    group_slots=(
        _pair_slot("floating pair"),
        _pung_slot("pung a", SuitRelation.ANY_SUIT),
        _pung_slot("pung b", SuitRelation.ANY_SUIT),
        _kong_slot("kong c", SuitRelation.ANY_SUIT),
    ),
    requires_pair=True,
)


PRACTICE_JOKERLESS_DRILL: PracticePattern = PracticePattern(
    pattern_id="practice_jokerless_drill",
    display_name="Jokerless Drill (SuitUp original)",
    difficulty=Difficulty.STRETCH,
    explanation=(
        "Three consecutive runs in the same suit plus a pair, with no "
        "joker substitution allowed anywhere. This is the hardest "
        "practice pattern and teaches disciplined tile reading without "
        "relying on jokers as a safety net."
    ),
    group_slots=(
        GroupSlot(
            group_type=GroupType.PAIR,
            size=2,
            joker_eligible=False,
            suit_relation=SuitRelation.SAME_AS_PATTERN,
            honor_only=False,
            label="strict pair",
        ),
        _run_slot("run one", SuitRelation.SAME_AS_PATTERN),
        _run_slot("run two", SuitRelation.SAME_AS_PATTERN),
        _run_slot("run three", SuitRelation.SAME_AS_PATTERN),
    ),
    requires_pair=True,
)


ALL_PRACTICE_PATTERNS: Tuple[PracticePattern, ...] = (
    PRACTICE_TRIPLE_STEP,
    PRACTICE_RUN_LADDER,
    PRACTICE_HONOR_GUARD,
    PRACTICE_QUAD_STACK,
    PRACTICE_JOKERLESS_DRILL,
)


def list_patterns() -> List[PracticePattern]:
    """Return all practice patterns in beginner-friendly order."""
    ordered = sorted(
        ALL_PRACTICE_PATTERNS,
        key=lambda pattern: (pattern.difficulty.value, pattern.pattern_id),
    )
    return list(ordered)


def get_pattern_by_id(pattern_id: str) -> Optional[PracticePattern]:
    """Look up a single practice pattern by its stable identifier."""
    for pattern in ALL_PRACTICE_PATTERNS:
        if pattern.pattern_id == pattern_id:
            return pattern
    return None


def patterns_for_difficulty(difficulty: Difficulty) -> List[PracticePattern]:
    """Return all practice patterns matching a given difficulty level."""
    matches = []
    for pattern in ALL_PRACTICE_PATTERNS:
        if pattern.difficulty == difficulty:
            matches.append(pattern)
    return matches


def validate_pattern_shapes() -> List[str]:
    """Sanity-check every pattern's tile math; return a list of problems.

    This does not raise on failure. It is meant to be called from
    tests or a startup check so a broken pattern definition surfaces
    as a readable message instead of a silent miscount during play.
    """
    problems: List[str] = []
    for pattern in ALL_PRACTICE_PATTERNS:
        total = pattern.total_tiles()
        if total != 14:
            problems.append(
                "{0} totals {1} tiles, expected 14".format(
                    pattern.pattern_id, total
                )
            )
        pair_slots = [
            slot for slot in pattern.group_slots
            if slot.group_type == GroupType.PAIR
        ]
        if pattern.requires_pair and len(pair_slots) != 1:
            problems.append(
                "{0} must have exactly one pair slot, found {1}".format(
                    pattern.pattern_id, len(pair_slots)
                )
            )
    return problems


__all__ = [
    "DISCLAIMER",
    "GroupType",
    "SuitRelation",
    "Difficulty",
    "GroupSlot",
    "PracticePattern",
    "PRACTICE_TRIPLE_STEP",
    "PRACTICE_RUN_LADDER",
    "PRACTICE_HONOR_GUARD",
    "PRACTICE_QUAD_STACK",
    "PRACTICE_JOKERLESS_DRILL",
    "ALL_PRACTICE_PATTERNS",
    "list_patterns",
    "get_pattern_by_id",
    "patterns_for_difficulty",
    "validate_pattern_shapes",
    "Suit",
]