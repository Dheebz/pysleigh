import logging
import re
import pytest
from pysleigh.utilities.logger import AoCLogger, AoCFormatter


@pytest.mark.unit
class TestAoCLogger:
    def test_get_logger_returns_logger_instance(self):
        logger = AoCLogger().get_logger()
        assert isinstance(logger, logging.Logger)
        assert logger.name == "pysleigh"

    def test_logger_uses_aoc_formatter(self):
        logger = AoCLogger().get_logger()
        handler = logger.handlers[0]
        assert isinstance(handler.formatter, AoCFormatter)

    def test_formatter_output_structure(self, capfd):
        logger = AoCLogger("test_logger").get_logger()
        logger.info("hello world")

        out, err = capfd.readouterr()
        assert "hello world" in err
        assert re.match(
            r"\| \d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} \| test_logger \| .* \| .* \| hello world\n?",
            err.strip(),
        )
