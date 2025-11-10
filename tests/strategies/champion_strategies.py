"""
Hypothesis strategies for generating Champion test data.
"""

from typing import TypedDict

from hypothesis import strategies as st
from hypothesis.strategies import DrawFn, SearchStrategy
from typing_extensions import Unpack

from src.wrdata.data import Champion, Lane, RankedTier
from src.wrdata.i18n.mappings.champions import CHAMPIONS


class ChampionKwargs(TypedDict, total=False):
    """Keyword arguments for champion_strategy."""

    name: str
    lane: Lane
    win_rate: float
    pick_rate: float
    ban_rate: float
    ranked_tier: RankedTier


@st.composite
def champion_strategy(
    draw: DrawFn,
    name: str | None = None,
    lane: Lane | None = None,
    win_rate: float | None = None,
    pick_rate: float | None = None,
    ban_rate: float | None = None,
    ranked_tier: RankedTier | None = None,
) -> Champion:
    """
    Generate a Champion instance with random or specified values.

    This composite strategy allows you to generate random Champion objects
    with sensible defaults, while also allowing you to override specific
    fields when needed for testing.

    Args:
        draw: Hypothesis draw function (automatically provided).
        name: Optional fixed name. If None, generates a random name.
        lane: Optional fixed lane. If None, randomly selects from
            Lane enum.
        win_rate: Optional fixed win rate. If None, generates float
            between 0.0-1.0.
        pick_rate: Optional fixed pick rate. If None, generates float
            between 0.0-1.0.
        ban_rate: Optional fixed ban rate. If None, generates float
            between 0.0-1.0.
        ranked_tier: Optional fixed ranked tier. If None, randomly
            selects from RankedTier enum.

    Returns:
        Champion: A Champion instance with either random or specified
            values.

    Examples:
        # Generate a completely random champion
        @given(champion=champion_strategy())
        def test_something(champion):
            pass

        # Generate a champion with a specific name but random values
        @given(champion=champion_strategy(name="Darius"))
        def test_darius(champion):
            pass

        # Generate a champion with specific lane and tier
        @given(
            champion=champion_strategy(
                lane=Lane.TOP, ranked_tier=RankedTier.DIAMOND_PLUS
            )
        )
        def test_top_lane_diamond(champion):
            pass
    """
    return Champion(
        name=(
            name
            if name is not None
            else draw(st.sampled_from(list(CHAMPIONS.values())))
        ),
        lane=lane if lane is not None else draw(st.sampled_from(Lane)),
        win_rate=(
            win_rate
            if win_rate is not None
            else draw(st.floats(min_value=0.0, max_value=1.0))
        ),
        pick_rate=(
            pick_rate
            if pick_rate is not None
            else draw(st.floats(min_value=0.0, max_value=1.0))
        ),
        ban_rate=(
            ban_rate
            if ban_rate is not None
            else draw(st.floats(min_value=0.0, max_value=1.0))
        ),
        ranked_tier=(
            ranked_tier
            if ranked_tier is not None
            else draw(st.sampled_from(RankedTier))
        ),
    )


def champions_list_strategy(
    min_size: int = 1,
    max_size: int = 10,
    **champion_kwargs: Unpack[ChampionKwargs],
) -> SearchStrategy[list[Champion]]:
    """
    Generate a list of Champion instances.

    Args:
        min_size: Minimum number of champions in the list.
        max_size: Maximum number of champions in the list.
        **champion_kwargs: Additional keyword arguments to pass to
            champion_strategy.

    Returns:
        A strategy that generates lists of Champion instances.

    Examples:
        # Generate a list of 1-10 random champions
        @given(champions=champions_list_strategy())
        def test_champion_list(champions):
            pass

        # Generate a list of 5 top lane champions
        @given(
            champions=champions_list_strategy(
                min_size=5, max_size=5, lane=Lane.TOP
            )
        )
        def test_five_top_laners(champions):
            pass
    """
    return st.lists(
        champion_strategy(**champion_kwargs),
        min_size=min_size,
        max_size=max_size,
    )
