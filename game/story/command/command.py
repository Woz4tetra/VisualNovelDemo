from __future__ import annotations

from dataclasses import dataclass

from game.dataclass_utils import from_dict, to_dict


@dataclass
class Command:
    @classmethod
    def from_dict(cls, data: dict) -> Command:
        return from_dict(cls, data)

    def to_dict(self) -> dict:
        return to_dict(self)
