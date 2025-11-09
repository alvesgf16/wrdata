"""
Tests for the PageParser class.
"""

from unittest.mock import Mock, patch

from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webelement import WebElement

from src.wrdata.data import Champion, Lane
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
    # Mock tier button
    mock_tier_button = Mock(spec=WebElement)
    mock_tier_button.get_attribute.return_value = (
        "钻石+"  # Diamond+ in Chinese
    )

    # Mock tier buttons container
    tier_buttons_container = Mock(spec=WebElement)
    tier_buttons_container.find_elements.return_value = [mock_tier_button]

    # Mock lane buttons container
    lane_buttons_container = Mock(spec=WebElement)
    lane_buttons_container.find_elements.return_value = [mock_lane_button]

    # Mock data list
    data_list = Mock(spec=WebElement)
    data_list.find_elements.return_value = mock_list_items

    # Set up the lane button's class attribute
    mock_lane_button.get_attribute.return_value = "lane-button Top"

    # Mock date element
    mock_date_element = Mock()
    mock_date_element.get_attribute.return_value = "2024-03-15"

    # Configure mock_driver.find_element to return appropriate elements
    def find_element_side_effect(by: str, value: str) -> Mock:
        if value == "dan-btn-box":  # Tier buttons container
            return tier_buttons_container
        elif value == "place-content":  # Lane buttons container
            return lane_buttons_container
        elif value == "data-time":  # Date element
            return mock_date_element
        else:  # Data list
            return data_list

    mock_driver.find_element.side_effect = find_element_side_effect

    parser = PageParser(mock_driver)
    with patch(
        "src.wrdata.data.infrastructure.parsers.page_parser.PageParser"
        "._PageParser__parse_lane_name_from_button",
        return_value=Lane.TOP,
    ):
        champions = parser.parse_champions()

        assert len(champions) > 0
        assert all(isinstance(champ, Champion) for champ in champions)
        assert champions[0].lane == Lane.TOP
