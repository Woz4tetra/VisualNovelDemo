import io
import logging
import re
from dataclasses import dataclass
from xml.dom import minidom

import pygame
import svgutils
from lxml import etree

from game.canvas.layout.shapes.rect_data import RectData
from game.canvas.layout.shapes.shape_data import ShapeData
from game.canvas.layout.shapes.text_data import TextData


@dataclass
class BubbleSearchResult:
    tag: str
    element: minidom.Element


def search_for_bubbles(node: minidom.Node) -> list[BubbleSearchResult]:
    """Recursively searches for all nodes with the contents [[...]] in an SVG layout.

    Args:
        node (minidom.Node): The root node to search from.

    Returns:
        list[minidom.Node]: A list of all nodes with the text [[...]].
    """
    bubbles = []
    if isinstance(node, minidom.Text):
        text = node.data.strip()
        match = re.search(r"\[\[(.*)\]\]", text)
        if match:
            tag = match.group(1)
            bubbles.append(BubbleSearchResult(tag, node.parentNode))
    for child in node.childNodes:
        bubbles.extend(search_for_bubbles(child))
    return bubbles


def remove_nodes(node: minidom.Node, nodes_to_remove: list[minidom.Node]) -> None:
    """Recursively removes nodes from an SVG layout.

    Args:
        node (minidom.Node): The root node to remove nodes from.
        nodes_to_remove (list[minidom.Node]): A list of nodes to remove.
    """
    for child in node.childNodes:
        if child in nodes_to_remove:
            node.removeChild(child)
        else:
            remove_nodes(child, nodes_to_remove)


def parse_attribute(attribute: str) -> int | float | str:
    try:
        return int(attribute)
    except ValueError:
        try:
            return float(attribute)
        except ValueError:
            return attribute


def load_pruned_svg(path: str) -> tuple[minidom.Document, list[BubbleSearchResult]]:
    with open(path) as file:
        svg = minidom.parse(file)
    bubbles = search_for_bubbles(svg)
    nodes_to_remove: list[minidom.Node] = [bubble.element for bubble in bubbles]
    remove_nodes(svg, nodes_to_remove)
    return svg, bubbles


def resize_to_screen(
    svg: minidom.Document, screen_size: tuple[int, int]
) -> pygame.Surface:
    doc = svgutils.transform.fromstring(svg.toxml())
    doc.set_size((str(screen_size[0]), str(screen_size[1])))
    resized_svg = etree.tostring(doc.root)
    surface = pygame.image.load(io.BytesIO(resized_svg))
    return surface


SVG_TAG_TO_SHAPE: dict[str, type[ShapeData]] = {
    "rect": RectData,
    "text": TextData,
}


def extract_shape_data(bubbles: list[BubbleSearchResult]) -> list[ShapeData]:
    shape_data: list[ShapeData] = []
    for bubble in bubbles:
        shape_class = SVG_TAG_TO_SHAPE.get(bubble.element.tagName)
        if shape_class is None:
            raise ValueError(f"Unsupported SVG tag: {bubble.element.tagName}")
        data = {}
        for key, value in bubble.element.attributes.items():
            key = key.replace("-", "_")
            data[key] = parse_attribute(value)
        data["tag"] = bubble.tag
        shape_data.append(shape_class.from_dict(data))
    return shape_data


def load_layout(
    path: str, screen_size: tuple[int, int]
) -> tuple[pygame.Surface, list[ShapeData]]:
    logger = logging.getLogger(__name__)
    logger.debug(f"Loading layout from {path}")

    svg, bubbles = load_pruned_svg(path)
    surface = resize_to_screen(svg, screen_size)
    shape_data = extract_shape_data(bubbles)

    return surface, shape_data
