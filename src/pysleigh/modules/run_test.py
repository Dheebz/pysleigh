import subprocess
import os
import sys
from pathlib import Path
from typing import Optional

from pysleigh.utilities.config import AoCConfig
from pysleigh.utilities.date import AoCDate
from pysleigh.utilities.logger import AoCLogger


class AoCTestRunner:
    logger = AoCLogger().get_logger()

    def __init__(
        self, aoc_date: Optional[AoCDate] = None, config: Optional[AoCConfig] = None
    ):
        self.aoc_date = aoc_date
        self.config = config or AoCConfig()
        self.logger = AoCLogger().get_logger()

        # Ensure solution path is in sys.path and available for subprocess
        self.sol_path = Path(
            self.config.config.get("solutions", {}).get("path", "")
        ).expanduser()

        if self.sol_path.exists() and str(self.sol_path) not in sys.path:
            sys.path.insert(0, str(self.sol_path))
            self.logger.debug(f"Added AoC solution path to sys.path: {self.sol_path}")
        else:
            self.logger.warning(
                f"AoC solution path not found or already in sys.path: {self.sol_path}"
            )

    def _get_test_path(self) -> Optional[Path]:
        cfg = self.config.config.get("tests", {})
        base_path = Path(cfg.get("path", "tests/python")).expanduser()
        fmt = cfg.get("format", "year_{year}/test_{year}_day_{day:02d}.py")

        if self.aoc_date:
            rel = fmt.format(year=self.aoc_date.year, day=self.aoc_date.day)
            return base_path.joinpath(rel)
        return None

    def _run_pytest(self, path: Path) -> bool:
        env = {**os.environ, "PYTHONPATH": str(self.sol_path)}
        result = subprocess.run(["pytest", str(path)], env=env, capture_output=False)
        return result.returncode == 0

    def run_specific_test(self) -> bool:
        test_path = self._get_test_path()
        if test_path and test_path.exists():
            self.logger.info(f"Running test: {test_path}")
            return self._run_pytest(test_path)
        else:
            self.logger.warning(f"Test file not found: {test_path}")
            return False

    def run_year_tests(self, year: int) -> bool:
        cfg = self.config.config.get("tests", {})
        base_path = Path(cfg.get("path", "tests/python")).expanduser()
        year_path = base_path / f"year_{year}"

        if not year_path.exists():
            self.logger.warning(f"No tests found for year {year} at {year_path}")
            return False

        self.logger.info(f"Running all tests for {year} in {year_path}")
        return self._run_pytest(year_path)

    def run_all_tests(self) -> bool:
        cfg = self.config.config.get("tests", {})
        base_path = Path(cfg.get("path", "tests/python")).expanduser()
        if not base_path.exists():
            self.logger.error(f"Test directory not found: {base_path}")
            return False

        self.logger.info(f"Running all tests in {base_path}")
        return self._run_pytest(base_path)

    def run(self) -> bool:
        if self.aoc_date:
            return self.run_specific_test()
        return self.run_all_tests()
