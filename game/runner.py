import logging

from game.behaviors.load_behaviors import load_behaviors
from game.command_line_args import CommandLineArgs
from game.container import Container
from game.logger import initialize
from game.story_sequence.story_sequence import StorySequence


class Runner:
    def __init__(self, args: CommandLineArgs) -> None:
        initialize(args.log_level)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info("Initializing visual novel")
        self.container = Container(args)
        self._initialize_first_sequence()
        self.initialize_order = self.container.get_initialize_order()
        self.tick_order = self.container.get_tick_order()
        self.deinitialize_order = self.container.get_deinitialize_order()

    def _initialize_first_sequence(self) -> None:
        behaviors = load_behaviors(self.container.root_commands, self.container)
        first_sequence = StorySequence(behaviors)
        self.container.story_sequence_runner.load(first_sequence)

    def run(self) -> None:
        self.initialize()
        while self.tick():
            pass
        self.deinitialize()

    def initialize(self) -> bool:
        self.logger.info("Initializing visual novel")
        for tickable in self.initialize_order:
            self.logger.debug(f"Initializing {tickable.__class__.__name__}")
            tickable.initialize()
        self.logger.debug("Visual novel initialized")
        return True

    def tick(self) -> bool:
        results = [tickable.tick() for tickable in self.tick_order]
        return all(results)

    def deinitialize(self) -> None:
        self.logger.info("Closing visual novel")
        for tickable in self.deinitialize_order:
            self.logger.debug(f"Closing {tickable.__class__.__name__}")
            tickable.deinitialize()
        self.logger.debug("Visual novel closed")
