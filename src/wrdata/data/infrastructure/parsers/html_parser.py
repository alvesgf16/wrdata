"""
HTML-based champion parser implementation.

This module provides a concrete implementation of the ChampionParser port
using Selenium WebDriver and the existing PageParser infrastructure.
"""

from selenium.webdriver.remote.webdriver import WebDriver

from ...domain.models.champion import Champion
from ...domain.ports.parsers import ChampionParser
from ..fetchers.webdriver_factory import WebDriverFactory
from .page_parser import PageParser


class HTMLChampionParser(ChampionParser):
    """HTML-based implementation of the ChampionParser port."""

    def __init__(self) -> None:
        """Initialize the HTML champion parser."""
        self._webdriver_factory = WebDriverFactory()

    def parse(self, source: str) -> list[list[Champion]]:
        """Parse champion data from HTML source.

        This implementation uses a WebDriver to load and interact with the
        HTML content, leveraging the existing PageParser infrastructure.

        Args:
            source: The HTML source code to parse.

        Returns:
            A list of lists containing Champion objects, organized by tier.

        Raises:
            ScrapingError: If there are issues parsing the HTML content.
        """
        driver: WebDriver | None = None
        try:
            driver = self._webdriver_factory.create_driver()
            # Load the HTML source into the driver
            driver.get("data:text/html;charset=utf-8," + source)
            return PageParser(driver).parse_champions()
        finally:
            if driver is not None:
                driver.quit()
