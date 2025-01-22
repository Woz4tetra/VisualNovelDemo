from dataclasses import dataclass

from game.canvas.layout.shapes.shape_data import ShapeData


@dataclass
class RectData(ShapeData):
    x: int
    y: int
    width: int
    height: int
    fill: str
    id: str
