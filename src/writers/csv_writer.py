"""
CSV writer module for champion data output.

This module provides functionality for writing champion data to CSV files.
It implements the Writer abstract base class to handle the specific
requirements of CSV file output, including proper encoding and
formatting.
"""

import csv
from pathlib import Path
from ..models.champion import Champion
from .writer import Writer


class CsvWriter(Writer):
    """A class for writing champion data to CSV files.

    This class implements the Writer abstract base class to write
    champion data to CSV format. It handles the creation of separate
    CSV files for each tier and ensures proper CSV formatting and
    encoding.

    The output files are created in the 'res' directory with the
    format: 'output_filename_tier.csv'

    Methods:
    ---
    write():
        Write champion data to separate CSV files for each tier.
    """

    def write(self, data: list[list[Champion]]) -> None:
        """Write champion data to separate CSV files for each tier.

        This method processes the champion data and creates individual
        CSV files for each tier. It iterates through the tiers and
        their corresponding champion data, writing each to a separate
        file.

        Args:
            data (list[list[Champion]]): A list of lists containing
                Champion objects, where each inner list represents a
                specific tier.
        """
        for tier_name, tier_data in zip(self._tiers, data):
            self.__write_tier_file(tier_name, tier_data)

    def __write_tier_file(
        self, tier_name: str, tier_data: list[Champion]
    ) -> None:
        """Write data for a single tier to a CSV file.

        This method creates a CSV file for a specific tier and writes
        the champion data to it. The file is created with the tier name
        appended to the base filename.

        Args:
            tier_name (str): The name of the tier being written.
            tier_data (list[Champion]): List of Champion objects
                belonging to this tier.
        """
        output_file = self._create_output_file(tier_name).with_suffix(".csv")
        self.__write_to_file(output_file, tier_data)

    def __write_to_file(
        self, output_file: Path, tier_data: list[Champion]
    ) -> None:
        """Write the CSV data to the specified output file.

        This method handles the actual writing of CSV data to the file,
        including proper encoding and formatting. It writes the headers
        first, followed by the champion data rows.

        Args:
            output_file (Path): The Path object representing the output
                file location.
            tier_data (list[Champion]): List of Champion objects to
                write to the CSV file.
        """
        csv_data = [champion.to_csv_row() for champion in tier_data]

        with output_file.open("w", encoding="utf-8", newline="") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(self._headers)
            csv_writer.writerows(csv_data)
