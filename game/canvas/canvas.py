import logging
from dataclasses import dataclass
from typing import Callable

import pygame

from game.canvas.animate.animation_definition import AnimationDefinition
from game.canvas.animate.animator import Animator
from game.canvas.animate.animator_keys import AnimatorKey
from game.canvas.animate.fade_animator import FadeAnimator


@dataclass
class ActiveAnimation:
    animator: Animator
    definition: AnimationDefinition


class Canvas:
    def __init__(self) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        if pygame.get_sdl_version()[0] == 2:
            pygame.mixer.pre_init(44100, 32, 2, 1024)
        pygame.init()

        if pygame.mixer and not pygame.mixer.get_init():
            self.logger.warning("Warning, no sound")
            pygame.mixer = None

        self.screen_size = (640, 480)
        self.screen_rect = pygame.Rect(0, 0, self.screen_size[0], self.screen_size[1])
        # Set the display mode
        winstyle = 0  # |FULLSCREEN
        bestdepth = pygame.display.mode_ok(self.screen_rect.size, winstyle, 32)
        self.screen = pygame.display.set_mode(
            self.screen_rect.size, winstyle, bestdepth
        )

        self.active_animators: list[ActiveAnimation] = []
        self.animators_builders: dict[
            AnimatorKey, Callable[[AnimationDefinition], Animator]
        ] = {
            AnimatorKey.FADE_IN: self.make_fade,
            AnimatorKey.FADE_OUT: self.make_fade,
        }
        self.animators: dict[AnimationDefinition, Animator] = {}
        self.backdrop: pygame.Surface | None = None

        # decorate the game window
        # icon = pygame.transform.scale(image, (32, 32))
        # pygame.display.set_icon(icon)
        pygame.display.set_caption("Visual Novel")
        pygame.mouse.set_visible(0)

        # fill with black
        self.screen.fill((0, 0, 0))

    def initialize(self) -> None:
        pass

    def tick(self) -> bool:
        pygame.display.flip()
        running = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT or not self.handle_event(event):
                running = False
                break
        if len(self.active_animators) != 0:
            self.draw_background()
        for active_anim in self.active_animators:
            result = active_anim.animator.tick()
            if result.surface:
                self.screen.blit(result.surface, result.destination)
            if result.finished:
                active_anim.animator.deinitialize()
                self.active_animators.remove(active_anim)
        return running

    def deinitialize(self) -> None:
        pygame.quit()

    def set_background(self, image: pygame.Surface) -> None:
        self.backdrop = pygame.transform.scale(image, self.screen_rect.size)
        self.draw_background()

    def draw_background(self) -> None:
        if self.backdrop:
            self.screen.blit(self.backdrop, (0, 0))
        else:
            self.screen.fill((0, 0, 0))

    def play_animation(self, animation_definition: AnimationDefinition) -> None:
        animation_type = animation_definition.type
        if animation_type not in self.animators:
            animator = self.animators_builders[animation_type](animation_definition)
            self.animators[animation_definition] = animator
        else:
            animator = self.animators[animation_definition]
        animator.initialize()
        self.active_animators.append(ActiveAnimation(animator, animation_definition))

    def get_active_animations(self) -> list[AnimationDefinition]:
        return [active.definition for active in self.active_animators]

    def make_fade(self, animation: AnimationDefinition) -> FadeAnimator:
        if animation.type == AnimatorKey.FADE_IN:
            is_fade_in = True
        elif animation.type == AnimatorKey.FADE_OUT:
            is_fade_in = False
        else:
            raise ValueError(f"Invalid fade type: {animation.type}")
        if not (duration := animation.get("duration", float)):
            raise ValueError("Missing duration")
        if not (new_backdrop := animation.get("surface", pygame.Surface)):
            raise ValueError("Missing next backdrop")
        return FadeAnimator(self.screen_size, duration, is_fade_in, new_backdrop)

    def hex_to_rgb(self, hex_color: str) -> tuple[int, int, int]:
        return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))  # type: ignore

    def handle_event(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.QUIT:
            return False
        return True
