from dataclasses import dataclass
from typing import Literal

from game.command import Command


@dataclass
class SetBackdropCommand(Command):
    type: Literal["set_backdrop"] = "set_backdrop"
    backdrop: str = ""
