"""
List item parser module for champion data extraction.

This module provides functionality for parsing individual champion data from
web elements. It handles the extraction of champion names and statistics
from list items, including translation from Chinese to English names.
"""

from typing import cast

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from ....exceptions import ScrapingError
from ....i18n.translator import translator
from ...domain import Champion, Lane, RankedTier


class ListItemParser:
    """A class to parse champion data from web elements.

    Methods:
    ---
    parse_champion():
        Create a Champion object from parsed champion details.
    """

    def __init__(self, a_lane_name: str, a_list_item: WebElement, a_tier: str):
        """Initialize the champion parser.

        Args:
            a_lane_name (str): The name of the lane associated with the
                champion.
            a_list_item (WebElement): The web element containing the champion's
                data.
            a_tier (str): The tier classification for the champion.
        """
        self.__lane = Lane(a_lane_name)
        self.__list_item = a_list_item
        self.__tier = a_tier

    def parse_champion(self) -> Champion:
        """Create a Champion object from parsed champion details.

        This method orchestrates the parsing of champion data by extracting
        the champion name and statistics from the web element. It combines
        all the parsed information into a single Champion object.

        Returns:
            Champion: An instance of the Champion class containing the
                parsed details including lane, name, win rate, pick rate,
                and ban rate.

        Raises:
            ScrapingError: If there are issues parsing champion data from
                the web element
        """
        try:
            champion_name = self.__parse_champion_name()
            win_rate, pick_rate, ban_rate = self.__parse_champion_stats()
            ranked_tier = self.__parse_ranked_tier()

            return Champion(
                self.__lane,
                champion_name,
                win_rate,
                pick_rate,
                ban_rate,
                ranked_tier,
            )
        except KeyError as e:
            raise ScrapingError(
                f"Failed to translate champion name: {e}",
                details="Champion name not found in translation dictionary",
            ) from e
        except Exception as e:
            raise ScrapingError(
                "Failed to parse champion data from web element",
                details=str(e),
            ) from e

    def __parse_champion_name(self) -> str:
        """Parse the champion's name from a web element.

        This method extracts the champion's name from the hero-name element
        and translates it from Chinese to English using the translation
        dictionary.

        Returns:
            str: The English translation of the champion's Chinese name.
        """
        name_element = self.__list_item.find_element(
            By.CLASS_NAME, "hero-name"
        )
        champion_name_in_chinese = str(name_element.get_attribute("innerHTML"))
        english_name = translator.translate_champion(champion_name_in_chinese)
        if english_name is None:
            raise ScrapingError(
                f"Unknown champion name: {champion_name_in_chinese}"
            )
        return english_name

    def __parse_champion_stats(self) -> tuple[float, float, float]:
        """Parse the champion's statistics from web elements.

        This method extracts the win rate, pick rate, and ban rate from the
        last three statistics elements in the list item. Each percentage
        value is converted from a string to a float.

        Returns:
            tuple[float, float, float]: A tuple containing the win rate,
                pick rate, and ban rate as floats between 0 and 1.
        """
        stats_elements = self.__get_stats_elements()
        win_rate, pick_rate, ban_rate = [
            self.__parse_percentage_from_element(stat_element)
            for stat_element in stats_elements
        ]

        return win_rate, pick_rate, ban_rate

    def __get_stats_elements(self) -> list[WebElement]:
        """Retrieve the three statistics elements from the list item.

        This method finds all elements with class "li-div" and returns the
        last three elements, which contain the win rate, pick rate, and
        ban rate statistics.

        Returns:
            list[WebElement]: A list containing the three WebElements for
                win rate, pick rate, and ban rate statistics.
        """
        return (self.__list_item.find_elements(By.CLASS_NAME, "li-div"))[-3:]

    def __parse_percentage_from_element(
        self, a_stat_element: WebElement
    ) -> float:
        """Parse a percentage value from a web element.

        This method extracts the percentage value from the element's innerHTML,
        removes the '%' symbol, and converts the string to a float value
        between 0 and 1.

        Args:
            a_stat_element (WebElement): The web element containing the
                percentage value.

        Returns:
            float: The converted float value representing the percentage
                (between 0 and 1).
        """
        percentage_string = cast(
            str, a_stat_element.get_attribute("innerHTML")
        )
        return float(percentage_string.strip("%")) / 100

    def __parse_ranked_tier(self) -> RankedTier:
        """Parse the ranked tier from the tier string.

        Converts the tier string (e.g., "钻石+", "大师+", "超凡", "传奇")
        to the corresponding RankedTier enum value.

        Returns:
            RankedTier: The parsed ranked tier enum value.

        Raises:
            ScrapingError: If the tier string is not recognized.
        """
        # Map Chinese tier names to RankedTier enum values
        tier_mapping = {
            "钻石+": RankedTier.DIAMOND_PLUS,
            "大师+": RankedTier.MASTER_PLUS,
            "超凡": RankedTier.SOVEREIGN,
            "传奇": RankedTier.LEGENDARY,
        }

        tier = tier_mapping.get(self.__tier)
        if tier is None:
            raise ScrapingError(
                f"Unknown ranked tier: {self.__tier}",
                details="Tier name not found in mapping dictionary",
            )
        return tier
