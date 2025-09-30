"""
Main CLI entry point for the WRData application.

This module provides a clean command-line interface for the WRData application,
which processes and collects League of Legends: Wild Rift champion data.
"""

from ..core.orchestrator import process_champions


def main() -> None:
    """
    Main entry point for the WRData application.

    This function initiates the champion data collection and processing
    workflow. It serves as the primary interface for users running the
    application from the command line.

    The function coordinates the entire data pipeline:
    1. Data fetching from web sources
    2. Data processing and analysis
    3. Output generation in multiple formats
    """
    try:
        process_champions()
        print("✅ Champion data processing completed successfully!")
    except Exception as e:
        print(f"❌ Error during data processing: {e}")
        raise


if __name__ == "__main__":
    main()
