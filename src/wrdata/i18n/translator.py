"""Translation service for game content localization."""

from typing import Dict, Optional

from .mappings.champions import CHAMPIONS
from .mappings.game_terms import HEADERS, LANES, TIERS


class GameTranslator:
    """Translates game-related content from Chinese to English."""

    def __init__(self) -> None:
        """Initialize the translator with all mapping dictionaries."""
        self._champions = CHAMPIONS
        self._tiers = TIERS
        self._lanes = LANES
        self._headers = HEADERS

    def translate_champion(self, chinese_name: str) -> Optional[str]:
        """Translate a champion name from Chinese to English.

        Args:
            chinese_name: The Chinese champion name

        Returns:
            The English champion name, or None if not found
        """
        return self._champions.get(chinese_name)

    def translate_tier(self, chinese_tier: str) -> Optional[str]:
        """Translate a tier name from Chinese to English.

        Args:
            chinese_tier: The Chinese tier name

        Returns:
            The English tier name, or None if not found
        """
        return self._tiers.get(chinese_tier)

    def translate_lane(self, chinese_lane: str) -> Optional[str]:
        """Translate a lane name from Chinese to English.

        Args:
            chinese_lane: The Chinese lane name

        Returns:
            The English lane name, or None if not found
        """
        return self._lanes.get(chinese_lane)

    def translate_header(self, chinese_header: str) -> Optional[str]:
        """Translate a table header from Chinese to English.

        Args:
            chinese_header: The Chinese header text

        Returns:
            The English header text, or None if not found
        """
        return self._headers.get(chinese_header)

    @property
    def champion_mapping(self) -> Dict[str, str]:
        """Get the complete champion name mapping dictionary."""
        return self._champions.copy()


# Global translator instance for convenience
translator = GameTranslator()
