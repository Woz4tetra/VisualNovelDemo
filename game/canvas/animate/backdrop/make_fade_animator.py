from typing import Any

import pygame

from game.canvas.animate.animator import Animator
from game.canvas.animate.backdrop.fade_animator import FadeAnimator
from game.canvas.animate.noop_animator import NoopAnimator
from game.command.commands.set_backdrop_command import (
    BackdropAppearProperties,
    BackdropFadeInProperties,
    BackdropFadeOutProperties,
    SetBackdropCommand,
)


def make_fade_animator(
    commmand: SetBackdropCommand, data: dict[str, Any], screen_size: tuple[int, int]
) -> Animator:
    properties = commmand.load_animation
    if isinstance(properties, BackdropFadeInProperties):
        is_fade_in = True
    elif isinstance(properties, BackdropFadeOutProperties):
        is_fade_in = False
    elif isinstance(properties, BackdropAppearProperties):
        return NoopAnimator()
    else:
        raise ValueError(f"Invalid fade type: {properties.type}")
    if not (new_backdrop := data.get("image", pygame.Surface)):
        raise ValueError("Missing next backdrop")
    return FadeAnimator(screen_size, properties.duration, is_fade_in, new_backdrop)
