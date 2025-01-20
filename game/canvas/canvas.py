import pygame


class Canvas:
    def __init__(self) -> None:
        if pygame.get_sdl_version()[0] == 2:
            pygame.mixer.pre_init(44100, 32, 2, 1024)
        pygame.init()

        if pygame.mixer and not pygame.mixer.get_init():
            print("Warning, no sound")
            pygame.mixer = None

        self.screen_rect = pygame.Rect(0, 0, 640, 480)
        fullscreen = False
        # Set the display mode
        winstyle = 0  # |FULLSCREEN
        bestdepth = pygame.display.mode_ok(self.screen_rect.size, winstyle, 32)
        self.screen = pygame.display.set_mode(
            self.screen_rect.size, winstyle, bestdepth
        )

        # decorate the game window
        # icon = pygame.transform.scale(image, (32, 32))
        # pygame.display.set_icon(icon)
        pygame.display.set_caption("Visual Novel")
        pygame.mouse.set_visible(0)

    def set_background(self, image: pygame.Surface) -> None:
        scaled = pygame.transform.scale(image, self.screen_rect.size)
        self.screen.blit(scaled, (0, 0))
        pygame.display.flip()
