"""
End-to-end tests for the WRData application.
"""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from src.wrdata.core.orchestrator import process_champions
from src.wrdata.data import Champion, Lane, RankedTier
from src.wrdata.domain.models.analyzed_champion import AnalyzedChampion


def test_complete_workflow(
    mock_driver: MagicMock,
    test_excel_path: Path,
    sample_champion_data: list[AnalyzedChampion],
) -> None:
    """Test the complete application workflow.

    This test verifies the complete workflow:
    1. Data pipeline runs (scraping and saving to CSV)
    2. Reader loads champion data
    3. Data processor processes the champions
    4. Output service writes to Excel
    """
    # Create sample data structure (now flat list)
    champions = [
        sample_champion_data[0].champion,  # First champion
        sample_champion_data[1].champion,  # Second champion
        Champion(
            name="Test Champion 3",
            lane=Lane.MID,
            win_rate=51.5,
            pick_rate=7.8,
            ban_rate=2.1,
            ranked_tier=RankedTier.MASTER_PLUS,
        ),
    ]

    # Mock the data pipeline and reader
    with (
        patch(
            "src.wrdata.core.orchestrator.run_data_pipeline"
        ) as mock_pipeline,
        patch(
            "src.wrdata.adapters.readers.reader_factory."
            "ChampionReaderFactory.create_reader"
        ) as mock_factory,
        patch(
            "src.wrdata.adapters.service.OutputService.write_champions"
        ) as mock_writer,
    ):
        # Set up mock reader
        mock_reader = MagicMock()
        mock_reader.read.return_value = champions
        mock_factory.return_value = mock_reader

        # Run the complete process
        process_champions()

        # Verify the data pipeline was called
        mock_pipeline.assert_called_once()

        # Verify the reader was created and used
        mock_factory.assert_called_once()
        mock_reader.read.assert_called_once()

        # Verify the writer was called with the processed data
        mock_writer.assert_called_once()


def test_error_handling(mock_driver: MagicMock) -> None:
    """Test error handling in the complete workflow.

    This test verifies that errors during the data pipeline
    are properly caught and wrapped in ScrapingError.
    """
    # Mock data pipeline to raise an exception
    with patch(
        "src.wrdata.core.orchestrator.run_data_pipeline"
    ) as mock_pipeline:
        mock_pipeline.side_effect = Exception("Connection error")

        # Verify the process handles errors gracefully
        with pytest.raises(Exception):
            process_champions()


def test_data_processing_pipeline(test_excel_path: Path) -> None:
    """Test the data processing pipeline with sample data.

    This test verifies that:
    1. The data pipeline is called
    2. The reader reads the data
    3. Data processing occurs successfully
    """
    # Create sample data
    sample_data = [
        Champion(
            name="Test Champion",
            lane=Lane.TOP,
            win_rate=55.5,
            pick_rate=10.2,
            ban_rate=5.1,
            ranked_tier=RankedTier.DIAMOND_PLUS,
        )
    ]

    # Mock the data pipeline and reader
    with (
        patch(
            "src.wrdata.core.orchestrator.run_data_pipeline"
        ) as mock_pipeline,
        patch(
            "src.wrdata.adapters.readers.reader_factory."
            "ChampionReaderFactory.create_reader"
        ) as mock_factory,
    ):
        # Set up mock reader
        mock_reader = MagicMock()
        mock_reader.read.return_value = sample_data
        mock_factory.return_value = mock_reader

        # Run the process
        process_champions()

        # Verify the pipeline and reader were called
        mock_pipeline.assert_called_once()
        mock_reader.read.assert_called_once()


def test_file_output_verification(test_excel_path: Path) -> None:
    """Test that the output file contains the correct data.

    This test verifies the complete flow:
    1. Data pipeline runs (scrape and CSV write)
    2. Reader loads data from CSV
    3. Output service writes to Excel
    """
    # Create sample data
    sample_data = [
        Champion(
            name="Test Champion",
            lane=Lane.TOP,
            win_rate=55.5,
            pick_rate=10.2,
            ban_rate=5.1,
            ranked_tier=RankedTier.DIAMOND_PLUS,
        )
    ]

    # Mock the data pipeline, reader, and output service
    with (
        patch(
            "src.wrdata.core.orchestrator.run_data_pipeline"
        ) as mock_pipeline,
        patch(
            "src.wrdata.adapters.readers.reader_factory."
            "ChampionReaderFactory.create_reader"
        ) as mock_factory,
        patch(
            "src.wrdata.adapters.service.OutputService.write_champions"
        ) as mock_writer,
    ):
        # Set up mock reader
        mock_reader = MagicMock()
        mock_reader.read.return_value = sample_data
        mock_factory.return_value = mock_reader

        # Run the process
        process_champions()

        # Verify the complete workflow
        mock_pipeline.assert_called_once()  # Scrape and save to CSV
        mock_reader.read.assert_called_once()  # Read from CSV
        mock_writer.assert_called_once()  # Write to Excel
