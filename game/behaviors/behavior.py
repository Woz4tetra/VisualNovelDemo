from abc import ABC, abstractmethod

from game.command import Command
from game.container import Container
from game.events.event import Event


class Behavior(ABC):
    def __init__(self, command: Command, container: Container) -> None:
        self.command = command
        self.container = container

    @abstractmethod
    def initialize(self) -> None: ...

    @abstractmethod
    def tick(self) -> Event: ...

    @abstractmethod
    def deinitialize(self) -> None: ...
