"""
Data processing service module for champion metrics calculation.

This module provides functionality for processing champion data by
coordinating with analyzers to update metrics and calculations.
"""

from itertools import groupby
from operator import attrgetter

from ..data import Champion
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
        # Sort by lane value before grouping (groupby requires sorted data)
        sorted_data = sorted(data, key=lambda c: c.lane.value)
        for _, champions_iterator in groupby(sorted_data, attrgetter("lane")):
            # Convert iterator to list immediately to avoid consumption issues
            lane_champions = list(champions_iterator)
            if lane_champions:  # Skip empty groups
                analyzer = ChampionsAnalyzer(iter(lane_champions))
                result.extend(analyzer.update_metrics())
        return result
