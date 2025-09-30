"""Enumerations for WRData application."""

from enum import Enum


class Lane(Enum):
    """Lane enumeration."""

    TOP = "Top"
    JUNGLE = "Jungle"
    MID = "Mid"
    BOT = "Bot"
    SUPPORT = "Support"


class Tier(Enum):
    """Tier enumeration."""

    S_PLUS = "S+"
    S = "S"
    A = "A"
    B = "B"
    C = "C"
    D = "D"
