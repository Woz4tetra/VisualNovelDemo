import pygame

from game.assets.paths import ASSETS


def load_image(name: str) -> pygame.Surface:
    files = list(ASSETS.glob(name + ".*"))
    if not files:
        raise FileNotFoundError(f'Could not find image "{name}"')
    files_no_extension = [file for file in files if file.stem == name]
    if len(files_no_extension) > 1:
        raise ValueError(f'Found multiple images with name "{name}"')
    file = files_no_extension[0]
    try:
        surface = pygame.image.load(file)
    except pygame.error as e:
        raise SystemExit(f'Could not load image "{file}" {pygame.get_error()}') from e
    return surface.convert()


class ImageAssetCache:
    def __init__(self) -> None:
        self._cache = {}

    def get(self, name: str) -> pygame.Surface:
        if name not in self._cache:
            self._cache[name] = load_image(name)
        return self._cache[name]
