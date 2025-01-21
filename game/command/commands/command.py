from __future__ import annotations

from typing import TypeVar

from game.dataclass_utils import from_dict, to_dict

T = TypeVar("T", bound="Command")


class Command:
    type: str

    @classmethod
    def from_dict(cls: type[T], data: dict) -> T:
        return from_dict(cls, data)

    def to_dict(self) -> dict:
        return to_dict(self)
