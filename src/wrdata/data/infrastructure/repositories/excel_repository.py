"""
Excel-based champion repository implementation.

This module provides a concrete implementation of the ChampionRepository port
for persisting champion data to Excel workbooks.
"""

from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo

from ....exceptions import OutputError
from ...domain import Champion, RankedTier
from .base_repository import BaseChampionRepository


class ExcelChampionRepository(BaseChampionRepository):
    """Excel-based implementation of the ChampionRepository port."""

    def __init__(self, filepath: str = "champions.xlsx") -> None:
        """Initialize the Excel champion repository.

        Args:
            filepath: The path where the Excel file will be saved.
        """
        super().__init__(filepath)

    def save(self, champions: list[Champion]) -> None:
        """Save champion data to an Excel workbook.

        Creates a workbook with separate worksheets for each ranked tier,
        grouping champions by their ranked_tier attribute.

        Args:
            champions: A flat list of Champion objects.

        Raises:
            OutputError: If there are issues writing to the Excel file.
        """
        try:
            self._ensure_directory_exists()

            workbook = Workbook()

            # Remove default sheet
            if "Sheet" in workbook.sheetnames:
                default_sheet = workbook["Sheet"]
                workbook.remove(default_sheet)

            # Group champions by their ranked_tier attribute
            tier_groups: dict[RankedTier, list[Champion]] = {}
            for champion in champions:
                if champion.ranked_tier not in tier_groups:
                    tier_groups[champion.ranked_tier] = []
                tier_groups[champion.ranked_tier].append(champion)

            # Create a worksheet for each tier group
            for ranked_tier, tier_champions in tier_groups.items():
                self._write_tier_worksheet(
                    workbook, ranked_tier.value, tier_champions
                )

            workbook.save(self._filepath)

        except Exception as e:
            raise OutputError(
                f"Failed to write champions to Excel file "
                f"{self._filepath}",
                details=str(e),
            ) from e

    def _write_tier_worksheet(
        self,
        workbook: Workbook,
        tier_name: str,
        tier_data: list[Champion],
    ) -> None:
        """Create and populate a worksheet for a single tier.

        Args:
            workbook: The Excel workbook to add the worksheet to.
            tier_name: The name of the tier worksheet.
            tier_data: List of Champion objects for this tier.
        """
        worksheet = workbook.create_sheet(title=tier_name)

        # Write headers
        for col_idx, header in enumerate(self._headers, start=1):
            worksheet.cell(row=1, column=col_idx, value=header)

        # Write data
        for row_idx, champion in enumerate(tier_data, start=2):
            row_data = self._serialize_champion(champion)
            for col_idx, value in enumerate(row_data, start=1):
                worksheet.cell(row=row_idx, column=col_idx, value=value)

        # Create table if there's data
        if tier_data:
            last_row = len(tier_data) + 1
            last_col = get_column_letter(len(self._headers))

            table = Table(
                displayName=f"Table_{tier_name.replace(' ', '_')}",
                ref=f"A1:{last_col}{last_row}",
            )

            style = TableStyleInfo(
                name="TableStyleMedium2",
                showFirstColumn=False,
                showLastColumn=False,
                showRowStripes=True,
                showColumnStripes=False,
            )
            table.tableStyleInfo = style

            worksheet.add_table(table)
