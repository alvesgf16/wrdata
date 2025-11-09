"""
CSV-based champion repository implementation.

This module provides a concrete implementation of the ChampionRepository port
for persisting champion data to CSV files.
"""

import csv

from .....exceptions import OutputError
from ....domain import Champion
from ..base_repository import BaseChampionRepository


class CSVChampionRepository(BaseChampionRepository):
    """CSV-based implementation of the ChampionRepository port."""

    def __init__(self, filepath: str = "champions.csv") -> None:
        """Initialize the CSV champion repository.

        Args:
            filepath: The path where the CSV file will be saved.
        """
        super().__init__(filepath)

    def save(self, champions: list[Champion]) -> None:
        """Save champion data to a CSV file.

        Args:
            champions: A flat list of Champion objects.

        Raises:
            OutputError: If there are issues writing to the CSV file.
        """
        try:
            self._ensure_directory_exists()

            self._write_to_csv(champions)

        except Exception as e:
            raise OutputError(
                f"Failed to write champions to CSV file {self._filepath}",
                details=str(e),
            ) from e

    def _write_to_csv(self, champions: list[Champion]) -> None:
        with self._filepath.open(
            "w", encoding="utf-8", newline=""
        ) as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(self._headers)
            csv_writer.writerows(
                [self._serialize_champion(champ) for champ in champions]
            )
