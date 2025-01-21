from .command import Command
from .delay_command import DelayCommand
from .set_backdrop_command import SetBackdropCommand

Commands = (
    SetBackdropCommand,
    DelayCommand,
)
CommandType = SetBackdropCommand | DelayCommand

__all__ = [
    "Commands",
    "CommandType",
    "Command",
]
