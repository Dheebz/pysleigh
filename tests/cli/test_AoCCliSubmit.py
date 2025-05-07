from typer.testing import CliRunner
from unittest.mock import patch, MagicMock
import pysleigh.cli.main as cli_main

runner = CliRunner()

class TestAoCCliSubmit:
    @patch("pysleigh.cli.submit.AoCDate")
    @patch("pysleigh.cli.submit.AoCSubmitter")
    def test_submit_answer(self, mock_submitter, mock_date):
        mock_date.return_value = MagicMock()
        mock_instance = mock_submitter.return_value
        mock_instance.compute_answer.return_value = "42"
        mock_instance.submit.return_value = "<article><p>That's the right answer!</p></article>"
        mock_instance.parse_response.return_value = ("correct", "Great job!")

        result = runner.invoke(cli_main.main, [
            "submit", "answer", "--year", "2022", "--day", "1", "--part", "1"
        ])
        assert result.exit_code == 0
        assert "[CORRECT]" in result.stdout.upper()
