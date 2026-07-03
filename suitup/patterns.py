"""Practice pattern catalog for SuitUp's teaching-only Mah Jongg hands.

IMPORTANT DISCLAIMER (read this before anything else):
    The patterns defined in this module are ORIGINAL, SuitUp-authored practice
    hands created purely for instructional purposes. They are NOT National Mah
    Jongg League (NMJL) hands, they do NOT reproduce any NMJL card content,
    names, numbering, or scoring, and they carry NO official standing. Their
    only purpose is to give a beginner (and the built-in AI opponents)
    concrete, checkable targets while practicing groupings, pairs, runs,
    pungs, kongs, and joker rules in a low-stakes way.

Schema overview:
    A ``PracticePattern`` is a named, described collection of ``PatternGroup``
    objects. Each group describes a structural requirement (pair / run / pung
    / kong), what category of tile it applies to (suit / wind / dragon /
    any-honor), how many tiles it needs, whether jokers may substitute into
    it, and optional suit-linkage rules so the matcher can enforce "same
    suit across these groups" or "three different suits" style constraints
    without hardcoding tile identities.

    The total tile count across a pattern's groups is always 14, matching
    the size of a complete American Mah Jongg hand (13 tiles in hand plus
    the winning/drawn tile).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, unique
from typing import Dict, List, Optional


@unique
class GroupKind(Enum):
    """Structural shape a PatternGroup must satisfy."""

    PAIR = "pair"
    PUNG = "pung"
    KONG = "kong"
    RUN = "run"


@unique
class TileCategory(Enum):
    """What family of tile a PatternGroup draws from."""

    SUIT = "suit"
    WIND = "wind"
    DRAGON = "dragon"
    ANY_HONOR = "any_honor"


# Canonical tile-count for each structural shape. A RUN's length is stored
# on the group itself (usually 3) since practice patterns may use short or
# long runs; PAIR/PUNG/KONG lengths are fixed by definition.
FIXED_GROUP_LENGTHS: Dict[GroupKind, int] = {
    GroupKind.PAIR: 2,
    GroupKind.PUNG: 3,
    GroupKind.KONG: 4,
}


@dataclass(frozen=True)
class PatternGroup:
    """One structural requirement inside a PracticePattern.

    Attributes:
        kind: The structural shape (pair, pung, kong, run).
        category: The tile family this group draws from.
        length: Tile count for this group. For PAIR/PUNG/KONG this must
            match FIXED_GROUP_LENGTHS; for RUN it is caller-specified
            (practice patterns in this file use 3-tile runs).
        suit_link: Optional label. Any two groups sharing the same
            non-None suit_link must be filled with the SAME suit when the
            matcher assigns concrete tiles. Use distinct labels (or None)
            when groups should be free to pick independently.
        distinct_from: Optional label. Any two groups sharing the same
            non-None distinct_from tag must use DIFFERENT suits from one
            another when the matcher assigns concrete tiles.
        allowed_honors: For WIND/DRAGON/ANY_HONOR categories, an optional
            restriction to specific honor values (e.g. ["east", "south"]
            or ["red", "green", "soap"]). None means "any value in that
            category is acceptable."
        consecutive: For RUN groups, whether the numeric tiles must be
            sequential (e.g. 2-3-4). Practice runs in this catalog are
            always consecutive.
        joker_allowed: Whether a joker may substitute for a tile in this
            group. Per American Mah Jongg convention inherited here,
            jokers may NOT substitute into a pair unless explicitly
            marked otherwise, and single/pair positions are the most
            joker-restrictive by default.
    """

    kind: GroupKind
    category: TileCategory
    length: int
    suit_link: Optional[str] = None
    distinct_from: Optional[str] = None
    allowed_honors: Optional[List[str]] = None
    consecutive: bool = False
    joker_allowed: bool = True

    def __post_init__(self) -> None:
        if self.kind in FIXED_GROUP_LENGTHS:
            expected = FIXED_GROUP_LENGTHS[self.kind]
            if self.length != expected:
                raise ValueError(
                    "PatternGroup of kind {0} must have length {1}, got {2}".format(
                        self.kind.value, expected, self.length
                    )
                )
        if self.kind == GroupKind.RUN and self.length < 3:
            raise ValueError("RUN groups must have length >= 3")
        if self.category == TileCategory.SUIT and self.allowed_honors is not None:
            raise ValueError("SUIT category groups cannot carry allowed_honors")


@dataclass(frozen=True)
class PracticePattern:
    """A complete, original, teaching-only practice hand definition.

    NOT an NMJL hand. See the module docstring disclaimer above.
    """

    pattern_id: str
    name: str
    description: str
    groups: List[PatternGroup]
    difficulty: int = 1
    concealed_only: bool = False
    tags: List[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        total = sum(group.length for group in self.groups)
        if total != 14:
            raise ValueError(
                "Pattern '{0}' must total 14 tiles, got {1}".format(self.pattern_id, total)
            )
        if not 1 <= self.difficulty <= 3:
            raise ValueError(
                "Pattern '{0}' difficulty must be 1, 2, or 3".format(self.pattern_id)
            )

    @property
    def total_tiles(self) -> int:
        return sum(group.length for group in self.groups)

    @property
    def has_pair(self) -> bool:
        return any(group.kind == GroupKind.PAIR for group in self.groups)


def _pair(
    category: TileCategory,
    suit_link: Optional[str] = None,
    distinct_from: Optional[str] = None,
    allowed_honors: Optional[List[str]] = None,
    joker_allowed: bool = False,
) -> PatternGroup:
    return PatternGroup(
        kind=GroupKind.PAIR,
        category=category,
        length=2,
        suit_link=suit_link,
        distinct_from=distinct_from,
        allowed_honors=allowed_honors,
        joker_allowed=joker_allowed,
    )


def _pung(
    category: TileCategory,
    suit_link: Optional[str] = None,
    distinct_from: Optional[str] = None,
    allowed_honors: Optional[List[str]] = None,
    joker_allowed: bool = True,
) -> PatternGroup:
    return PatternGroup(
        kind=GroupKind.PUNG,
        category=category,
        length=3,
        suit_link=suit_link,
        distinct_from=distinct_from,
        allowed_honors=allowed_honors,
        joker_allowed=joker_allowed,
    )


def _kong(
    category: TileCategory,
    suit_link: Optional[str] = None,
    distinct_from: Optional[str] = None,
    allowed_honors: Optional[List[str]] = None,
    joker_allowed: bool = True,
) -> PatternGroup:
    return PatternGroup(
        kind=GroupKind.KONG,
        category=category,
        length=4,
        suit_link=suit_link,
        distinct_from=distinct_from,
        allowed_honors=allowed_honors,
        joker_allowed=joker_allowed,
    )


def _run(
    length: int = 3,
    suit_link: Optional[str] = None,
    distinct_from: Optional[str] = None,
    joker_allowed: bool = True,
) -> PatternGroup:
    return PatternGroup(
        kind=GroupKind.RUN,
        category=TileCategory.SUIT,
        length=length,
        suit_link=suit_link,
        distinct_from=distinct_from,
        consecutive=True,
        joker_allowed=joker_allowed,
    )


# ---------------------------------------------------------------------------
# THE CATALOG
#
# All patterns below are original SuitUp teaching hands. None reproduce
# NMJL card content, names, or numbering. They exist solely so a beginner
# (or an AI opponent) has a concrete, checkable shape to aim for while
# practicing pairs, pungs, kongs, runs, suit consistency, and joker rules.
# ---------------------------------------------------------------------------

PATTERNS: List[PracticePattern] = [
    PracticePattern(
        pattern_id="practice-01-triple-run",
        name="Triple Run Starter",
        description=(
            "Three consecutive same-suit runs of three, a pung of any one "
            "wind, and a dragon pair. Teaches suit consistency across runs "
            "and basic pung formation."
        ),
        difficulty=1,
        tags=["beginner", "runs", "suit-consistency"],
        groups=[
            _pair(TileCategory.DRAGON, joker_allowed=False),
            _run(3, suit_link="A"),
            _run(3, suit_link="A"),
            _run(3, suit_link="A"),
            _pung(TileCategory.WIND),
        ],
    ),
    PracticePattern(
        pattern_id="practice-02-like-pungs",
        name="Three-Suit Pung Ladder",
        description=(
            "A same-suit numeric pair plus three pungs, one in each suit, "
            "plus a dragon pung. Teaches the 'one pung per suit' shape and "
            "distinct-suit enforcement."
        ),
        difficulty=1,
        tags=["beginner", "pungs", "distinct-suits"],
        groups=[
            _pair(TileCategory.SUIT, suit_link="A", joker_allowed=False),
            _pung(TileCategory.SUIT, suit_link="A"),
            _pung(TileCategory.SUIT, distinct_from="suit-set"),
            _pung(TileCategory.SUIT, distinct_from="suit-set"),
            _pung(TileCategory.DRAGON),
        ],
    ),
    PracticePattern(
        pattern_id="practice-03-four-winds",
        name="Four Winds Muster",
        description=(
            "A dragon pair plus one pung of each of the four winds. "
            "Teaches honor-tile pungs and the 'no numeric tiles at all' "
            "all-honors shape."
        ),
        difficulty=2,
        tags=["intermediate", "honors", "winds"],
        groups=[
            _pair(TileCategory.DRAGON, joker_allowed=False),
            _pung(TileCategory.WIND, allowed_honors=["east"]),
            _pung(TileCategory.WIND, allowed_honors=["south"]),
            _pung(TileCategory.WIND, allowed_honors=["west"]),
            _pung(TileCategory.WIND, allowed_honors=["north"]),
        ],
    ),
    PracticePattern(
        pattern_id="practice-04-dragon-trio",
        name="Dragon Trio with Run",
        description=(
            "A numeric pair, all three matched dragon pungs (Red, Green, "
            "Soap), and one same-suit run. Teaches suit-matched dragons and "
            "mixing honors with a numeric run."
        ),
        difficulty=2,
        tags=["intermediate", "dragons", "mixed"],
        groups=[
            _pair(TileCategory.SUIT, suit_link="A", joker_allowed=False),
            _pung(TileCategory.DRAGON, allowed_honors=["red"]),
            _pung(TileCategory.DRAGON, allowed_honors=["green"]),
            _pung(TileCategory.DRAGON, allowed_honors=["soap"]),
            _run(3, suit_link="A"),
        ],
    ),
    PracticePattern(
        pattern_id="practice-05-kong-challenge",
        name="Concealed Kong Challenge",
        description=(
            "A wind pair, a same-suit pung, a concealed kong in a second "
            "suit, and a run in a third suit. Teaches kong mechanics and "
            "three-suit distinctness at once."
        ),
        difficulty=3,
        tags=["advanced", "kongs", "distinct-suits"],
        concealed_only=True,
        groups=[
            _pair(TileCategory.WIND, joker_allowed=False),
            _pung(TileCategory.SUIT, distinct_from="triad"),
            _kong(TileCategory.SUIT, distinct_from="triad", joker_allowed=False),
            _run(3, distinct_from="triad"),
        ],
    ),
    PracticePattern(
        pattern_id="practice-06-no-joker-purist",
        name="Purist's Pair and Pungs",
        description=(
            "An all-pung hand plus pair, with jokers disabled everywhere. "
            "Teaches players to build a hand using only natural tiles, no "
            "substitutions allowed."
        ),
        difficulty=3,
        tags=["advanced", "no-jokers", "pungs"],
        groups=[
            _pair(TileCategory.SUIT, suit_link="A", joker_allowed=False),
            _pung(TileCategory.SUIT, suit_link="A", joker_allowed=False),
            _pung(TileCategory.SUIT, distinct_from="suit-set", joker_allowed=False),
            _pung(TileCategory.SUIT, distinct_from="suit-set", joker_allowed=False),
            _pung(TileCategory.DRAGON, joker_allowed=False),
        ],
    ),
]


_PATTERNS_BY_ID: Dict[str, PracticePattern] = {p.pattern_id: p for p in PATTERNS}


def list_patterns() -> List[PracticePattern]:
    """Return all curated practice patterns."""
    return list(PATTERNS)


def get_pattern(pattern_id: str) -> Optional[PracticePattern]:
    """Look up a single practice pattern by its id, or None if unknown."""
    return _PATTERNS_BY_ID.get(pattern_id)


def patterns_by_difficulty(difficulty: int) -> List[PracticePattern]:
    """Return all patterns matching an exact difficulty level (1, 2, or 3)."""
    return [p for p in PATTERNS if p.difficulty == difficulty]


def patterns_by_tag(tag: str) -> List[PracticePattern]:
    """Return all patterns carrying the given tag."""
    return [p for p in PATTERNS if tag in p.tags]