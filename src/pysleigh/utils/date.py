"""
Custom date class for Advent of Code (AoC) challenges.

This module provides a class `AoCDate` that represents a date in the context of
Advent of Code challenges. It validates the year and day based on the current date
and the rules of Advent of Code. The class also provides a method to get the current
date in the AoC context.

Usage:
    from pysleigh.utils.date import AoCDate

    # Create an AoCDate object for December 25, 2023
    aoc_date = AoCDate(2023, 25)

    # Print the date
    print(aoc_date)  # Output: 2023-25

"""

from __future__ import annotations
from datetime import datetime
from zoneinfo import ZoneInfo

from pysleigh.utils.logger import aoc_logger

AOC_OFFSET: ZoneInfo = ZoneInfo("America/New_York")
MIN_YEAR: int = 2015
DECEMBER_INT: int = 12  # Because PLR2004 is stupid


# TODO: @Dheebz: Set a Cache Value for the max date
def get_max_aoc_date() -> tuple[int, int]:
    """
    Get the maximum valid AoC date based on the current date.

    This function calculates the maximum valid date for the AoCDate class based
    on the current date. If the current month is December, it returns the
    current year and day. Otherwise, it returns the previous year's December 25.
    This is because the AoC challenges typically start on December 1st and
    end on December 25th of the following year.

    Returns:
        AoCDate: The maximum valid AoC date.

    """
    now = get_aoc_now()
    year = now.year if now.month == DECEMBER_INT else now.year - 1
    day = now.day if now.month == DECEMBER_INT else 25
    return int(year), int(day)


# TODO: @Dheebz: Set a Cache Value for the max date
def get_aoc_now() -> datetime:
    """
    Get the current date and time in the AoC context.

    This function returns the current date and time adjusted to the AoC timezone
    (America/New_York). It is used to determine the maximum valid year and day for
    the AoCDate class.

    Returns:
        datetime: The current date and time in the AoC timezone.

    """
    return datetime.now(tz=AOC_OFFSET)


class AoCDate:
    """
    Custom date class for Advent of Code (AoC) challenges.

    This class represents a date in the context of Advent of Code challenges. It
    validates the year and day based on the current date and the rules of Advent
    of Code. The class also provides a method to get the current date in the AoC
    context.

    Attributes:
        year (int): The year of the AoC date.
        day (int): The day of the AoC date.

    Methods:
        _validate(year: int, day: int) -> bool:
            Validates the year and day against the current date and AoC rules.

    """

    def __init__(self, year: int, day: int) -> None:
        """
        Initialize the AoCDate object.

        Args:
            year (int): The year of the AoC date.
            day (int): The day of the AoC date.

        Raises:
            ValueError: If the year or day is out of range.

        """
        self.logger = aoc_logger.get_logger(__name__)
        self.now = get_aoc_now()
        self._validate(year, day)
        if not self._validate(year, day):
            max_year, max_day = get_max_aoc_date()
            msg = f"Invalid AoC date: {year}-{day}."
            msg = msg + f"Must be between {MIN_YEAR}-01 and {max_year}-{max_day}."
            self.logger.error(msg)
            raise ValueError(msg)
        self.year = year
        self.day = day

    def _validate(self, year: int, day: int) -> bool:
        """
        Validate the year and day against the current date and AoC rules.

        Args:
            year (int): The year of the AoC date.
            day (int): The day of the AoC date.

        Returns:
            bool: True if the year and day are valid, False otherwise.

        """
        max_year, max_day = get_max_aoc_date()
        if year < MIN_YEAR:
            msg = f"Year {year} is less than the minimum year {MIN_YEAR}."
            self.logger.error(msg)
            return False
        if year > max_year:
            msg = f"Year {year} is greater than the maximum year {max_year}."
            self.logger.error(msg)
            return False
        if year == max_year and day > max_day:
            msg = f"Day {day} is greater than the maximum day {max_day} for year {year}."
            self.logger.error(msg)
            return False
        return True

    def __str__(self) -> str:
        """
        Return a string representation of the AoCDate object.

        Returns:
            str: A string representation of the AoCDate object in the format YYYY-DD.

        """
        return f"{self.year:04d}-{self.day:02d}"

    def __repr__(self) -> str:
        """
        Return a string representation of the AoCDate object for debugging.

        Returns:
            str: A string representation of the AoCDate object.

        """
        return f"AoCDate(year={self.year:04d}, day={self.day:02d})"


# End of File: src/pysleigh/utils/date.py
