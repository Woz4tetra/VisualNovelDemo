import logging

from game.command.commands import DelayCommand
from game.container import Container
from game.events import event
from game.utils.now import now


class DelayBehavior:
    command: DelayCommand

    def __init__(self, command: DelayCommand, container: Container) -> None:
        self.start_time = 0.0
        self.duration = command.duration
        self.logger = logging.getLogger(self.__class__.__name__)

    def initialize(self) -> None:
        self.logger.debug(f"Delaying for {self.duration} seconds")
        self.start_time = now()

    def tick(self) -> event.Event:
        if now() - self.start_time < self.duration:
            return event.RUNNING
        return event.DONE

    def deinitialize(self) -> None:
        self.logger.debug("Delay complete")
