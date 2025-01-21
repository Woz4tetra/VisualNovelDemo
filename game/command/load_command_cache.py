import logging
from pathlib import Path

from game.assets.paths import STORIES
from game.command.command_sequence_cache import CommandSequenceCache
from game.command.commands import Commands
from game.command.load_command_sequence import load_command_sequence


def load_command_cache(story_path: str) -> CommandSequenceCache:
    logger = logging.getLogger(__name__)
    story_dir = Path(story_path)
    if not story_dir.is_absolute():
        story_dir = STORIES / story_dir
    if not story_dir.exists():
        raise FileNotFoundError(f"Story directory {story_dir} not found")
    if not story_dir.is_dir():
        raise NotADirectoryError(f"Story path {story_dir} is not a directory")
    logger.debug(f"Loading story from {story_dir}")

    command_sequence_cache = CommandSequenceCache()
    for path, dirnames, filenames in story_dir.walk():
        for filename in filenames:
            filepath = path / filename
            if not filename.endswith(".json"):
                continue
            command_sequence = load_command_sequence(Commands, filepath)
            logger.debug(f"Loaded {len(command_sequence)} commands from {filepath}")
            command_sequence_cache.add(filepath.stem, command_sequence)
    logger.debug(f"Loaded {len(command_sequence_cache)} command sequences")
    return command_sequence_cache
