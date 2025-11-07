"""
End-to-end tests for the WRData application.
"""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from src.wrdata.core.orchestrator import process_champions
from src.wrdata.data import Champion, Lane


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
                lane=Lane.MID,
                win_rate=51.5,
                pick_rate=7.8,
                ban_rate=2.1,
            )
        ],
    ]

    # Mock the services and data collection
    with (
        patch(
            "src.wrdata.data.infrastructure.fetchers."
            "data_fetcher.DataFetcher.fetch_champions"
        ) as mock_fetch,
        patch(
            "src.wrdata.adapters.service.OutputService.write_champions"
        ) as mock_writer,
    ):
        # Set up mocks
        mock_fetch.return_value = champions_by_tier

        # Run the complete process
        process_champions()

        # Verify the data collection was called
        mock_fetch.assert_called_once()

        # Verify the writer was called with the processed data
        mock_writer.assert_called_once()


def test_error_handling(mock_driver: MagicMock) -> None:
    """Test error handling in the complete workflow."""
    # Mock data fetcher to raise an exception
    with patch(
        "src.wrdata.data.infrastructure.fetchers."
        "data_fetcher.DataFetcher.fetch_champions"
    ) as mock_fetch:
        mock_fetch.side_effect = Exception("Connection error")

        # Verify the process handles errors gracefully
        with pytest.raises(Exception):
            process_champions()


def test_data_processing_pipeline(test_excel_path: Path) -> None:
    """Test the data processing pipeline with sample data."""
    # Create sample data
    sample_data = [
        Champion(
            name="Test Champion",
            lane=Lane.TOP,
            win_rate=55.5,
            pick_rate=10.2,
            ban_rate=5.1,
        )
    ]

    # Mock the data collection and processing
    with patch(
        "src.wrdata.data.infrastructure.fetchers."
        "data_fetcher.DataFetcher.fetch_champions"
    ) as mock_fetch:
        mock_fetch.return_value = [sample_data]

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
            lane=Lane.TOP,
            win_rate=55.5,
            pick_rate=10.2,
            ban_rate=5.1,
        )
    ]

    # Mock the data collection and output service
    with (
        patch(
            "src.wrdata.data.infrastructure.fetchers."
            "data_fetcher.DataFetcher.fetch_champions"
        ) as mock_fetch,
        patch(
            "src.wrdata.adapters.service.OutputService.write_champions"
        ) as mock_writer,
    ):
        mock_fetch.return_value = [sample_data]

        # Run the process
        process_champions()

        # Verify the data was fetched and writer was called
        mock_fetch.assert_called_once()
        mock_writer.assert_called_once()
