import logging
from typing import Any

import pygame

from game.canvas.animate.animator import AnimationResult, Animator
from game.canvas.animate.text import text_effects
from game.canvas.animate.text.font import TTF
from game.canvas.animate.text.text_appear_renderer import TextAppearRenderer
from game.canvas.animate.text.text_renderer_interface import TextRendererInterface
from game.canvas.animate.text.text_type_writer_renderer import TextTypeWriterRenderer
from game.canvas.user_input.user_event import UserEvent
from game.command.commands.text_command import (
    TextBubbleProperties,
    TextCommand,
    TextSegmentProperties,
    TextStyle,
    TextTypingProperties,
)
from game.utils.hex_to_color import hex_to_color
from game.utils.optional_pop import optional_pop


def make_text_animator(
    commmand: TextCommand, data: dict[str, Any], screen_size: tuple[int, int]
) -> Animator:
    return TextAnimator(screen_size, commmand)


class TextAnimator(Animator):
    def __init__(self, screen_size: tuple[int, int], text_command: TextCommand) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.screen_size = screen_size
        self.default_size = 30
        self.default_font_name = pygame.font.get_default_font()
        self.default_font = TTF(self.default_font_name, self.default_size)

        self.plain_text = "".join(
            [
                "".join([seg.text for seg in bubble.segments])
                for bubble in text_command.bubbles
            ]
        )
        self.effects = {
            TextStyle.JITTER: text_effects.jitter,
            TextStyle.SINGSONG: text_effects.singsong,
        }

        self.renderer = [
            self.make_formatted_text(bubble) for bubble in text_command.bubbles
        ]
        self.is_renderer_done = []

    def initialize(self) -> None:
        self.logger.debug(f"Showing text: {self.plain_text}")
        self.is_renderer_done = [False] * len(self.renderer)

    def tick(self, events: tuple[UserEvent, ...]) -> AnimationResult:
        screen = pygame.Surface(self.screen_size, pygame.SRCALPHA)
        screen.fill((0, 0, 0, 0))
        next_pressed = UserEvent.NEXT_DIALOG in events
        all_renderers_done = all(self.is_renderer_done)
        finished = False
        if all_renderers_done and next_pressed:
            finished = True
        for index, renderer in enumerate(self.renderer):
            status = renderer.draw(screen, 0, 0)
            if next_pressed:
                renderer.skip()
            self.is_renderer_done[index] = status
        return AnimationResult(finished=finished, surface=screen)

    def deinitialize(self) -> None:
        self.logger.debug(f"Text complete: {self.plain_text}")

    def make_formatted_text(
        self, bubble_config: TextBubbleProperties
    ) -> TextRendererInterface:
        appear_renderer = TextAppearRenderer(self.default_font)
        if isinstance(bubble_config.load_animation, TextTypingProperties):
            renderer = TextTypeWriterRenderer(appear_renderer)
        else:
            renderer = appear_renderer
        for text_segment in bubble_config.segments:
            self.apply_appear_render(text_segment, renderer)
            if isinstance(renderer, TextTypeWriterRenderer):
                if not isinstance(bubble_config.load_animation, TextTypingProperties):
                    raise Exception(f"Invalid animation configuration. {bubble_config}")
                self.apply_type_writer_render(
                    text_segment, bubble_config.load_animation, renderer
                )
            else:
                self.apply_text_render(text_segment, renderer)
        return renderer

    def apply_appear_render(
        self,
        text_segment: TextSegmentProperties,
        appear_renderer: TextAppearRenderer | TextTypeWriterRenderer,
    ) -> None:
        styles = text_segment.get_styles()
        color = hex_to_color(text_segment.color or "#000000")
        appear_renderer.color(*color)
        font_family_name = text_segment.font or self.default_font_name
        text_size = text_segment.size if text_segment.size != -1 else self.default_size
        bold = optional_pop(styles, TextStyle.BOLD) is not None
        italic = optional_pop(styles, TextStyle.ITALIC) is not None
        font_path = pygame.font.match_font(font_family_name, bold=bold, italic=italic)
        for style in styles:
            if style in self.effects:
                appear_renderer.shake(self.effects[style])
        font = TTF(font_path, text_size)
        appear_renderer.font(font)

    def apply_type_writer_render(
        self,
        text_segment: TextSegmentProperties,
        load_animation: TextTypingProperties,
        renderer: TextTypeWriterRenderer,
    ) -> None:
        renderer.slow_string(load_animation.speed, text_segment.text)

    def apply_text_render(
        self,
        text_segment: TextSegmentProperties,
        appear_renderer: TextAppearRenderer | TextTypeWriterRenderer,
    ) -> None:
        appear_renderer.string(text_segment.text)
