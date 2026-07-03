"""Tile domain model and 152-tile factory for American Mah Jongg (SuitUp)."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, unique
from typing import Dict, List, Optional


@unique
class Suit(Enum):
    DOTS = "dots"
    BAMS = "bams"
    CRAKS = "craks"


@unique
class Wind(Enum):
    EAST = "east"
    SOUTH = "south"
    WEST = "west"
    NORTH = "north"


@unique
class Dragon(Enum):
    RED = "red"
    GREEN = "green"
    SOAP = "soap"


@unique
class Flower(Enum):
    FLOWER = "flower"
    SEASON = "season"


@unique
class TileKind(Enum):
    SUIT = "suit"
    WIND = "wind"
    DRAGON = "dragon"
    JOKER = "joker"
    FLOWER = "flower"


SUIT_DISPLAY_NAMES: Dict[Suit, str] = {
    Suit.DOTS: "Dot",
    Suit.BAMS: "Bam",
    Suit.CRAKS: "Crak",
}

SUIT_CODES: Dict[Suit, str] = {
    Suit.DOTS: "D",
    Suit.BAMS: "B",
    Suit.CRAKS: "C",
}

WIND_DISPLAY_NAMES: Dict[Wind, str] = {
    Wind.EAST: "East Wind",
    Wind.SOUTH: "South Wind",
    Wind.WEST: "West Wind",
    Wind.NORTH: "North Wind",
}

WIND_CODES: Dict[Wind, str] = {
    Wind.EAST: "E",
    Wind.SOUTH: "S",
    Wind.WEST: "W",
    Wind.NORTH: "N",
}

DRAGON_DISPLAY_NAMES: Dict[Dragon, str] = {
    Dragon.RED: "Red Dragon",
    Dragon.GREEN: "Green Dragon",
    Dragon.SOAP: "Soap Dragon",
}

DRAGON_CODES: Dict[Dragon, str] = {
    Dragon.RED: "RD",
    Dragon.GREEN: "GD",
    Dragon.SOAP: "SD",
}

# In American Mah Jongg, each Dragon is conventionally matched to a suit:
# Red -> Craks, Green -> Bams, Soap (White) -> D