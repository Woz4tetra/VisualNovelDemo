from typing import Protocol

from game.events.event import Event


class BehaviorInterface(Protocol):
    def initialize(self) -> None: ...

    def tick(self) -> Event: ...

    def deinitialize(self) -> None: ...
