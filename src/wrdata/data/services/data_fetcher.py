"""
Data fetching service module for web scraping operations.

This module provides functionality for fetching champion data from web
sources using WebDriver and coordinating with parsers to extract
structured data.
"""

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from ...config.settings import settings
from ...exceptions import ScrapingError
from ..models.champion import Champion
from ..parsers.page_parser import PageParser
from ..webdriver_factory import WebDriverFactory


class DataFetcher:
    """Service for fetching champion data from web sources."""

    def __init__(self) -> None:
        """Initialize the data fetcher."""
        self._webdriver_service = WebDriverFactory()

    def fetch_champions(self) -> list[list[Champion]]:
        """Fetch champion data from the configured source URL.

        This function initializes a headless Chrome webdriver, navigates to the
        configured source URL, and waits for the page to load before parsing
        the champion data. The champions are returned as a list of lists,
        where each inner list represents a tier of champions.

        Returns:
            list[list[Champion]]: A list of lists containing Champion objects,
                organized by tier.

        Raises:
            ScrapingError: If there are issues with webdriver operations or
                page loading
        """
        try:
            with self._webdriver_service.create_driver() as driver:
                driver.get(settings.scraping.source_url)
                return self._parse_when_ready(driver)
        except ScrapingError:
            # Re-raise ScrapingError from create_driver
            raise
        except Exception as e:
            raise ScrapingError(
                "Failed to fetch champions from source URL", details=str(e)
            ) from e

    def _parse_when_ready(self, driver: WebDriver) -> list[list[Champion]]:
        """Parse champion data after the page has finished loading.

        Waits for the page to be ready by checking for the absence of a
        "nodata-text" element, then proceeds to parse the champion data from
        the page.

        Args:
            driver (WebDriver): The webdriver instance to use for page
                interaction.

        Returns:
            list[list[Champion]]: A list of lists containing Champion objects,
                organized by tier.

        Note:
            The function will attempt to parse the page even if the wait times
            out, ensuring data is collected even if the page load is slow.
        """
        try:
            WebDriverWait(driver, settings.scraping.timeout).until_not(
                EC.presence_of_element_located(("class-name", "nodata-text"))
            )
        finally:
            return PageParser(driver).parse_champions()
