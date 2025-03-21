"""
Main module for the WRData project.

This module serves as the entry point for the WRData application, which
processes and collects champion data. It provides a simple interface to
initiate the data collection process.
"""

from .src.champion_data_collector import process_champions


def main() -> None:
    """
    Main entry point for the WRData application.
    """
    process_champions()


if __name__ == "__main__":
    main()
