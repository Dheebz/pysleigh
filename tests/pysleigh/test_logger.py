import logging
from unittest.mock import patch

from datetime import datetime, timezone
from pysleigh.utils.logger import AoCLogger, AoCLogFormatter, LEVEL_COLORS, LOG_FORMAT


class TestAoCLogger:
    def test_logger_singleton_behavior(self):
        logger1 = AoCLogger().get_logger("test_logger")
        logger2 = AoCLogger().get_logger("test_logger")
        assert logger1 is logger2

    def test_logger_creation_sets_handlers(self):
        logger = AoCLogger().get_logger("handler_logger")
        assert any(isinstance(h, logging.StreamHandler) for h in logger.handlers)
        assert logger.level == logging.INFO

    def test_logger_env_flag_sets_propagation(self, monkeypatch):
        monkeypatch.setenv("PYTEST_CURRENT_TEST", "true")
        logger = AoCLogger().get_logger("env_logger")
        assert logger.propagate is True

    def test_logger_env_flag_false(self, monkeypatch):
        monkeypatch.delenv("PYTEST_CURRENT_TEST", raising=False)
        logger = AoCLogger().get_logger("non_env_logger")
        assert logger.propagate is False

    def test_logger_set_level_affects_all_loggers(self):
        aoc = AoCLogger()
        logger = aoc.get_logger("level_logger")
        aoc.set_level(logging.DEBUG)
        assert logger.level == logging.DEBUG
        assert all(h.level == logging.DEBUG for h in logger.handlers)

    def test_logger_get_existing_logger_instance(self):
        aoc = AoCLogger()
        logger1 = aoc.get_logger("existing_logger")
        logger2 = aoc.get_logger("existing_logger")
        assert logger1 is logger2


class TestAoCLogFormatter:
    def test_color_formatting_per_level(self):
        formatter = AoCLogFormatter(LOG_FORMAT)
        record = logging.LogRecord(
            name="test",
            level=logging.ERROR,
            pathname="",
            lineno=0,
            msg="boom",
            args=(),
            exc_info=None,
            func="func",
        )
        record.created = datetime.now().timestamp()
        formatted = formatter.format(record)
        assert "boom" in formatted
        assert LEVEL_COLORS["ERROR"] in formatted

    def test_fallback_color_for_unknown_level(self):
        formatter = AoCLogFormatter(LOG_FORMAT)
        record = logging.LogRecord(
            name="test",
            level=42,
            pathname="",
            lineno=0,
            msg="strange",
            args=(),
            exc_info=None,
            func="func",
        )
        record.levelname = "UNKNOWN"
        record.created = datetime.now().timestamp()
        output = formatter.format(record)
        assert "strange" in output  # Even if level unknown, message should still appear

    def test_format_time_respects_date_format(self):
        formatter = AoCLogFormatter(LOG_FORMAT)
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="",
            lineno=0,
            msg="msg",
            args=(),
            exc_info=None,
            func="func",
        )

        # Use UTC 12:00 for clarity
        fixed_dt = datetime(2023, 12, 1, 12, 0, 0, tzinfo=timezone.utc)
        record.created = fixed_dt.timestamp()

        with patch("pysleigh.utils.logger.datetime") as mock_dt:
            mock_dt.fromtimestamp.return_value = fixed_dt
            mock_dt.now.return_value = fixed_dt
            mock_dt.strftime = datetime.strftime  # allow formatting
            mock_dt.astimezone.return_value = fixed_dt

            formatted_time = formatter.format_time(record, "%Y/%m/%d %H-%M")

        assert formatted_time == "2023/12/01 12-00"
