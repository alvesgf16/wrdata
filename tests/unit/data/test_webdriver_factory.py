"""
Tests for the WebDriver factory.
"""

from unittest.mock import Mock, patch

import pytest

from src.wrdata.data.webdriver_factory import WebDriverFactory
from src.wrdata.exceptions import ScrapingError


@patch("src.wrdata.data.webdriver_factory.ChromeDriverManager")
@patch("src.wrdata.data.webdriver_factory.Service")
@patch("src.wrdata.data.webdriver_factory.webdriver.Chrome")
def test_create_driver_success(
    mock_webdriver_chrome: Mock, mock_service: Mock, mock_driver_manager: Mock
) -> None:
    """Test successful WebDriver creation."""
    # Mock the driver manager
    mock_driver_manager.return_value.install.return_value = "/path/to/driver"

    # Mock the service
    mock_service_instance = Mock()
    mock_service.return_value = mock_service_instance

    # Mock the webdriver
    mock_driver = Mock()
    mock_webdriver_chrome.return_value = mock_driver

    # Call the factory method
    driver = WebDriverFactory.create_driver()

    # Verify calls
    mock_driver_manager.assert_called_once()
    mock_driver_manager.return_value.install.assert_called_once()
    mock_service.assert_called_once_with("/path/to/driver")
    mock_webdriver_chrome.assert_called_once()

    # Verify returned driver
    assert driver == mock_driver


@patch("src.wrdata.data.webdriver_factory.ChromeDriverManager")
def test_create_driver_manager_failure(mock_driver_manager: Mock) -> None:
    """Test WebDriver creation failure during driver manager setup."""
    # Mock driver manager to raise an exception
    mock_driver_manager.return_value.install.side_effect = Exception(
        "Driver download failed"
    )

    # Expect ScrapingError to be raised
    with pytest.raises(ScrapingError) as exc_info:
        WebDriverFactory.create_driver()

    assert "Failed to create Chrome webdriver instance" in str(exc_info.value)


@patch("src.wrdata.data.webdriver_factory.ChromeDriverManager")
@patch("src.wrdata.data.webdriver_factory.Service")
@patch("src.wrdata.data.webdriver_factory.webdriver.Chrome")
def test_create_driver_webdriver_failure(
    mock_webdriver_chrome: Mock, mock_service: Mock, mock_driver_manager: Mock
) -> None:
    """Test WebDriver creation failure during Chrome initialization."""
    # Mock successful driver manager and service
    mock_driver_manager.return_value.install.return_value = "/path/to/driver"
    mock_service.return_value = Mock()

    # Mock Chrome webdriver to raise an exception
    mock_webdriver_chrome.side_effect = Exception(
        "Chrome initialization failed"
    )

    # Expect ScrapingError to be raised
    with pytest.raises(ScrapingError) as exc_info:
        WebDriverFactory.create_driver()

    assert "Failed to create Chrome webdriver instance" in str(exc_info.value)


@patch("src.wrdata.data.webdriver_factory.ChromeDriverManager")
@patch("src.wrdata.data.webdriver_factory.Service")
@patch("src.wrdata.data.webdriver_factory.webdriver.Chrome")
@patch("src.wrdata.data.webdriver_factory.settings")
def test_create_driver_with_custom_settings(
    mock_settings: Mock,
    mock_webdriver_chrome: Mock,
    mock_service: Mock,
    mock_driver_manager: Mock,
) -> None:
    """Test WebDriver creation with custom settings."""
    # Mock settings
    mock_settings.scraping.window_size = (1024, 768)
    mock_settings.scraping.headless = False

    # Mock other dependencies
    mock_driver_manager.return_value.install.return_value = "/path/to/driver"
    mock_service.return_value = Mock()
    mock_driver = Mock()
    mock_webdriver_chrome.return_value = mock_driver

    # Call the factory method
    driver = WebDriverFactory.create_driver()

    # Verify that Chrome was called with options
    mock_webdriver_chrome.assert_called_once()
    call_args = mock_webdriver_chrome.call_args

    # Check that options were passed
    assert "options" in call_args.kwargs
    assert "service" in call_args.kwargs

    # Verify returned driver
    assert driver == mock_driver


@patch("src.wrdata.data.webdriver_factory.ChromeDriverManager")
@patch("src.wrdata.data.webdriver_factory.Service")
@patch("src.wrdata.data.webdriver_factory.Options")
@patch("src.wrdata.data.webdriver_factory.webdriver.Chrome")
def test_chrome_options_configuration(
    mock_webdriver_chrome: Mock,
    mock_options_class: Mock,
    mock_service: Mock,
    mock_driver_manager: Mock,
) -> None:
    """Test that Chrome options are properly configured."""
    # Mock the Options instance
    mock_options = Mock()
    mock_options_class.return_value = mock_options

    # Mock other dependencies
    mock_driver_manager.return_value.install.return_value = "/path/to/driver"
    mock_service.return_value = Mock()
    mock_webdriver_chrome.return_value = Mock()

    # Call the factory method
    WebDriverFactory.create_driver()

    # Verify that options were configured
    mock_options_class.assert_called_once()

    # Verify that add_argument was called multiple times for different options
    assert mock_options.add_argument.call_count > 0

    # Check that Chrome was called with the options
    mock_webdriver_chrome.assert_called_once()
    call_kwargs = mock_webdriver_chrome.call_args.kwargs
    assert call_kwargs["options"] == mock_options
