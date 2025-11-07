"""Tests for CSV writer functionality."""

from pathlib import Path
from unittest.mock import patch

import pytest

from src.wrdata.adapters.writers.csv_writer import CsvWriter
from src.wrdata.data.domain.models.champion import Champion, Lane
from src.wrdata.domain.models.analyzed_champion import AnalyzedChampion, Tier


@pytest.fixture
def sample_champion_data() -> list[AnalyzedChampion]:
    """Sample champion data for testing."""
    return [
        AnalyzedChampion(
            champion=Champion(
                lane=Lane.TOP,
                name="Jinx",
                win_rate=52.5,
                pick_rate=12.3,
                ban_rate=8.1,
            ),
            adjusted_win_rate=53.0,
            tier=Tier.A,
        ),
        AnalyzedChampion(
            champion=Champion(
                lane=Lane.MID,
                name="Yasuo",
                win_rate=48.2,
                pick_rate=15.7,
                ban_rate=25.4,
            ),
            adjusted_win_rate=49.0,
            tier=Tier.B,
        ),
        AnalyzedChampion(
            champion=Champion(
                lane=Lane.SUP,
                name="Thresh",
                win_rate=51.8,
                pick_rate=8.9,
                ban_rate=3.2,
            ),
            adjusted_win_rate=52.0,
            tier=Tier.A,
        ),
        AnalyzedChampion(
            champion=Champion(
                lane=Lane.BOT,
                name="Akali",
                win_rate=47.3,
                pick_rate=7.2,
                ban_rate=18.5,
            ),
            adjusted_win_rate=48.0,
            tier=Tier.C,
        ),
    ]


def test_csv_writer_basic(
    sample_champion_data: list[AnalyzedChampion], tmp_path: Path
) -> None:
    """Test basic CSV writer functionality."""
    writer = CsvWriter("test_basic")

    # Mock the _create_output_file method to use tmp_path
    def mock_create_output_file(tier: str = "") -> Path:
        filename = f"test_basic_{tier.lower()}" if tier else "test_basic"
        return tmp_path / filename

    with patch.object(
        writer, "_create_output_file", side_effect=mock_create_output_file
    ):
        writer.write([sample_champion_data[:2]])

    # Check if file was created
    expected_file = tmp_path / "test_basic_diamond.csv"
    assert expected_file.exists()


def test_csv_writer_empty_data(tmp_path: Path) -> None:
    """Test CSV writer with empty data."""
    writer = CsvWriter("test_empty")

    # Mock the _create_output_file method to use tmp_path
    def mock_create_output_file(tier: str = "") -> Path:
        filename = f"test_empty_{tier.lower()}" if tier else "test_empty"
        return tmp_path / filename

    with patch.object(
        writer, "_create_output_file", side_effect=mock_create_output_file
    ):
        writer.write([])

    # Check that no files were created for empty data
    csv_files = list(tmp_path.glob("test_empty_*.csv"))
    assert len(csv_files) == 0


def test_csv_writer_multiple_tiers(
    sample_champion_data: list[AnalyzedChampion], tmp_path: Path
) -> None:
    """Test CSV writer with multiple tiers."""
    writer = CsvWriter("test_multi")

    # Mock the _create_output_file method to use tmp_path
    def mock_create_output_file(tier: str = "") -> Path:
        filename = f"test_multi_{tier.lower()}" if tier else "test_multi"
        return tmp_path / filename

    with patch.object(
        writer, "_create_output_file", side_effect=mock_create_output_file
    ):
        # Split data into tiers
        tier_data = [
            sample_champion_data[:2],  # First tier
            (
                sample_champion_data[2:]
                if len(sample_champion_data) > 2
                else []
            ),  # Second tier
        ]
        writer.write(tier_data)

    # Check if multiple files were created
    csv_files = list(tmp_path.glob("test_multi_*.csv"))
    assert len(csv_files) >= 1  # At least one file should be created


def test_csv_writer_headers(
    sample_champion_data: list[AnalyzedChampion], tmp_path: Path
) -> None:
    """Test that CSV files have proper headers."""
    writer = CsvWriter("test_headers")

    # Mock the _create_output_file method to use tmp_path
    def mock_create_output_file(tier: str = "") -> Path:
        filename = f"test_headers_{tier.lower()}" if tier else "test_headers"
        return tmp_path / filename

    with patch.object(
        writer, "_create_output_file", side_effect=mock_create_output_file
    ):
        writer.write([sample_champion_data[:1]])

    # Find the created CSV file
    csv_files = list(tmp_path.glob("test_headers_*.csv"))
    assert len(csv_files) > 0

    # Read the file and check headers
    csv_file = csv_files[0]
    content = csv_file.read_text(encoding="utf-8")
    lines = content.strip().split("\n")

    # Should have at least header + 1 data row
    assert len(lines) >= 2

    # Check that first line contains expected headers
    header = lines[0].lower()
    assert "champion" in header
    assert "lane" in header
