from abc import ABC, abstractmethod

from game.story.command.command import Command


class Behavior(ABC):
    def __init__(self, command: Command) -> None:
        self.command = command

    @abstractmethod
    def initialize(self) -> None: ...

    @abstractmethod
    def tick(self) -> None: ...

    @abstractmethod
    def deinitialize(self) -> None: ...
