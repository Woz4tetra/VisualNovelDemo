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
    magnitude = info.font_size * 0.1
    time_value = (info.current_time + info.char_index * 0.05) * 10.0
    x = int(magnitude * math.cos(time_value))
    y = int(magnitude * math.sin(time_value))
    return x, y
