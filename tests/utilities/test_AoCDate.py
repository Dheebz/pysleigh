import pytest
from pysleigh.utilities.date import AoCDate, AOC_START_YEAR, AOC_MAX_DAY


@pytest.mark.unit
class TestAoCDate:
    def test_valid_date_initialization(self):
        d = AoCDate(2015, 1)
        assert d.year == 2015
        assert d.day == 1

    def test_year_before_start_logs_error(self, caplog):
        with caplog.at_level("ERROR"):
            AoCDate(2014, 1)
        assert "before AoC started" in caplog.text

    def test_day_out_of_bounds_low(self, caplog):
        with caplog.at_level("ERROR"):
            AoCDate(2020, 0)
        assert "out of bounds" in caplog.text

    def test_day_out_of_bounds_high(self, caplog):
        with caplog.at_level("ERROR"):
            AoCDate(2020, AOC_MAX_DAY + 1)
        assert "out of bounds" in caplog.text

    def test_future_year_logs_error(self, caplog):
        future_year = 3000
        with caplog.at_level("ERROR"):
            AoCDate(future_year, 1)
        assert "not yet unlocked" in caplog.text
