"""
Test fixtures and configuration for the WRData test suite.
"""

from pathlib import Path
from unittest.mock import Mock

import pytest
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from src.wrdata.data.models.champion import Champion, Lane


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
        name_element.get_attribute.return_value = (
            "疾风剑豪"  # Yasuo in Chinese
        )
        item.find_element.return_value = name_element

        stat_elements = [Mock() for _ in range(3)]
        stat_elements[0].get_attribute.return_value = "52.5%"
        stat_elements[1].get_attribute.return_value = "10.2%"
        stat_elements[2].get_attribute.return_value = "25.3%"
        item.find_elements.return_value = stat_elements

    return items


@pytest.fixture
def sample_champion_data() -> list[Champion]:
    """Create sample champion data for testing."""
    return [
        # Top Lane Champions
        Champion(
            name="Darius",
            lane=Lane.TOP,
            win_rate=52.3,
            pick_rate=8.7,
            ban_rate=15.2,
        ),
        Champion(
            name="Garen",
            lane=Lane.TOP,
            win_rate=51.8,
            pick_rate=7.5,
            ban_rate=5.1,
        ),
        Champion(
            name="Sett",
            lane=Lane.TOP,
            win_rate=50.9,
            pick_rate=6.8,
            ban_rate=8.3,
        ),
        # Jungle Lane Champions
        Champion(
            name="Lee Sin",
            lane=Lane.JUNGLE,
            win_rate=48.5,
            pick_rate=12.3,
            ban_rate=20.1,
        ),
        Champion(
            name="Jarvan IV",
            lane=Lane.JUNGLE,
            win_rate=51.2,
            pick_rate=9.4,
            ban_rate=7.8,
        ),
        Champion(
            name="Vi",
            lane=Lane.JUNGLE,
            win_rate=52.7,
            pick_rate=8.1,
            ban_rate=4.2,
        ),
        # Mid Lane Champions
        Champion(
            name="Yasuo",
            lane=Lane.MID,
            win_rate=47.8,
            pick_rate=15.6,
            ban_rate=25.4,
        ),
        Champion(
            name="Zed",
            lane=Lane.MID,
            win_rate=49.2,
            pick_rate=13.4,
            ban_rate=22.8,
        ),
        Champion(
            name="Ahri",
            lane=Lane.MID,
            win_rate=51.5,
            pick_rate=10.9,
            ban_rate=8.7,
        ),
        # Bot Lane Champions (ADCs)
        Champion(
            name="Jinx",
            lane=Lane.BOT,
            win_rate=52.1,
            pick_rate=11.2,
            ban_rate=6.5,
        ),
        Champion(
            name="Kai'Sa",
            lane=Lane.BOT,
            win_rate=50.8,
            pick_rate=14.5,
            ban_rate=12.3,
        ),
        Champion(
            name="Ashe",
            lane=Lane.BOT,
            win_rate=51.4,
            pick_rate=9.8,
            ban_rate=3.2,
        ),
        # Support Lane Champions
        Champion(
            name="Thresh",
            lane=Lane.SUP,
            win_rate=49.8,
            pick_rate=13.2,
            ban_rate=18.9,
        ),
        Champion(
            name="Leona",
            lane=Lane.SUP,
            win_rate=51.6,
            pick_rate=10.5,
            ban_rate=7.4,
        ),
        Champion(
            name="Nami",
            lane=Lane.SUP,
            win_rate=52.3,
            pick_rate=8.9,
            ban_rate=4.1,
        ),
    ]


@pytest.fixture
def test_excel_path(tmp_path: Path) -> Path:
    """Create a temporary path for test Excel files."""
    return tmp_path / "test_output.xlsx"
