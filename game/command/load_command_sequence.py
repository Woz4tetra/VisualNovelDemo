import json
from pathlib import Path
from typing import Any, TypeVar

from game.command import Command

T = TypeVar("T", bound=Command)


def parse_command(data_type: tuple[type[T], ...], data: dict[str, Any]) -> T:
    # if data_type is union, match based on the type field
    type_keys = {sub_type.type: sub_type for sub_type in data_type}
    for type_name, sub_type in type_keys.items():
        if type_name == data["type"]:
            return sub_type.from_dict(data)
    raise ValueError(f"Unknown type {data['type']}")


def load_command_sequence(data_type: tuple[type[T], ...], path: Path | str) -> list[T]:
    with open(path) as file:
        data = json.load(file)
    commands: list[T] = []
    for row in data:
        commands.append(parse_command(data_type, row))
    return commands
