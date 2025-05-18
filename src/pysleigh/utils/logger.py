"""
Custom logger for AoC (Advent of Code) solutions.

This logger uses colorama for colored output in the terminal.
It formats log messages with a specific structure and color codes based on the log level.

Usage:
    logger = AoCLogger().get_logger("my_module")
    logger.info("This is an info message.")
    logger.warning("This is a warning message.")
    logger.error("This is an error message.")
    logger.debug("This is a debug message.")


"""

from __future__ import annotations
import os
import sys
import logging
from datetime import datetime, timezone

from colorama import Fore, Style, init as colorama_init

"""
Custom logger for AoC (Advent of Code) solutions.

This logger uses colorama for colored output in the terminal.
It formats log messages with a specific structure and color codes based on the log level.

Usage:
    logger = AoCLogger().get_logger("my_module")
    logger.info("This is an info message.")
    logger.warning("This is a warning message.")
    logger.error("This is an error message.")
    logger.debug("This is a debug message.")
"""

# TODO: @Dheebz: Make Timestamps UTC timezone aware

colorama_init(autoreset=True)

LEVEL_COLORS: dict[str, str] = {
    "INFO": Style.BRIGHT + Fore.WHITE,
    "WARNING": Style.BRIGHT + Fore.YELLOW,
    "ERROR": Style.BRIGHT + Fore.RED,
    "CRITICAL": Style.BRIGHT + Fore.RED,
    "DEBUG": Style.BRIGHT + Fore.CYAN,
}

LOG_FORMAT: str = "| %(asctime)s | %(levelname)-5s | %(name)s | %(funcName)s | %(message)s"
DATE_FORMAT: str = "%Y-%m-%d %H:%M:%S"


class AoCLogFormatter(logging.Formatter):
    """
    Custom log formatter for AoC (Advent of Code) solutions.

    This formatter uses colorama for colored output in the terminal.
    It formats log messages with a specific structure and color codes based on the log level.

    Args:
        fmt (str): The format string for the log message.
        datefmt (str): The format string for the date and time.

    """

    def format_time(
        self,
        record: logging.LogRecord,
        datefmt: str | None = None,
    ) -> str | None:
        """
        Format the time of the log record.

        Args:
            record (logging.LogRecord): The log record to format.
            datefmt (Optional[str]): The format string for the date and time.

        Returns:
            str: The formatted time string.

        """
        dt = datetime.fromtimestamp(record.created).astimezone(timezone.utc)
        return dt.strftime(datefmt or DATE_FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record.

        Args:
            record (logging.LogRecord): The log record to format.

        Returns:
            str: The formatted log message.

        """
        color = LEVEL_COLORS.get(record.levelname, "")
        reset = Style.RESET_ALL
        base = super().format(record)
        return f"{color}{base}{reset}"


class AoCLogger:
    """
    Custom logger for AoC (Advent of Code) solutions.

    This logger uses colorama for colored output in the terminal.
    It formats log messages with a specific structure and color codes based on the log level.

    Args:
        level (int): The logging level for the logger. Default is logging.INFO.

    Attributes:
        level (int): The logging level for the logger.
        formatter (AoCLogFormatter): The log formatter for the logger.
        loggers (Dict[str, logging.Logger]): A dictionary of loggers by name.

    """

    def __init__(self, level: int = logging.INFO) -> None:
        """
        Initialize the AoCLogger.

        Args:
            level (int): The logging level for the logger. Default is logging.INFO.

        """
        self.level: int = level
        self.formatter: AoCLogFormatter = AoCLogFormatter(LOG_FORMAT)
        self.loggers: dict[str, logging.Logger] = {}

    def get_logger(self, name: str) -> logging.Logger:
        """
        Get a logger by name.

        If the logger does not exist, create it with the specified name.

        Args:
            name (str): The name of the logger.

        Returns:
            logging.Logger: The logger instance.

        """
        if name in self.loggers:
            return self.loggers[name]

        logger: logging.Logger = logging.getLogger(name)

        if not logger.handlers:
            handler = logging.StreamHandler(sys.stderr)

            handler.setFormatter(self.formatter)
            handler.setLevel(self.level)

            logger.setLevel(self.level)
            logger.addHandler(handler)

            if os.getenv("PYTEST_CURRENT_TEST"):
                logger.propagate = True
            else:
                logger.propagate = False

        self.loggers[name] = logger
        return logger

    def set_level(self, level: int) -> None:
        """
        Set the logging level for all loggers.

        Args:
            level (int): The logging level to set.

        """
        self.level = level
        for logger in self.loggers.values():
            logger.setLevel(level)
            for handler in logger.handlers:
                handler.setLevel(level)


# Singleton instance
aoc_logger: AoCLogger = AoCLogger()

# End of File: src/pysleigh/utils/logger.py
