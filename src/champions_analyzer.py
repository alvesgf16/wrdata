"""
Champion analysis module for processing and tiering champions.

This module provides functionality for analyzing champion performance data
and assigning tier classifications. It processes win rates, handles
outliers, and implements a sophisticated tiering system based on
statistical analysis.
"""

from typing import Iterator

import numpy as np

from .config.settings import settings
from .exceptions import DataProcessingError
from .models.champion import Champion


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
        self.__win_rate_adjustment_factor = 0.0
        self.__lower_boundary = 0.0
        self.__upper_boundary = 0.0
        self.__max_adjusted_win_rate = 0.0
        self.__adjusted_win_rate_spread_per_tier = 0.0

    def update_metrics(self) -> list[Champion]:
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
            list[Champion]: The updated list of champions with adjusted
                metrics and assigned tiers.

        Raises:
            DataProcessingError: If there are issues processing champion
                metrics or calculating tiers
        """
        try:
            self.__calculate_win_rate_adjustment_factor()
            self.__calculate_adjusted_win_rates()

            self.__sort_by_adjusted_win_rate()

            self.__calculate_boundaries()
            self.__filter_lower_outliers()
            self.__calculate_tier_determination_parameters()
            self.__assign_tiers()

            return self.__champions
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

    def __calculate_adjusted_win_rates(self) -> None:
        """Calculate adjusted win rates for each champion.

        This method applies the win rate adjustment factor to each
        champion's win rate, taking into account their pick rate. The
        adjustment helps normalize win rates across different pick rate
        ranges.

        Formula: adjusted_win_rate = win_rate - (adjustment_factor * pick_rate)
        """
        for champion in self.__champions:
            champion.adjusted_win_rate = (
                champion.win_rate
                - self.__win_rate_adjustment_factor * champion.pick_rate
            )

    def __sort_by_adjusted_win_rate(self) -> None:
        """Sort champions by their adjusted win rates in descending order.

        This method sorts the internal list of champions based on their
        adjusted win rates, with higher rates appearing first in the list.
        """
        self.__champions.sort(
            key=lambda champion: champion.adjusted_win_rate, reverse=True
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
            [champion.adjusted_win_rate for champion in self.__champions],
            [25, 75],
            method="midpoint",
        )
        iqr = q3 - q1
        self.__lower_boundary = q1 - 1.5 * iqr
        self.__upper_boundary = q3 + 1.5 * iqr

    def __filter_lower_outliers(self) -> None:
        """Remove champions with adjusted win rates below the lower boundary.

        This method filters out champions whose adjusted win rates fall
        below the calculated lower boundary, ensuring that only
        statistically significant champions are included in the final
        analysis.
        """
        self.__champions = [
            champion
            for champion in self.__champions
            if (self.__lower_boundary <= champion.adjusted_win_rate)
        ]

    def __calculate_tier_determination_parameters(self) -> None:
        """Calculate parameters for tier determination.

        This method determines the maximum adjusted win rate within
        normal range and calculates the spread of win rates per tier.
        These parameters are used to establish the boundaries between
        different tier levels.
        """
        self.__max_adjusted_win_rate = max(
            champion.adjusted_win_rate
            for champion in self.__champions
            if champion.adjusted_win_rate <= self.__upper_boundary
        )
        min_adjusted_win_rate = min(
            champion.adjusted_win_rate for champion in self.__champions
        )
        self.__adjusted_win_rate_spread_per_tier = (
            self.__max_adjusted_win_rate - min_adjusted_win_rate
        ) / settings.analysis.number_of_tiers

    def __assign_tiers(self) -> None:
        """Assign tier classifications to all champions.

        This method iterates through the champions and assigns each one
        a tier based on their adjusted win rate. The tier assignment
        uses the calculated tier boundaries and spread parameters.
        """
        for champion in self.__champions:
            tier_str = self.__determine_tier(champion.adjusted_win_rate)
            champion.set_tier_from_string(tier_str)

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
