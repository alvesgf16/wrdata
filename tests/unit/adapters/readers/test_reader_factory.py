"""Tests for the ChampionReaderFactory."""

import pytest

from src.wrdata.adapters.readers.csv_reader import CSVChampionReader
from src.wrdata.adapters.readers.excel_reader import ExcelChampionReader
from src.wrdata.adapters.readers.reader_factory import ChampionReaderFactory


def test_factory_creates_csv_reader():
    """Test that factory creates CSVChampionReader when type is 'csv'."""
    reader = ChampionReaderFactory.create_reader(reader_type="csv")
    assert isinstance(reader, CSVChampionReader)


def test_factory_creates_excel_reader():
    """Test that factory creates ExcelChampionReader when type is 'excel'."""
    reader = ChampionReaderFactory.create_reader(reader_type="excel")
    assert isinstance(reader, ExcelChampionReader)


def test_factory_creates_csv_reader_with_custom_filepath():
    """Test that factory creates CSVChampionReader with custom filepath."""
    from pathlib import Path

    custom_path = "custom_champions.csv"
    reader = ChampionReaderFactory.create_reader(
        reader_type="csv", filepath=custom_path
    )
    assert isinstance(reader, CSVChampionReader)
    assert reader._filepath == Path(custom_path)


def test_factory_creates_excel_reader_with_custom_filepath():
    """Test that factory creates ExcelChampionReader with custom filepath."""
    custom_path = "custom_champions.xlsx"
    reader = ChampionReaderFactory.create_reader(
        reader_type="excel", filepath=custom_path
    )
    assert isinstance(reader, ExcelChampionReader)


def test_factory_uses_default_reader_type_from_settings():
    """Test that factory uses reader type from settings when not specified."""
    # Default from settings is "csv"
    reader = ChampionReaderFactory.create_reader()
    assert isinstance(reader, CSVChampionReader)


def test_factory_raises_error_for_unsupported_reader_type():
    """Test that factory raises ValueError for unsupported reader types."""
    with pytest.raises(ValueError, match="Unsupported reader type: database"):
        ChampionReaderFactory.create_reader(reader_type="database")
