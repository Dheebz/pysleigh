# utilities/logging.py
import logging


class AoCFormatter(logging.Formatter):
    def format(self, record):
        dt = self.formatTime(record, "%Y-%m-%d %H:%M:%S")
        app = record.name
        mod = record.module
        func = record.funcName
        msg = record.getMessage()
        return f"| {dt} | {app} | {mod} | {func} | {msg}"


class AoCLogger:
    def __init__(self, name: str = "pysleigh", level: int = logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        if not self.logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(AoCFormatter())
            self.logger.addHandler(handler)

    def get_logger(self):
        return self.logger
