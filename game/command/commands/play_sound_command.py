from dataclasses import dataclass
from typing import Literal

from game.command.commands import Command


@dataclass
class PlaySoundCommand(Command):
    type: Literal["play_sound"] = "play_sound"
    sound: str = ""
    volume: float = 1.0
