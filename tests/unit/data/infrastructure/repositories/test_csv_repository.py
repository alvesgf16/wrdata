import csv
import tempfile
import unittest
from pathlib import Path

from hypothesis import given

from src.wrdata.data import Champion
from src.wrdata.data.infrastructure.repositories.csv_repository import (
    CSVChampionRepository,
)
from src.wrdata.exceptions import OutputError
from tests.strategies.champion_strategies import champions_list_strategy


class TestCSVChampionRepository(unittest.TestCase):

    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_csv_path = Path(self.temp_dir.name) / "test_champions.csv"
        self.repo = CSVChampionRepository(filepath=str(self.temp_csv_path))

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    @staticmethod
    def _get_data_rows(csv_path: Path) -> list[list[str]]:
        with csv_path.open("r", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader)
            return list(reader)

    @given(champions=champions_list_strategy())
    def test_save_writes_correct_number_of_rows(
        self, champions: list[Champion]
    ) -> None:
        self.repo.save(champions)
        rows = self._get_data_rows(self.temp_csv_path)
        self.assertEqual(len(rows), len(champions))

    @given(champions=champions_list_strategy(min_size=1, max_size=1))
    def test_save_writes_champion_fields_correctly(
        self, champions: list[Champion]
    ) -> None:
        self.repo.save(champions)
        rows = self._get_data_rows(self.temp_csv_path)
        row = rows[0]

        champ = champions[0]
        self.assertEqual(row[0], champ.lane.value)
        self.assertEqual(row[1], champ.name)
        self.assertEqual(float(row[2]), champ.win_rate)
        self.assertEqual(float(row[3]), champ.pick_rate)
        self.assertEqual(float(row[4]), champ.ban_rate)
        self.assertEqual(row[5], champ.ranked_tier.value)

    def test_save_with_empty_list(self) -> None:
        self.repo.save([])
        rows = self._get_data_rows(self.temp_csv_path)
        self.assertEqual(len(rows), 0)

    def test_save_raises_output_error_on_invalid_path(self) -> None:
        invalid_path = "/\x00invalid/path"
        repo = CSVChampionRepository(filepath=invalid_path)

        with self.assertRaises(OutputError) as context:
            repo.save([])

        self.assertIn(
            "Failed to write champions to CSV file", str(context.exception)
        )
