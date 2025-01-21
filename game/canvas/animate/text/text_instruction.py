from enum import Enum, auto
from typing import Any, TypeVar

T = TypeVar("T")


class TextInstructionType(Enum):
    CHAR = auto()
    NEWLINE = auto()
    FONT = auto()
    COLOR = auto()
    SHAKE = auto()
    WAIT = auto()
    CUSTOM = auto()


class TextInstruction:
    def __init__(self, type: TextInstructionType, *parameters: Any) -> None:
        self.type = type
        self.parameters = parameters

    def get(self, index: int, expected_type: type[T]) -> T:
        value = self.parameters[index]
        if not isinstance(value, expected_type):
            raise TypeError(f"Expected {expected_type}, got {type(value)}")
        return value
