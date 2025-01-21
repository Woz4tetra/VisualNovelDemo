from typing import TypeVar

T = TypeVar("T")
T_co = TypeVar("T_co", covariant=True)


def optional_pop(a_list: list[T], value: T, default: T_co = None) -> T | T_co:
    return a_list.pop(a_list.index(value)) if value in a_list else default
