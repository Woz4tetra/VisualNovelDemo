from .command import Command
from .composite_command import CompositeCommand
from .delay_command import DelayCommand
from .play_sound_command import PlaySoundCommand
from .set_backdrop_command import SetBackdropCommand
from .text_command import TextCommand
from .transition_to_sequence_command import TransitionToSequenceCommand

Commands = (
    SetBackdropCommand,
    DelayCommand,
    TransitionToSequenceCommand,
    CompositeCommand,
    PlaySoundCommand,
    TextCommand,
)
CommandType = (
    SetBackdropCommand
    | DelayCommand
    | TransitionToSequenceCommand
    | CompositeCommand
    | PlaySoundCommand
    | TextCommand
)

__all__ = [
    "Commands",
    "CommandType",
    "Command",
]
