"""
CSV-based champion data reader implementation.

This module provides a concrete implementation of the ChampionReader port
for reading champion data from CSV files.
"""

import csv
from pathlib import Path

from ...data import Champion, Lane, RankedTier
from .reader import ChampionReader


class CSVChampionReader(ChampionReader):
    """CSV-based implementation of the ChampionReader port.

    Reads champion data from CSV files and reconstructs Champion objects
    organized by tier. This reader is designed to work with CSV files
    created by CSVChampionRepository.
    """

    def __init__(self, filepath: str = "champions.csv") -> None:
        """Initialize the CSV champion reader.

        Args:
            filepath: The path to the CSV file to read from.
        """
        self._filepath = Path(filepath)

    def read(self) -> list[Champion]:
        """Read champion data from the CSV file.

        Parses the CSV file and reconstructs Champion objects
        with tier information from the ranked_tier column.

        Returns:
            A flat list of Champion objects.

        Raises:
            FileNotFoundError: If the CSV file doesn't exist.
            ValueError: If the CSV data is malformed.
            Exception: For other reading errors.
        """
        if not self._filepath.exists():
            raise FileNotFoundError(f"CSV file not found: {self._filepath}")

        try:
            champions: list[Champion] = []

            with self._filepath.open("r", encoding="utf-8") as csv_file:
                csv_reader = csv.DictReader(csv_file)

                for row in csv_reader:
                    champion = self._deserialize_champion(row)
                    champions.append(champion)

            return champions

        except Exception as e:
            raise Exception(
                f"Failed to read champions from CSV file {self._filepath}: {e}"
            ) from e

    def _deserialize_champion(self, row: dict[str, str]) -> Champion:
        """Deserialize a CSV row into a Champion object.

        Args:
            row: A dictionary representing one CSV row.

        Returns:
            A Champion object reconstructed from the CSV data.

        Raises:
            ValueError: If the row data is invalid.
        """
        try:
            return Champion(
                name=row["Champion"],
                lane=Lane(row["Lane"]),
                win_rate=float(row["Win Rate"]),
                pick_rate=float(row["Pick Rate"]),
                ban_rate=float(row["Ban Rate"]),
                ranked_tier=RankedTier(row.get("Ranked Tier", "Diamond+")),
            )
        except (KeyError, ValueError) as e:
            raise ValueError(f"Invalid CSV row data: {row}. Error: {e}") from e
