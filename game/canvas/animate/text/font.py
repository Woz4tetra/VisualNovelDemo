from abc import ABC, abstractmethod

import pygame


class Font(ABC):
    @abstractmethod
    def draw_glyph(
        self, dst: pygame.Surface, x: int, y: int, color: tuple[int, int, int], ch: str
    ) -> None: ...

    @abstractmethod
    def get_linesize(self) -> int: ...

    @abstractmethod
    def get_glyph_width(self, ch: str) -> int: ...


class BitmapFont(Font):
    def __init__(self, surface: pygame.Surface, glyph_rects: list[pygame.Rect]):
        self.surface = surface
        self.glyph_rects = glyph_rects

    def draw_glyph(
        self, dst: pygame.Surface, x: int, y: int, color: tuple[int, int, int], ch: str
    ) -> None:
        index = ord(ch) - ord(" ")

        old_color = self.surface.get_palette_at(1)
        self.surface.set_palette_at(1, color)

        dst.blit(self.surface, (x, y), self.glyph_rects[index])

        self.surface.set_palette_at(1, old_color)

    def get_linesize(self) -> int:
        return self.glyph_rects[0].h

    def get_glyph_width(self, ch) -> int:
        index = ord(ch) - ord(" ")
        return self.glyph_rects[index].w


class TTF(Font):
    def __init__(self, name: str, size: int):
        self.pg_font = pygame.font.Font(name, size)
        self.cached_chars = {}

    def draw_glyph(
        self, dst: pygame.Surface, x: int, y: int, color: tuple[int, int, int], ch: str
    ) -> None:
        # Make a quick integer key for this glyph: 0xRRGGBB + (ch<<24)
        key = (color[0] << 16) | (color[1] << 8) | color[2]
        key |= ord(ch) << 24

        # Cache it
        if key not in self.cached_chars:
            self.cached_chars[key] = self.pg_font.render(ch, True, color)

        # Draw it
        surf = self.cached_chars[key]
        dst.blit(surf, (x, y))

    def get_linesize(self) -> int:
        return self.pg_font.get_linesize()

    def get_glyph_width(self, ch: str) -> int:
        return self.pg_font.metrics(ch)[0][4]
