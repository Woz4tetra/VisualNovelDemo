import logging

from game.behaviors.behavior_interface import BehaviorInterface


class StorySequence:
    def __init__(self, behaviors: list[BehaviorInterface]) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self._behaviors = behaviors
        self._current_behavior = None
        self._index = 0

    def next(self) -> BehaviorInterface | None:
        if self._index >= len(self._behaviors):
            return None
        if self._current_behavior is not None:
            self.logger.debug(
                f"Deinitializing {self._current_behavior.__class__.__name__}"
            )
            self._current_behavior.deinitialize()
        self._current_behavior = self._behaviors[self._index]
        self.logger.debug(
            f"Initializing {self._current_behavior.__class__.__name__} ({self._index})"
        )
        self._current_behavior.initialize()
        self._index += 1
        return self._current_behavior

    def get_index(self) -> int:
        return self._index - 1

    def reset(self) -> None:
        self._index = 0
        self._current_behavior = None
        self.logger.debug("Story sequence reset")
