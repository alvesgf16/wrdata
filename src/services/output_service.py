"""
Output service module for writing processed data to files.

This module provides functionality for coordinating the output of processed
champion data using various writers like CSV and Excel writers.
"""

from ..models.champion import Champion
from ..writers.xlsx_writer import XlsxWriter
# from ..writers.csv_writer import CsvWriter


class OutputService:
    """Service for writing processed champion data to output files."""

    def __init__(self) -> None:
        """Initialize the output service with available writers."""
        self._xlsx_writer = XlsxWriter()
        # self._csv_writer = CsvWriter()

    def write_champions(
        self, champions_with_metrics: list[list[Champion]]
    ) -> None:
        """Write champion data to output files.

        Args:
            champions_with_metrics: A list of lists containing Champion objects
                with updated metrics, organized by tier.

        Raises:
            Exception: If there are issues writing the output files
        """
        self._xlsx_writer.write(champions_with_metrics)
        # self._csv_writer.write(champions_with_metrics)
