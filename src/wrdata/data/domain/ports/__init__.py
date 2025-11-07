"""Port interfaces for the data package."""

from .fetchers import WebFetcher
from .handlers import ChampionPipeline
from .parsers import ChampionParser
from .repositories import ChampionRepository

__all__ = [
    "ChampionPipeline",
    "WebFetcher",
    "ChampionParser",
    "ChampionRepository",
]
