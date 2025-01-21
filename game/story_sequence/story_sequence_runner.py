import logging

from game.behaviors.behavior_interface import BehaviorInterface
from game.events import event
from game.story_sequence.story_sequence import StorySequence


class StorySequenceRunner:
    def __init__(self) -> None:
        self.current_story_sequence: StorySequence | None = None
        self.current_behavior: BehaviorInterface | None = None
        self.logger = logging.getLogger(self.__class__.__name__)

    def load(self, story_sequence: StorySequence) -> None:
        story_sequence.reset()
        self.current_story_sequence = story_sequence

    def initialize(self) -> None:
        self.logger.debug("Initializing story sequence")
        if self.current_story_sequence is None:
            raise ValueError("No story sequence loaded")
        self.current_behavior = self.current_story_sequence.next()
        self.logger.debug(
            f"Initialized story sequence with {self._get_behavior_log_string()}"
        )

    def tick(self) -> bool:
        if self.current_story_sequence is None:
            raise ValueError("No story sequence loaded")
        if self.current_behavior is None:
            return False
        next_event = self.current_behavior.tick()
        if next_event == event.DONE:
            self.current_behavior = self.current_story_sequence.next()
            self.logger.debug(f"Transitioned to {self._get_behavior_log_string()}")
            return True
        elif next_event == event.RUNNING:
            return True
        else:
            raise ValueError(f"Unknown event {next_event}")

    def deinitialize(self) -> None:
        self.logger.debug("Deinitializing story sequence")
        if self.current_behavior is not None:
            self.logger.debug(f"Deinitializing {self._get_behavior_log_string()}")
            self.current_behavior.deinitialize()

    def _get_behavior_log_string(self) -> str:
        if self.current_behavior is None:
            return "No behavior"
        if self.current_story_sequence is None:
            return "No story sequence"
        return f"{self.current_behavior.__class__.__name__} ({self.current_story_sequence.get_index()})"
