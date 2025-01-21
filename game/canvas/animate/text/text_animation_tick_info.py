from dataclasses import dataclass


@dataclass
class TickInfo:
    current_time: float
    tick_number: int
    char_index: int
    font_size: int
