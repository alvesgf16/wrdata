"""Port interface for reading champion data from storage.

This module defines the abstract interface for champion data readers,
following the hexagonal architecture pattern. Concrete implementations
can read from CSV files, Excel files, databases, or any other storage medium.
"""

from abc import ABC, abstractmethod

from ...data import Champion


class ChampionReader(ABC):
    """Abstract interface for reading champion data.

    This port defines the contract for reading champion data from any
    storage medium. Implementations should reconstruct Champion objects
    organized by tier from their respective storage formats.
    """

    @abstractmethod
    def read(self) -> list[Champion]:
        """Read champion data from storage.

        Returns:
            A flat list of Champion objects with tier information
            stored in the ranked_tier attribute.

        Raises:
            Exception: If there are issues reading from storage
        """
        pass
