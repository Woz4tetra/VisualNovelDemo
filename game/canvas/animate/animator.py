from abc import ABC, abstractmethod
from dataclasses import dataclass

import pygame

from game.canvas.user_input.user_event import UserEvent


@dataclass
class AnimationResult:
    finished: bool = False
    surface: pygame.Surface | None = None
    destination: tuple[int, int] = (0, 0)


class Animator(ABC):
    @abstractmethod
    def initialize(self) -> None: ...

    @abstractmethod
    def tick(self, events: tuple[UserEvent, ...]) -> AnimationResult: ...

    @abstractmethod
    def deinitialize(self) -> None: ...
