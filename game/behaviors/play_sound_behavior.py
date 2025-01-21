import logging

from game.command.commands import PlaySoundCommand
from game.container import Container
from game.events import event


class PlaySoundBehavior:
    command: PlaySoundCommand

    def __init__(self, command: PlaySoundCommand, container: Container) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.sound = command.sound

    def initialize(self) -> None:
        self.logger.debug(f"Playing sound {self.sound}")

    def tick(self) -> event.Event:
        return event.DONE

    def deinitialize(self) -> None:
        self.logger.debug(f"Sound {self.sound} complete")
