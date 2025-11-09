"""
Tests for the data writers.
"""

from pathlib import Path

import pytest

from src.wrdata.adapters.writers.xlsx_writer import XlsxWriter
from src.wrdata.data import Champion, Lane, RankedTier
from src.wrdata.domain.models.analyzed_champion import AnalyzedChampion, Tier
from src.wrdata.exceptions import OutputError


def test_xlsx_writer(
    sample_champion_data: list[AnalyzedChampion], test_excel_path: Path
) -> None:
    """Test Excel file writing functionality."""
    # Create test data structure
    champions_by_tier = [
        sample_champion_data,  # Tier S
        [  # Tier A
            AnalyzedChampion(
                champion=Champion(
                    name="Test Champion 3",
                    lane=Lane.MID,
                    win_rate=51.5,
                    pick_rate=7.8,
                    ban_rate=2.1,
                    ranked_tier=RankedTier.MASTER_PLUS,
                ),
                adjusted_win_rate=52.0,
                tier=Tier.A,
            )
        ],
    ]

    # Write data to Excel
    writer = XlsxWriter(str(test_excel_path))
    writer.write(champions_by_tier)

    # Verify file was created
    assert Path(test_excel_path).exists()


def test_xlsx_writer_empty_data(test_excel_path: Path) -> None:
    """Test Excel writer with empty data."""
    writer = XlsxWriter(str(test_excel_path))
    writer.write([])

    # Verify file was created even with empty data
    assert Path(test_excel_path).exists()


def test_xlsx_writer_file_permissions(test_excel_path: Path) -> None:
    """Test Excel writer with file permission issues."""
    writer = XlsxWriter(str(test_excel_path))

    # Create a read-only file
    test_excel_path.touch()
    test_excel_path.chmod(0o444)  # Read-only

    # Expect OutputError for file permission issues
    with pytest.raises(OutputError):
        writer.write([[]])
