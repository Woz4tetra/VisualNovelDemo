import logging

from game.behaviors.behavior import Behavior
from game.command.set_backdrop_command import SetBackdropCommand
from game.container import Container
from game.events import event


class SetBackdropBehavior(Behavior):
    command: SetBackdropCommand

    def __init__(self, command: SetBackdropCommand, container: Container) -> None:
        super().__init__(command, container)
        self.canvas = container.canvas
        self.image_cache = container.images
        self.background = self.image_cache.get(command.backdrop)
        self.logger = logging.getLogger(self.__class__.__name__)

    def initialize(self) -> None:
        self.logger.debug(f"Setting backdrop to {self.command.backdrop}")
        self.canvas.set_background(self.background)

    def tick(self) -> event.Event:
        return event.DONE

    def deinitialize(self) -> None:
        pass
