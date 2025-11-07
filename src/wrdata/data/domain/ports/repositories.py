"""Outbound port for champion persistence."""

from abc import ABC, abstractmethod

from ..models.champion import Champion


class ChampionRepository(ABC):
    """Defines contract for persisting champion data.

    This is an outbound port - it defines what the application needs
    from persistence infrastructure.
    """

    @abstractmethod
    def save(self, champions: list[list[Champion]]) -> None:
        """Save champions to persistent storage.

        Args:
            champions: Champions organized by tier, where each inner list
                contains champions from a specific tier
        """
        pass
