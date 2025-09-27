"""
Champion data collection and processing module.

This module handles the automated collection, processing, and analysis of
champion data from a web source. It provides functionality for web scraping
champion information, processing the data, and updating various metrics for
different champion tiers and lanes.
"""

from itertools import groupby
from operator import attrgetter

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from .champions_analyzer import ChampionsAnalyzer
from .config.settings import settings
from .models.champion import Champion
from .parsers.page_parser import PageParser

# from .writers.csv_writer import CsvWriter
from .writers.xlsx_writer import XlsxWriter


def process_champions() -> None:
    """Process and save champion data from the source.

    This function orchestrates the complete workflow of champion data
    processing:
    1. Fetches champion data from the source URL
    2. Updates metrics for each tier of champions
    3. Saves the processed data to an Excel file

    The champions are processed in tiers, and their metrics are updated
    based on their respective lanes. The final data is written to an Excel
    file using the XlsxWriter.
    """
    champions_by_tier = fetch_champions()

    champions_with_metrics: list[list[Champion]] = []
    for tier_champions in champions_by_tier:
        tier_data = update_metrics(tier_champions)
        champions_with_metrics.append(tier_data)

    XlsxWriter().write(champions_with_metrics)
    # CsvWriter().write(champions_with_metrics)


def fetch_champions() -> list[list[Champion]]:
    """Fetch champion data from the configured source URL.

    This function initializes a headless Chrome webdriver, navigates to the
    configured source URL, and waits for the page to load before parsing the
    champion data. The champions are returned as a list of lists, where each
    inner list represents a tier of champions.

    Returns:
        list[list[Champion]]: A list of lists containing Champion objects,
            organized by tier.
    """
    with create_driver() as driver:
        driver.get(settings.scraping.source_url)
        return parse_when_ready(driver)


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
    """
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
    return webdriver.Chrome(service=chrome_service, options=chrome_options)


def parse_when_ready(a_driver: WebDriver) -> list[list[Champion]]:
    """Parse champion data after the page has finished loading.

    Waits for the page to be ready by checking for the absence of a
    "nodata-text" element, then proceeds to parse the champion data from
    the page.

    Args:
        a_driver (WebDriver): The webdriver instance to use for page
            interaction.

    Returns:
        list[list[Champion]]: A list of lists containing Champion objects,
            organized by tier.

    Note:
        The function will attempt to parse the page even if the wait times
        out, ensuring data is collected even if the page load is slow.
    """
    try:
        WebDriverWait(a_driver, settings.scraping.timeout).until_not(
            EC.presence_of_element_located(("class-name", "nodata-text"))
        )
    finally:
        return PageParser(a_driver).parse_champions()


def update_metrics(data: list[Champion]) -> list[Champion]:
    """Update metrics for champions grouped by their lane.

    Processes a list of champions by grouping them by lane and analyzing
    each group using the ChampionsAnalyzer. This ensures that metrics are
    calculated appropriately within the context of each lane.

    Args:
        data (list[Champion]): A list of Champion objects to process.

    Returns:
        list[Champion]: The processed list of champions with updated
            metrics.
    """
    result: list[Champion] = []
    for _, champions_iterator in groupby(data, attrgetter("lane")):
        result.extend(ChampionsAnalyzer(champions_iterator).update_metrics())
    return result
