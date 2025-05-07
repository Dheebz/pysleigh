from typer.testing import CliRunner
from unittest.mock import patch, MagicMock
from pysleigh.cli.benchmark import benchmark_app

runner = CliRunner()

class TestAoCCliBenchmark:
    @patch("pysleigh.cli.benchmark.AoCDate")
    @patch("pysleigh.cli.benchmark.AoCBenchmark")
    def test_benchmark_day(self, mock_benchmark, mock_date):
        mock_date.return_value = MagicMock()
        mock_instance = mock_benchmark.return_value
        mock_instance.benchmark_day.return_value = {"avg_part1": 0.001, "avg_part2": 0.002, "runs": 1}
        result = runner.invoke(benchmark_app, ["solution", "--year", "2015", "--day", "1", "--runs", "1"])
        assert result.exit_code == 0

    @patch("pysleigh.cli.benchmark.AoCDate")
    @patch("pysleigh.cli.benchmark.AoCBenchmark")
    def test_benchmark_year(self, mock_benchmark, mock_date):
        mock_date.return_value = MagicMock()
        mock_instance = mock_benchmark.return_value
        result = runner.invoke(benchmark_app, ["solution", "--year", "2015"])
        assert result.exit_code == 0

    @patch("pysleigh.cli.benchmark.AoCDate")
    @patch("pysleigh.cli.benchmark.AoCBenchmark")
    def test_benchmark_all(self, mock_benchmark, mock_date):
        mock_date.return_value = MagicMock()
        mock_instance = mock_benchmark.return_value
        result = runner.invoke(benchmark_app, ["solution"])
        assert result.exit_code == 0

    @patch("pysleigh.cli.benchmark.AoCDate")
    @patch("pysleigh.cli.benchmark.AoCBenchmark")
    def test_invalid_args(self, mock_benchmark, mock_date):
        mock_date.return_value = MagicMock()
        mock_instance = mock_benchmark.return_value
        mock_instance.benchmark_day.return_value = {}
        result = runner.invoke(benchmark_app, ["solution", "--year", "2015", "--day", "99"])
        assert result.exit_code == 0
