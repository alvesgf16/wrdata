import pytest
from unittest.mock import Mock, patch
from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from ..src.page_parser import PageParser
from ..src.champion import Champion


@pytest.fixture
def mock_driver() -> Mock:
    driver = Mock(spec=WebDriver)

    # Mock date element
    date_element = Mock()
    date_element.get_attribute.return_value = "2024-03-15"
    driver.find_element.return_value = date_element

    return driver


@pytest.fixture
def mock_lane_button() -> Mock:
    return Mock(spec=WebElement)


@pytest.fixture
def mock_list_items() -> list[Mock]:
    items = [Mock(spec=WebElement) for _ in range(2)]

    # Mock champion data elements
    for item in items:
        name_element = Mock()
        name_element.get_attribute.return_value = "疾风剑豪"  # Yasuo in Chinese
        item.find_element.return_value = name_element

        stat_elements = [Mock() for _ in range(3)]
        stat_elements[0].get_attribute.return_value = "52.5%"
        stat_elements[1].get_attribute.return_value = "10.2%"
        stat_elements[2].get_attribute.return_value = "25.3%"
        item.find_elements.return_value = stat_elements

    return items


def test_page_parser_initialization(
    mock_driver: Mock, mock_lane_button: Mock
) -> None:
    with patch.object(ActionChains, "click") as mock_click:
        mock_click.return_value.perform.return_value = None
        PageParser(mock_driver, mock_lane_button)
        mock_click.assert_called_once()


def test_parse_champions(
    mock_driver: Mock, mock_lane_button: Mock, mock_list_items: Mock
) -> None:
    # Mock lane buttons
    content_element = Mock(spec=WebElement)
    content_element.find_elements.return_value = [mock_lane_button]
    mock_driver.find_element.return_value = content_element

    # Mock data list
    data_list = Mock(spec=WebElement)
    data_list.find_elements.return_value = mock_list_items
    mock_driver.find_element.return_value = data_list

    parser = PageParser(mock_driver)
    with patch(
        "wrdata.src.page_parser.PageParser._PageParser__parse_lane_name_from_button",
        return_value="Top",
    ):
        champions = parser.parse_champions()

        assert len(champions) > 0
        assert all(isinstance(champ, Champion) for champ in champions)
        assert champions[0].lane == "Top"
