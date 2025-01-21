from dataclasses import dataclass
from typing import Literal

from game.command.commands import Command


@dataclass
class TransitionToSequenceCommand(Command):
    type: Literal["transition_to_sequence"] = "transition_to_sequence"
    sequence: str = ""
