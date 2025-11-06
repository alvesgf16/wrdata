"""
Champion data model module.

This module defines the Champion class, which represents a champion's
performance data as scraped from the website. It includes only the raw
statistics without any calculated metrics or tier classifications.

Domain logic such as adjusted win rates and tier assignments is handled
by the AnalyzedChampion class in the domain layer.
"""

from dataclasses import dataclass
from enum import Enum


class Lane(Enum):
    """Lane enumeration."""

    TOP = "Top"
    JUNGLE = "Jungle"
    MID = "Mid"
    BOT = "Bot"
    SUP = "Sup"


@dataclass
class Champion:
    """A class representing scraped champion performance data.

    This class encapsulates the raw statistics scraped from the website
    for a champion in a specific lane. It contains only the base data
    without any calculated metrics or tier classifications.

    Domain logic such as adjusted win rates and tier assignments is
    handled by the AnalyzedChampion class in the domain layer.
    Serialization logic is handled by ChampionSerializer in the adapters
    layer.

    Attributes:
        lane (Lane): The lane where the champion is played.
        name (str): The name of the champion.
        win_rate (float): The champion's win rate (0-1).
        pick_rate (float): The champion's pick rate (0-1).
        ban_rate (float): The champion's ban rate (0-1).
    """

    lane: Lane
    name: str
    win_rate: float
    pick_rate: float
    ban_rate: float

    @classmethod
    def from_raw_data(
        cls,
        lane: str,
        name: str,
        win_rate: float,
        pick_rate: float,
        ban_rate: float,
    ) -> "Champion":
        """Create a Champion instance from raw string data.

        This factory method converts string lane data to the appropriate
        Lane enum value, making it easier to create Champion instances
        from scraped or parsed data.

        Args:
            lane (str): The lane name as a string.
            name (str): The champion's name.
            win_rate (float): The champion's win rate (0-1).
            pick_rate (float): The champion's pick rate (0-1).
            ban_rate (float): The champion's ban rate (0-1).

        Returns:
            Champion: A new Champion instance.

        Raises:
            ValueError: If lane string doesn't match any Lane enum.
        """
        lane_enum = Lane(lane)
        return cls(lane_enum, name, win_rate, pick_rate, ban_rate)
