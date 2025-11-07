"""Outbound port for web fetching."""

from abc import ABC, abstractmethod
from typing import Any


class WebFetcher(ABC):
    """Defines contract for fetching web data.

    This is an outbound port - it defines what the application needs
    from external web fetching infrastructure.
    """

    @abstractmethod
    def fetch(self, url: str) -> Any:
        """Fetch web page from the given URL.

        Args:
            url: The URL to fetch

        Returns:
            The fetched page data (WebDriver, HTML string, or other
            representation depending on the implementation)
        """
        pass

    @abstractmethod
    def close(self) -> None:
        """Clean up resources (close browser, connections, etc.)."""
        pass
