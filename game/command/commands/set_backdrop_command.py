from dataclasses import dataclass, field
from typing import Literal

from game.command.commands import Command


@dataclass
class BackdropFadeInProperties:
    type: Literal["fade_in"] = "fade_in"
    duration: float = 0.0


@dataclass
class BackdropFadeOutProperties:
    type: Literal["fade_out"] = "fade_out"
    duration: float = 0.0


@dataclass
class BackdropAppearProperties:
    type: Literal["appear"] = "appear"


BackdropAnimationProperties = (
    BackdropFadeInProperties | BackdropFadeOutProperties | BackdropAppearProperties
)


@dataclass
class SetBackdropCommand(Command):
    type: Literal["set_backdrop"] = "set_backdrop"
    backdrop: str = ""
    load_animation: BackdropAnimationProperties = field(
        default_factory=BackdropAppearProperties
    )
