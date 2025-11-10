"""
CSV-based champion repository implementation.

This module provides a concrete implementation of the ChampionRepository port
for persisting champion data to CSV files.
"""

import csv
from typing import Protocol, Sequence, TextIO

from .....exceptions import OutputError
from ....domain import Champion
from ..base_repository import BaseChampionRepository


class _CSVWriter(Protocol):
    """Protocol for csv.writer type."""

    def writerow(self, row: Sequence[str | float]) -> None:
        """Write a single row."""
        ...

    def writerows(self, rows: Sequence[Sequence[str | float]]) -> None:
        """Write multiple rows."""
        ...


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

            self._write(champions)

        except Exception as e:
            raise OutputError(
                f"Failed to write champions to CSV file {self._filepath}",
                details=str(e),
            ) from e

    def _write(self, champions: list[Champion]) -> None:
        with self._filepath.open(
            "w", encoding="utf-8", newline=""
        ) as csv_file:
            csv_writer = self._create_writer(csv_file)

            self._write_headers(csv_writer)
            self._write_data(champions, csv_writer)

    def _create_writer(self, csv_file: TextIO) -> _CSVWriter:
        return csv.writer(csv_file)

    def _write_headers(self, csv_writer: _CSVWriter) -> None:
        csv_writer.writerow(self._headers)

    def _write_data(
        self, champions: list[Champion], csv_writer: _CSVWriter
    ) -> None:
        csv_writer.writerows(
            [self._serialize_champion(champ) for champ in champions]
        )
