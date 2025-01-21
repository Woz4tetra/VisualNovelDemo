from typing import Protocol


class CommandLineArgs(Protocol):
    story: str
    log_level: str
