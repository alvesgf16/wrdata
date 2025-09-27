"""
Main module for the WRData project.

This module serves as the entry point for the WRData application, which
processes and collects champion data. It provides a simple interface to
initiate the data collection process.

The application can be run directly as a script or installed as a package
and executed using the 'wrdata' command.
"""

import sys
from pathlib import Path

# Add src to path for development usage
if __name__ == "__main__":
    src_path = Path(__file__).parent / "src"
    sys.path.insert(0, str(src_path))

from src.champion_data_collector import process_champions


def main() -> None:
    """
    Main entry point for the WRData application.

    This function initiates the champion data collection and processing
    workflow. It can be called directly or through the installed console
    script 'wrdata'.

    Returns:
        None
    """
    try:
        process_champions()
        print("✅ WRData processing completed successfully!")
    except KeyboardInterrupt:
        print("\n⚠️  Process interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error occurred during processing: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
