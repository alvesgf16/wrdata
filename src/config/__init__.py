"""Configuration package for WRData application."""

from .settings import settings
from .webdriver_factory import WebDriverFactory

__all__ = ["settings", "WebDriverFactory"]
