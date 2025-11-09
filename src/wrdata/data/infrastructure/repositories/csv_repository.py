"""
CSV-based champion repository implementation.

This module provides a concrete implementation of the ChampionRepository port
for persisting champion data to CSV files.
"""

import csv
from pathlib import Path

from ....exceptions import OutputError
from ...domain import Champion
from ...domain.ports.repositories import ChampionRepository


class CSVChampionRepository(ChampionRepository):
    """CSV-based implementation of the ChampionRepository port."""

    def __init__(self, filepath: str = "champions.csv") -> None:
        """Initialize the CSV champion repository.

        Args:
            filepath: The path where the CSV file will be saved.
        """
        self._filepath = Path(filepath)
        self._headers = [
            "Lane",
            "Champion",
            "Win Rate",
            "Pick Rate",
            "Ban Rate",
        ]

    def save(self, champions: list[list[Champion]]) -> None:
        """Save champion data to a CSV file.

        Flattens the nested list structure and writes all champions
        to a single CSV file.

        Args:
            champions: A list of lists containing Champion objects.

        Raises:
            OutputError: If there are issues writing to the CSV file.
        """
        try:
            # Ensure parent directory exists
            self._filepath.parent.mkdir(parents=True, exist_ok=True)

            # Flatten the nested list
            flat_champions = [champ for tier in champions for champ in tier]

            self.write_to_csv(flat_champions)

        except Exception as e:
            raise OutputError(
                f"Failed to write champions to CSV file {self._filepath}",
                details=str(e),
            ) from e

    def write_to_csv(self, flat_champions: list[Champion]) -> None:
        with self._filepath.open(
            "w", encoding="utf-8", newline=""
        ) as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(self._headers)
            csv_writer.writerows(
                [self._serialize_champion(champ) for champ in flat_champions]
            )

    def _serialize_champion(self, champion: Champion) -> list[str | float]:
        """Serialize a champion to CSV row format.

        Args:
            champion: The Champion object to serialize.

        Returns:
            A list containing the champion's data fields.
        """
        return [
            champion.lane.value,
            champion.name,
            round(champion.win_rate, 4),
            round(champion.pick_rate, 4),
            round(champion.ban_rate, 4),
        ]
