from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Literal

from game.command.commands import Command

from .delay_command import DelayCommand
from .play_sound_command import PlaySoundCommand
from .set_backdrop_command import SetBackdropCommand
from .text_command import TextCommand


class CompositeExitCondition(str, Enum):
    ALL = "all"
    ANY = "any"


@dataclass
class CompositeCommand(Command):
    type: Literal["composite"] = "composite"
    subcommands: list[
        CompositeCommand
        | DelayCommand
        | SetBackdropCommand
        | PlaySoundCommand
        | TextCommand
    ] = field(default_factory=list)
    exit_condition: CompositeExitCondition = CompositeExitCondition.ALL
