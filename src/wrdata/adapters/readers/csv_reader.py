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

    def read(self) -> list[list[Champion]]:
        """Read champion data from the CSV file.

        Parses the CSV file and reconstructs Champion objects.
        Since the CSV format flattens tiers, this returns all
        champions in a single list wrapped in another list.

        Returns:
            A list containing one list of all Champion objects.
            The nested structure maintains consistency with the
            interface, though CSV doesn't preserve tier information.

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

            # TODO: After refactoring is complete, update CSV format to
            # preserve tier information (add tier column) so champions
            # can be properly grouped when reading back
            return [champions] if champions else []

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
