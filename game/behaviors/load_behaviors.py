from game.behaviors.behavior_interface import BehaviorInterface
from game.command.commands import CommandType
from game.container import Container


def load_behaviors(
    commands: list[CommandType], container: Container
) -> list[BehaviorInterface]:
    from game.behaviors import Behaviors, BehaviorType

    behavior_map: dict[type[CommandType], type[BehaviorType]] = {
        beh.__annotations__["command"]: beh for beh in Behaviors
    }
    behaviors: list[BehaviorInterface] = []
    for command in commands:
        behavior = behavior_map[type(command)](command, container)  # type: ignore
        behaviors.append(behavior)
    return behaviors
