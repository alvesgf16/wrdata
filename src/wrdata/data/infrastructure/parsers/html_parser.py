"""
HTML-based champion parser implementation.

This module provides a concrete implementation of the ChampionParser port
using Selenium WebDriver and the existing PageParser infrastructure.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from ....config.settings import settings
from ...domain import Champion
from ...domain.ports.parsers import ChampionParser
from ..fetchers.webdriver_factory import WebDriverFactory
from .page_parser import PageParser


class HTMLChampionParser(ChampionParser):
    """HTML-based implementation of the ChampionParser port."""

    def __init__(self) -> None:
        """Initialize the HTML champion parser."""
        self._webdriver_factory = WebDriverFactory()

    def parse(self, source: str) -> list[Champion]:
        """Parse champion data from URL or HTML source.

        This implementation uses a WebDriver to load and interact with the
        content. If the source is a URL (starts with http), it loads the URL
        directly. Otherwise, it treats it as HTML content.

        Args:
            source: The URL or HTML source code to parse.

        Returns:
            A flat list of Champion objects.

        Raises:
            ScrapingError: If there are issues parsing the content.
        """
        driver: WebDriver | None = None
        try:
            driver = self._webdriver_factory.create_driver()

            # If source is a URL, load it directly; otherwise load as HTML
            if source.startswith(("http://", "https://")):
                driver.get(source)
                # Wait for the page to be ready
                self._wait_for_page_ready(driver)
            else:
                self.load_html_source_into_driver(source, driver)

            return PageParser(driver).parse_champions()
        finally:
            if driver is not None:
                driver.quit()

    def _wait_for_page_ready(self, driver: WebDriver) -> None:
        """Wait for the page to be ready by checking for key elements.

        Args:
            driver: The WebDriver instance.
        """
        try:
            WebDriverWait(driver, settings.scraping.timeout).until(
                EC.presence_of_element_located((By.CLASS_NAME, "dan-btn-box"))
            )
        except Exception:
            # Continue even if wait times out
            pass

    def load_html_source_into_driver(
        self, source: str, driver: WebDriver
    ) -> None:
        """Load HTML source into the WebDriver and wait for it to be ready.

        Args:
            source: The HTML source code to load.
            driver: The WebDriver instance to load the HTML into.
        """
        driver.get("data:text/html;charset=utf-8," + source)
        # Wait for the page to be ready by checking for the dan-btn-box element
        try:
            WebDriverWait(driver, settings.scraping.timeout).until(
                EC.presence_of_element_located((By.CLASS_NAME, "dan-btn-box"))
            )
        except Exception:
            # Continue even if wait times out
            pass
