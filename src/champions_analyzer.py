from typing import Iterator

import numpy as np

from .champion import Champion
from .constants import NUMBER_OF_TIERS


class ChampionsAnalyzer:
    """A class to analyze a list of champions based on their win
    rates.

    Methods:
    ---
    update_metrics():
        Update metrics of the list of champions.
    """

    def __init__(self, champions_iterator: Iterator[Champion]):
        """Initialize the class with a list of champions and default metrics.

        Args:
            champions_iterator (Iterator[Champion]): An iterator providing
                Champion objects.
        """
        self.__champions = list(champions_iterator)
        self.__win_rate_adjustment_factor = 0.0
        self.__lower_boundary = 0.0
        self.__upper_boundary = 0.0
        self.__max_adjusted_win_rate = 0.0
        self.__adjusted_win_rate_spread_per_tier = 0.0

    def update_metrics(self) -> list[Champion]:
        """Update metrics of the list of champions.

        This method orchestrates a series of calculations and adjustments to
        the champions' win rates, sorts them, filters outliers, and assigns
        tiers, ultimately returning the updated list of champions.

        Returns:
            list[Champion]: The updated list of champions with adjusted
                metrics and assigned tiers.
        """
        self.__calculate_win_rate_adjustment_factor()
        self.__calculate_adjusted_win_rates()

        self.__sort_by_adjusted_win_rate()

        self.__calculate_boundaries()
        self.__filter_lower_outliers()
        self.__calculate_tier_determination_parameters()
        self.__assign_tiers()

        return self.__champions

    def __calculate_win_rate_adjustment_factor(self) -> None:
        """Calculate the win rate adjustment factor based on champions'
        statistics.

        This method determines the adjustment factor for win rates by analyzing
        the maximum and minimum win rates along with the maximum pick rate of
        the champions, which is used to normalize win rates for further
        calculations.
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
        """Calculate and update the adjusted win rates for each champion.

        This method iterates through the list of champions and computes their
        adjusted win rates based on their existing win rates, ensuring that
        the champions' performance metrics are accurately reflected.
        """
        for champion in self.__champions:
            champion.adjusted_win_rate = (
                champion.win_rate
                - self.__win_rate_adjustment_factor * champion.pick_rate
            )

    def __sort_by_adjusted_win_rate(self) -> None:
        """Sort the champions by their adjusted win rates in descending
        order.
        """
        self.__champions.sort(
            key=lambda champion: champion.adjusted_win_rate, reverse=True
        )

    def __calculate_boundaries(self) -> None:
        """Calculate the lower and upper boundaries for adjusted win rates.

        This method computes the lower and upper boundaries using the
        interquartile range (IQR) based on the adjusted win rates of the
        champions, which helps in identifying outliers in the dataset.
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
        """Filter out champions with adjusted win rates below a specified
            lower boundary.

        This method updates the list of champions by removing those whose
        adjusted win rates fall below the defined lower boundary, ensuring
        that only relevant champions are retained for further analysis.
        """
        self.__champions = [
            champion
            for champion in self.__champions
            if (self.__lower_boundary <= champion.adjusted_win_rate)
        ]

    def __calculate_tier_determination_parameters(self) -> None:
        """Calculate parameters for tier determination based on champions' win
        rates.

        This method computes the maximum adjusted win rate of champions that
        fall within a specified upper boundary and determines the spread of
        adjusted win rates across tiers.
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
        ) / NUMBER_OF_TIERS

    def __assign_tiers(self) -> None:
        """Assign tiers to each champion based on their adjusted win rates.

        This function iterates through a list of champions and updates their
            tier attribute using the adjusted win rate.
        """
        for champion in self.__champions:
            champion.tier = self.__determine_tier(champion.adjusted_win_rate)

    def __determine_tier(
        self,
        adjusted_win_rate: float,
    ) -> str:
        """Determine the tier classification based on the adjusted win rate.

        Args:
            adjusted_win_rate (float): The adjusted win rate to evaluate for
                tier classification.

        Returns:
            str: The tier classification corresponding to the adjusted win
                rate.
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
