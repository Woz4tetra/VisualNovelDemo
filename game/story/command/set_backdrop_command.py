from dataclasses import dataclass
from typing import Literal

from game.story.command.command import Command


@dataclass
class SetBackdropCommand(Command):
    command: Literal["set_backdrop"] = "set_backdrop"
    backdrop: str = ""
