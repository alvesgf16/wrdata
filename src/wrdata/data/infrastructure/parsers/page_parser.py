"""
Web page parser module for champion data extraction.

This module provides functionality for parsing champion data from web pages
using Selenium WebDriver. It handles the extraction of champion information
across different tiers and lanes, providing structured data for further
analysis.
"""

from __future__ import annotations

from typing import cast

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from ....config.settings import settings
from ....exceptions import ScrapingError
from ...domain import Champion
from .list_item_parser import ListItemParser


class PageParser:
    """A class to parse web page data related to champions.

    Methods:
    ---
    parse_champions():
        Retrieve a list of Champion objects by processing lane buttons.
    """

    def __init__(
        self,
        a_driver: WebDriver,
        a_button: WebElement | None = None,
        a_tier: str | None = None,
    ):
        """Initialize a new instance of the PageParser.

        This constructor takes a WebDriver instance and an optional WebElement
        for a button. If the button is provided, it performs a click action on
        it using ActionChains.

        Args:
            a_driver (WebDriver): The WebDriver instance to control the
                browser.
            a_button (WebElement, optional): The WebElement representing the
                button to click. Defaults to None.
            a_tier (str, optional): The tier name for champions being parsed.
                Defaults to None.
        """
        self.__driver = a_driver
        self.__button = a_button
        self.__tier = a_tier

        if a_button is not None:
            ActionChains(a_driver).click(a_button).perform()

    def parse_champions(self) -> list[list[Champion]]:
        """Retrieve champion data organized by tiers.

        This method processes the page by iterating through tier buttons and
        collecting champion data for each tier. The data is organized as a
        list of lists, where each inner list contains champions from a
        specific tier.

        Returns:
            list[list[Champion]]: A list of lists containing Champion objects,
                organized by tier.

        Raises:
            ScrapingError: If there are issues parsing champion data from
                the page
        """
        try:
            data: list[list[Champion]] = []
            tier_buttons = self.__get_tier_buttons()
            for tier_button in tier_buttons:
                tier_name = self.__parse_tier_name_from_button(tier_button)
                tier_champions = self.__with_button_to_click(
                    self.__driver, tier_button, tier_name
                ).__parse_champions_from_tier()
                data.append(tier_champions)
            print(f"Data parsed for date {self.__get_date()}")
            return data
        except NoSuchElementException as e:
            raise ScrapingError(
                "Failed to find required elements on the page", details=str(e)
            ) from e
        except Exception as e:
            raise ScrapingError(
                "Failed to parse champions from page", details=str(e)
            ) from e

    def __get_date(self) -> str:
        """Retrieve the date from the data-time element.

        Returns:
            str: The date string extracted from the data-time element.
        """
        return str(
            self.__driver.find_element(By.ID, "data-time").get_attribute(
                "innerHTML"
            )
        )

    def __get_tier_buttons(self) -> list[WebElement]:
        """Retrieve tier button elements from the web page.

        Returns:
            list[WebElement]: A list of WebElement objects corresponding to
                the tier buttons found.
        """
        return self.__driver.find_element(
            By.CLASS_NAME, "dan-btn-box"
        ).find_elements(By.TAG_NAME, "a")

    def __parse_champions_from_tier(self) -> list[Champion]:
        """Retrieve champion data for a specific tier.

        Returns:
            list[Champion]: A list of Champion objects parsed from all lanes
                in the current tier.
        """
        data = []
        tier = cast(str, self.__tier)
        for lane_button in self.__get_lane_buttons():
            data.extend(
                self.__with_button_to_click(
                    self.__driver, lane_button, tier
                ).__parse_champions_from_lane()
            )
        return data

    def __get_lane_buttons(self) -> list[WebElement]:
        """Retrieve lane button elements from the web page.

        Returns:
            list[WebElement]: A list of WebElement objects corresponding to
                the lane buttons found.
        """
        return self.__driver.find_element(
            By.CLASS_NAME, "place-content"
        ).find_elements(By.TAG_NAME, "a")

    def __parse_champions_from_lane(self) -> list[Champion]:
        """Generate champion data for a specific lane.

        Returns:
            list[Champion]: A list of Champion objects parsed from the current
                lane's data.
        """
        lane_name = self.__parse_lane_name_from_button()
        tier = cast(str, self.__tier)
        champions = []
        for list_item in self.__get_data_list_items():
            try:
                champion = ListItemParser(
                    lane_name, list_item, tier
                ).parse_champion()
                champions.append(champion)
            except (NoSuchElementException, ScrapingError):
                continue
        return champions

    def __parse_lane_name_from_button(self) -> str:
        """Extract and format the lane name from the button's class attribute.

        Returns:
            str: The formatted lane name extracted from the lane button's
                class attribute.
        """
        lane_button = cast(WebElement, self.__button)
        lane_button_class_list = cast(str, lane_button.get_attribute("class"))
        lane_button_class = lane_button_class_list.split()[0]
        prefix_length = len(settings.scraping.lane_element_class_prefix)

        return lane_button_class[prefix_length:].capitalize()

    def __parse_tier_name_from_button(self, tier_button: WebElement) -> str:
        """Extract the tier name from the tier button.

        Args:
            tier_button: The WebElement representing the tier button.

        Returns:
            str: The tier name extracted from the button text.
        """
        tier_text = str(tier_button.get_attribute("innerHTML"))
        return tier_text.strip()

    def __get_data_list_items(self) -> list[WebElement]:
        """Retrieve list items from the data list container.

        Returns:
            list[WebElement]: A list of WebElement items found within the
                data list container.
        """
        return self.__driver.find_element(
            By.CLASS_NAME, "data-list"
        ).find_elements(By.TAG_NAME, "li")

    @classmethod
    def __with_button_to_click(
        cls, a_driver: WebDriver, a_button: WebElement, a_tier: str
    ) -> PageParser:
        """Create a new PageParser instance with a button to click.

        This class method provides a convenient way to create a PageParser
        instance that will click a specific button during initialization.

        Args:
            a_driver (WebDriver): The WebDriver instance to control the
                browser.
            a_button (WebElement): The WebElement representing the button to
                click.
            a_tier (str): The tier name for champions being parsed.

        Returns:
            PageParser: A new instance of the PageParser class with the
                specified WebDriver and button to click.
        """
        return cls(a_driver, a_button, a_tier)
