from dataclasses import dataclass

from game.events.event_key import EventKey


@dataclass
class Event:
    key: EventKey


RUNNING = Event(EventKey.RUNNING)
DONE = Event(EventKey.DONE)
