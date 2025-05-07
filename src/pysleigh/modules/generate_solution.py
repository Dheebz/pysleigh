import re
from pathlib import Path
from datetime import date

from pysleigh.utilities.config import AoCConfig
from pysleigh.utilities.date import AoCDate
from pysleigh.utilities.logger import AoCLogger


class AoCSolutionGenerator:
    logger = AoCLogger().get_logger()
    DEFAULT_PATH = Path("~/Workspace/advent-of-code/solutions/python")

    def __init__(
        self, aoc_date: AoCDate | None = None, config: AoCConfig | None = None
    ):
        self.aoc_date = aoc_date or AoCDate(*AoCDate._compute_max_date())
        self.config = config or AoCConfig()
        self.solution_path = self.get_solution_path()
        self.template_path = self.get_template_path()

    def get_solution_path(self) -> Path:
        cfg = self.config.config.get("solutions", {})
        base_path = cfg.get("path", str(self.DEFAULT_PATH))
        format_str = cfg.get("format", "year_{year}/solution_{year}_day_{day:02d}.py")
        rel_path = format_str.format(year=self.aoc_date.year, day=self.aoc_date.day)
        return Path(base_path).expanduser().joinpath(rel_path)

    def get_template_path(self) -> Path:
        return Path(
            self.config.config.get("template", {}).get("solution_path", "")
        ).expanduser()

    def check_local(self) -> bool:
        exists = self.solution_path.exists()
        self.logger.info(
            f"{'Found' if exists else 'No'} local solution at {self.solution_path}"
        )
        return exists

    def load_template(self) -> str:
        if self.template_path and self.template_path.exists():
            return self.template_path.read_text()

        self.logger.warning("No custom solution template found. Using default.")

    def load_template(self) -> str:
        if self.template_path and self.template_path.exists():
            return self.template_path.read_text()

        self.logger.warning("No custom solution template found. Using default.")
        return (
            "from typing import List\n\n"
            "class Solution:\n"
            '    def __init__(self, input_path: str = "{input_path}") -> None:\n'
            '        with open(input_path, encoding="utf-8") as f:\n'
            "            self.raw_input: str = f.read()\n"
            "        self.data: List[str] = self.parse_input()\n\n"
            "    def parse_input(self) -> List[str]:\n"
            "        return self.raw_input.strip().splitlines()\n\n"
            "    def part1(self) -> int | str:\n"
            "        return NotImplemented\n\n"
            "    def part2(self) -> int | str:\n"
            "        return NotImplemented\n\n"
            "def main() -> None:\n"
            '    input_path = "{input_path}"\n'
            "    solution = Solution(input_path)\n"
            '    print("Part 1:", solution.part1())\n'
            '    print("Part 2:", solution.part2())\n\n'
            'if __name__ == "__main__":\n'
            "    main()\n"
        )

    def render_template(self, template: str) -> str:
        input_cfg = self.config.config.get("inputs", {})
        input_base = Path(input_cfg.get("path", "")).expanduser()
        input_fmt = input_cfg.get(
            "format", "year_{year}/input_{year}_day_{day:02d}.txt"
        )
        input_rel = input_fmt.format(year=self.aoc_date.year, day=self.aoc_date.day)
        full_input_path = input_base.joinpath(input_rel)

        substitutions = {
            "year": str(self.aoc_date.year),
            "day": f"{self.aoc_date.day:02d}",
            "date": date.today().isoformat(),
            "input_path": str(full_input_path),
        }

        def replace_var(match):
            key = match.group(1)
            return substitutions.get(key, match.group(0))

        return re.sub(r"{(\w+)}", replace_var, template)

    def write_solution(self, overwrite: bool = False) -> None:
        if self.check_local() and not overwrite:
            self.logger.info(
                "Solution file exists. Skipping write (use overwrite=True to force)."
            )
            return

        self.solution_path.parent.mkdir(parents=True, exist_ok=True)
        rendered = self.render_template(self.load_template())
        self.solution_path.write_text(rendered)
        self.logger.info(f"Solution written to {self.solution_path}")

    def get_or_generate(self) -> Path:
        if not self.check_local():
            self.write_solution(overwrite=False)
        return self.solution_path
