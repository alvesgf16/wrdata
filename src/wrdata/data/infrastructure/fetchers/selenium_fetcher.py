"""
Selenium-based web fetcher implementation.

This module provides a concrete implementation of the WebFetcher port
using Selenium WebDriver for web scraping operations.
"""

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from ....config.settings import settings
from ....exceptions import ScrapingError
from ...domain.ports.fetchers import WebFetcher
from .webdriver_factory import WebDriverFactory


class SeleniumFetcher(WebFetcher):
    """Selenium-based implementation of the WebFetcher port."""

    def __init__(self) -> None:
        """Initialize the Selenium fetcher."""
        self._driver: WebDriver | None = None
        self._webdriver_factory = WebDriverFactory()

    def fetch(self, url: str) -> str:
        """Fetch the HTML content from the specified URL.

        Args:
            url: The URL to fetch content from.

        Returns:
            The HTML page source as a string.

        Raises:
            ScrapingError: If there are issues with webdriver operations or
                page loading.
        """
        try:
            if self._driver is None:
                self._driver = self._webdriver_factory.create_driver()

            self._driver.get(url)
            self._wait_for_page_ready()
            return self._driver.page_source

        except ScrapingError:
            raise
        except Exception as e:
            raise ScrapingError(
                f"Failed to fetch content from {url}", details=str(e)
            ) from e

    def _wait_for_page_ready(self) -> None:
        """Wait for the page to be ready by checking for loading indicators.

        Waits for the absence of a "nodata-text" element, which indicates
        the page has finished loading.

        Note:
            The function will continue even if the wait times out, ensuring
            data is collected even if the page load is slow.
        """
        if self._driver is None:
            return

        try:
            WebDriverWait(self._driver, settings.scraping.timeout).until_not(
                EC.presence_of_element_located(("class-name", "nodata-text"))
            )
        except Exception:
            pass

    def close(self) -> None:
        """Close the WebDriver and clean up resources."""
        if self._driver is not None:
            try:
                self._driver.quit()
            finally:
                self._driver = None
