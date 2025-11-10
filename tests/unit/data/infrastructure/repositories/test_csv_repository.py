"""
Tests for the CSV Champion Repository.
"""

import csv
from pathlib import Path

import pytest

from src.wrdata.data import Champion, Lane, RankedTier
from src.wrdata.data.infrastructure.repositories.csv_repository import (
    CSVChampionRepository,
)
from src.wrdata.exceptions import OutputError


@pytest.fixture
def sample_champions() -> list[Champion]:
    """Create sample champions for testing."""
    return [
        Champion(
            name="Darius",
            lane=Lane.TOP,
            win_rate=52.3456,
            pick_rate=8.7654,
            ban_rate=15.2345,
            ranked_tier=RankedTier.DIAMOND_PLUS,
        ),
        Champion(
            name="Lee Sin",
            lane=Lane.JUNGLE,
            win_rate=48.5678,
            pick_rate=12.3456,
            ban_rate=20.1234,
            ranked_tier=RankedTier.SOVEREIGN,
        ),
    ]


@pytest.fixture
def temp_csv_path(tmp_path: Path) -> Path:
    """Create a temporary CSV file path."""
    return tmp_path / "test_champions.csv"


def test_csv_repository_initialization() -> None:
    """Test CSV repository initialization with default filepath."""
    repo = CSVChampionRepository()
    assert repo._filepath == Path("champions.csv")


def test_csv_repository_custom_filepath() -> None:
    """Test CSV repository initialization with custom filepath."""
    custom_path = "custom/path/champions.csv"
    repo = CSVChampionRepository(filepath=custom_path)
    assert repo._filepath == Path(custom_path)


def test_save_creates_csv_file(
    sample_champions: list[Champion], temp_csv_path: Path
) -> None:
    """Test that save creates a CSV file."""
    repo = CSVChampionRepository(filepath=str(temp_csv_path))
    repo.save(sample_champions)

    assert temp_csv_path.exists()
    assert temp_csv_path.is_file()


def test_save_writes_headers(
    sample_champions: list[Champion], temp_csv_path: Path
) -> None:
    """Test that headers are written correctly."""
    repo = CSVChampionRepository(filepath=str(temp_csv_path))
    repo.save(sample_champions)

    with temp_csv_path.open("r", encoding="utf-8") as f:
        reader = csv.reader(f)
        headers = next(reader)

    expected_headers = [
        "Lane",
        "Champion",
        "Win Rate",
        "Pick Rate",
        "Ban Rate",
        "Ranked Tier",
    ]
    assert headers == expected_headers


def test_save_writes_champion_data(
    sample_champions: list[Champion], temp_csv_path: Path
) -> None:
    """Test that champion data is written correctly."""
    repo = CSVChampionRepository(filepath=str(temp_csv_path))
    repo.save(sample_champions)

    with temp_csv_path.open("r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)  # Skip headers
        rows = list(reader)

    assert len(rows) == 2

    # Check first champion
    assert rows[0][0] == "Top"
    assert rows[0][1] == "Darius"
    assert float(rows[0][2]) == 52.3456
    assert float(rows[0][3]) == 8.7654
    assert float(rows[0][4]) == 15.2345
    assert rows[0][5] == "Diamond+"

    # Check second champion
    assert rows[1][0] == "Jungle"
    assert rows[1][1] == "Lee Sin"
    assert float(rows[1][2]) == 48.5678
    assert float(rows[1][3]) == 12.3456
    assert float(rows[1][4]) == 20.1234
    assert rows[1][5] == "Sovereign"


def test_save_with_empty_list(temp_csv_path: Path) -> None:
    """Test saving an empty list of champions."""
    repo = CSVChampionRepository(filepath=str(temp_csv_path))
    repo.save([])

    with temp_csv_path.open("r", encoding="utf-8") as f:
        reader = csv.reader(f)
        headers = next(reader)
        rows = list(reader)

    assert len(headers) == 6
    assert len(rows) == 0


def test_save_creates_nested_directories(tmp_path: Path) -> None:
    """Test that save creates nested directories if they don't exist."""
    nested_path = tmp_path / "nested" / "dir" / "champions.csv"
    repo = CSVChampionRepository(filepath=str(nested_path))

    repo.save(
        [
            Champion(
                name="Test",
                lane=Lane.MID,
                win_rate=50.0,
                pick_rate=5.0,
                ban_rate=2.0,
                ranked_tier=RankedTier.DIAMOND_PLUS,
            )
        ]
    )

    assert nested_path.exists()
    assert nested_path.parent.exists()


def test_save_overwrites_existing_file(
    sample_champions: list[Champion], temp_csv_path: Path
) -> None:
    """Test that save overwrites an existing file."""
    repo = CSVChampionRepository(filepath=str(temp_csv_path))

    # First save
    repo.save(sample_champions[:1])

    with temp_csv_path.open("r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)  # Skip headers
        rows = list(reader)
    assert len(rows) == 1

    # Second save should overwrite
    repo.save(sample_champions)

    with temp_csv_path.open("r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)  # Skip headers
        rows = list(reader)
    assert len(rows) == 2


def test_save_raises_output_error_on_invalid_path() -> None:
    """Test that save raises OutputError on invalid path."""
    # Use an invalid path (e.g., path with invalid characters on Windows)
    invalid_path = "/\x00invalid/path"
    repo = CSVChampionRepository(filepath=invalid_path)

    with pytest.raises(OutputError) as exc_info:
        repo.save([])

    assert "Failed to write champions to CSV file" in str(exc_info.value)


def test_csv_encoding_utf8(
    sample_champions: list[Champion], temp_csv_path: Path
) -> None:
    """Test that CSV is written with UTF-8 encoding."""
    # Add a champion with unicode characters
    unicode_champion = Champion(
        name="疾风剑豪",  # Yasuo in Chinese
        lane=Lane.MID,
        win_rate=50.5,
        pick_rate=15.2,
        ban_rate=10.3,
        ranked_tier=RankedTier.MASTER_PLUS,
    )

    repo = CSVChampionRepository(filepath=str(temp_csv_path))
    repo.save([unicode_champion])

    # Read back with UTF-8 encoding
    with temp_csv_path.open("r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)  # Skip headers
        row = next(reader)

    assert row[1] == "疾风剑豪"
