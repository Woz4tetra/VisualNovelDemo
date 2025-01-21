from dataclasses import dataclass, field
from enum import Enum
from typing import Literal

from game.command.commands import Command


@dataclass
class TextTypingProperties:
    type: Literal["typing"] = "typing"
    speed: float = 0.1


@dataclass
class TextAppearProperties:
    type: Literal["appear"] = "appear"


@dataclass
class TextFadeOutProperties:
    type: Literal["fade_out"] = "fade_out"
    duration: float = 1.0


TextAnimationProperties = (
    TextTypingProperties | TextFadeOutProperties | TextAppearProperties
)


class TextStyle(Enum):
    BOLD = "bold"
    ITALIC = "italic"
    JITTER = "jitter"
    SINGSONG = "singsong"


@dataclass
class TextSegmentProperties:
    text: str = ""
    color: str = ""
    styles: list[str] = field(default_factory=list)
    font: str = ""
    size: int = -1

    def get_styles(self) -> list[TextStyle]:
        return [TextStyle(style) for style in self.styles]


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
