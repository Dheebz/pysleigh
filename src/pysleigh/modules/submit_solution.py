import re
import sys
from pathlib import Path
from pysleigh.utilities.config import AoCConfig
from pysleigh.utilities.date import AoCDate
from pysleigh.utilities.logger import AoCLogger
from pysleigh.utilities.session import AoCSession
import importlib


class AoCSubmitter:
    logger = AoCLogger().get_logger()

    def __init__(self, aoc_date: AoCDate, config: AoCConfig = None):
        self.aoc_date = aoc_date
        self.config = config or AoCConfig()
        self.session = AoCSession(self.config)

        sol_path_str = self.config.config.get("solutions", {}).get("path", "")
        if sol_path_str:
            sol_path = Path(sol_path_str).expanduser()
            if sol_path.exists() and str(sol_path) not in sys.path:
                sys.path.insert(0, str(sol_path))

        self.url = f"https://adventofcode.com/{aoc_date.year}/day/{aoc_date.day}/answer"

    def submit(self, part: int, answer: str) -> str:
        data = {"level": str(part), "answer": answer}
        response = self.session.post(self.url, data=data)
        if response.status_code == 200:
            return response.text
        else:
            self.logger.error(f"Failed to submit answer: HTTP {response.status_code}")
            return f"Error: HTTP {response.status_code}"

    def compute_answer(self, part: int) -> str:
        modname = f"year_{self.aoc_date.year}.solution_{self.aoc_date.year}_day_{self.aoc_date.day:02d}"
        mod = importlib.import_module(modname)
        solution = mod.Solution()
        return str(solution.part1() if part == 1 else solution.part2())

    def parse_response(self, html: str) -> tuple[str, str]:
        """Extracts and categorizes the AoC submission response and removes HTML tags."""
        match = re.search(r"<article><p>(.*?)</p>", html, re.DOTALL)
        raw_message = match.group(1).strip() if match else "Unknown response."

        # Strip HTML tags
        clean_message = re.sub(r"<.*?>", "", raw_message)

        if "That's the right answer" in clean_message:
            return "✅ CORRECT", clean_message
        if "That's not the right answer" in clean_message:
            return "❌ INCORRECT", clean_message
        if "Did you already complete it?" in clean_message:
            return "📎 ALREADY SUBMITTED", clean_message
        if "You gave an answer too recently" in clean_message:
            return "⏱ COOLDOWN", clean_message

        return "❗ UNKNOWN", clean_message
