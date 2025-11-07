"""Inbound port for application handlers."""

from abc import ABC, abstractmethod


class ChampionPipeline(ABC):
    """Defines what the application can do.

    This is the inbound port - it defines the use case that external
    actors can trigger.
    """

    @abstractmethod
    def run(self) -> None:
        """Execute the champion data pipeline: fetch → parse → save."""
        pass
