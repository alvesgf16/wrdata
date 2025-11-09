"""
Output service module for writing processed data to files.

This module provides functionality for coordinating the output of processed
champion data using various writers like CSV and Excel writers.
"""

from ..domain.models.analyzed_champion import AnalyzedChampion
from .writers.xlsx_writer import XlsxWriter

# from .writers.csv_writer import CsvWriter


class OutputService:
    """Service for writing processed champion data to output files."""

    def __init__(self) -> None:
        """Initialize the output service with available writers."""
        self._xlsx_writer = XlsxWriter()
        # self._csv_writer = CsvWriter()

    def write_champions(
        self, champions_with_metrics: list[AnalyzedChampion]
    ) -> None:
        """Write champion data to output files.

        Args:
            champions_with_metrics: A flat list of AnalyzedChampion
                objects with updated metrics.

        Raises:
            Exception: If there are issues writing the output files
        """
        self._xlsx_writer.write(champions_with_metrics)
        # self._csv_writer.write(champions_with_metrics)
