from abc import ABC, abstractmethod
from dataclasses import dataclass

import pygame


@dataclass
class AnimationResult:
    finished: bool = False
    surface: pygame.Surface | None = None
    destination: tuple[int, int] = (0, 0)


class Animator(ABC):
    @abstractmethod
    def initialize(self) -> None: ...

    @abstractmethod
    def tick(self, events: tuple[pygame.event.Event, ...]) -> AnimationResult: ...

    @abstractmethod
    def deinitialize(self) -> None: ...
