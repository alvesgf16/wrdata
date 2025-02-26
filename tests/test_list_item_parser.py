import pytest
from unittest.mock import Mock
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from ..src.list_item_parser import ListItemParser
from ..src.champion import Champion


@pytest.fixture
def mock_list_item() -> Mock:
    list_item = Mock(spec=WebElement)

    # Mock hero name element
    name_element = Mock(spec=WebElement)
    name_element.get_attribute.return_value = "疾风剑豪"  # Yasuo in Chinese
    list_item.find_element.return_value = name_element

    # Mock stat elements
    stat_elements = [Mock(spec=WebElement) for _ in range(3)]
    stat_elements[0].get_attribute.return_value = "52.5%"
    stat_elements[1].get_attribute.return_value = "10.2%"
    stat_elements[2].get_attribute.return_value = "25.3%"
    list_item.find_elements.return_value = stat_elements

    return list_item


def test_parse_champion(mock_list_item: Mock) -> None:
    parser = ListItemParser("MID", mock_list_item)
    champion = parser.parse_champion()

    assert isinstance(champion, Champion)
    assert champion.lane == "MID"
    assert champion.name == "Yasuo"
    assert champion.win_rate == 0.525
    assert champion.pick_rate == 0.102
    assert champion.ban_rate == 0.253


def test_parse_champion_stats(mock_list_item: Mock) -> None:
    parser = ListItemParser("TOP", mock_list_item)
    champion = parser.parse_champion()

    # Verify the stats were parsed correctly
    assert champion.win_rate == 0.525
    assert champion.pick_rate == 0.102
    assert champion.ban_rate == 0.253

    # Verify the correct methods were called
    mock_list_item.find_elements.assert_called_once_with(
        By.CLASS_NAME, "li-div"
    )


def test_parse_champion_name(mock_list_item: Mock) -> None:
    parser = ListItemParser("JGL", mock_list_item)
    champion = parser.parse_champion()

    # Verify name parsing
    assert champion.name == "Yasuo"
    mock_list_item.find_element.assert_called_once_with(
        By.CLASS_NAME, "hero-name"
    )
