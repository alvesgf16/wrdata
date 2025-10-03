"""
Tests for the data writers.
"""

from pathlib import Path

import pytest
from xlsxwriter.exceptions import FileCreateError  # type: ignore

from src.wrdata.adapters.writers.xlsx_writer import XlsxWriter
from src.wrdata.data.models.champion import Champion
from src.wrdata.data.models.enums import Lane


def test_xlsx_writer(
    sample_champion_data: list[Champion], test_excel_path: Path
) -> None:
    """Test Excel file writing functionality."""
    # Create test data structure
    champions_by_tier = [
        sample_champion_data,  # Tier S
        [  # Tier A
            Champion(
                name="Test Champion 3",
                lane=Lane.MID,
                win_rate=51.5,
                pick_rate=7.8,
                ban_rate=2.1,
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

    # On Windows, we expect OutputError, on Unix systems, FileCreateError
    import platform

    if platform.system() == "Windows":
        from src.wrdata.exceptions import OutputError

        with pytest.raises(OutputError):
            writer.write([[]])
    else:
        with pytest.raises(FileCreateError):
            writer.write([[]])
