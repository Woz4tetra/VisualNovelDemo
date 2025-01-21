from typing import Any

import pygame

from game.canvas.animate.animator import AnimationResult, Animator
from game.command.commands.text_command import TextCommand


def make_text_animator(
    commmand: TextCommand, data: dict[str, Any], screen_size: tuple[int, int]
) -> Animator:
    return TextAnimator(screen_size, commmand)


class TextAnimator(Animator):
    def __init__(self, screen_size: tuple[int, int], text_command: TextCommand) -> None:
        pass

    def initialize(self) -> None:
        pass

    def tick(self, events: tuple[pygame.event.Event, ...]) -> AnimationResult:
        return AnimationResult(finished=True)

    def deinitialize(self) -> None:
        pass
