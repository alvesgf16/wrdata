from __future__ import annotations

from typing import cast

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from .champion import Champion
from .list_item_parser import ListItemParser
from .constants import LANE_ELEMENT_CLASS_PREFIX


class PageParser:
    """A class to parse web page data related to champions.

    Methods:
    ---
    parse_champions():
        Retrieve a list of Champion objects by processing lane buttons.
    """

    def __init__(
        self, a_driver: WebDriver, a_lane_button: WebElement | None = None
    ):
        """Initialize a new instance of the class.

        This constructor takes a WebDriver instance and an optional WebElement
        for a lane button. If the lane button is provided, it performs a click
        action on it using ActionChains.

        Args:
            a_driver (WebDriver): The WebDriver instance to control the
                browser.
            a_lane_button (WebElement, optional): The WebElement representing
                the lane button to click. Defaults to None.
        """
        self.__driver = a_driver
        self.__lane_button = a_lane_button

        if a_lane_button is not None:
            ActionChains(a_driver).click(a_lane_button).perform()

    def parse_champions(self) -> list[Champion]:
        """Retrieve a list of Champion objects by processing lane buttons.

        This method collects lane buttons and uses them to create instances of
        NewClass, which are then parsed to extract Champion data. It is
        designed to aggregate Champion information from multiple lanes
        into a single list.

        Returns:
            list[Champion]: A list of Champion objects parsed from the lanes.
        """
        data = []
        for lane_button in self.__get_lane_buttons():
            data.extend(
                self.__with_button_to_click(
                    self.__driver, lane_button
                ).__parse_champions_from_lane()
            )
        print(f"Data parsed for date {self.__get_date()}")
        return data

    def __get_date(self) -> str:
        return str(
            self.__driver.find_element(By.ID, "data-time").get_attribute(
                "innerHTML"
            )
        )

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
        """Generate a list of Champion objects based on parsed lane data.

        Returns:
            list[Champion]: A list of Champion objects parsed from the data.
        """
        lane_name = self.__parse_lane_name_from_button()
        return [
            ListItemParser(lane_name, list_item).parse_champion()
            for list_item in self.__get_data_list_items()
        ]

    def __parse_lane_name_from_button(self) -> str:
        """Format the lane name extracted from the lane button's class
        attribute.

        Returns:
            str: The formatted lane name extracted from the lane button's
            class attribute.
        """
        lane_button = cast(WebElement, self.__lane_button)
        lane_button_class_list = cast(str, lane_button.get_attribute("class"))
        lane_button_class = lane_button_class_list.split()[0]
        prefix_length = len(LANE_ELEMENT_CLASS_PREFIX)

        return lane_button_class[prefix_length:].capitalize()

    def __get_data_list_items(self) -> list[WebElement]:
        """Retrieve a list of WebElement items from a data list in the web
            page.

        Returns:
            list[WebElement]: A list of WebElement items found within the data
                list.
        """
        return self.__driver.find_element(
            By.CLASS_NAME, "data-list"
        ).find_elements(By.TAG_NAME, "li")

    @classmethod
    def __with_button_to_click(
        cls, a_driver: WebDriver, a_lane_button: WebElement
    ) -> PageParser:
        """Create a new instance of the class with a lane button to click.

        This class method simplifies creating a class instance for immediate
        lane button clicks. It directly passes the WebDriver and lane button
        WebElement to the constructor, which handles the click action.

        Args:
            a_driver (WebDriver): The WebDriver instance to control the
                browser.
            a_lane_button (WebElement): The WebElement representing the lane
                button to click.

        Returns:
            NewClass: A new instance of the class with the specified WebDriver
                and lane button.
        """
        return cls(a_driver, a_lane_button)
