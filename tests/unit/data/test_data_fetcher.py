"""
Tests for the data fetcher module.
"""

from unittest.mock import Mock, patch

import pytest

from src.wrdata.data.data_fetcher import DataFetcher
from src.wrdata.data.models.champion import Champion, Lane
from src.wrdata.exceptions import ScrapingError


def test_data_fetcher_initialization() -> None:
    """Test DataFetcher initialization."""
    fetcher = DataFetcher()
    assert hasattr(fetcher, "_webdriver_service")
    assert fetcher._webdriver_service is not None


@patch("src.wrdata.data.data_fetcher.WebDriverWait")
@patch("src.wrdata.data.data_fetcher.PageParser")
@patch("src.wrdata.data.data_fetcher.WebDriverFactory")
def test_fetch_champions_success(
    mock_webdriver_factory: Mock, mock_parser_class: Mock, mock_wait: Mock
) -> None:
    """Test successful champion data fetching."""
    # Mock driver
    mock_driver = Mock()
    mock_driver.__enter__ = Mock(return_value=mock_driver)
    mock_driver.__exit__ = Mock(return_value=None)

    # Mock webdriver factory
    mock_factory_instance = Mock()
    mock_factory_instance.create_driver.return_value = mock_driver
    mock_webdriver_factory.return_value = mock_factory_instance

    # Mock parser and its methods
    mock_parser = Mock()
    mock_parser_class.return_value = mock_parser

    # Mock sample champion data
    sample_champions = [
        [Champion(Lane.TOP, "Test1", 50.0, 10.0, 5.0)],
        [Champion(Lane.MID, "Test2", 52.0, 12.0, 7.0)],
    ]
    mock_parser.parse_champions.return_value = sample_champions

    # Create fetcher and fetch data
    fetcher = DataFetcher()
    result = fetcher.fetch_champions()

    # Verify webdriver factory was used
    mock_factory_instance.create_driver.assert_called_once()

    # Verify parser was created and called
    mock_parser_class.assert_called_once_with(mock_driver)
    mock_parser.parse_champions.assert_called_once()

    # Verify result
    assert result == sample_champions


@patch("src.wrdata.data.data_fetcher.PageParser")
@patch("src.wrdata.data.data_fetcher.WebDriverFactory")
def test_fetch_champions_parser_error(
    mock_webdriver_factory: Mock, mock_parser_class: Mock
) -> None:
    """Test fetch_champions when parser raises an exception."""
    # Mock driver
    mock_driver = Mock()
    mock_driver.__enter__ = Mock(return_value=mock_driver)
    mock_driver.__exit__ = Mock(return_value=None)

    # Mock webdriver factory
    mock_factory_instance = Mock()
    mock_factory_instance.create_driver.return_value = mock_driver
    mock_webdriver_factory.return_value = mock_factory_instance

    # Mock parser to raise an exception
    mock_parser = Mock()
    mock_parser_class.return_value = mock_parser
    mock_parser.parse_champions.side_effect = Exception("Parse error")

    # Create fetcher
    fetcher = DataFetcher()

    # Expect ScrapingError to be raised
    with pytest.raises(ScrapingError) as exc_info:
        fetcher.fetch_champions()

    assert "Failed to fetch champions from source URL" in str(exc_info.value)


@patch("src.wrdata.data.data_fetcher.PageParser")
@patch("src.wrdata.data.data_fetcher.WebDriverFactory")
def test_fetch_champions_empty_result(
    mock_webdriver_factory: Mock, mock_parser_class: Mock
) -> None:
    """Test fetch_champions when parser returns empty data."""
    # Mock driver
    mock_driver = Mock()
    mock_driver.__enter__ = Mock(return_value=mock_driver)
    mock_driver.__exit__ = Mock(return_value=None)

    # Mock webdriver factory
    mock_factory_instance = Mock()
    mock_factory_instance.create_driver.return_value = mock_driver
    mock_webdriver_factory.return_value = mock_factory_instance

    # Mock parser to return empty data
    mock_parser = Mock()
    mock_parser_class.return_value = mock_parser
    mock_parser.parse_champions.return_value = []

    # Create fetcher and fetch data
    fetcher = DataFetcher()
    result = fetcher.fetch_champions()

    # Verify empty result is handled correctly
    assert result == []


@patch("src.wrdata.data.data_fetcher.WebDriverFactory")
def test_fetch_champions_webdriver_error(mock_webdriver_factory: Mock) -> None:
    """Test fetch_champions when webdriver creation fails."""
    # Mock webdriver factory to raise an exception
    mock_factory_instance = Mock()
    mock_factory_instance.create_driver.side_effect = ScrapingError(
        "WebDriver creation failed"
    )
    mock_webdriver_factory.return_value = mock_factory_instance

    # Create fetcher
    fetcher = DataFetcher()

    # Expect ScrapingError to be re-raised
    with pytest.raises(ScrapingError) as exc_info:
        fetcher.fetch_champions()

    assert "WebDriver creation failed" in str(exc_info.value)
