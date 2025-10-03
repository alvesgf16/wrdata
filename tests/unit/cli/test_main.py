"""
Tests for the CLI main module.
"""

from unittest.mock import patch

import pytest

from src.wrdata.cli.main import main


def test_main_success() -> None:
    """Test successful execution of main function."""
    with patch("src.wrdata.cli.main.process_champions") as mock_process:
        # Mock successful execution
        mock_process.return_value = None

        # Capture stdout
        with patch("builtins.print") as mock_print:
            main()

        # Verify process_champions was called
        mock_process.assert_called_once()

        # Verify success message was printed
        mock_print.assert_called_with(
            "✅ Champion data processing completed successfully!"
        )


def test_main_exception_handling() -> None:
    """Test exception handling in main function."""
    with patch("src.wrdata.cli.main.process_champions") as mock_process:
        # Mock an exception
        test_error = Exception("Test error message")
        mock_process.side_effect = test_error

        # Capture stdout and expect exception to be re-raised
        with patch("builtins.print") as mock_print, pytest.raises(Exception):
            main()

        # Verify process_champions was called
        mock_process.assert_called_once()

        # Verify error message was printed
        mock_print.assert_called_with(
            "❌ Error during data processing: Test error message"
        )


def test_main_with_specific_exception_type() -> None:
    """Test main function with specific exception types."""
    from src.wrdata.exceptions import ScrapingError

    with patch("src.wrdata.cli.main.process_champions") as mock_process:
        # Mock a ScrapingError
        test_error = ScrapingError("Scraping failed")
        mock_process.side_effect = test_error

        with patch("builtins.print") as mock_print:
            with pytest.raises(ScrapingError):
                main()

        # Verify error message includes the ScrapingError details
        mock_print.assert_called_with(
            "❌ Error during data processing: Scraping failed"
        )
