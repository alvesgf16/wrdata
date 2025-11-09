"""Application settings and configuration."""

from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple


@dataclass
class ScrapingConfig:
    """Configuration for web scraping operations."""

    source_url: str = "https://lolm.qq.com/act/a20220818raider/index.html"
    timeout: int = 10
    headless: bool = True
    window_size: Tuple[int, int] = (1920, 1200)
    lane_element_class_prefix: str = "btn-place-"


@dataclass
class OutputConfig:
    """Configuration for data output."""

    output_directory: Path = Path("res")
    default_filename: str = "wrdata"
    supported_formats: Optional[List[str]] = None

    def __post_init__(self) -> None:
        if self.supported_formats is None:
            self.supported_formats = ["xlsx", "csv"]


@dataclass
class AnalysisConfig:
    """Configuration for data analysis."""

    number_of_tiers: int = 5
    tier_names: Optional[List[str]] = None

    def __post_init__(self) -> None:
        if self.tier_names is None:
            self.tier_names = ["S+", "S", "A", "B", "C"]


@dataclass
class ReaderConfig:
    """Configuration for data reading."""

    reader_type: str = "csv"  # Options: "csv", "excel"
    csv_filepath: str = "champions.csv"
    excel_filepath: str = "wrdata.xlsx"


class Settings:
    """Application settings container."""

    def __init__(self) -> None:
        self.scraping = ScrapingConfig()
        self.output = OutputConfig()
        self.analysis = AnalysisConfig()
        self.reader = ReaderConfig()


settings = Settings()
