"""
Base repository implementation with shared functionality.

This module provides an abstract base class that implements common
functionality for file-based champion repositories.
"""

from abc import ABC
from pathlib import Path

from ...domain import Champion
from ...domain.ports.repositories import ChampionRepository


class BaseChampionRepository(ChampionRepository, ABC):
    """Abstract base repository with shared functionality.

    Provides common functionality for file-based champion persistence.
    """

    def __init__(self, filepath: str) -> None:
        """Initialize the base champion repository.

        Args:
            filepath: The path where the file will be saved.
        """
        self._filepath = Path(filepath)
        self._headers = [
            "Lane",
            "Champion",
            "Win Rate",
            "Pick Rate",
            "Ban Rate",
            "Ranked Tier",
        ]

    def _serialize_champion(self, champion: Champion) -> list[str | float]:
        """Serialize a champion to row format.

        Args:
            champion: The Champion object to serialize.

        Returns:
            A list containing the champion's data fields.
        """
        return [
            champion.lane.value,
            champion.name,
            round(champion.win_rate, 4),
            round(champion.pick_rate, 4),
            round(champion.ban_rate, 4),
            champion.ranked_tier.value,
        ]

    def _ensure_directory_exists(self) -> None:
        """Ensure the parent directory for the output file exists."""
        self._filepath.parent.mkdir(parents=True, exist_ok=True)
