from dataclasses import dataclass

from game.canvas.layout.shapes.shape_data import ShapeData


@dataclass
class TextData(ShapeData):
    x: float = 0.0
    y: float = 0.0
    dominant_baseline: str = ""
    text_anchor: str = ""
