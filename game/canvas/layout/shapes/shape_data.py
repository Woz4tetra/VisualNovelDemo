from __future__ import annotations

from dataclasses import dataclass
from typing import TypeVar

from game.dataclass_utils import from_dict, to_dict

T = TypeVar("T", bound="ShapeData")


@dataclass
class ShapeData:
    tag: str

    @classmethod
    def from_dict(cls: type[T], data: dict) -> T:
        return from_dict(cls, data, strict=False)

    def to_dict(self) -> dict:
        return to_dict(self)
