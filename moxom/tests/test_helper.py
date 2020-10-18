from moxom.helper import Helper
from moxom.runtime_context import create_routines, Routine
import unittest
import sys
from io import StringIO
from typing import Callable, Any


class HelperTest(unittest.TestCase):

    def setUp(self) -> None:
        self.original_stdout = sys.stdout
        self.new_stdout = StringIO()
        sys.stdout = self.new_stdout

    def tearDown(self) -> None:
        sys.stdout = self.original_stdout

    def test_help_should_list_all_commands_with(self):
        # given
        routines = create_routines(
            Routine("thing", lambda x: print(x)),
            Routine("test", lambda x: print(x))
        )

        # when
        helped_routines = Helper.with_help(routines)

        # then
        self.assertIn("help", helped_routines.keys())

        # when
        self.run_until_not_callable(helped_routines["help"].body)
        result = self.new_stdout.getvalue().strip().split("\n")

        # then
        assert "thing" in result
        assert "test" in result

    def test_help_command_should_print_provided_help(self):
        # given
        test_help = "Some test help"
        routines = Helper.with_help(create_routines(
            Routine("thing", lambda x: print(x), help=test_help)
        ))

        # when
        self.run_until_not_callable(routines["help"].subroutines["thing"].body())
        result = self.new_stdout.getvalue().strip().split("\n")

        # then
        self.assertIn(test_help, result)

    def test_help_command_should_print_help_from_method_comments(self):
        # given
        test_help = "Some test help"

        def some_method(*args):
            """
            Some test help
            :param args:
            :return:
            """
            print(*args)
            return
        routines = Helper.with_help(create_routines(
            Routine("test_method", some_method)
        ))

        # when
        self.run_until_not_callable(routines["help"].subroutines["test_method"].body())
        result = self.new_stdout.getvalue().strip()

        # then
        self.assertIn(test_help, result)

    def run_until_not_callable(self, body: Callable) -> Any:
        if isinstance(body, Callable):
            return self.run_until_not_callable(body())
        else:
            return body
