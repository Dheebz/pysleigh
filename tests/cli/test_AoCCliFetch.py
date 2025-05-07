import pytest
from typer.testing import CliRunner
from unittest.mock import patch, MagicMock
from pysleigh.cli.fetch import fetch_app

runner = CliRunner()


class TestAoCCliFetch:
    def test_fetch_input(self):
        result = runner.invoke(fetch_app, ["input", "--year", "2022", "--day", "1"])
        assert result.exit_code == 0
        assert "Input available at" in result.stdout

    def test_fetch_article(self):
        result = runner.invoke(fetch_app, ["article", "--year", "2022", "--day", "1"])
        assert result.exit_code == 0
        assert "Article available at" in result.stdout

    def test_fetch_answers(self):
        result = runner.invoke(fetch_app, ["answer", "--year", "2022", "--day", "1"])
        assert result.exit_code == 0
        assert "Answers file available at" in result.stdout

    @patch("pysleigh.cli.fetch.AoCInput")
    def test_fetch_input_with_show(self, mock_input):
        mock_instance = mock_input.return_value
        mock_instance.read_local.return_value = "test input data"
        mock_instance.check_local.return_value = True

        result = runner.invoke(
            fetch_app, ["input", "--year", "2022", "--day", "1", "--show"]
        )
        assert result.exit_code == 0
        assert "Input available at" in result.stdout
        assert "test input data" in result.stdout

    def test_fetch_article_with_show(self):
        result = runner.invoke(
            fetch_app, ["article", "--year", "2022", "--day", "1", "--show"]
        )
        assert result.exit_code == 0
        assert "Article available at" in result.stdout
        assert (
            "# --- Advent of Code" in result.stdout
            or "## --- Part One ---" in result.stdout
        )

    def test_fetch_answers_with_show(self):
        result = runner.invoke(
            fetch_app, ["answer", "--year", "2022", "--day", "1", "--show"]
        )
        assert result.exit_code == 0
        assert "Answers file available at" in result.stdout
        assert "Part 1:" in result.stdout or "Part 2:" in result.stdout
