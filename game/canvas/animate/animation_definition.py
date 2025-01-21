from dataclasses import dataclass, field
from typing import Any

from game.command.commands.set_backdrop_command import SetBackdropCommand
from game.command.commands.text_command import TextCommand


@dataclass
class AnimationDefinition:
    properties: SetBackdropCommand | TextCommand
    data: dict[str, Any] = field(default_factory=dict)
