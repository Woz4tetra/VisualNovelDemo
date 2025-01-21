from dataclasses import dataclass, field
from typing import Literal

from game.command.commands import Command


@dataclass
class TextTypingProperties:
    type: Literal["typing"] = "typing"
    speed: float = 1.0


@dataclass
class TextFadeOutProperties:
    type: Literal["fade_out"] = "fade_out"
    duration: float = 1.0


TextAnimationProperties = TextTypingProperties | TextFadeOutProperties


@dataclass
class TextSegmentProperties:
    text: str = ""
    color: str = ""
    styles: list[str] = field(default_factory=list)


@dataclass
class TextBubbleProperties:
    segments: list[TextSegmentProperties] = field(default_factory=list)
    load_animation: TextAnimationProperties | None = None
    unload_animation: TextAnimationProperties | None = None


@dataclass
class TextCommand(Command):
    type: Literal["text"] = "text"
    style: str = ""
    bubbles: list[TextBubbleProperties] = field(default_factory=list)
