import logging

from game.behaviors.load_behaviors import load_behaviors
from game.command.commands import TransitionToSequenceCommand
from game.container import Container
from game.events import event
from game.story_sequence.story_sequence import StorySequence
from game.story_sequence.story_sequence_runner import StorySequenceRunner


class TransitionToSequenceBehavior:
    command: TransitionToSequenceCommand

    def __init__(
        self, command: TransitionToSequenceCommand, container: Container
    ) -> None:
        self.container = container
        self.logger = logging.getLogger(self.__class__.__name__)
        self.sequence_name = command.sequence
        self.command_sequences = container.command_sequences
        self.sub_runner = StorySequenceRunner()

    def initialize(self) -> None:
        self.logger.debug(f"Transitioning to sub-sequence {self.sequence_name}")
        commands = self.command_sequences.get(self.sequence_name)
        behaviors = load_behaviors(commands, self.container)
        self.sub_runner.load(StorySequence(behaviors))
        self.sub_runner.initialize()

    def tick(self) -> event.Event:
        is_running = self.sub_runner.tick()
        return event.RUNNING if is_running else event.DONE

    def deinitialize(self) -> None:
        self.sub_runner.deinitialize()
