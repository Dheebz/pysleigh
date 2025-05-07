import importlib
import sys
from pathlib import Path
import time
import traceback
import os
import subprocess
from pysleigh.utilities.config import AoCConfig
from pysleigh.utilities.date import AoCDate
from pysleigh.utilities.logger import AoCLogger


class AoCRunner:
    logger = AoCLogger().get_logger()

    def __init__(
        self, aoc_date: AoCDate | None = None, config: AoCConfig | None = None
    ):
        self.aoc_date = aoc_date or AoCDate(*AoCDate._compute_max_date())
        self.config = config or AoCConfig()
        self.logger = AoCLogger().get_logger()

        sol_path_str = self.config.config.get("solutions", {}).get("path", "")
        if sol_path_str:
            sol_path = Path(sol_path_str).expanduser()
            if sol_path.exists() and str(sol_path) not in sys.path:
                sys.path.insert(0, str(sol_path))
                self.logger.debug(f"Added AoC solution path to sys.path: {sol_path}")
            else:
                self.logger.warning(
                    f"AoC solution path not found or already in sys.path: {sol_path}"
                )
        else:
            self.logger.warning("No solution path configured in [solutions.path]")

    def _get_module_name(self) -> str:
        return f"year_{self.aoc_date.year}.solution_{self.aoc_date.year}_day_{self.aoc_date.day:02d}"

    def _get_input_path(self) -> str:
        input_cfg = self.config.config.get("inputs", {})
        base_path = Path(input_cfg.get("path", "input/")).expanduser()
        fmt = input_cfg.get("format", "year_{year}/input_{year}_day_{day:02d}.txt")
        return str(
            base_path.joinpath(
                fmt.format(year=self.aoc_date.year, day=self.aoc_date.day)
            )
        )

    def run_solution(self) -> dict:
        module_name = self._get_module_name()
        input_path = self._get_input_path()

        self.logger.info(f"Running {module_name} with input: {input_path}")
        try:
            mod = importlib.import_module(module_name)
            solution = mod.Solution(input_path)

            t1 = time.perf_counter()
            part1 = solution.part1()
            t1_done = time.perf_counter()

            t2 = time.perf_counter()
            part2 = solution.part2()
            t2_done = time.perf_counter()

            return {
                "part1": part1,
                "part2": part2,
                "time_part1": t1_done - t1,
                "time_part2": t2_done - t2,
            }

        except Exception as e:
            self.logger.error(f"Error running solution: {e}")
            traceback.print_exc()
            return {}

    def run_tests(self) -> bool:
        test_cfg = self.config.config.get("tests", {})
        base_path = Path(test_cfg.get("path", "tests/python")).expanduser()
        fmt = test_cfg.get("format", "year_{year}/test_{year}_day_{day:02d}.py")
        test_path = base_path.joinpath(
            fmt.format(year=self.aoc_date.year, day=self.aoc_date.day)
        )

        if not test_path.exists():
            self.logger.warning(f"No test file found at {test_path}")
            return False

        self.logger.info(f"Running tests from {test_path}")

        # ✅ Inject PYTHONPATH for pytest subprocess
        sol_path_str = self.config.config.get("solutions", {}).get("path", "")
        sol_path = Path(sol_path_str).expanduser()
        env = {**os.environ, "PYTHONPATH": str(sol_path)}

        result = subprocess.run(
            ["pytest", str(test_path)], env=env, capture_output=False
        )
        return result.returncode == 0
