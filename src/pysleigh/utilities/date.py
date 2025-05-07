from typing import Tuple, Optional
from datetime import datetime
from zoneinfo import ZoneInfo
from pysleigh.utilities.logger import AoCLogger


AOC_START_YEAR: int = 2015
AOC_MAX_DAY: int = 25
AOC_TIMEZONE = ZoneInfo("America/New_York")
from zoneinfo import ZoneInfo


AOC_START_YEAR = 2015
AOC_MAX_DAY = 25
AOC_TIMEZONE = ZoneInfo("America/New_York")


class AoCDate:
    logger = AoCLogger().get_logger()

    def __init__(self, year: int, day: int):
        self.year = year
        self.day = day

        if not self._is_valid():
            self.logger.error(self._validation_message())

        self.logger.info(f"AoCDate initialized: year={year}, day={day}")

    @staticmethod
    def _compute_max_date() -> Tuple[int, int]:
        now = datetime.now(AOC_TIMEZONE)
        if now.month < 12:
            return now.year - 1, AOC_MAX_DAY
        return now.year, min(now.day, AOC_MAX_DAY)

    def _is_valid(self) -> bool:
        return self._validation_message() is None

    def _validation_message(self) -> Optional[str]:
        max_year, max_day = AoCDate._compute_max_date()
        if self.year < AOC_START_YEAR:
            return f"Year {self.year} is before AoC started ({AOC_START_YEAR})."
        if self.year > max_year:
            return f"Year {self.year} is not yet unlocked. Latest: {max_year}."
        if not (1 <= self.day <= AOC_MAX_DAY):
            return f"Day {self.day} is out of bounds. Must be 1–{AOC_MAX_DAY}."
        if self.year == max_year and self.day > max_day:
            return f"Day {self.day} is not yet available in {self.year}. Latest: {max_day}."
        return None
