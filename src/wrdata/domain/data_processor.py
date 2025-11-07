"""
Data processing service module for champion metrics calculation.

This module provides functionality for processing champion data by
coordinating with analyzers to update metrics and calculations.
"""

from itertools import groupby
from operator import attrgetter

from ..data.domain.models.champion import Champion
from .analyzer import ChampionsAnalyzer
from .models.analyzed_champion import AnalyzedChampion


class DataProcessor:
    """Service for processing champion data and updating metrics."""

    def update_metrics(self, data: list[Champion]) -> list[AnalyzedChampion]:
        """Update metrics for champions grouped by their lane.

        Processes a list of champions by grouping them by lane and
        analyzing each group using the ChampionsAnalyzer. This ensures
        that metrics are calculated appropriately within the context of
        each lane.

        Args:
            data (list[Champion]): A list of Champion objects to process.

        Returns:
            list[AnalyzedChampion]: The processed list of analyzed
                champions with calculated metrics and assigned tiers.
        """
        result: list[AnalyzedChampion] = []
        for _, champions_iterator in groupby(data, attrgetter("lane")):
            analyzer = ChampionsAnalyzer(champions_iterator)
            result.extend(analyzer.update_metrics())
        return result
