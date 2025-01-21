# inspired by https://github.com/ChillyCider/pmtext
from typing import Callable, cast

import pygame

from game.canvas.animate.text.font import Font
from game.canvas.animate.text.text_animation_tick_info import TickInfo
from game.canvas.animate.text.text_instruction import (
    TextInstruction,
    TextInstructionType,
)
from game.canvas.animate.text.text_renderer_interface import TextRendererInterface
from game.utils.now import now


class TextAppearRenderer(TextRendererInterface):
    def __init__(self, default_font: Font):
        self.instructions: list[TextInstruction] = []
        self.default_font = default_font
        self.tick_number = 0
        self.wait_timer: float | None = None

    def string(self, next_string: str) -> None:
        """Adds a string of characters to the text."""
        for char in next_string:
            self.instructions.append(TextInstruction(TextInstructionType.CHAR, char))

    def draw(self, dst: pygame.Surface, x: int, y: int) -> bool:
        """Draw the text."""
        current_time = now()
        cursor_x = x
        cursor_y = y
        font = self.default_font
        color = (255, 255, 255)
        shake = None
        char_index = 0  # For shake effects

        for op in self.instructions:
            tick_info = TickInfo(
                current_time, self.tick_number, char_index, font.get_linesize()
            )
            match op.type:
                case TextInstructionType.CHAR:
                    # The character we need to draw
                    ch = op.get(0, str)

                    # Offset by shake
                    off_x, off_y = 0, 0
                    if shake:
                        off_x, off_y = shake(tick_info)

                    # Draw it
                    font.draw_glyph(dst, cursor_x + off_x, cursor_y + off_y, color, ch)

                    # Advance the cursor
                    cursor_x += font.get_glyph_width(ch)
                    char_index += 1
                case TextInstructionType.NEWLINE:
                    cursor_x = x
                    cursor_y += font.get_linesize()
                case TextInstructionType.FONT:
                    font = op.get(0, Font)
                case TextInstructionType.COLOR:
                    color = (op.get(0, int), op.get(1, int), op.get(2, int))
                case TextInstructionType.SHAKE:
                    shake = cast(Callable, op.parameters[0])
                case TextInstructionType.CUSTOM:
                    cast(Callable, op.parameters[0])()

        return True  # Done drawing

    def newline(self) -> None:
        """Add a newline to the passage."""
        self.instructions.append(TextInstruction(TextInstructionType.NEWLINE))

    def font(self, font: Font) -> None:
        """Use a new font for this part of the passage."""
        self.instructions.append(TextInstruction(TextInstructionType.FONT, font))

    def color(self, r: int, g: int, b: int) -> None:
        """Use a new color for this part of the passage."""
        self.instructions.append(TextInstruction(TextInstructionType.COLOR, r, g, b))

    def shake(self, func: Callable[[TickInfo], tuple[int, int]]) -> None:
        """Use a shake function for this part of the passage."""
        self.instructions.append(TextInstruction(TextInstructionType.SHAKE, func))

    def wait(self, delay: float) -> None:
        """Queue up a delay."""
        self.instructions.append(TextInstruction(TextInstructionType.WAIT, delay))

    def skip(self) -> None:
        pass  # rendered in one frame, so no need to skip
