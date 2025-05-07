import sys
import time
from statistics import mean
from pathlib import Path
import importlib

from pysleigh.utilities.config import AoCConfig
from pysleigh.utilities.date import AoCDate
from pysleigh.utilities.logger import AoCLogger
from pysleigh.modules.answers import AoCAnswers


class AoCBenchmark:
    logger = AoCLogger().get_logger()

    def __init__(
        self,
        aoc_date: AoCDate | None = None,
        config: AoCConfig | None = None,
        runs: int = 5,
    ):
        self.aoc_date = aoc_date
        self.config = config or AoCConfig()
        self.runs = runs

        # Ensure AoC solutions are in sys.path
        sol_path_str = self.config.config.get("solutions", {}).get("path", "")
        if sol_path_str:
            sol_path = Path(sol_path_str).expanduser()
            if sol_path.exists() and str(sol_path) not in sys.path:
                sys.path.insert(0, str(sol_path))

    def _get_module_name(self, year: int, day: int) -> str:
        return f"year_{year}.solution_{year}_day_{day:02d}"

    def _get_input_path(self, year: int, day: int) -> str:
        input_cfg = self.config.config.get("inputs", {})
        base_path = Path(input_cfg.get("path", "input/"))
        fmt = input_cfg.get("format", "year_{year}/input_{year}_day_{day:02d}.txt")
        return str(base_path.expanduser().joinpath(fmt.format(year=year, day=day)))

    def benchmark_day(self, year: int, day: int) -> dict:
        module_name = self._get_module_name(year, day)
        input_path = self._get_input_path(year, day)
        aoc_date = AoCDate(year, day)

        try:
            mod = importlib.import_module(module_name)
            times_part1 = []
            times_part2 = []

            # Always instantiate fresh solutions
            expected = AoCAnswers(aoc_date, self.config).get_or_fetch()
            first_solution = mod.Solution(input_path)

            actual1 = str(first_solution.part1())
            actual2 = str(first_solution.part2())

            if actual1 != str(expected.get("part1")) or actual2 != str(
                expected.get("part2")
            ):
                self.logger.error(
                    f"Mismatch on {year}-Day{day:02d}. Skipping benchmark."
                )
                return {}

            # Benchmark 1st run
            t1 = time.perf_counter()
            first_solution.part1()
            times_part1.append(time.perf_counter() - t1)

            t2 = time.perf_counter()
            first_solution.part2()
            times_part2.append(time.perf_counter() - t2)

            for _ in range(self.runs - 1):
                solution = mod.Solution(input_path)

                t1 = time.perf_counter()
                solution.part1()
                t1_done = time.perf_counter()
                times_part1.append(t1_done - t1)

                t2 = time.perf_counter()
                solution.part2()
                t2_done = time.perf_counter()
                times_part2.append(t2_done - t2)

            avg1 = mean(times_part1)
            avg2 = mean(times_part2)

            self.logger.info(
                f"{year}-Day{day:02d} Benchmark Passed over {self.runs} runs: Part1 {avg1:.6f}s, Part2 {avg2:.6f}s"
            )
            return {
                "year": year,
                "day": day,
                "avg_part1": round(avg1, 6),
                "avg_part2": round(avg2, 6),
                "runs": self.runs,
            }

        except Exception as e:
            self.logger.error(f"Benchmark failed for {year}-Day{day:02d}: {e}")
            return {}

    def benchmark_year(self, year: int):
        for day in range(1, 26):
            self.benchmark_day(year, day)

    def benchmark_all(self):
        for year in range(2015, AoCDate._compute_max_date()[0] + 1):
            self.benchmark_year(year)

    def benchmark(self) -> dict:
        if self.aoc_date:
            return self.benchmark_day(self.aoc_date.year, self.aoc_date.day)
        return {}
