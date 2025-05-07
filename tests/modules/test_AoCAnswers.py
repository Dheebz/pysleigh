import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path
from pysleigh.modules.answers import AoCAnswers
from pysleigh.utilities.date import AoCDate


@pytest.mark.unit
class TestAoCAnswers:
    def test_get_answers_path_uses_config(self, tmp_path):
        cfg = {
            "answers": {
                "path": str(tmp_path),
                "format": "custom/answer_{year}_{day}.txt",
            }
        }
        date = AoCDate(2022, 5)
        a = AoCAnswers(date, config=MagicMock(config=cfg))
        expected = tmp_path / "custom" / "answer_2022_5.txt"
        assert a.get_answers_path() == expected

    def test_check_local_true_if_file_exists(self, tmp_path):
        file = tmp_path / "answer.txt"
        file.write_text("Part 1: foo\nPart 2: bar")
        a = AoCAnswers(AoCDate(2022, 1))
        a.answers_path = file
        assert a.check_local()

    def test_read_local_parses_answers_correctly(self, tmp_path):
        file = tmp_path / "answers.txt"
        file.write_text("Part 1: 123\nPart 2: 456")
        a = AoCAnswers(AoCDate(2022, 1))
        a.answers_path = file
        result = a.read_local()
        assert result == {"part1": "123", "part2": "456"}

    def test_write_answers_creates_file(self, tmp_path):
        file = tmp_path / "a" / "b" / "answer.txt"
        a = AoCAnswers(AoCDate(2022, 1))
        a.answers_path = file
        a.write_answers({"part1": "aaa", "part2": "bbb"}, overwrite=True)
        assert file.read_text() == "Part 1: aaa\nPart 2: bbb"

    def test_fetch_answers_extracts_parts(self):
        html = """
        <p>Your puzzle answer was <code>one</code>.</p>
        <p>Your puzzle answer was <code>two</code>.</p>
        """
        with patch("pysleigh.utilities.session.AoCSession.get") as mock_get:
            mock_resp = MagicMock(status_code=200, text=html)
            mock_get.return_value = mock_resp
            a = AoCAnswers(AoCDate(2022, 1))
            result = a.fetch_answers()
            assert result == {"part1": "one", "part2": "two"}
