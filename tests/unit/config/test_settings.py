"""
Tests for the configuration settings.
"""

from pathlib import Path

from src.wrdata.config.settings import OutputConfig, ScrapingConfig, settings


def test_scraping_config_defaults() -> None:
    """Test ScrapingConfig default values."""
    config = ScrapingConfig()

    expected_url = "https://lolm.qq.com/act/a20220818raider/index.html"
    assert config.source_url == expected_url
    assert config.timeout == 10
    assert config.headless is True
    assert config.window_size == (1920, 1200)
    assert config.lane_element_class_prefix == "btn-place-"


def test_scraping_config_custom_values() -> None:
    """Test ScrapingConfig with custom values."""
    config = ScrapingConfig(
        source_url="https://custom.example.com",
        timeout=30,
        headless=False,
        window_size=(1024, 768),
        lane_element_class_prefix="custom-",
    )

    assert config.source_url == "https://custom.example.com"
    assert config.timeout == 30
    assert config.headless is False
    assert config.window_size == (1024, 768)
    assert config.lane_element_class_prefix == "custom-"


def test_output_config_defaults() -> None:
    """Test OutputConfig default values."""
    config = OutputConfig()

    assert config.output_directory == Path("res")
    assert config.default_filename == "wrdata"
    assert config.supported_formats == ["xlsx", "csv"]


def test_output_config_custom_values() -> None:
    """Test OutputConfig with custom values."""
    custom_path = Path("/custom/output")
    config = OutputConfig(
        output_directory=custom_path,
        default_filename="custom_data",
        supported_formats=["json", "xml"],
    )

    assert config.output_directory == custom_path
    assert config.default_filename == "custom_data"
    assert config.supported_formats == ["json", "xml"]


def test_output_config_post_init() -> None:
    """Test OutputConfig __post_init__ method."""
    # Test with None supported_formats
    config = OutputConfig(supported_formats=None)
    assert config.supported_formats == ["xlsx", "csv"]

    # Test with empty list
    config = OutputConfig(supported_formats=[])
    assert config.supported_formats == []

    # Test with custom formats
    config = OutputConfig(supported_formats=["pdf"])
    assert config.supported_formats == ["pdf"]


def test_settings_instance() -> None:
    """Test that settings instance is properly configured."""
    assert hasattr(settings, "scraping")
    assert hasattr(settings, "output")

    assert isinstance(settings.scraping, ScrapingConfig)
    assert isinstance(settings.output, OutputConfig)


def test_settings_scraping_config() -> None:
    """Test settings scraping configuration."""
    scraping = settings.scraping

    # Verify it has expected attributes
    assert hasattr(scraping, "source_url")
    assert hasattr(scraping, "timeout")
    assert hasattr(scraping, "headless")
    assert hasattr(scraping, "window_size")
    assert hasattr(scraping, "lane_element_class_prefix")

    # Verify types
    assert isinstance(scraping.source_url, str)
    assert isinstance(scraping.timeout, int)
    assert isinstance(scraping.headless, bool)
    assert isinstance(scraping.window_size, tuple)
    assert isinstance(scraping.lane_element_class_prefix, str)


def test_settings_output_config() -> None:
    """Test settings output configuration."""
    output = settings.output

    # Verify it has expected attributes
    assert hasattr(output, "output_directory")
    assert hasattr(output, "default_filename")
    assert hasattr(output, "supported_formats")

    # Verify types and values
    assert isinstance(output.output_directory, Path)
    assert isinstance(output.default_filename, str)
    assert isinstance(output.supported_formats, list)
    assert all(isinstance(fmt, str) for fmt in output.supported_formats)
