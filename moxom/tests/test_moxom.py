from moxom import create_routines, Routine, Moxom
import unittest
import sys
from io import StringIO


class MoxomTest(unittest.TestCase):

    def setUp(self) -> None:
        self.original_stdout = sys.stdout
        self.new_stdout = StringIO()
        sys.stdout = self.new_stdout

    def tearDown(self) -> None:
        sys.stdout = self.original_stdout

    def test_should_execute_simple_command(self):
        # given
        expected_output_foo = "aaa"
        def foo(*args):
            print(expected_output_foo)
        routines = create_routines(Routine("foo", foo))
        moxom = Moxom(routines)

        # when
        moxom.execute("foo")
        result = self.new_stdout.getvalue().strip().split("\n")

        # then
        self.assertIn("aaa", result)

    def test_should_execute_command_with_argument(self):
        # given
        mock_input = "bbb"
        routines = create_routines(Routine("foo", lambda x: print(x)))
        moxom = Moxom(routines)

        # when
        moxom.execute(f"foo \"{mock_input}\"")
        result = self.new_stdout.getvalue().strip().split("\n")

        # then
        self.assertIn(mock_input, result)

    def test_should_execute_commands_with_and_operator(self):
        # given
        expected_output_foo = "aaa"
        mock_input = "bbb"
        def foo(*args):
            print(expected_output_foo)
        def bar(x):
            print(x)
        routines = create_routines(
            Routine("foo", foo),
            Routine("bar", bar)
        )
        moxom = Moxom(routines)

        # when
        moxom.execute(f"foo and bar \"{mock_input}\"")
        result = self.new_stdout.getvalue().strip().split("\n")

        # then
        self.assertIn(expected_output_foo, result)
        self.assertIn(mock_input, result)

    def test_should_execute_commands_with_then_operator(self):
        # given
        expected_output_foo = "aaa"
        mock_input = "bbb"
        def foo(*args):
            print(expected_output_foo)
        def bar(x):
            print(x)
        routines = create_routines(
            Routine("foo", foo),
            Routine("bar", bar)
        )
        moxom = Moxom(routines)

        # when
        moxom.execute(f"foo then bar \"{mock_input}\"")
        result = self.new_stdout.getvalue().strip().split("\n")

        # then
        self.assertIn(expected_output_foo, result)
        self.assertIn(mock_input, result)

    def test_should_consume_definitions_with_functions(self):
        # given
        expected_output_foo = "aaa"
        expected_output_bar = "bbb"

        def foo(*args):
            print(expected_output_foo)
        def bar(*args):
            print(expected_output_bar)

        routines = create_routines(
            Routine("foo", foo),
            Routine("bar", bar)
        )
        moxom = Moxom(routines)

        # when
        moxom.execute("test = foo then bar")
        moxom.execute("test")
        result = self.new_stdout.getvalue().strip().split("\n")

        # then
        self.assertIn(expected_output_foo, result)
        self.assertIn(expected_output_bar, result)

    def test_should_consume_definitions_with_functions_with_arguments(self):
        # given
        mocked_input_a = "aaa"
        mocked_input_b = "bbb"
        routines = create_routines(
            Routine("foo", lambda x: print(x)),
            Routine("bar", lambda x: print(x))
        )
        moxom = Moxom(routines)

        # when
        moxom.execute("test a b = foo a then bar b")
        moxom.execute(f"test \"{mocked_input_a}\" \"{mocked_input_b}\"")
        result = self.new_stdout.getvalue().strip().split("\n")

        # then
        self.assertIn(mocked_input_a, result)
        self.assertIn(mocked_input_b, result)

    def test_should_consume_definitions_of_primitives(self):
        # given
        expected_output_foo = "aaa"
        routines = create_routines(Routine("foo", lambda x: print(x)))
        moxom = Moxom(routines)

        # when
        moxom.execute(f"test_a = \"{expected_output_foo}\"")
        moxom.execute("foo test_a")
        result = self.new_stdout.getvalue().strip().split("\n")

        # then
        self.assertIn(expected_output_foo, result)

    def test_should_automatically_add_help_command(self):
        # given
        foo_output = "aaa"
        help_text = "some help text"
        def foo(*args):
            print(foo_output)
        routines = create_routines(Routine("foo", foo, help=help_text))
        moxom = Moxom(routines)

        # when
        moxom.execute("help")
        result = self.new_stdout.getvalue().strip().split("\n")

        # then
        self.assertIn("foo", result)

        # when
        moxom.execute("help foo")
        result = self.new_stdout.getvalue().strip().split("\n")

        # then
        self.assertIn(help_text, result)
