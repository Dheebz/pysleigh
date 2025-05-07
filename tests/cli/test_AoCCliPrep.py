from typer.testing import CliRunner
from unittest.mock import patch, MagicMock
from pysleigh.cli.prep import prep_app

runner = CliRunner()


class TestAoCCliPrep:
    @patch("pysleigh.cli.prep._prep_day")
    def test_prep_solution_day(self, mock_prep_day):
        result = runner.invoke(prep_app, ["solution", "--year", "2022", "--day", "1"])
        assert result.exit_code == 0
        mock_prep_day.assert_called_once_with(2022, 1, False)

    @patch("pysleigh.cli.prep._prep_test_day")
    def test_prep_test_day(self, mock_prep_test):
        result = runner.invoke(prep_app, ["test", "--year", "2022", "--day", "1"])
        assert result.exit_code == 0
        mock_prep_test.assert_called_once_with(2022, 1, False)
