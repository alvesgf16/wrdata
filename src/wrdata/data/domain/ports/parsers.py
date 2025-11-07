"""Outbound port for champion parsing."""

from abc import ABC, abstractmethod
from typing import Any

from ..models.champion import Champion


class ChampionParser(ABC):
    """Defines contract for parsing champion data.

    This is an outbound port - it defines what the application needs
    from champion parsing infrastructure.
    """

    @abstractmethod
    def parse(self, source: Any) -> list[list[Champion]]:
        """Parse champions from the data source.

        Args:
            source: The raw data source (WebDriver, HTML, JSON, etc.)

        Returns:
            Champions organized by tier, where each inner list contains
            champions from a specific tier
        """
        pass
