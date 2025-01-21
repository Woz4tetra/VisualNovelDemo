import logging

from game.canvas.animate.animation_definition import AnimationDefinition
from game.command.commands import TextCommand
from game.container import Container
from game.events import event


class TextBehavior:
    command: TextCommand

    def __init__(self, command: TextCommand, container: Container) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.canvas = container.canvas
        self.animation_definition = AnimationDefinition(properties=command)

    def initialize(self) -> None:
        self.logger.debug(f"Playing text animation {self.animation_definition}")
        self.canvas.play_animation(self.animation_definition)

    def tick(self) -> event.Event:
        if self.animation_definition in self.canvas.get_active_animations():
            return event.RUNNING
        return event.DONE

    def deinitialize(self) -> None:
        self.logger.debug("Text animation complete")
