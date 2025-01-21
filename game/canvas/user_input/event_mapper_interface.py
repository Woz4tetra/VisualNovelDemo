from abc import ABC, abstractmethod

import pygame

from game.canvas.user_input.user_event import UserEvent


class EventMapperInterface(ABC):
    @abstractmethod
    def parse(self, event: pygame.event.Event) -> UserEvent | None: ...
