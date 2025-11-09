"""Factory for creating champion readers based on configuration."""

from ...config.settings import settings
from .csv_reader import CSVChampionReader
from .excel_reader import ExcelChampionReader
from .reader import ChampionReader


class ChampionReaderFactory:
    """Factory for creating champion readers.

    This factory creates the appropriate reader based on the
    configuration settings, supporting CSV, Excel, and future
    database readers.
    """

    @staticmethod
    def create_reader(
        reader_type: str | None = None, filepath: str | None = None
    ) -> ChampionReader:
        """Create a champion reader based on type.

        Args:
            reader_type: The type of reader to create ("csv" or "excel").
                If None, uses settings.reader.reader_type.
            filepath: Optional filepath to use. If None, uses default from
                settings based on reader type.

        Returns:
            An instance of ChampionReader.

        Raises:
            ValueError: If reader_type is not supported.
        """
        # Use settings if not provided
        if reader_type is None:
            reader_type = settings.reader.reader_type

        # Determine filepath based on reader type
        if filepath is None:
            if reader_type == "csv":
                filepath = settings.reader.csv_filepath
            elif reader_type == "excel":
                filepath = settings.reader.excel_filepath
            else:
                raise ValueError(
                    f"Unsupported reader type: {reader_type}. "
                    f"Supported types: 'csv', 'excel'"
                )

        # Create the appropriate reader
        if reader_type == "csv":
            return CSVChampionReader(filepath=filepath)
        elif reader_type == "excel":
            return ExcelChampionReader(filepath=filepath)
        else:
            raise ValueError(
                f"Unsupported reader type: {reader_type}. "
                f"Supported types: 'csv', 'excel'"
            )
