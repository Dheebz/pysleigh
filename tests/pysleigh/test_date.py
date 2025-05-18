import pytest
from unittest import mock

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from pysleigh.utils.date import AoCDate
from pysleigh.utils.date import AOC_OFFSET, MIN_YEAR, DECEMBER_INT, get_aoc_now, get_max_aoc_date


class TestAoCDate:
    # Testing of Constants
    class TestConstants:
        def test_constant_AOC_OFFSET(self):
            assert isinstance(AOC_OFFSET, ZoneInfo)
            assert AOC_OFFSET.key == "America/New_York"
            assert AOC_OFFSET.utcoffset(datetime(2023, 12, 1, 0, 0)) == timedelta(hours=-5)

        def test_constant_MIN_YEAR(self):
            assert isinstance(MIN_YEAR, int)
            assert MIN_YEAR == 2015

        def test_constant_DECEMBER_INT(self):
            assert isinstance(DECEMBER_INT, int)
            assert DECEMBER_INT == 12

    # Testing of non class methods
    class TestGetAocNow:
        def test_get_aoc_now(self):
            assert isinstance(get_aoc_now(), datetime)
            assert get_aoc_now().tzinfo == AOC_OFFSET
            offset = get_aoc_now().utcoffset().total_seconds()
            assert offset == (-5 * 60 * 60) or offset == (-4 * 60 * 60)

    class TestGetMaxAoCDate:
        def test_get_aoc_max_date_valid(self):
            rtn = get_max_aoc_date()
            assert isinstance(rtn, tuple)
            assert len(rtn) == 2
            assert isinstance(rtn[0], int) and isinstance(rtn[1], int)

            mock_dt = datetime(2022, 12, 4, tzinfo=ZoneInfo("America/New_York"))
            with mock.patch("pysleigh.utils.date.get_aoc_now", return_value=mock_dt):
                rtn_year, rtn_day = get_max_aoc_date()
                assert isinstance(rtn_year, int)
                assert isinstance(rtn_day, int)
                assert rtn_year == 2022
                assert rtn_day == 4

            mock_dt = datetime(2022, 11, 4, tzinfo=ZoneInfo("America/New_York"))
            with mock.patch("pysleigh.utils.date.get_aoc_now", return_value=mock_dt):
                rtn_year, rtn_day = get_max_aoc_date()
                assert isinstance(rtn_year, int)
                assert isinstance(rtn_day, int)
                assert rtn_year == 2021
                assert rtn_day == 25

    # Testing of Core Class
    class TestAoCDate:
        def test_aoc_date_valid_init(self):
            aoc_date = AoCDate(2015, 1)
            assert isinstance(aoc_date, AoCDate)
            assert aoc_date.year == 2015
            assert aoc_date.day == 1

        def test_aoc_date_invalid_init(self):
            # Future Year
            with pytest.raises(ValueError):
                future_year = datetime.now().year + 1
                AoCDate(future_year, 1)

            # Future Day
            with mock.patch("pysleigh.utils.date.datetime") as mock_datetime:
                mock_datetime.now.return_value = datetime(2015, 12, 1)
                with pytest.raises(ValueError):
                    AoCDate(2015, 10)
            # Past Day
            with pytest.raises(ValueError):
                AoCDate(2014, 1)

        def test_aoc_date_str(self):
            assert str(AoCDate(2015, 1)) == "2015-01"
            assert str(AoCDate(2015, 10)) == "2015-10"

        def test_aoc_date_repr(self):
            assert repr(AoCDate(2015, 1)) == "AoCDate(year=2015, day=01)"
            assert repr(AoCDate(2015, 10)) == "AoCDate(year=2015, day=10)"

    class TestAoCDateLogging:
        def test_aoc_date_logs_below_min_year(self, caplog):
            year = MIN_YEAR - 1
            expected = f"Year {year} is less than the minimum year {MIN_YEAR}."

            with caplog.at_level("ERROR"):
                with pytest.raises(ValueError):
                    year = MIN_YEAR - 1
                    AoCDate(year, 1)
            assert "ERROR" in caplog.text
            assert "pysleigh.utils.date" in caplog.text
            assert expected in caplog.text

        def test_aoc_date_logs_above_max_year(self, caplog):
            max_year, max_day = get_max_aoc_date()
            year = max_year + 1
            expected = f"Year {year} is greater than the maximum year {max_year}."
            with caplog.at_level("ERROR"):
                with pytest.raises(ValueError):
                    year = max_year + 1
                    AoCDate(year, 1)
            assert "ERROR" in caplog.text
            assert "pysleigh.utils.date" in caplog.text
            assert expected in caplog.text

        def test_aoc_date_logs_invalid_day(self, caplog):
            mock_dt = datetime(2022, 12, 15, tzinfo=ZoneInfo("America/New_York"))
            with mock.patch("pysleigh.utils.date.get_aoc_now", return_value=mock_dt):
                max_year, max_day = get_max_aoc_date()
                year = max_year
                day = max_day + 1
                expected = f"Day {day} is greater than the maximum day {max_day} for year {year}."
                with caplog.at_level("ERROR"):
                    with pytest.raises(ValueError):
                        AoCDate(2022, 16)
                assert "ERROR" in caplog.text
                assert "pysleigh.utils.date" in caplog.text
                assert expected in caplog.text
