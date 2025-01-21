import logging

from game.assets.image_asset_cache import ImageAssetCache
from game.canvas import Canvas
from game.command.load_command_cache import load_command_cache
from game.command_line_args import CommandLineArgs
from game.story_sequence.story_sequence_runner import StorySequenceRunner
from game.tickable import Tickable


class Container:
    def __init__(self, args: CommandLineArgs) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.canvas = Canvas()
        self.images = ImageAssetCache()

        self.command_sequences = load_command_cache(args.story)
        self.logger.debug(
            f"Loaded command sequence{'' if len(self.command_sequences) == 1 else 's'}"
        )
        if self.command_sequences.root is None:
            raise ValueError("No root command found")
        self.root_commands = self.command_sequences.root
        self.story_sequence_runner = StorySequenceRunner()

        self.logger.debug("Container initialized")

    def get_initialize_order(self) -> list[Tickable]:
        return [
            self.canvas,
            self.story_sequence_runner,
        ]

    def get_tick_order(self) -> list[Tickable]:
        return [
            self.story_sequence_runner,
            self.canvas,
        ]

    def get_deinitialize_order(self) -> list[Tickable]:
        return [
            self.story_sequence_runner,
            self.canvas,
        ]
