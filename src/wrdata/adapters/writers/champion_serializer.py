"""
Champion serialization module for output formatting.

This module provides functionality for serializing champion data into
various output formats. It acts as a bridge between domain models and
output writers, handling the conversion of AnalyzedChampion objects
into format-specific representations.
"""

from ...domain.models.analyzed_champion import AnalyzedChampion


class ChampionSerializer:
    """Serializes champion data for output formats.

    This class provides static methods to convert AnalyzedChampion
    objects into various output formats like CSV rows. It centralizes
    serialization logic, making it easy to maintain and extend to
    support additional output formats.

    Methods:
    ---
    to_csv_row():
        Convert analyzed champion to CSV row format.
    """

    @staticmethod
    def to_csv_row(analyzed_champion: AnalyzedChampion) -> list[str | float]:
        """Convert analyzed champion data to a CSV row format.

        This method formats all champion statistics into a list suitable
        for CSV output. All numeric values are rounded to 4 decimal
        places for consistency.

        Args:
            analyzed_champion (AnalyzedChampion): The analyzed champion
                object containing both base data and calculated metrics.

        Returns:
            list[str | float]: A list containing the champion's data
                in the order: lane, name, win rate, pick rate, ban rate,
                adjusted win rate, and tier.
        """
        champ = analyzed_champion.champion
        return [
            champ.lane.value,
            champ.name,
            round(champ.win_rate, 4),
            round(champ.pick_rate, 4),
            round(champ.ban_rate, 4),
            round(analyzed_champion.adjusted_win_rate, 4),
            analyzed_champion.tier.value if analyzed_champion.tier else "",
        ]
