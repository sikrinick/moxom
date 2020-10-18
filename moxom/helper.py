from .runtime_context import Routine, Routines
from typing import Dict, Optional


class Helper:

    @staticmethod
    def with_help(routines: Routines) -> Routines:
        help_creator = Helper()
        root_routines = routines
        help_routine = Routine(
            "help",
            help_creator.list_commands(routines),
            LazyHelpDict(routines)
        )
        root_routines[help_routine.name] = help_routine
        return root_routines

    def list_commands(self, routines):
        def print_commands(name: str, command: Routine):
            print(name)
            for sub_name in command.subroutines.keys():
                print_commands("%s %s" % (name, sub_name), command.subroutines[sub_name])

        def root_help(*args):
            commands = routines.copy()
            commands.pop("help")
            print("Available routines:")
            for name in commands.keys():
                print_commands(name, commands[name])
        return help_wrapper(root_help)


class LazyHelpDict(Dict[str, Routine]):
    def __init__(self, routines: Routines):
        super().__init__()
        self.routines = routines

    def get(self, routine_name: str) -> Optional[Routine]:
        return self.__getitem__(routine_name)

    def __getitem__(self, routine_name: str) -> Routine:
        routine = self.routines.get(routine_name)
        return Routine(
            routine_name,
            create_help(routine),
            EagerHelpDict(routine.subroutines)
        )


class EagerHelpDict(Dict[str, Routine]):
    def __init__(self, routines: Routines):
        super().__init__()
        for routine_name, routine in routines.items():
            super(EagerHelpDict, self).__setitem__(
                routine_name,
                Routine(
                    routine_name,
                    create_help(routine),
                    EagerHelpDict(routine.subroutines)
                )
            )
        self.routines = routines


def create_help(routine):
    def helper(*args):
        if routine.help is not None:
            print(routine.help)
        else:
            help(routine.body)
    return help_wrapper(helper)


def help_wrapper(help_callable):
    def helper(*args):
        return help_callable
    return helper
