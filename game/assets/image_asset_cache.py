import logging

import pygame

from game.assets.paths import ASSETS

SUPPORTED_IMAGE_EXTENSIONS = [".png", ".jpg", ".jpeg", ".bmp", ".gif"]


def load_image(path: str) -> pygame.Surface:
    logger = logging.getLogger(__name__)
    logger.debug(f"Loading image from {path}")

    try:
        surface = pygame.image.load(path)
    except pygame.error as e:
        raise SystemExit(f'Could not load image "{path}" {pygame.get_error()}') from e
    return surface.convert()


class ImageAssetCache:
    def __init__(self) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self._cache = {}
        self._path_cache = self._load_path_cache()

    def get(self, name: str) -> pygame.Surface:
        if name not in self._cache:
            path = self._path_cache.get(name)
            if path is None:
                raise FileNotFoundError(f'Could not find image "{name}"')
            self.logger.debug(f"Loading image {name} -> {path}")
            self._cache[name] = load_image(path)
            self.logger.debug(f"Loaded image {name}")
        return self._cache[name]

    def _load_path_cache(self) -> dict[str, str]:
        files = {}
        for path, dirnames, filenames in ASSETS.walk():
            for filename in filenames:
                filename_lower = filename.lower()
                if not any(
                    filename_lower.endswith(ext) for ext in SUPPORTED_IMAGE_EXTENSIONS
                ):
                    continue
                filepath = path / filename
                key = str(path.relative_to(ASSETS) / filepath.stem)
                files[key] = filepath
                self.logger.debug(f"Found image {key} at {filepath}")
        self.logger.debug(
            f"Loaded {len(files)} image path{'' if len(files) == 1 else 's'}"
        )
        return files
