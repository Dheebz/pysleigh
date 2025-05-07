import re
from pathlib import Path
from bs4 import BeautifulSoup

from pysleigh.utilities.config import AoCConfig
from pysleigh.utilities.logger import AoCLogger
from pysleigh.utilities.date import AoCDate
from pysleigh.utilities.session import AoCSession


class AoCAnswers:
    logger = AoCLogger().get_logger()
    DEFAULT_PATH = Path("~/Workspace/advent-of-code/answers")

    def __init__(
        self, aoc_date: AoCDate | None = None, config: AoCConfig | None = None
    ):
        self.aoc_date = aoc_date or AoCDate(*AoCDate._compute_max_date())
        self.config = config or AoCConfig()
        self.answers_path = self.get_answers_path()

        self.url = self._format_url()

    def _format_url(self) -> str:
        year = self.aoc_date.year
        day = self.aoc_date.day
        return f"https://adventofcode.com/{year}/day/{day}"

    def get_answers_path(self) -> Path:
        answer_cfg = self.config.config.get("answers", {})
        base_path = answer_cfg.get("path", str(self.DEFAULT_PATH))
        file_str = answer_cfg.get("format", "{year}/answer_{year}_day_{day:02d}.txt")
        rel_path = file_str.format(year=self.aoc_date.year, day=self.aoc_date.day)
        full_path = Path(base_path).expanduser().joinpath(rel_path)
        return full_path

    def check_local(self) -> bool:
        if self.answers_path.exists():
            self.logger.info(f"Local answer file found at {self.answers_path}")
            return True
        else:
            self.logger.info(f"Local answer file not found at {self.answers_path}")
            return False

    def fetch_answers(self) -> dict:
        session = AoCSession(self.config)
        response = session.get(self.url)
        if response.status_code != 200:
            self.logger.warning(f"Failed to fetch answers: {response.status_code}")
            return {}

        self.logger.info(
            f"Fetched HTML for {self.aoc_date.year} Day {self.aoc_date.day:02d}"
        )
        html = response.text
        soup = BeautifulSoup(html, "html.parser")

        answers = re.findall(
            r"<p>Your puzzle answer was <code>(.*?)</code>\.</p>", html
        )
        result = {
            "part1": answers[0] if len(answers) > 0 else None,
            "part2": answers[1] if len(answers) > 1 else None,
        }

        if self.aoc_date.day == 25:
            result["part2"] = "Merry Christmas!"

        self.logger.debug(f"Extracted answers: {result}")
        return result

    def format_answer(self, html: str) -> str:
        soup = BeautifulSoup(html, "html.parser")
        title = self.__extract_title(soup)
        header = self.__generate_header(title)
        answer = self.__extract_answer(soup)
        return f"{header}\n\n{answer}"

    def read_local(self) -> dict:
        try:
            content = self.answers_path.read_text()
            lines = content.strip().splitlines()
            result = {}
            for line in lines:
                if line.startswith("Part 1:"):
                    result["part1"] = line.split(":", 1)[1].strip()
                elif line.startswith("Part 2:"):
                    result["part2"] = line.split(":", 1)[1].strip()
            return result
        except FileNotFoundError:
            self.logger.error(f"Answer file not found: {self.answers_path}")
            return {}

    def write_answers(self, answers: dict, overwrite: bool = False) -> None:
        if self.check_local() and not overwrite:
            self.logger.info(
                "Answer file exists. Skipping write (use overwrite=True to force)."
            )
            return

        self.answers_path.parent.mkdir(parents=True, exist_ok=True)
        content = (
            f"Part 1: {answers.get('part1', '')}\nPart 2: {answers.get('part2', '')}"
        )
        self.answers_path.write_text(content.strip())
        self.logger.info(f"Answers written to {self.answers_path}")

    def get_or_fetch(self) -> dict:
        if self.check_local():
            return self.read_local()

        self.logger.info("Fetching answers because they were not found locally.")
        answers = self.fetch_answers()
        self.write_answers(answers)
        return answers
