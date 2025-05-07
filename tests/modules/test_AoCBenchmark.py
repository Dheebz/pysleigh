import pytest
from unittest.mock import patch, MagicMock
from pysleigh.modules.benchmark import AoCBenchmark
from pysleigh.utilities.date import AoCDate


@pytest.mark.unit
class TestAoCBenchmark:

    @patch("pysleigh.modules.benchmark.importlib.import_module")
    @patch("pysleigh.modules.benchmark.AoCAnswers")
    def test_benchmark_day_returns_timings(self, MockAnswers, mock_import):
        benchmark = AoCBenchmark(AoCDate(2024, 2), runs=2)

        # Mock solution module
        fake_mod = MagicMock()
        sol = MagicMock()
        sol.part1.return_value = "abc"
        sol.part2.return_value = "def"
        fake_mod.Solution.side_effect = lambda _: sol
        mock_import.return_value = fake_mod

        # Mock AoCAnswers
        mock_ans = MockAnswers.return_value
        mock_ans.get_or_fetch.return_value = {"part1": "abc", "part2": "def"}
        mock_ans.check_local.return_value = False
        mock_ans.answers_path = None

        result = benchmark.benchmark_day(2024, 2)
        assert result["avg_part1"] > 0
        assert result["avg_part2"] > 0
        assert result["runs"] == 2



    def test_benchmark_day_skips_on_mismatch(self, caplog):
        benchmark = AoCBenchmark(AoCDate(2022, 1), runs=1)

        sol = MagicMock()
        sol.part1.return_value = "wrong"
        sol.part2.return_value = "def"
        fake_mod = MagicMock(Solution=lambda _: sol)

        with patch("pysleigh.modules.benchmark.importlib.import_module", return_value=fake_mod), \
             patch("pysleigh.modules.benchmark.AoCAnswers.get_or_fetch", return_value={"part1": "abc", "part2": "def"}):
            result = benchmark.benchmark_day(2022, 1)
            assert result == {}
            assert "Mismatch" in caplog.text

    def test_benchmark_day_logs_on_failure(self, caplog):
        benchmark = AoCBenchmark(AoCDate(2022, 1))

        with patch("pysleigh.modules.benchmark.importlib.import_module", side_effect=ImportError("boom")):
            result = benchmark.benchmark_day(2022, 1)
            assert result == {}
            assert "Benchmark failed" in caplog.text
