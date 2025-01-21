import logging

from game.canvas.animate.animation_definition import AnimationDefinition
from game.canvas.animate.animator_keys import AnimatorKey
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
        if len(command.load_animation) == 0:
            self.animation = None
        else:
            parameters = {}
            parameters.update(command.load_animation)
            animation_type = parameters.pop("type")
            parameters["surface"] = self.background
            if not isinstance(animation_type, str):
                raise ValueError(f"Invalid animation type: {animation_type}")
            self.animation = AnimationDefinition(
                AnimatorKey(animation_type), parameters
            )

        self.logger = logging.getLogger(self.__class__.__name__)

    def initialize(self) -> None:
        if self.animation:
            self.logger.debug(f"Playing animation {self.animation}")
            self.canvas.play_animation(self.animation)

    def tick(self) -> event.Event:
        if self.animation and self.animation in self.canvas.get_active_animations():
            return event.RUNNING
        else:
            self.logger.debug(f"Setting backdrop to {self.backdrop}")
            self.canvas.set_background(self.background)
            return event.DONE

    def deinitialize(self) -> None:
        pass
