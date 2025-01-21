import math
import random

from game.canvas.animate.text.text_animation_tick_info import TickInfo


def jitter(info: TickInfo) -> tuple[int, int]:
    """Angry text motion."""
    x = int(info.font_size * random.random() * 0.25)
    y = int(info.font_size * random.random() * 0.25)
    return x, y


def singsong(info: TickInfo) -> tuple[int, int]:
    """Happy text motion."""
    x = int(info.font_size * math.cos(float(info.current_time + info.char_index) / 2))
    y = int(info.font_size * math.sin(float(info.current_time + info.char_index) / 2))
    return x, y
