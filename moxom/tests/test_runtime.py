import unittest
import sys
import asyncio
from moxom.runtime import Runtime
from moxom.runtime_context import RuntimeScope, Routine
from moxom.types import Then, And
from moxom.runtime_context import create_routines
from io import StringIO

def p(text, *args): print(text + " " + "".join(map(str, args)))
def print_computer(*args): p("computer", args)
def print_laptop(*args): p("laptop", args)
def print_start(*args): p("start", args)
def print_open(*args): p("open", args)
def print_shutdown(*args): p("shutdown", args)


routines = create_routines(
    Routine("computer", print_computer, create_routines(
        Routine("start", print_start),
        Routine("open", print_open),
        Routine("shutdown", print_shutdown)
    )),
    Routine("laptop", print_laptop, create_routines(
        Routine("start", print_start),
        Routine("open", print_open),
        Routine("shutdown", print_shutdown)
    ))
)


invoke_tests = [
    (
        [routines["computer"].body,
         routines["computer"].subroutines["start"].body],
        ["computer ()", "start ()"]
    ),
    (
        [routines["computer"].body,
         "Macbook",
         routines["computer"].subroutines["start"].body],
        ["computer ('Macbook',)", "start ()"]
    ),
    (
        [Then(
            [routines["computer"].body, "Macbook", routines["computer"].subroutines["start"].body],
            [routines["computer"].body, "Macbook", routines["computer"].subroutines["shutdown"].body]
        )],
        ["computer ('Macbook',)", 'start ()', "computer ('Macbook',)", 'shutdown ()']
    ),
    (
        [And(
            [routines["computer"].body, "Dell", routines["computer"].subroutines["open"].body, "Chrome"],
            [routines["laptop"].body, "Macbook", routines["laptop"].subroutines["open"].body, "Safari"]
        )],
        ["computer ('Dell',)", "open ('Chrome',)", "laptop ('Macbook',)", "open ('Safari',)"]
    ),
    (
        [And(
            [Then(
                [routines["computer"].body, routines["computer"].subroutines["start"].body],
                [routines["computer"].body, routines["computer"].subroutines["open"].body, "Chrome"]
            )],
            [Then(
                [routines["laptop"].body, routines["laptop"].subroutines["start"].body],
                [routines["laptop"].body, routines["laptop"].subroutines["open"].body, "Safari"]
            )]
        )],
        ['computer ()', 'start ()', 'computer ()', "open ('Chrome',)", 'laptop ()', 'start ()', 'laptop ()', "open ('Safari',)"]
    )
]


class RuntimeTest(unittest.TestCase):

    def test_should_correctly_interpret_invokes(self):
        for input_commands, expected_results in invoke_tests:
            with self.subTest(input_commands):
                original_stdout = sys.stdout
                new_stdout = StringIO()
                sys.stdout = new_stdout

                asyncio.get_event_loop().run_until_complete(Runtime().run(input_commands))

                result = new_stdout.getvalue().strip().split("\n")
                print(result)
                self.assertListEqual(result, expected_results)

                sys.stdout = original_stdout
