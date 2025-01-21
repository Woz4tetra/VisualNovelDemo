import logging
from dataclasses import dataclass

import pygame

from game.canvas.animate.animation_definition import AnimationDefinition
from game.canvas.animate.animator import Animator
from game.canvas.animate.make_fade_animator import make_fade_animator
from game.canvas.animate.text_animator import make_text_animator
from game.command.commands.set_backdrop_command import SetBackdropCommand
from game.command.commands.text_command import TextCommand


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
        self.animators: dict[int, Animator] = {}
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
        user_events = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT or not self.handle_event(event):
                running = False
                break
            user_events.append(event)
        user_events_frozen = tuple(user_events)
        if len(self.active_animators) != 0:
            self.draw_background()
        for active_anim in self.active_animators:
            result = active_anim.animator.tick(user_events_frozen)
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
        definition_id = id(animation_definition)
        if definition_id not in self.animators:
            self.animators[definition_id] = self.make_animator(animation_definition)
        animator = self.animators[definition_id]
        animator.initialize()
        self.active_animators.append(ActiveAnimation(animator, animation_definition))

    def make_animator(self, animation_definition: AnimationDefinition) -> Animator:
        return {
            SetBackdropCommand: make_fade_animator,
            TextCommand: make_text_animator,
        }[type(animation_definition.properties)](
            animation_definition.properties, animation_definition.data, self.screen_size
        )

    def get_active_animations(self) -> list[AnimationDefinition]:
        return [active.definition for active in self.active_animators]

    def handle_event(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.QUIT:
            return False
        return True
