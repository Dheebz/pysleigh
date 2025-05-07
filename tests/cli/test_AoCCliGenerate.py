from typer.testing import CliRunner
from unittest.mock import patch, MagicMock
from pysleigh.cli.generate import generate_app

runner = CliRunner()


class TestAoCCliGenerate:
    @patch("pysleigh.cli.generate.AoCDate")
    @patch("pysleigh.cli.generate.AoCSolutionGenerator")
    def test_generate_solution(self, mock_gen, mock_date):
        mock_date.return_value = MagicMock()
        mock_gen.return_value.solution_path.read_text.return_value = "solution"
        result = runner.invoke(
            generate_app, ["solution", "--year", "2022", "--day", "1", "--show"]
        )
        assert result.exit_code == 0
        assert "solution" in result.stdout

    @patch("pysleigh.cli.generate.AoCDate")
    @patch("pysleigh.cli.generate.AoCTestGenerator")
    def test_generate_test(self, mock_gen, mock_date):
        mock_date.return_value = MagicMock()
        mock_gen.return_value.test_path.exists.return_value = True
        mock_gen.return_value.test_path.read_text.return_value = "test"
        result = runner.invoke(
            generate_app, ["test", "--year", "2022", "--day", "1", "--show"]
        )
        assert result.exit_code == 0
        assert "test" in result.stdout
