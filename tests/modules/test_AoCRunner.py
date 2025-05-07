import pytest
from unittest.mock import patch, MagicMock
from pysleigh.modules.run_solution import AoCRunner
from pysleigh.utilities.date import AoCDate


@pytest.mark.unit
class TestAoCRunner:

    def test_run_solution_imports_and_executes(self):
        date = AoCDate(2022, 1)
        runner = AoCRunner(aoc_date=date)

        fake_solution = MagicMock()
        fake_solution.part1.return_value = "one"
        fake_solution.part2.return_value = "two"

        mock_mod = MagicMock()
        mock_mod.Solution.return_value = fake_solution

        with patch("importlib.import_module", return_value=mock_mod):
            result = runner.run_solution()

        assert result["part1"] == "one"
        assert result["part2"] == "two"
        assert isinstance(result["time_part1"], float)
        assert isinstance(result["time_part2"], float)

    def test_run_solution_handles_failure(self):
        date = AoCDate(2022, 1)
        runner = AoCRunner(aoc_date=date)

        with patch("importlib.import_module", side_effect=ImportError("boom")):
            result = runner.run_solution()
            assert result == {}

    def test_run_tests_executes_pytest(self):
        date = AoCDate(2022, 1)
        runner = AoCRunner(aoc_date=date)

        with patch("pathlib.Path.exists", return_value=True), \
             patch("subprocess.run") as mock_run:
            mock_run.return_value.returncode = 0
            assert runner.run_tests() is True

    def test_run_tests_missing_file_logs_warning(self):
        date = AoCDate(2022, 1)
        runner = AoCRunner(aoc_date=date)

        with patch("pathlib.Path.exists", return_value=False):
            assert runner.run_tests() is False
