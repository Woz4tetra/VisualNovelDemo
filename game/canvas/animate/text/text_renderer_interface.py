from __future__ import annotations

from abc import ABC, abstractmethod

import pygame


class TextRendererInterface(ABC):
    @abstractmethod
    def draw(
        self, screen: pygame.Surface, location_x: int, location_y: int
    ) -> bool: ...

    @abstractmethod
    def skip(self) -> None: ...
