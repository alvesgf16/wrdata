"""
Tests for the Champions Analyzer.
"""

from src.wrdata.data import Champion, Lane, RankedTier
from src.wrdata.domain.analyzer import ChampionsAnalyzer


def test_metric_calculation(sample_champion_data: list[Champion]) -> None:
    """Test metric calculations for champions."""
    champions_iterator = iter(sample_champion_data)
    analyzer = ChampionsAnalyzer(champions_iterator)
    updated_champions = analyzer.update_metrics()

    # Check that metrics were updated
    for champion in updated_champions:
        assert champion.adjusted_win_rate != 0
        assert champion.tier is not None


def test_lane_based_grouping() -> None:
    """Test grouping champions by lane."""
    champions = [
        Champion(
            name="Champ1",
            lane=Lane.TOP,
            win_rate=55.5,
            pick_rate=10.2,
            ban_rate=5.1,
            ranked_tier=RankedTier.DIAMOND_PLUS,
        ),
        Champion(
            name="Champ2",
            lane=Lane.TOP,
            win_rate=52.3,
            pick_rate=8.7,
            ban_rate=3.2,
            ranked_tier=RankedTier.DIAMOND_PLUS,
        ),
        Champion(
            name="Champ3",
            lane=Lane.JUNGLE,
            win_rate=54.1,
            pick_rate=9.5,
            ban_rate=4.3,
            ranked_tier=RankedTier.DIAMOND_PLUS,
        ),
    ]

    champions_iterator = iter(champions)
    analyzer = ChampionsAnalyzer(champions_iterator)
    updated_champions = analyzer.update_metrics()

    # Verify champions are processed by lane
    top_champs = [c for c in updated_champions if c.lane == Lane.TOP]
    jungle_champs = [c for c in updated_champions if c.lane == Lane.JUNGLE]

    assert len(top_champs) == 2
    assert len(jungle_champs) == 1


def test_single_champion() -> None:
    """Test analyzer with single champion data."""
    champion = Champion(
        name="Test Champion",
        lane=Lane.TOP,
        win_rate=55.5,
        pick_rate=10.2,
        ban_rate=5.1,
        ranked_tier=RankedTier.DIAMOND_PLUS,
    )

    champion_iterator = iter([champion])
    analyzer = ChampionsAnalyzer(champion_iterator)
    result = analyzer.update_metrics()

    assert len(result) == 1
    assert result[0].champion == champion
    assert result[0].adjusted_win_rate != 0
    assert result[0].tier is not None
