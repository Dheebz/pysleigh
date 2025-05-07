from pathlib import Path
from datetime import date

from pysleigh.utilities.config import AoCConfig
from pysleigh.utilities.date import AoCDate
from pysleigh.utilities.logger import AoCLogger
from pysleigh.modules.answers import AoCAnswers


class AoCTestGenerator:
    logger = AoCLogger().get_logger()
    DEFAULT_PATH = Path("~/Workspace/advent-of-code/tests/python")

    def __init__(
        self, aoc_date: AoCDate | None = None, config: AoCConfig | None = None
    ):
        self.aoc_date = aoc_date or AoCDate(*AoCDate._compute_max_date())
        self.config = config or AoCConfig()
        self.test_path = self.get_test_path()
        self.template_path = self.get_template_path()

    def get_test_path(self) -> Path:
        cfg = self.config.config.get("tests", {})
        base_path = cfg.get("path", str(self.DEFAULT_PATH))
        format_str = cfg.get("format", "year_{year}/test_{year}_day_{day:02d}.py")
        rel_path = format_str.format(year=self.aoc_date.year, day=self.aoc_date.day)
        return Path(base_path).expanduser().joinpath(rel_path)

    def get_template_path(self) -> Path:
        return Path(
            self.config.config.get("template", {}).get("test_path", "")
        ).expanduser()

    def check_local(self) -> bool:
        exists = self.test_path.exists()
        self.logger.info(
            f"{'Found' if exists else 'No'} local test at {self.test_path}"
        )
        return exists

    def load_template(self) -> str:
        if self.template_path and self.template_path.exists():
            return self.template_path.read_text()

        self.logger.warning("No custom test template found. Using default.")
        return (
            "from pathlib import Path\n"
            "from year_{year}.solution_{year}_day_{day:02d} import Solution\n\n"
            "class TestSolution_{year}_{day:02d}:\n"
            "    def setup_method(self):\n"
            "        root = Path(__file__).resolve().parents[5]  # Adjust to point to AoC repo root\n"
            '        self.input_path = str(root / "input" / "year_{year}" / "input_{year}_day_{day:02d}.txt")\n'
            "        self.solution = Solution(self.input_path)\n\n"
            "    def test_part1(self):\n"
            "        result = self.solution.part1()\n"
            "        {test_assert_1}\n\n"
            "    def test_part2(self):\n"
            "        result = self.solution.part2()\n"
            "        {test_assert_2}\n"
        )

    def render_template(self, template: str, answers: dict) -> str:
        def answer_assert(key):
            val = answers.get(key)
            return f'assert str(result) == "{val}"'

        substitutions = {
            "year": self.aoc_date.year,
            "day": self.aoc_date.day,
            "date": date.today().isoformat(),
            "test_assert_1": answer_assert("part1"),
            "test_assert_2": answer_assert("part2"),
        }

        return template.format(**substitutions)

    def write_test(self, overwrite: bool = False) -> None:
        if self.check_local() and not overwrite:
            self.logger.info(
                "Test file exists. Skipping write (use overwrite=True to force)."
            )
            return

        answers = AoCAnswers(self.aoc_date, self.config).get_or_fetch()
        if not answers.get("part1") or not answers.get("part2"):
            self.logger.warning(
                "Both answers must be known to generate tests. Skipping."
            )
            return

        self.test_path.parent.mkdir(parents=True, exist_ok=True)
        rendered = self.render_template(self.load_template(), answers)
        self.test_path.write_text(rendered)
        self.logger.info(f"Test file written to {self.test_path}")

    def get_or_generate(self) -> Path:
        if not self.check_local():
            self.write_test(overwrite=False)
        return self.test_path
