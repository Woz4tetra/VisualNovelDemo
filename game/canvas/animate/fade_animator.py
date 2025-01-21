import logging
import time

import pygame

from game.canvas.animate.animator import AnimationResult, Animator


def now() -> float:
    return time.monotonic()


class FadeAnimator(Animator):
    def __init__(
        self,
        screen_size: tuple[int, int],
        duration: float,
        is_fade_in: bool,
        surface: pygame.Surface,
    ) -> None:
        self.screen_size = screen_size
        self.duration = duration
        self.is_fade_in = is_fade_in
        self.start_time = 0.0
        self.logger = logging.getLogger(self.__class__.__name__)
        self.surface = pygame.transform.scale(surface, screen_size)

    def initialize(self) -> None:
        self.start_time = now()

    def tick(self, events: tuple[pygame.event.Event, ...]) -> AnimationResult:
        is_running = (elapsed := now() - self.start_time) < self.duration
        if not is_running:
            self.logger.debug("Fade complete")
            return AnimationResult(finished=True)
        alpha = int(255 * (elapsed / self.duration))
        if not self.is_fade_in:
            alpha = 255 - alpha
        self.surface.set_alpha(alpha)
        return AnimationResult(surface=self.surface)

    def deinitialize(self) -> None:
        pass
