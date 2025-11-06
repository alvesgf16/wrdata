"""
Analyzed Champion domain model module.

This module defines the AnalyzedChampion class, which represents a champion
with calculated domain metrics such as adjusted win rate and tier
classification. It wraps the base Champion data model with analysis results.
"""

from dataclasses import dataclass
from enum import Enum

from ...data.models.champion import Champion, Lane


class Tier(Enum):
    """Tier enumeration for champion classification."""

    S_PLUS = "S+"
    S = "S"
    A = "A"
    B = "B"
    C = "C"
    D = "D"


@dataclass
class AnalyzedChampion:
    """A champion with calculated domain metrics.

    This class encapsulates a Champion along with calculated analysis
    metrics. It separates raw scraped data (in Champion) from processed
    domain data (adjusted win rate and tier).

    Attributes:
        champion (Champion): The base champion data from scraping.
        adjusted_win_rate (float): The calculated adjusted win rate (0-1).
        tier (Tier | None): The calculated tier classification.
    """

    champion: Champion
    adjusted_win_rate: float
    tier: Tier | None = None

    @property
    def lane(self) -> Lane:
        """Get the lane from the underlying champion."""
        return self.champion.lane

    @property
    def name(self) -> str:
        """Get the name from the underlying champion."""
        return self.champion.name

    @property
    def win_rate(self) -> float:
        """Get the win rate from the underlying champion."""
        return self.champion.win_rate

    @property
    def pick_rate(self) -> float:
        """Get the pick rate from the underlying champion."""
        return self.champion.pick_rate

    @property
    def ban_rate(self) -> float:
        """Get the ban rate from the underlying champion."""
        return self.champion.ban_rate
