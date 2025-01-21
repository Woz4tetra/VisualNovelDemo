from game.behaviors import Behaviors
from game.behaviors.behavior import Behavior
from game.behaviors.behavior_interface import BehaviorInterface
from game.command import CommandType
from game.container import Container


def load_behaviors(
    commands: list[CommandType], container: Container
) -> list[BehaviorInterface]:
    behavior_map: dict[type[CommandType], type[Behavior]] = {
        beh.__annotations__["command"]: beh for beh in Behaviors
    }
    behaviors: list[BehaviorInterface] = []
    for command in commands:
        behavior = behavior_map[type(command)](command, container)
        behaviors.append(behavior)
    return behaviors
