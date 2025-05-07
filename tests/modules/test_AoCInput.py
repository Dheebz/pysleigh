import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path
from pysleigh.modules.input import AoCInput
from pysleigh.utilities.date import AoCDate


@pytest.mark.unit
class TestAoCInput:
    def test_get_input_path_uses_config(self, tmp_path):
        config = {
            "inputs": {
                "path": str(tmp_path),
                "format": "y{year}/input_{year}_d{day}.txt",
            }
        }
        inp = AoCInput(AoCDate(2022, 2), config=MagicMock(config=config))
        expected = tmp_path / "y2022" / "input_2022_d2.txt"
        assert inp.get_input_path() == expected

    def test_check_local_true_if_file_exists(self, tmp_path):
        file = tmp_path / "input.txt"
        file.write_text("data")
        i = AoCInput(AoCDate(2022, 1))
        i.input_path = file
        assert i.check_local() is True

    def test_check_local_false_if_missing(self, tmp_path):
        file = tmp_path / "missing.txt"
        i = AoCInput(AoCDate(2022, 1))
        i.input_path = file
        assert i.check_local() is False

    def test_fetch_input_successful(self, monkeypatch):
        mock_resp = MagicMock(status_code=200, text="abc123")
        monkeypatch.setattr(
            "pysleigh.utilities.session.AoCSession.get",
            lambda self, url: mock_resp
        )
        i = AoCInput(AoCDate(2022, 1))
        result = i.fetch_input()
        assert result == "abc123"

    def test_fetch_input_fails_logs(self, monkeypatch, caplog):
        mock_resp = MagicMock(status_code=404)
        monkeypatch.setattr(
            "pysleigh.utilities.session.AoCSession.get",
            lambda self, url: mock_resp
        )
        i = AoCInput(AoCDate(2022, 1))
        result = i.fetch_input()
        assert result == ""
        assert "Failed to fetch input: 404" in caplog.text

    def test_write_input_creates_file(self, tmp_path, monkeypatch):
        file = tmp_path / "test.txt"
        monkeypatch.setattr(
            "pysleigh.modules.input.AoCInput.fetch_input", lambda self: "data"
        )
        i = AoCInput(AoCDate(2022, 1))
        i.input_path = file
        i.write_input(overwrite=True)
        assert file.read_text() == "data"

    def test_read_local_returns_content(self, tmp_path):
        file = tmp_path / "a.txt"
        file.write_text("hello world")
        i = AoCInput(AoCDate(2022, 1))
        i.input_path = file
        assert i.read_local() == "hello world"

    def test_get_or_fetch_reads_existing(monkeypatch, tmp_path):
        file = tmp_path / "i.txt"
        file.write_text("cached")
        i = AoCInput(AoCDate(2022, 1))
        i.input_path = file
        assert i.get_or_fetch() == "cached"






