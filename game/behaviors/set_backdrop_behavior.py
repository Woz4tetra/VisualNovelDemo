from game.behaviors.behavior import Behavior
from game.story.command.set_backdrop_command import SetBackdropCommand


class SetBackdropBehavior(Behavior):
    command: SetBackdropCommand

    def __init__(self, command: SetBackdropCommand) -> None:
        super().__init__(command)

    def initialize(self) -> None:
        pass

    def tick(self) -> None:
        pass

    def deinitialize(self) -> None:
        pass
