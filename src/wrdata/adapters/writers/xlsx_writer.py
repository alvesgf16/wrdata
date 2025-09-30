"""
Excel writer module for champion data output.

This module provides functionality for writing champion data to Excel
workbooks. It implements the Writer abstract base class to handle the
specific requirements of Excel file output, including worksheet
creation and table formatting.
"""

from xlsxwriter import Workbook  # type: ignore

from ...exceptions import OutputError
from ...data.models.champion import Champion
from .writer import Writer

TableOptions = dict[str, list[dict[str, str]] | list[list[str | float]]]


class XlsxWriter(Writer):
    """A class for writing champion data to Excel workbooks.

    This class implements the Writer abstract base class to write
    champion data to Excel format. It creates a single workbook with
    multiple worksheets, one for each tier, and formats the data as
    tables with proper headers.

    The output file is created in the 'res' directory with the
    format: 'output_filename.xlsx'

    Methods:
    ---
    write():
        Write champion data to an Excel workbook with multiple worksheets.
    """

    def write(self, data: list[list[Champion]]) -> None:
        """Write champion data to an Excel workbook with multiple worksheets.

        This method creates a single Excel workbook and writes the
        champion data to separate worksheets for each tier. It handles
        the workbook creation and worksheet population process.

        Args:
            data (list[list[Champion]]): A list of lists containing
                Champion objects, where each inner list represents a
                specific tier.

        Raises:
            OutputError: If there are issues creating or writing to the
                Excel file
        """
        try:
            output_file = self._create_output_file().with_suffix(".xlsx")
            with Workbook(output_file) as workbook:
                for tier_name, tier_data in zip(self._tiers, data):
                    self.__write_tier_worksheet(workbook, tier_name, tier_data)
        except Exception as e:
            raise OutputError(
                "Failed to write champion data to Excel file", details=str(e)
            ) from e

    def __write_tier_worksheet(
        self,
        workbook: Workbook,
        tier_name: str,
        tier_data: list[Champion],
    ) -> None:
        """Create and populate a worksheet for a single tier.

        This method creates a new worksheet in the workbook for a
        specific tier and formats the champion data as a table with
        proper headers. The table includes all champion statistics
        defined in the headers.

        Args:
            workbook (Workbook): The Excel workbook to add the
                worksheet to.
            tier_name (str): The name of the tier being written.
            tier_data (list[Champion]): List of Champion objects
                belonging to this tier.
        """
        worksheet = workbook.add_worksheet(tier_name)

        table_options: TableOptions = {
            "columns": [{"header": header} for header in self._headers],
            "data": [champion.to_csv_row() for champion in tier_data],
        }

        worksheet.add_table(
            0,  # First row
            0,  # First column
            len(tier_data),  # Last row
            len(self._headers) - 1,  # Last column
            table_options,
        )
