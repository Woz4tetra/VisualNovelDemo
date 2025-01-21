import pygame

from game.canvas.animate.animator import AnimationResult, Animator


class NoopAnimator(Animator):
    def __init__(self) -> None:
        pass

    def initialize(self) -> None:
        pass

    def tick(self, events: tuple[pygame.event.Event, ...]) -> AnimationResult:
        return AnimationResult(finished=True)

    def deinitialize(self) -> None:
        pass
