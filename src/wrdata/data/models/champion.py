"""
Champion data model module.

This module defines the Champion class, which represents a champion's
performance data in a specific lane. It includes various statistics
such as win rates, pick rates, and ban rates, along with methods for
data formatting and access.
"""

from enum import Enum


class Lane(Enum):
    """Lane enumeration."""

    TOP = "Top"
    JUNGLE = "Jungle"
    MID = "Mid"
    BOT = "Bot"
    SUP = "Sup"


class Tier(Enum):
    """Tier enumeration."""

    S_PLUS = "S+"
    S = "S"
    A = "A"
    B = "B"
    C = "C"
    D = "D"


class Champion:
    """A class representing a champion's performance data.

    This class encapsulates all the relevant statistics and information
    for a champion in a specific lane, including various rates and
    tier classification. It provides properties for data access and
    methods for data formatting.

    Methods:
    ---
    to_csv_row():
        Convert champion data to a CSV row format.
    """

    def __init__(
        self,
        lane: Lane,
        name: str,
        win_rate: float,
        pick_rate: float,
        ban_rate: float,
    ):
        """Initialize a new Champion instance.

        Args:
            lane (Lane): The lane where the champion is played.
            name (str): The name of the champion.
            win_rate (float): The champion's win rate (0-1).
            pick_rate (float): The champion's pick rate (0-1).
            ban_rate (float): The champion's ban rate (0-1).
        """
        self.__lane = lane
        self.__name = name
        self.__win_rate = win_rate
        self.__pick_rate = pick_rate
        self.__ban_rate = ban_rate
        self.__adjusted_win_rate = 0.0
        self.__tier: Tier | None = None

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
            ValueError: If the lane string doesn't match any Lane enum value.
        """
        lane_enum = Lane(lane)
        return cls(lane_enum, name, win_rate, pick_rate, ban_rate)

    @property
    def lane(self) -> Lane:
        """Get the lane where the champion is played.

        Returns:
            Lane: The lane enum value.
        """
        return self.__lane

    @property
    def name(self) -> str:
        """Get the champion's name.

        Returns:
            str: The champion name.
        """
        return self.__name

    @property
    def win_rate(self) -> float:
        """Get the champion's win rate.

        Returns:
            float: The win rate value (0-1).
        """
        return self.__win_rate

    @property
    def pick_rate(self) -> float:
        """Get the champion's pick rate.

        Returns:
            float: The pick rate value (0-1).
        """
        return self.__pick_rate

    @property
    def ban_rate(self) -> float:
        """Get the champion's ban rate.

        Returns:
            float: The ban rate value (0-1).
        """
        return self.__ban_rate

    @property
    def adjusted_win_rate(self) -> float:
        """Get the champion's adjusted win rate.

        Returns:
            float: The adjusted win rate value (0-1).
        """
        return self.__adjusted_win_rate

    @adjusted_win_rate.setter
    def adjusted_win_rate(self, value: float) -> None:
        """Set the champion's adjusted win rate.

        Args:
            value (float): The new adjusted win rate value (0-1).
        """
        self.__adjusted_win_rate = value

    @property
    def tier(self) -> Tier | None:
        """Get the champion's tier classification.

        Returns:
            Tier | None: The tier classification enum value, or None if not set.
        """
        return self.__tier

    @tier.setter
    def tier(self, value: Tier | None) -> None:
        """Set the champion's tier classification.

        Args:
            value (Tier | None): The new tier classification enum value.
        """
        self.__tier = value

    def set_tier_from_string(self, tier_str: str) -> None:
        """Set the champion's tier from a string value.

        This method converts string tier data to the appropriate Tier enum value.

        Args:
            tier_str (str): The tier as a string (e.g., "S+", "A", "B", etc.).

        Raises:
            ValueError: If the tier string doesn't match any Tier enum value.
        """
        if tier_str:
            self.__tier = Tier(tier_str)
        else:
            self.__tier = None

    def to_csv_row(self) -> list[str | float]:
        """Convert champion data to a CSV row format.

        This method formats all champion statistics into a list suitable
        for CSV output. All numeric values are rounded to 4 decimal
        places for consistency.

        Returns:
            list[str | float]: A list containing the champion's data
                in the order: lane, name, win rate, pick rate, ban rate,
                adjusted win rate, and tier.
        """
        return [
            self.__lane.value,
            self.__name,
            round(self.__win_rate, 4),
            round(self.__pick_rate, 4),
            round(self.__ban_rate, 4),
            round(self.__adjusted_win_rate, 4),
            self.__tier.value if self.__tier else "",
        ]

    def __str__(self) -> str:
        """Return a string representation of the champion.

        Returns:
            str: A string representation of the champion's data.
        """
        return (
            f"Champion(name='{self.__name}', lane='{self.__lane.value}', "
            + f"win_rate={self.__win_rate}, pick_rate={self.__pick_rate}, "
            + f"ban_rate={self.__ban_rate})"
        )
