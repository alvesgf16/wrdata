"""
Champion analysis module for processing and tiering champions.

This module provides functionality for analyzing champion performance data
and assigning tier classifications. It processes win rates, handles
outliers, and implements a sophisticated tiering system based on
statistical analysis.
"""

from typing import Iterator

import numpy as np

from ..config.settings import settings
from ..data import Champion
from ..exceptions import DataProcessingError
from .models.analyzed_champion import AnalyzedChampion, Tier


class ChampionsAnalyzer:
    """A class to analyze and tier champions based on their performance
    metrics.

    Methods:
    ---
    update_metrics():
        Update metrics of the list of champions.
    """

    def __init__(self, champions_iterator: Iterator[Champion]):
        """Initialize the analyzer with a list of champions.

        Args:
            champions_iterator (Iterator[Champion]): An iterator providing
                Champion objects to analyze.
        """
        self.__champions = list(champions_iterator)
        self.__analyzed_champions: list[AnalyzedChampion] = []
        self.__win_rate_adjustment_factor = 0.0
        self.__lower_boundary = 0.0
        self.__upper_boundary = 0.0
        self.__max_adjusted_win_rate = 0.0
        self.__adjusted_win_rate_spread_per_tier = 0.0

    def update_metrics(self) -> list[AnalyzedChampion]:
        """Update metrics and assign tiers to the list of champions.

        This method orchestrates the complete analysis process:
        1. Calculates win rate adjustments
        2. Adjusts win rates based on pick rates
        3. Sorts champions by adjusted win rates
        4. Calculates statistical boundaries
        5. Filters out outliers
        6. Determines tier parameters
        7. Assigns final tier classifications

        Returns:
            list[AnalyzedChampion]: The analyzed champions with calculated
                metrics and assigned tiers.

        Raises:
            DataProcessingError: If there are issues processing champion
                metrics or calculating tiers
        """
        try:
            self.__calculate_win_rate_adjustment_factor()
            self.__create_analyzed_champions()

            self.__sort_by_adjusted_win_rate()

            self.__calculate_boundaries()
            self.__filter_lower_outliers()
            self.__calculate_tier_determination_parameters()
            self.__assign_tiers()

            return self.__analyzed_champions
        except (ValueError, ZeroDivisionError) as e:
            raise DataProcessingError(
                "Failed to calculate champion metrics", details=str(e)
            ) from e
        except Exception as e:
            raise DataProcessingError(
                "Failed to update champion metrics and assign tiers",
                details=str(e),
            ) from e

    def __calculate_win_rate_adjustment_factor(self) -> None:
        """Calculate the win rate adjustment factor based on champion
        statistics.

        This method determines the adjustment factor by analyzing the
        spread between maximum and minimum win rates, normalized by the
        maximum pick rate. This factor is used to adjust win rates to
        account for pick rate influence.

        The formula used is:
        (min_win_rate - max_win_rate) / (4 * max_pick_rate)
        """
        max_win_rate = max(champion.win_rate for champion in self.__champions)
        min_win_rate = min(champion.win_rate for champion in self.__champions)
        max_pick_rate = max(
            champion.pick_rate for champion in self.__champions
        )
        self.__win_rate_adjustment_factor = (min_win_rate - max_win_rate) / (
            4 * max_pick_rate
        )

    def __create_analyzed_champions(self) -> None:
        """Create AnalyzedChampion instances with adjusted win rates.

        For each champion, calculates the adjusted win rate using the
        formula: win_rate - (adjustment_factor * pick_rate)
        The tier is initially set to None and will be assigned later.
        """
        self.__analyzed_champions = [
            AnalyzedChampion(
                champion=champion,
                adjusted_win_rate=champion.win_rate
                - self.__win_rate_adjustment_factor * champion.pick_rate,
                tier=None,
            )
            for champion in self.__champions
        ]

    def __sort_by_adjusted_win_rate(self) -> None:
        """Sort champions by their adjusted win rates in descending order.

        This method sorts the internal list of analyzed champions based on
        their adjusted win rates, with higher rates appearing first.
        """
        self.__analyzed_champions.sort(
            key=lambda ac: ac.adjusted_win_rate, reverse=True
        )

    def __calculate_boundaries(self) -> None:
        """Calculate statistical boundaries for outlier detection.

        This method uses the interquartile range (IQR) to determine
        lower and upper boundaries for identifying outliers in the
        adjusted win rate distribution. The boundaries are calculated as:
        - Lower: Q1 - 1.5 * IQR
        - Upper: Q3 + 1.5 * IQR
        """
        q1, q3 = np.percentile(
            [ac.adjusted_win_rate for ac in self.__analyzed_champions],
            [25, 75],
            method="midpoint",
        )
        iqr = q3 - q1
        self.__lower_boundary = q1 - 1.5 * iqr
        self.__upper_boundary = q3 + 1.5 * iqr

    def __filter_lower_outliers(self) -> None:
        """Remove champions with adjusted win rates below lower boundary.

        This method filters out analyzed champions whose adjusted win rates
        fall below the calculated lower boundary, ensuring that only
        statistically significant champions are included in the final
        analysis.
        """
        self.__analyzed_champions = [
            ac
            for ac in self.__analyzed_champions
            if (self.__lower_boundary <= ac.adjusted_win_rate)
        ]

    def __calculate_tier_determination_parameters(self) -> None:
        """Calculate parameters for tier determination.

        This method determines the maximum adjusted win rate within
        normal range and calculates the spread of win rates per tier.
        These parameters are used to establish the boundaries between
        different tier levels.
        """
        # Filter champions within normal range (not upper outliers)
        champions_in_range = [
            ac
            for ac in self.__analyzed_champions
            if ac.adjusted_win_rate <= self.__upper_boundary
        ]

        # If no champions remain after filtering, use all analyzed champions
        if not champions_in_range:
            champions_in_range = self.__analyzed_champions

        self.__max_adjusted_win_rate = max(
            ac.adjusted_win_rate for ac in champions_in_range
        )
        min_adjusted_win_rate = min(
            ac.adjusted_win_rate for ac in champions_in_range
        )
        self.__adjusted_win_rate_spread_per_tier = (
            self.__max_adjusted_win_rate - min_adjusted_win_rate
        ) / settings.analysis.number_of_tiers

    def __assign_tiers(self) -> None:
        """Assign tier classifications to all analyzed champions.

        This method iterates through the analyzed champions and assigns
        each one a tier based on their adjusted win rate. The tier
        assignment uses the calculated tier boundaries and spread
        parameters.
        """
        for i, analyzed_champion in enumerate(self.__analyzed_champions):
            tier_str = self.__determine_tier(
                analyzed_champion.adjusted_win_rate
            )

            self.__analyzed_champions[i] = self.assign_tier_to_champion(
                tier_str, analyzed_champion
            )

    def assign_tier_to_champion(
        self, tier_str: str, analyzed_champion: AnalyzedChampion
    ) -> AnalyzedChampion:
        tier_map = {
            "S+": Tier.S_PLUS,
            "S": Tier.S,
            "A": Tier.A,
            "B": Tier.B,
            "C": Tier.C,
            "D": Tier.D,
        }

        return AnalyzedChampion(
            champion=analyzed_champion.champion,
            adjusted_win_rate=analyzed_champion.adjusted_win_rate,
            tier=tier_map.get(tier_str),
        )

    def __determine_tier(
        self,
        adjusted_win_rate: float,
    ) -> str:
        """Determine the tier classification for a given adjusted win rate.

        This method implements the tier classification logic based on
        the adjusted win rate value. The tiers are assigned as follows:
        - S+: Above upper boundary
        - S: Top tier within normal range
        - A: Second tier
        - B: Third tier
        - C: Fourth tier
        - D: Bottom tier

        Args:
            adjusted_win_rate (float): The adjusted win rate to evaluate
                for tier classification.

        Returns:
            str: The tier classification (S+, S, A, B, C, or D).
        """
        if adjusted_win_rate > self.__upper_boundary:
            return "S+"
        elif (
            adjusted_win_rate
            > self.__max_adjusted_win_rate
            - self.__adjusted_win_rate_spread_per_tier
        ):
            return "S"
        elif (
            adjusted_win_rate
            > self.__max_adjusted_win_rate
            - 2 * self.__adjusted_win_rate_spread_per_tier
        ):
            return "A"
        elif (
            adjusted_win_rate
            > self.__max_adjusted_win_rate
            - 3 * self.__adjusted_win_rate_spread_per_tier
        ):
            return "B"
        elif (
            adjusted_win_rate
            > self.__max_adjusted_win_rate
            - 4 * self.__adjusted_win_rate_spread_per_tier
        ):
            return "C"
        else:
            return "D"
