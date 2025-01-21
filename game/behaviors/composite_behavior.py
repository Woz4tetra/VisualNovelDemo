import logging

from game.behaviors.load_behaviors import load_behaviors
from game.command.commands.composite_command import (
    CompositeCommand,
    CompositeExitCondition,
)
from game.container import Container
from game.events import event


class CompositeBehavior:
    command: CompositeCommand

    def __init__(self, command: CompositeCommand, container: Container) -> None:
        self.start_time = 0.0
        self.exit_condition = command.exit_condition
        self.subbehaviors = load_behaviors(command.subcommands, container)  # type: ignore
        self.logger = logging.getLogger(self.__class__.__name__)
        self.active_subbehaviors = self.subbehaviors.copy()

    def initialize(self) -> None:
        for behavior in self.subbehaviors:
            behavior.initialize()

    def tick(self) -> event.Event:
        for behavior in self.active_subbehaviors:
            result = behavior.tick()
            if result != event.DONE:
                continue
            if self.exit_condition == CompositeExitCondition.ANY:
                self.logger.debug(
                    f"Composite behavior finished due to {behavior.__class__.__name__}"
                )
                return event.DONE
            self.active_subbehaviors.remove(behavior)
        if (
            not self.active_subbehaviors
            and self.exit_condition == CompositeExitCondition.ALL
        ):
            self.logger.debug("Composite behavior finished. All subbehaviors done.")
            return event.DONE
        return event.RUNNING

    def deinitialize(self) -> None:
        self.logger.debug("Delay complete")
        for behavior in self.subbehaviors:
            behavior.deinitialize()
