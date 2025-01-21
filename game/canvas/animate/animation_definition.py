from dataclasses import dataclass
from typing import Any, Type, TypeVar, cast

from game.canvas.animate.animator_keys import AnimatorKey

T = TypeVar("T")


@dataclass
class AnimationDefinition:
    type: AnimatorKey
    parameters: dict[str, Any]

    def get(self, key: str, expected_type: Type[T]) -> T | None:
        if not isinstance(self.parameters[key], expected_type):
            raise ValueError(f"Invalid parameter {key}: {self.parameters[key]}")
        return cast(T, self.parameters[key])

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, AnimationDefinition):
            return False
        return self.type == other.type and self.parameters == other.parameters

    def __hash__(self) -> int:
        return hash((self.type, frozenset(self.parameters.items())))
