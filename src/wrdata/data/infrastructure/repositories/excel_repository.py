"""
Excel-based champion repository implementation.

This module provides a concrete implementation of the ChampionRepository port
for persisting champion data to Excel workbooks.
"""

from pathlib import Path

from xlsxwriter import Workbook  # type: ignore

from ....exceptions import OutputError
from ...domain import Champion
from ...domain.ports.repositories import ChampionRepository

TableOptions = dict[str, list[dict[str, str]] | list[list[str | float]]]


class ExcelChampionRepository(ChampionRepository):
    """Excel-based implementation of the ChampionRepository port."""

    def __init__(self, filepath: str = "champions.xlsx") -> None:
        """Initialize the Excel champion repository.

        Args:
            filepath: The path where the Excel file will be saved.
        """
        self._filepath = Path(filepath)
        self._headers = [
            "Lane",
            "Champion",
            "Win Rate",
            "Pick Rate",
            "Ban Rate",
        ]
        self._tier_names = ["Tier 1", "Tier 2", "Tier 3", "Tier 4"]

    def save(self, champions: list[list[Champion]]) -> None:
        """Save champion data to an Excel workbook.

        Creates a workbook with separate worksheets for each tier.

        Args:
            champions: A list of lists containing Champion objects,
                where each inner list represents a tier.

        Raises:
            OutputError: If there are issues writing to the Excel file.
        """
        try:
            # Ensure parent directory exists
            self._filepath.parent.mkdir(parents=True, exist_ok=True)

            with Workbook(self._filepath) as workbook:
                for tier_name, tier_data in zip(self._tier_names, champions):
                    self._write_tier_worksheet(workbook, tier_name, tier_data)

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
        worksheet = workbook.add_worksheet(tier_name)

        table_options: TableOptions = {
            "columns": [{"header": header} for header in self._headers],
            "data": [
                self._serialize_champion(champion) for champion in tier_data
            ],
        }

        worksheet.add_table(
            0,  # First row
            0,  # First column
            len(tier_data),  # Last row
            len(self._headers) - 1,  # Last column
            table_options,
        )

    def _serialize_champion(self, champion: Champion) -> list[str | float]:
        """Serialize a champion to Excel row format.

        Args:
            champion: The Champion object to serialize.

        Returns:
            A list containing the champion's data fields.
        """
        return [
            champion.lane.value,
            champion.name,
            round(champion.win_rate, 4),
            round(champion.pick_rate, 4),
            round(champion.ban_rate, 4),
        ]
