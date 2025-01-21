import datetime
import logging
import sys


class GameLogFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:  # type: ignore[override]
        date = datetime.datetime.fromtimestamp(record.created)
        formatted_time = date.strftime("%Y-%m-%dT%H:%M:%S,%f")
        return f"[{record.levelname:<5}] {formatted_time} <{record.name}>\t: {record.getMessage()}"


class GameLogger(logging.Logger):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(GameLogFormatter())
        super().addHandler(handler)


def initialize(log_level: str) -> None:
    level_number = getattr(logging, log_level.upper(), None)
    if level_number is None:
        raise ValueError(
            f"Invalid log level: {log_level}. Valid log levels are: DEBUG, INFO, WARNING, ERROR, CRITICAL"
        )
    logging.setLoggerClass(GameLogger)

    logging.getLogger().setLevel(level_number)

    # clear handlers in case any libraries have added any handlers to the root logger
    logging.root.handlers = []

    # Do not keep track of processes to increase performance
    logging.logProcesses = False
