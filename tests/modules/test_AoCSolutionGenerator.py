import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path
from pysleigh.modules.generate_solution import AoCSolutionGenerator
from pysleigh.utilities.date import AoCDate

@pytest.mark.unit
class TestAoCSolutionGenerator:

    def test_get_solution_path_uses_config(self, tmp_path):
        cfg = {
            "solutions": {
                "path": str(tmp_path),
                "format": "Y{year}/solution_{year}_{day}.py"
            }
        }
        gen = AoCSolutionGenerator(AoCDate(2022, 3), config=MagicMock(config=cfg))
        expected = tmp_path / "Y2022" / "solution_2022_3.py"
        assert gen.get_solution_path() == expected

    def test_check_local_true_if_file_exists(self, tmp_path):
        file = tmp_path / "s.py"
        file.write_text("print('ok')")
        gen = AoCSolutionGenerator(AoCDate(2022, 1))
        gen.solution_path = file
        assert gen.check_local() is True

    def test_load_template_returns_default(self):
        gen = AoCSolutionGenerator(AoCDate(2022, 1))
        gen.template_path = Path("nonexistent_file")
        template = gen.load_template()
        assert "def part1" in template
        assert "{input_path}" in template

    def test_render_template_substitutes_values(self):
        cfg = {
            "inputs": {
                "path": "~/aoc/input",
                "format": "year_{year}/input_{year}_day_{day:02d}.txt"
            }
        }
        gen = AoCSolutionGenerator(AoCDate(2022, 5), config=MagicMock(config=cfg))
        templ = "load from {input_path} for {day}/{year}"
        result = gen.render_template(templ)
        assert "2022" in result
        assert "05" in result
        assert str(Path("~/aoc/input").expanduser()) in result

    def test_write_solution_creates_file(self, tmp_path):
        path = tmp_path / "soln.py"
        gen = AoCSolutionGenerator(AoCDate(2022, 1))
        gen.solution_path = path
        gen.load_template = lambda: "placeholder"
        gen.render_template = lambda _: "output = 42"
        gen.write_solution(overwrite=True)
        assert path.read_text() == "output = 42"
