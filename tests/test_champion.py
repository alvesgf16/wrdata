from ..src.champion import Champion


def test_champion_initialization() -> None:
    champion = Champion("TOP", "Darius", 52.5, 10.2, 25.3)
    assert champion.lane == "TOP"
    assert champion.name == "Darius"
    assert champion.win_rate == 52.5
    assert champion.pick_rate == 10.2
    assert champion.ban_rate == 25.3
    assert champion.adjusted_win_rate == 0.0
    assert champion.tier == ""


def test_champion_setters() -> None:
    champion = Champion("MID", "Ahri", 51.0, 8.5, 15.0)
    champion.adjusted_win_rate = 52.5
    champion.tier = "S"
    assert champion.adjusted_win_rate == 52.5
    assert champion.tier == "S"


def test_champion_to_csv_row() -> None:
    champion = Champion("Jungle", "Lee Sin", 48.5, 12.3, 18.7)
    champion.adjusted_win_rate = 49.2
    champion.tier = "A"
    expected_row = ["Jungle", "Lee Sin", 48.5, 12.3, 18.7, 49.2, "A"]
    assert champion.to_csv_row() == expected_row
