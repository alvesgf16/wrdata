from typing import cast

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from .champion import Champion
from .chinese_english import (
    chinese_to_english_champions as translate_to_english,
)


class ListItemParser:
    """Parses champion data from web elements associated with a specific lane.

    Methods:
    ---
    parse_champion():
        Create a Champion object from parsed champion details.
    """

    def __init__(self, a_lane_name: str, a_list_item: WebElement):
        """Initialize the champion parser.

        Args:
            a_lane_name (str): The name of the lane associated with the
                champion.
            a_list_item (WebElement): The web element containing the champion's
                data.
        """
        self.__lane_name = a_lane_name
        self.__list_item = a_list_item

    def parse_champion(self) -> Champion:
        """Create a Champion object from parsed champion details.

        Returns:
            Champion: An instance of the Champion class containing the parsed
            details.
        """
        champion_name = self.__parse_champion_name()
        win_rate, pick_rate, ban_rate = self.__parse_champion_stats()

        return Champion(
            self.__lane_name,
            champion_name,
            win_rate,
            pick_rate,
            ban_rate,
        )

    def __parse_champion_name(self) -> str:
        """Parse the champion's name from a web element.

        Returns:
            str: The English translation of the champion's Chinese name.
        """
        name_element = self.__list_item.find_element(
            By.CLASS_NAME, "hero-name"
        )
        champion_name_in_chinese = str(name_element.get_attribute("innerHTML"))
        return translate_to_english[champion_name_in_chinese]

    def __parse_champion_stats(self) -> tuple[float, float, float]:
        """Parse the champion's statistics from web elements.

        Returns:
            tuple: A tuple containing the win rate, pick rate, and ban rate as
                floats.
        """
        stats_elements = self.__get_stats_elements()
        win_rate, pick_rate, ban_rate = [
            self.__parse_percentage_from_element(stat_element)
            for stat_element in stats_elements
        ]

        return win_rate, pick_rate, ban_rate

    def __get_stats_elements(self) -> list[WebElement]:
        """Retrieve the three statistics elements from the list item.

        Returns:
            list[WebElement]: A list containing the three WebElements found.
        """
        return (self.__list_item.find_elements(By.CLASS_NAME, "li-div"))[-3:]

    def __parse_percentage_from_element(
        self, a_stat_element: WebElement
    ) -> float:
        """Parse a percentage value from a web element.

        Args:
            a_stat_element (WebElement): The web element containing the
                percentage value.

        Returns:
            float: The converted float value representing the percentage.
        """
        percentage_string = cast(
            str, a_stat_element.get_attribute("innerHTML")
        )
        return float(percentage_string.strip("%")) / 100
