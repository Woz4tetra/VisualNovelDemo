from game.command.commands import CommandType


class CommandSequenceCache:
    def __init__(self) -> None:
        self._cache = {}
        self.root: list[CommandType] | None = None

    def add(self, name: str, command_sequence: list[CommandType]) -> None:
        self._cache[name] = command_sequence
        if name == "root":
            self.root = command_sequence

    def get(self, name: str) -> list[CommandType]:
        return self._cache[name]

    def __len__(self) -> int:
        return len(self._cache)
