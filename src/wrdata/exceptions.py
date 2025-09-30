"""Custom exceptions for WRData application."""


class WRDataError(Exception):
    """Base exception for WRData application."""

    def __init__(self, message: str, details: str | None = None) -> None:
        """Initialize the exception with a message and optional details.

        Args:
            message: The main error message
            details: Additional details about the error
        """
        self.message = message
        self.details = details
        super().__init__(self.message)

    def __str__(self) -> str:
        """Return a string representation of the exception."""
        if self.details:
            return f"{self.message}. Details: {self.details}"
        return self.message


class ScrapingError(WRDataError):
    """Exception raised during web scraping operations.

    This exception is raised when there are issues with:
    - Web driver initialization
    - Page loading timeouts
    - Element not found errors
    - Network connectivity issues
    """

    pass


class DataProcessingError(WRDataError):
    """Exception raised during data processing operations.

    This exception is raised when there are issues with:
    - Data parsing and transformation
    - Champion analysis calculations
    - Data validation failures
    - Metric computation errors
    """

    pass


class OutputError(WRDataError):
    """Exception raised during data output operations.

    This exception is raised when there are issues with:
    - File writing operations
    - Directory creation failures
    - Unsupported file formats
    - Permission errors during file operations
    """

    pass


class ConfigurationError(WRDataError):
    """Exception raised for configuration issues.

    This exception is raised when there are issues with:
    - Invalid configuration values
    - Missing required configuration
    - Configuration file loading errors
    - Environment variable issues
    """

    pass
