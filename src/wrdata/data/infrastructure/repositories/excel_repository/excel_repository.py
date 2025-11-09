"""
Excel-based champion repository implementation.

This module provides a concrete implementation of the ChampionRepository port
for persisting champion data to Excel workbooks.
"""

from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.worksheet.worksheet import Worksheet

from .....exceptions import OutputError
from ....domain import Champion, RankedTier
from ..base_repository import BaseChampionRepository


class ExcelChampionRepository(BaseChampionRepository):
    """Excel-based implementation of the ChampionRepository port."""

    def __init__(self, filepath: str = "champions.xlsx") -> None:
        """Initialize the Excel champion repository.

        Args:
            filepath: The path where the Excel file will be saved.
        """
        super().__init__(filepath)
        self.__workbook = Workbook()

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

            self.__write_to_excel(champions)

        except Exception as e:
            raise OutputError(
                f"Failed to write champions to Excel file "
                f"{self._filepath}",
                details=str(e),
            ) from e

    def __write_to_excel(self, champions: list[Champion]) -> None:
        self._remove_default_sheet(self.__workbook)

        ranked_tier_groups = self._group_champions_by_ranked_tier(champions)

        for ranked_tier, tier_champions in ranked_tier_groups.items():
            self._write_tier_worksheet(
                self.__workbook, ranked_tier.value, tier_champions
            )

        self.__workbook.save(self._filepath)

    def _remove_default_sheet(self, workbook: Workbook) -> None:
        if "Sheet" in workbook.sheetnames:
            default_sheet = workbook["Sheet"]
            workbook.remove(default_sheet)

    def _group_champions_by_ranked_tier(
        self, champions: list[Champion]
    ) -> dict[RankedTier, list[Champion]]:
        tier_groups: dict[RankedTier, list[Champion]] = {}
        for champion in champions:
            if champion.ranked_tier not in tier_groups:
                tier_groups[champion.ranked_tier] = []
            tier_groups[champion.ranked_tier].append(champion)
        return tier_groups

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
        self._write_headers(worksheet)

        # Write data
        self._write_data(tier_data, worksheet)

        # Create table if there's data
        if tier_data:
            table = self.create_tier_table(tier_name, tier_data)

            worksheet.add_table(table)

    def _write_headers(self, worksheet: Worksheet) -> None:
        for col_idx, header in enumerate(self._headers, start=1):
            worksheet.cell(row=1, column=col_idx, value=header)

    def _write_data(
        self, tier_data: list[Champion], worksheet: Worksheet
    ) -> None:
        for row_idx, champion in enumerate(tier_data, start=2):
            row_data = self._serialize_champion(champion)
            for col_idx, value in enumerate(row_data, start=1):
                worksheet.cell(row=row_idx, column=col_idx, value=value)

    def create_tier_table(
        self, tier_name: str, tier_data: list[Champion]
    ) -> Table:
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
        return table
