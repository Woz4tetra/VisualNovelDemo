import logging

import pygame

from game.assets.paths import ASSETS, load_path_cache

SUPPORTED_IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".bmp", ".gif")


def load_image(path: str) -> pygame.Surface:
    logger = logging.getLogger(__name__)
    logger.debug(f"Loading image from {path}")

    try:
        surface = pygame.image.load(path).convert()
    except pygame.error as e:
        raise SystemExit(f'Could not load image "{path}" {pygame.get_error()}') from e
    return surface


def make_solid_color_image(color: str) -> pygame.Surface:
    logger = logging.getLogger(__name__)
    logger.debug(f"Creating solid color image with {color}")

    if len(color) != 7 or color[0] != "#":
        raise ValueError(f"Invalid color format: {color}")
    try:
        surface = pygame.Surface((1, 1))
        surface.fill(pygame.Color(color))
    except ValueError as e:
        raise ValueError(f"Invalid color: {color}") from e
    return surface


class ImageAssetCache:
    def __init__(self) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self._cache = {}
        self._path_cache = load_path_cache(ASSETS, SUPPORTED_IMAGE_EXTENSIONS)
        self.logger.debug(
            f"Loaded {len(self._path_cache)} image path{'' if len(self._path_cache) == 1 else 's'}"
        )

    def get(self, name: str) -> pygame.Surface:
        if not name:
            raise ValueError("Image name cannot be empty")
        if name[0] == "#":
            return make_solid_color_image(name)
        if name not in self._cache:
            path = self._path_cache.get(name)
            if path is None:
                raise FileNotFoundError(f'Could not find image "{name}"')
            self.logger.debug(f"Loading image {name} -> {path}")
            self._cache[name] = load_image(path)
            self.logger.debug(f"Loaded image {name}")
        return self._cache[name]
