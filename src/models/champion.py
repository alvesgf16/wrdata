"""
Champion data model module.

This module defines the Champion class, which represents a champion's
performance data in a specific lane. It includes various statistics
such as win rates, pick rates, and ban rates, along with methods for
data formatting and access.
"""


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
        lane: str,
        name: str,
        win_rate: float,
        pick_rate: float,
        ban_rate: float,
    ):
        """Initialize a new Champion instance.

        Args:
            lane (str): The lane where the champion is played.
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
        self.__tier = ""

    @property
    def lane(self) -> str:
        """Get the lane where the champion is played.

        Returns:
            str: The lane name.
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
    def tier(self) -> str:
        """Get the champion's tier classification.

        Returns:
            str: The tier classification (e.g., "S+", "A", "B", etc.).
        """
        return self.__tier

    @tier.setter
    def tier(self, value: str) -> None:
        """Set the champion's tier classification.

        Args:
            value (str): The new tier classification.
        """
        self.__tier = value

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
            self.__lane,
            self.__name,
            round(self.__win_rate, 4),
            round(self.__pick_rate, 4),
            round(self.__ban_rate, 4),
            round(self.__adjusted_win_rate, 4),
            self.__tier,
        ]

    def __str__(self) -> str:
        """Return a string representation of the champion.

        Returns:
            str: A string representation of the champion's data.
        """
        return (
            f"Champion(name='{self.__name}', lane='{self.__lane}', "
            + f"win_rate={self.__win_rate}, pick_rate={self.__pick_rate}, "
            + f"ban_rate={self.__ban_rate})"
        )
