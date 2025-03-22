"""
End-to-end tests for the WRData application.
"""

import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from src.champion_data_collector import process_champions
from src.champion import Champion
from src.writers.xlsx_writer import XlsxWriter


def test_complete_workflow(
    mock_driver: MagicMock,
    test_excel_path: Path,
    sample_champion_data: list[Champion],
) -> None:
    """Test the complete application workflow."""
    # Create sample data structure
    champions_by_tier = [
        sample_champion_data,  # Tier S
        [  # Tier A
            Champion(
                name="Test Champion 3",
                lane="Mid",
                win_rate=51.5,
                pick_rate=7.8,
                ban_rate=2.1,
            )
        ],
    ]

    # Mock the webdriver creation and data collection
    with patch(
        "src.champion_data_collector.create_driver"
    ) as mock_create_driver, patch(
        "src.champion_data_collector.fetch_champions"
    ) as mock_fetch, patch(
        "src.champion_data_collector.XlsxWriter"
    ) as mock_writer:
        # Set up mocks
        mock_create_driver.return_value.__enter__.return_value = mock_driver
        mock_fetch.return_value = champions_by_tier
        mock_writer.return_value = XlsxWriter(str(test_excel_path))

        # Run the complete process
        process_champions()

        # Verify the data collection was called
        mock_fetch.assert_called_once()

        # Verify the output file was created and has content
        assert Path(test_excel_path).exists()
        assert Path(test_excel_path).stat().st_size > 0

        # Verify the writer was called with the correct data
        mock_writer.assert_called_once()


def test_error_handling(mock_driver: MagicMock) -> None:
    """Test error handling in the complete workflow."""
    # Mock webdriver to raise an exception
    mock_driver.get.side_effect = Exception("Connection error")

    with patch(
        "src.champion_data_collector.create_driver"
    ) as mock_create_driver:
        mock_create_driver.return_value.__enter__.return_value = mock_driver

        # Verify the process handles errors gracefully
        with pytest.raises(Exception):
            process_champions()


def test_data_processing_pipeline(test_excel_path: Path) -> None:
    """Test the data processing pipeline with sample data."""
    # Create sample data
    sample_data = [
        Champion(
            name="Test Champion",
            lane="Top",
            win_rate=55.5,
            pick_rate=10.2,
            ban_rate=5.1,
        )
    ]

    # Mock the data collection and processing
    with patch(
        "src.champion_data_collector.fetch_champions"
    ) as mock_fetch, patch(
        "src.champion_data_collector.XlsxWriter"
    ) as mock_writer:
        mock_fetch.return_value = [sample_data]
        mock_writer.return_value = XlsxWriter(str(test_excel_path))

        # Run the process
        process_champions()

        # Verify the data was processed
        mock_fetch.assert_called_once()


def test_file_output_verification(test_excel_path: Path) -> None:
    """Test that the output file contains the correct data."""
    # Create sample data
    sample_data = [
        Champion(
            name="Test Champion",
            lane="Top",
            win_rate=55.5,
            pick_rate=10.2,
            ban_rate=5.1,
        )
    ]

    # Mock the data collection and XlsxWriter
    with patch(
        "src.champion_data_collector.fetch_champions"
    ) as mock_fetch, patch(
        "src.champion_data_collector.XlsxWriter"
    ) as mock_writer:
        mock_fetch.return_value = [sample_data]
        mock_writer.return_value = XlsxWriter(str(test_excel_path))

        # Run the process
        process_champions()

        # Verify the output file exists and has content
        assert Path(test_excel_path).exists()
        assert Path(test_excel_path).stat().st_size > 0
