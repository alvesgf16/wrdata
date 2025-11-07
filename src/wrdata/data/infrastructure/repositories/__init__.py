"""Champion persistence adapters."""

from .csv_repository import CSVChampionRepository
from .excel_repository import ExcelChampionRepository

__all__ = ["CSVChampionRepository", "ExcelChampionRepository"]
