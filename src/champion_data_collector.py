import csv
from itertools import groupby
from operator import attrgetter
from pathlib import Path

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from .champion import Champion
from .constants import OUTPUT_FILE_NAME, SOURCE_URL
from .page_parser import PageParser
from .champions_analyzer import ChampionsAnalyzer


def process_champions() -> None:
    """Processes champion data by fetching, updating, and saving it."""
    raw_champions = fetch_champions()
    updated_champions = update_metrics(raw_champions)
    write_to_csv(updated_champions)


def fetch_champions() -> list[Champion]:
    """Fetches champion data from a specified source URL.

    Returns:
        list[Champion]: A list of Champion objects parsed from the source URL.
    """
    with create_driver() as driver:
        driver.get(SOURCE_URL)
        return parse_when_ready(driver)


def create_driver() -> WebDriver:
    """Creates and returns a headless Chrome webdriver instance.

    This function sets up a Chrome webdriver with various options,
    including headless mode, for automated web scraping.

    Returns:
        WebDriver: A configured headless Chrome webdriver.
    """
    chrome_service = Service(
        ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
    )

    chrome_options = Options()
    options = [
        "--headless",
        "--disable-gpu",
        "--window-size=1920,1200",
        "--ignore-certificate-errors",
        "--disable-extensions",
        "--no-sandbox",
        "--disable-dev-shm-usage",
    ]

    for option in options:
        chrome_options.add_argument(option)
    return webdriver.Chrome(service=chrome_service, options=chrome_options)


def parse_when_ready(a_driver: WebDriver) -> list[Champion]:
    """Waits for the absence of a specific element in the web driver before
    parsing champion data.

    This function uses a WebDriver to confirm that a specific element
    indicating no data is absent. It then proceeds to parse and return a list
    of champions from the page.

    Args:
        a_driver (WebDriver): The web driver instance used to interact with
            the web page.

    Returns:
        list[Champion]: A list of Champion objects parsed from the web page.
    """
    try:
        WebDriverWait(a_driver, 10).until_not(
            EC.presence_of_element_located(("class-name", "nodata-text"))
        )
    finally:
        return PageParser(a_driver).parse_champions()


def update_metrics(data: list[Champion]) -> list[Champion]:
    """Update metrics for a list of champions based on lane grouping.

    This function groups the provided list of Champion objects by their lane
    attribute, analyzes each group using the ChampionsAnalyzer, and returns a
    consolidated list of champions with updated metrics.

    Args:
        data (list[Champion]): A list of Champion objects to be processed.

    Returns:
        list[Champion]: A list of champions with updated metrics after
            analysis.
    """
    result = []
    for _, champions_iterator in groupby(data, attrgetter("lane")):
        result.extend(ChampionsAnalyzer(champions_iterator).update_metrics())
    return result


def write_to_csv(data: list[Champion]) -> None:
    """Writes champion data to a CSV file.


    Args:
        data (list[Champion]): A list of Champion objects to be converted to
            CSV format.
    """
    csv_data = [champion.to_csv_row() for champion in data]

    with open(
        Path("res", OUTPUT_FILE_NAME), "w+", encoding="utf-8", newline=""
    ) as csv_file:
        headers = [
            "Lane",
            "Champion",
            "Win Rate",
            "Pick Rate",
            "Ban Rate",
            "Adjusted Win Rate",
            "Tier",
        ]

        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(headers)
        csv_writer.writerows(csv_data)
