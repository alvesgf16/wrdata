"""
Tests for the PageParser class.
"""

from unittest.mock import Mock, patch

from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webelement import WebElement

from src.wrdata.data.domain.models.champion import Champion, Lane
from src.wrdata.data.infrastructure.parsers.page_parser import PageParser


def test_page_parser_initialization(
    mock_driver: Mock, mock_lane_button: Mock
) -> None:
    """Test PageParser initialization."""
    with patch.object(ActionChains, "click") as mock_click:
        mock_click.return_value.perform.return_value = None
        PageParser(mock_driver, mock_lane_button)
        mock_click.assert_called_once()


def test_parse_champions(
    mock_driver: Mock, mock_lane_button: Mock, mock_list_items: Mock
) -> None:
    """Test parsing champions from page."""
    # Mock lane buttons
    content_element = Mock(spec=WebElement)
    content_element.find_elements.return_value = [mock_lane_button]
    mock_driver.find_element.return_value = content_element

    # Mock data list
    data_list = Mock(spec=WebElement)
    data_list.find_elements.return_value = mock_list_items
    mock_driver.find_element.return_value = data_list

    # Set up the lane button's class attribute
    mock_lane_button.get_attribute.return_value = "lane-button Top"

    parser = PageParser(mock_driver)
    with patch(
        "src.wrdata.data.infrastructure.parsers.page_parser.PageParser"
        "._PageParser__parse_lane_name_from_button",
        return_value=Lane.TOP,
    ):
        champions_by_tier = parser.parse_champions()
        champions = champions_by_tier[0]  # Get champions from first tier

        assert len(champions) > 0
        assert all(isinstance(champ, Champion) for champ in champions)
        assert champions[0].lane == Lane.TOP
