from dataclasses import dataclass, field
from typing import Literal

from game.command.commands import Command


@dataclass
class SetBackdropCommand(Command):
    type: Literal["set_backdrop"] = "set_backdrop"
    backdrop: str = ""
    load_animation: dict[str, str | float | int] = field(default_factory=dict)
