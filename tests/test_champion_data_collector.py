import pytest
from unittest.mock import MagicMock, patch

from selenium import webdriver

from ..src.champion import Champion
from ..src.champion_data_collector import (
    fetch_champions,
    parse_when_ready,
    process_champions,
    update_metrics,
    write_to_csv,
)


@pytest.fixture
def mock_champions() -> list[Champion]:
    return [
        Champion("TOP", "Darius", 52.5, 10.2, 25.3),
        Champion("MID", "Ahri", 51.0, 8.5, 15.0),
        Champion("TOP", "Garen", 53.1, 9.8, 12.4),
    ]


@pytest.fixture
def mock_driver() -> MagicMock:
    return MagicMock(spec=webdriver.Chrome)


def test_fetch_champions(mock_champions: list[Champion]) -> None:
    with patch("selenium.webdriver.Chrome") as mock_chrome, patch(
        "wrdata.src.temp.parse_when_ready"
    ) as mock_parse:

        mock_driver = mock_chrome.return_value.__enter__.return_value
        mock_parse.return_value = mock_champions

        result = fetch_champions()

        mock_driver.get.assert_called_once()
        mock_parse.assert_called_once_with(mock_driver)
        assert result == mock_champions


def test_parse_when_ready(
    mock_champions: list[Champion], mock_driver: MagicMock
) -> None:
    with patch("wrdata.src.temp.WebDriverWait") as mock_wait, patch(
        "wrdata.src.temp.PageParser"
    ) as mock_parser:

        # Setup mock return values
        mock_parser.return_value.parse_champions.return_value = mock_champions

        # Call the function
        result = parse_when_ready(mock_driver)

        # Verify WebDriverWait was called with correct parameters
        mock_wait.assert_called_once_with(mock_driver, 10)
        mock_wait.return_value.until_not.assert_called_once()

        # Verify PageParser was used correctly
        mock_parser.assert_called_once_with(mock_driver)
        mock_parser.return_value.parse_champions.assert_called_once()

        # Verify the result
        assert isinstance(result, list)
        assert len(result) == 3
        assert isinstance(result[0], Champion)


def test_update_metrics(mock_champions: list[Champion]) -> None:
    result = update_metrics(mock_champions)

    assert isinstance(result, list)
    assert len(result) == len(mock_champions)
    for champion in result:
        assert isinstance(champion, Champion)
        assert hasattr(champion, "adjusted_win_rate")
        assert hasattr(champion, "tier")


def test_write_to_csv(mock_champions: list[Champion]) -> None:
    with patch("builtins.open") as mock_open:
        write_to_csv(mock_champions)
        mock_open.assert_called_once()


def test_process_champions(mock_champions: list[Champion]) -> None:
    with patch("wrdata.src.temp.fetch_champions") as mock_fetch, patch(
        "wrdata.src.temp.update_metrics"
    ) as mock_update, patch("wrdata.src.temp.write_to_csv") as mock_write:

        mock_fetch.return_value = mock_champions
        mock_update.return_value = mock_champions

        process_champions()

        mock_fetch.assert_called_once()
        mock_update.assert_called_once()
        mock_write.assert_called_once()
