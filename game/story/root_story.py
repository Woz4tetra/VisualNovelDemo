from __future__ import annotations

from dataclasses import dataclass

from game.dataclass_utils import from_dict, to_dict


@dataclass
class RootStory:
    root: str
    stories: list[str]

    @classmethod
    def from_dict(cls, data: dict) -> RootStory:
        return from_dict(cls, data)

    def to_dict(self) -> dict:
        return to_dict(self)
