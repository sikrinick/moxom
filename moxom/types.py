from typing import Union, Callable
from dataclasses import dataclass

Primitive = Union[bool, str, int, float]
Result = Union[Callable[[], 'Result'], Primitive, 'Operator', None]


@dataclass
class And:
    lhs: [Result]
    rhs: [Result]


@dataclass
class Then:
    lhs: [Result]
    rhs: [Result]
