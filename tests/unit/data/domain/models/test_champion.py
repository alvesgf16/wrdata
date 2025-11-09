"""
Tests for the Champion model.
"""

from src.wrdata.data import Champion, Lane


def test_champion_creation() -> None:
    """Test champion object creation with valid data."""
    champion = Champion(
        name="Test Champion",
        lane=Lane.TOP,
        win_rate=55.5,
        pick_rate=10.2,
        ban_rate=5.1,
        ranked_tier="Tier 1",
    )

    assert champion.name == "Test Champion"
    assert champion.lane == Lane.TOP
    assert champion.win_rate == 55.5
    assert champion.pick_rate == 10.2
    assert champion.ban_rate == 5.1
    assert champion.ranked_tier == "Tier 1"


def test_champion_string_representation() -> None:
    """Test champion string representation."""
    champion = Champion(
        name="Test Champion",
        lane=Lane.TOP,
        win_rate=55.5,
        pick_rate=10.2,
        ban_rate=5.1,
        ranked_tier="Tier 1",
    )

    # Dataclass default __repr__ is now used
    expected = (
        "Champion(lane=<Lane.TOP: 'Top'>, name='Test Champion', "
        "win_rate=55.5, pick_rate=10.2, ban_rate=5.1, ranked_tier='Tier 1')"
    )
    assert str(champion) == expected
