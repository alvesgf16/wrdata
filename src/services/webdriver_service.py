"""
WebDriver service module for browser automation.

This module provides functionality for creating and managing WebDriver
instances with proper configuration for web scraping operations.
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager

from ..config.settings import settings
from ..exceptions import ScrapingError


class WebDriverService:
    """Service for creating and managing WebDriver instances."""

    @staticmethod
    def create_driver() -> WebDriver:
        """Create and configure a headless Chrome webdriver instance.

        Sets up a Chrome webdriver with various options optimized for web
        scraping:
        - Headless mode for running without a GUI
        - Disabled GPU acceleration
        - Set window size for consistent rendering
        - Disabled certificate verification
        - Disabled extensions
        - Disabled sandbox and shared memory usage

        Returns:
            WebDriver: A configured headless Chrome webdriver instance.

        Raises:
            ScrapingError: If there are issues creating or configuring the
                webdriver
        """
        try:
            chrome_service = Service(ChromeDriverManager().install())

            chrome_options = Options()
            width, height = settings.scraping.window_size
            window_size = f"--window-size={width},{height}"

            options = [
                "--disable-gpu",
                window_size,
                "--ignore-certificate-errors",
                "--disable-extensions",
                "--no-sandbox",
                "--disable-dev-shm-usage",
            ]

            if settings.scraping.headless:
                options.insert(0, "--headless")

            for option in options:
                chrome_options.add_argument(option)
            return webdriver.Chrome(
                service=chrome_service, options=chrome_options
            )

        except Exception as e:
            raise ScrapingError(
                "Failed to create Chrome webdriver instance", details=str(e)
            ) from e