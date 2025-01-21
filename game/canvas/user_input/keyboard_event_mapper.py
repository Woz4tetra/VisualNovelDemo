import pygame

from game.canvas.user_input.event_mapper_interface import EventMapperInterface
from game.canvas.user_input.user_event import UserEvent


class KeyboardEventMapper(EventMapperInterface):
    def __init__(self) -> None:
        pass

    def parse(self, event: pygame.event.Event) -> UserEvent | None:
        user_event = None
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                user_event = UserEvent.NEXT_DIALOG
        return user_event
