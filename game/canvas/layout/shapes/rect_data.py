from dataclasses import dataclass

from game.canvas.layout.shapes.shape_data import ShapeData


@dataclass
class RectData(ShapeData):
    x: int = 0
    y: int = 0
    width: int = 0
    height: int = 0
    fill: str = ""
