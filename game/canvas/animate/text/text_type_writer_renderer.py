from typing import Callable, cast

import pygame

from game.canvas.animate.text.font import Font
from game.canvas.animate.text.text_animation_tick_info import TickInfo
from game.canvas.animate.text.text_appear_renderer import TextAppearRenderer
from game.canvas.animate.text.text_instruction import (
    TextInstruction,
    TextInstructionType,
)
from game.canvas.animate.text.text_renderer_interface import (
    TextRendererInterface,
)
from game.utils.now import now


class TextTypeWriterRenderer(TextRendererInterface):
    """Wraps around a TextAppearRenderer, throttling character output."""

    def __init__(self, renderer: TextAppearRenderer) -> None:
        self.renderer = renderer
        self.instruction_queue: list[TextInstruction] = []
        self.wait_timer: float | None = None

    def slow_string(self, delay: float, next_string: str) -> None:
        """Queue up a slow string of characters."""
        for char in next_string:
            self.wait(delay)
            self.string(char)

    def string(self, next_string: str) -> None:
        """Queue up a string of characters."""
        for char in next_string:
            self.instruction_queue.append(
                TextInstruction(TextInstructionType.CHAR, char)
            )

    def draw(self, dst: pygame.Surface, x: int, y: int) -> bool:
        """Draw the text."""
        current_time = now()
        done_drawing = self.renderer.draw(dst, x, y)
        if self._is_waiting(current_time):
            return False  # Still waiting
        self._next_operation(current_time)
        if done_drawing:
            return len(self.instruction_queue) == 0  # Done drawing when queue is empty
        return False  # Still drawing

    def newline(self) -> None:
        """Queue up a newline."""
        self.instruction_queue.append(
            TextInstruction(
                TextInstructionType.NEWLINE,
            )
        )

    def font(self, font: Font) -> None:
        """Queue up a font change."""
        self.instruction_queue.append(TextInstruction(TextInstructionType.FONT, font))

    def color(self, r: int, g: int, b: int) -> None:
        """Queue up a color change."""
        self.instruction_queue.append(
            TextInstruction(TextInstructionType.COLOR, r, g, b)
        )

    def shake(self, func: Callable[[TickInfo], tuple[int, int]]) -> None:
        """Queue up a shake-function change."""
        self.instruction_queue.append(TextInstruction(TextInstructionType.SHAKE, func))

    def _next_operation(self, current_time: float) -> None:
        """Executes the queue up to the first printed character."""

        self.wait_timer = None
        while self.instruction_queue:
            op = self.instruction_queue.pop(0)
            match op.type:
                case TextInstructionType.CHAR:
                    self.renderer.string(op.get(0, str))
                    break
                case TextInstructionType.NEWLINE:
                    self.renderer.newline()
                case TextInstructionType.FONT:
                    self.renderer.font(op.get(0, Font))
                case TextInstructionType.COLOR:
                    self.renderer.color(op.get(0, int), op.get(1, int), op.get(2, int))
                case TextInstructionType.SHAKE:
                    self.renderer.shake(cast(Callable, op.parameters[0]))
                case TextInstructionType.WAIT:
                    self.wait_timer = current_time + op.get(0, float)
                case TextInstructionType.CUSTOM:
                    cast(Callable, op.parameters[0])()

    def _is_waiting(self, current_time: float) -> bool:
        return self.wait_timer is not None and current_time < self.wait_timer

    def skip(self) -> None:
        """Skip the whole queue."""
        current_time = now()
        while self.instruction_queue:
            self._next_operation(current_time)

    def wait(self, delay: float) -> None:
        """Queue up a delay."""
        self.instruction_queue.append(TextInstruction(TextInstructionType.WAIT, delay))

    def custom(self, func: Callable[[], None]) -> None:
        """Queue up a custom function call."""
        self.instruction_queue.append(TextInstruction(TextInstructionType.CUSTOM, func))
