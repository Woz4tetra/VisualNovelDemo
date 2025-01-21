import logging

from game.command.commands import SetBackdropCommand
from game.container import Container
from game.events import event


class SetBackdropBehavior:
    command: SetBackdropCommand

    def __init__(self, command: SetBackdropCommand, container: Container) -> None:
        self.backdrop = command.backdrop
        self.canvas = container.canvas
        self.image_cache = container.images
        self.background = self.image_cache.get(self.backdrop)
        self.logger = logging.getLogger(self.__class__.__name__)

    def initialize(self) -> None:
        self.logger.debug(f"Setting backdrop to {self.backdrop}")
        self.canvas.set_background(self.background)

    def tick(self) -> event.Event:
        return event.DONE

    def deinitialize(self) -> None:
        pass
