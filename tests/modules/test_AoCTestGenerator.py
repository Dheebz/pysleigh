import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path
from pysleigh.modules.generate_test import AoCTestGenerator
from pysleigh.utilities.date import AoCDate


@pytest.mark.unit
class TestAoCTestGenerator:

    def test_get_test_path_uses_config(self, tmp_path):
        cfg = {
            "tests": {
                "path": str(tmp_path),
                "format": "Y{year}/test_{year}_{day}.py"
            }
        }
        gen = AoCTestGenerator(AoCDate(2022, 3), config=MagicMock(config=cfg))
        expected = tmp_path / "Y2022" / "test_2022_3.py"
        assert gen.get_test_path() == expected

    def test_check_local_detects_existence(self, tmp_path):
        f = tmp_path / "check.py"
        f.write_text("x")
        g = AoCTestGenerator(AoCDate(2022, 1))
        g.test_path = f
        assert g.check_local() is True

    def test_load_template_uses_fallback(self):
        g = AoCTestGenerator(AoCDate(2022, 1))
        g.template_path = Path("nonexistent")
        templ = g.load_template()
        assert "test_part1" in templ
        assert "{test_assert_1}" in templ

    def test_render_template_injects_answers(self):
        g = AoCTestGenerator(AoCDate(2022, 1))
        tmpl = "check {test_assert_1} and {test_assert_2}"
        rendered = g.render_template(tmpl, {"part1": "abc", "part2": "xyz"})
        assert 'assert str(result) == "abc"' in rendered
        assert 'assert str(result) == "xyz"' in rendered

    def test_write_test_creates_file(self, tmp_path):
        p = tmp_path / "t.py"
        g = AoCTestGenerator(AoCDate(2022, 1))
        g.test_path = p
        g.load_template = lambda: "TEMPLATE {test_assert_1}"
        g.render_template = lambda t, a: "assert 1"
        with patch("pysleigh.modules.generate_test.AoCAnswers.get_or_fetch", return_value={"part1": "1", "part2": "2"}):
            g.write_test(overwrite=True)
        assert "assert" in p.read_text()
