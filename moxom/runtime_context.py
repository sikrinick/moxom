from dataclasses import dataclass, field
from typing import Union, Callable, Dict, Any, Optional


@dataclass
class Routine:
    name: str
    body: Union[Callable, Any]
    subroutines: 'Routines' = field(default_factory=dict)
    help: Optional[str] = None


Routines = Dict[str, Routine]


def create_routines(*command_args: Routine) -> Routines:
    return {token.name: token for token in command_args}


@dataclass
class RuntimeScope:
    commands: Routines

