from dataclasses import dataclass
from typing import Literal

from game.command.commands import Command


@dataclass
class DelayCommand(Command):
    type: Literal["delay"] = "delay"
    duration: float = 0.0
