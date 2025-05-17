import os
import logging
import pytest
from io import StringIO
from datetime import datetime
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
        record.created = datetime(2023, 1, 1, 12, 0, 0).timestamp()
        formatted_time = formatter.format_time(record, "%Y/%m/%d %H-%M")
        assert formatted_time == "2023/01/01 12-00"
