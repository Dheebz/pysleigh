from typer.testing import CliRunner
from unittest.mock import patch, MagicMock
from pysleigh.cli.run import run_app

runner = CliRunner()


class TestAoCCliRun:
    @patch("pysleigh.cli.run.AoCDate")
    @patch("pysleigh.cli.run.AoCRunner")
    def test_run_solution(self, mock_runner, mock_date):
        mock_date.return_value = MagicMock()
        mock_runner.return_value.run_solution.return_value = {
            "part1": 1,
            "part2": 2,
            "time_part1": 0.1,
            "time_part2": 0.2,
        }
        result = runner.invoke(run_app, ["solution", "--year", "2022", "--day", "1"])
        assert result.exit_code == 0
        assert "Part 1:" in result.stdout

    @patch("pysleigh.cli.run.AoCTestRunner")
    def test_run_test_year(self, mock_runner):
        mock_runner.return_value.run_year_tests.return_value = True
        result = runner.invoke(run_app, ["test", "--year", "2022"])
        assert result.exit_code == 0
        assert "Tests passed" in result.stdout
