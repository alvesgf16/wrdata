"""
Champion data collection and processing module.

This module provides a high-level orchestrator for the automated collection,
processing, and analysis of champion data from a web source. It coordinates
between various services to handle web scraping, data processing, and output
generation.
"""

from ..adapters.readers.reader_factory import ChampionReaderFactory
from ..adapters.service import OutputService
from ..data import main as run_data_pipeline
from ..domain.data_processor import DataProcessor
from ..domain.models.analyzed_champion import AnalyzedChampion
from ..exceptions import DataProcessingError, OutputError, ScrapingError


def process_champions() -> None:
    """Process and save champion data from the source.

    This function orchestrates the complete workflow of champion data
    processing:
    1. Runs the data pipeline to scrape and save champions to CSV
    2. Reads champion data using the configured reader (CSV or Excel)
    3. Updates metrics for each tier of champions
    4. Saves the processed data to an Excel file

    The reader type is determined by the application settings. Champions
    are processed in tiers, and their metrics are updated based on their
    respective lanes. The final data is written to an Excel file using the
    available writers.

    Raises:
        ScrapingError: If there are issues fetching data from the source
        DataProcessingError: If there are issues processing the champion data
        OutputError: If there are issues writing the output file
    """
    # Use factory to create reader based on configuration
    champion_reader = ChampionReaderFactory.create_reader()
    data_processor = DataProcessor()
    output_service = OutputService()

    try:
        run_data_pipeline()
    except Exception as e:
        raise ScrapingError(
            "Failed to fetch champion data from source", details=str(e)
        ) from e

    try:
        champions_by_tier = champion_reader.read()
    except Exception as e:
        raise ScrapingError(
            "Failed to read champion data from CSV", details=str(e)
        ) from e

    try:
        champions_with_metrics: list[list[AnalyzedChampion]] = []
        for tier_champions in champions_by_tier:
            tier_data = data_processor.update_metrics(tier_champions)
            champions_with_metrics.append(tier_data)
    except Exception as e:
        raise DataProcessingError(
            "Failed to process champion metrics", details=str(e)
        ) from e

    try:
        output_service.write_champions(champions_with_metrics)
    except Exception as e:
        raise OutputError(
            "Failed to write champion data to output file", details=str(e)
        ) from e
