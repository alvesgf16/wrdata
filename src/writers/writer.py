"""
Writer module for champion data output.

This module provides an abstract base class for writing champion data to
different file formats. It defines the common interface and functionality
for data writers, including file path handling and data structure
definitions.
"""

from abc import ABC, abstractmethod
from pathlib import Path

from ..models.champion import Champion
from ..config.settings import settings


class Writer(ABC):
    """Abstract base class for writing champion data to files.

    This class defines the interface and common functionality for writing
    champion data to different file formats. It provides methods for
    handling file paths and defines the structure of the output data.

    Methods:
    ---
    write():
        Write champion data to a file.
    """

    def __init__(
        self, output_file_name: str = settings.output.default_filename
    ) -> None:
        """Initialize the writer with default tier names and headers.

        Sets up the writer with predefined tier names and column headers
        for the champion data output. The headers define the structure
        of the output data, including lane, champion name, various rates,
        and tier classification.
        """
        self._output_file_name = output_file_name
        self._tiers = ["Diamond", "Master", "Challenger", "Legendary"]
        self._headers = [
            "Lane",
            "Champion",
            "Win Rate",
            "Pick Rate",
            "Ban Rate",
            "Adjusted Win Rate",
            "Tier",
        ]

    @abstractmethod
    def write(self, data: list[list[Champion]]) -> None:
        """Write champion data to a file.

        This abstract method must be implemented by concrete writer
        classes to write the champion data to a specific file format.
        The data is organized as a list of lists, where each inner list
        contains champions from a specific tier.

        Args:
            data (list[list[Champion]]): The champion data to write,
                organized by tiers.
        """
        pass

    def _create_output_file(self, tier: str = "") -> Path:
        """Create and prepare the output file path.

        This method constructs the output file path based on the tier
        name and ensures the output directory exists. If a tier is
        specified, it's appended to the filename.

        Args:
            tier (str, optional): The tier name to append to the
                filename. Defaults to an empty string.

        Returns:
            Path: The Path object representing the output file location.
        """
        output_file = (
            Path("res", f"{self._output_file_name}_{tier.lower()}")
            if tier
            else Path("res", self._output_file_name)
        )
        output_file.parent.mkdir(parents=True, exist_ok=True)
        return output_file
