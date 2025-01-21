from .command import Command
from .delay_command import DelayCommand
from .set_backdrop_command import SetBackdropCommand
from .transition_to_sequence_command import TransitionToSequenceCommand

Commands = (
    SetBackdropCommand,
    DelayCommand,
    TransitionToSequenceCommand,
)
CommandType = SetBackdropCommand | DelayCommand | TransitionToSequenceCommand

__all__ = [
    "Commands",
    "CommandType",
    "Command",
]
