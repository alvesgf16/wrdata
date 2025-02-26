import pytest
from ..src.champions_analyzer import ChampionsAnalyzer
from ..src.champion import Champion


@pytest.fixture
def sample_champions() -> list[Champion]:
    return [
        Champion("TOP", "Darius", 53.5, 8.0, 20.0),
        Champion("MID", "Ahri", 51.0, 12.0, 15.0),
        Champion("JGL", "Lee Sin", 48.5, 15.0, 18.0),
        Champion("BOT", "Jinx", 52.0, 10.0, 12.0),
        Champion("SUP", "Thresh", 50.0, 9.0, 8.0),
    ]


def test_champions_analyzer_initialization(
    sample_champions: list[Champion],
) -> None:
    analyzer = ChampionsAnalyzer(iter(sample_champions))
    assert isinstance(analyzer, ChampionsAnalyzer)


def test_update_metrics(sample_champions: list[Champion]) -> None:
    analyzer = ChampionsAnalyzer(iter(sample_champions))
    updated_champions = analyzer.update_metrics()

    assert len(updated_champions) > 0
    for champion in updated_champions:
        assert champion.adjusted_win_rate != 0.0
        assert champion.tier != ""
        assert champion.tier in ["S+", "S", "A", "B", "C", "D"]


def test_champions_sorting(sample_champions: list[Champion]) -> None:
    analyzer = ChampionsAnalyzer(iter(sample_champions))
    updated_champions = analyzer.update_metrics()

    # Verify champions are sorted by adjusted win rate
    for i in range(len(updated_champions) - 1):
        assert (
            updated_champions[i].adjusted_win_rate
            >= updated_champions[i + 1].adjusted_win_rate
        )


def test_outlier_filtering(sample_champions: list[Champion]) -> None:
    # Add an outlier champion with very low win rate
    sample_champions.append(Champion("TOP", "OutlierChamp", 35.0, 1.0, 1.0))

    analyzer = ChampionsAnalyzer(iter(sample_champions))
    updated_champions = analyzer.update_metrics()

    # Verify the outlier was filtered out
    assert all(
        champion.name != "OutlierChamp" for champion in updated_champions
    )
