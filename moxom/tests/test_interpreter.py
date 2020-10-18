import unittest
from moxom.compiler.astparser import FunctionNode, AtomNode, BinaryNode, DeclarationNode, OperatorToken, IdentifierToken
from moxom.compiler.interpreter import Interpreter, RuntimeScope, Routine, Then, And
from moxom.runtime_context import create_routines
from typing import List


routines=create_routines(
    Routine("computer", lambda: print("computer"), create_routines(
        Routine("start", lambda: print("start")),
        Routine("open", lambda: print("open")),
        Routine("shutdown", lambda: print("shutdown"))
    )),
    Routine("laptop", lambda: print("laptop"), create_routines(
        Routine("start", lambda: print("start")),
        Routine("open", lambda: print("open")),
        Routine("shutdown", lambda: print("shutdown"))
    ))
)


invoke_tests = (
    (
        FunctionNode(
            IdentifierToken(value='computer'),
            chain=FunctionNode(IdentifierToken(value='start'))
        ),
        [routines["computer"].body,
         routines["computer"].subroutines["start"].body]
    ),
    (
        FunctionNode(
            IdentifierToken('computer'),
            chain=AtomNode(
                "Macbook",
                chain=FunctionNode(IdentifierToken("start"))
            )
        ),
        [routines["computer"].body,
         "Macbook",
         routines["computer"].subroutines["start"].body]
    ),
    (
        BinaryNode(
            OperatorToken('then'),
            lhs=FunctionNode(
                IdentifierToken(value='computer'),
                AtomNode(
                    "Macbook",
                    chain=FunctionNode(
                        token=IdentifierToken(value='start'),
                    )
                )
            ),
            rhs=FunctionNode(
                token=IdentifierToken(value='computer'),
                chain=AtomNode(
                    "Macbook",
                    chain=FunctionNode(token=IdentifierToken(value='shutdown'))
                )
            )
        ),
        [Then(
            [routines["computer"].body, "Macbook", routines["computer"].subroutines["start"].body],
            [routines["computer"].body, "Macbook", routines["computer"].subroutines["shutdown"].body]
        )]
    ),
    (
        BinaryNode(
            token=OperatorToken(value='and'),
            lhs=FunctionNode(
                token=IdentifierToken('computer'),
                chain=AtomNode(
                    "Dell",
                    FunctionNode(
                        token=IdentifierToken(value='open'),
                        chain=AtomNode("Chrome"),
                    )
                )
            ),
            rhs=FunctionNode(
                token=IdentifierToken(value='laptop'),
                chain=AtomNode(
                    "Macbook",
                    chain=FunctionNode(
                        token=IdentifierToken(value='open'),
                        chain=AtomNode("Safari")
                    )
                )
            )
        ),
        [And(
            [routines["computer"].body, "Dell", routines["computer"].subroutines["open"].body, "Chrome"],
            [routines["laptop"].body, "Macbook", routines["laptop"].subroutines["open"].body, "Safari"]
        )]
    ),
    (
        BinaryNode(
            token=OperatorToken(value='and'),
            lhs=BinaryNode(
                token=OperatorToken(value='then'),
                lhs=FunctionNode(
                    token=IdentifierToken(value='computer'),
                    chain=FunctionNode(
                        token=IdentifierToken(value='start')
                    )
                ),
                rhs=FunctionNode(
                    token=IdentifierToken(value='computer'),
                    chain=FunctionNode(
                        token=IdentifierToken(value='open'),
                        chain=AtomNode("Chrome")
                    ),
                )
            ),
            rhs=BinaryNode(
                token=OperatorToken(value='then'),
                lhs=FunctionNode(
                    token=IdentifierToken(value='laptop'),
                    chain=FunctionNode(token=IdentifierToken(value='start'))
                ),
                rhs=FunctionNode(
                    token=IdentifierToken(value='laptop'),
                    chain=FunctionNode(
                        token=IdentifierToken(value='open'),
                        chain=AtomNode("Safari")
                    )
                )
            )
        ),
        [And(
            [Then(
                [routines["computer"].body, routines["computer"].subroutines["start"].body],
                [routines["computer"].body, routines["computer"].subroutines["open"].body, "Chrome"]
            )],
            [Then(
                [routines["laptop"].body, routines["laptop"].subroutines["start"].body],
                [routines["laptop"].body, routines["laptop"].subroutines["open"].body, "Safari"]
            )]
        )]
    )
)

declaration_tests = [
    (
        DeclarationNode(
            token=IdentifierToken(value='full_work'),
            arguments=[],
            subroutine=BinaryNode(
                token=OperatorToken(value='and'),
                lhs=BinaryNode(
                    token=OperatorToken(value='then'),
                    lhs=FunctionNode(
                        token=IdentifierToken(value='computer'),
                        chain=FunctionNode(token=IdentifierToken(value='start'))
                    ),
                    rhs=FunctionNode(
                        token=IdentifierToken(value='computer'),
                        chain=FunctionNode(token=IdentifierToken(value='shutdown'))
                    )
                ),
                rhs=BinaryNode(
                    token=OperatorToken(value='then'),
                    lhs=FunctionNode(
                        token=IdentifierToken(value='laptop'),
                        chain=FunctionNode(token=IdentifierToken(value='start'))
                    ),
                    rhs=FunctionNode(
                        token=IdentifierToken(value='laptop'),
                        chain=FunctionNode(token=IdentifierToken(value='shutdown'))
                    )
                )
            )
        ),
        lambda routines: routines["full_work"].body(),
        [And(
            [Then(
                [routines["computer"].body, routines["computer"].subroutines["start"].body],
                [routines["computer"].body, routines["computer"].subroutines["shutdown"].body]
            )],
            [Then(
                [routines["laptop"].body, routines["laptop"].subroutines["start"].body],
                [routines["laptop"].body, routines["laptop"].subroutines["shutdown"].body]
            )]
        )]
    ),
    (
        DeclarationNode(
            token=IdentifierToken(value='start_mac'),
            arguments=[],
            subroutine=FunctionNode(
                token=IdentifierToken(value='computer'),
                chain=AtomNode(
                    "Macbook",
                    chain=FunctionNode(token=IdentifierToken(value='start'))
                )
            )
        ),
        lambda routines: routines["start_mac"].body(),
        [routines["computer"].body, "Macbook", routines["computer"].subroutines["start"].body]
    ),
    (
        DeclarationNode(
            token=IdentifierToken(value='full_computer'),
            arguments=[],
            subroutine=BinaryNode(
                token=OperatorToken(value='then'),
                lhs=FunctionNode(
                    token=IdentifierToken(value='computer'),
                    chain=FunctionNode(
                        token=IdentifierToken(value='start')
                    )
                ),
                rhs=BinaryNode(
                    token=OperatorToken(value='then'),
                    lhs=FunctionNode(
                        token=IdentifierToken(value='computer'),
                        chain=FunctionNode(
                            token=IdentifierToken(value='open'),
                            chain=AtomNode("Youtube")
                        )
                    ),
                    rhs=FunctionNode(
                        token=IdentifierToken(value='computer'),
                        chain=FunctionNode(token=IdentifierToken(value='shutdown'))
                    )
                )
            )
        ),
        lambda routines: routines["full_computer"].body(),
        [Then(
            [routines["computer"].body, routines["computer"].subroutines["start"].body],
            [Then(
                [routines["computer"].body, routines["computer"].subroutines["open"].body, "Youtube"],
                [routines["computer"].body, routines["computer"].subroutines["shutdown"].body]
            )]
        )]
    ),
    (
        DeclarationNode(
            token=IdentifierToken(value='both_open'),
            arguments=[IdentifierToken("url")],
            subroutine=BinaryNode(
                token=OperatorToken(value='and'),
                lhs=FunctionNode(
                    token=IdentifierToken(value='computer'),
                    chain=FunctionNode(
                        token=IdentifierToken(value='open'),
                        chain=FunctionNode(IdentifierToken("url")),
                    )
                ),
                rhs=FunctionNode(
                    token=IdentifierToken(value='laptop'),
                    chain=FunctionNode(
                        token=IdentifierToken(value='open'),
                        chain=FunctionNode(IdentifierToken("url"))
                    )
                )
            )
        ),
        lambda routines: routines["both_open"].body("test_url"),
        [And(
            [routines["computer"].body, routines["computer"].subroutines["open"].body, "test_url"],
            [routines["laptop"].body, routines["laptop"].subroutines["open"].body, "test_url"]
        )]
    ),
    (
        DeclarationNode(
            IdentifierToken("url"),
            arguments=[],
            subroutine=AtomNode("https://test.com")
        ),
        lambda routines: routines["url"].body,
        "https://test.com"
    )
]


class InterpreterTest(unittest.TestCase):

    def test_should_correctly_interpret_invokes(self):
        for input_ast, expected_results in invoke_tests:
            with self.subTest(input_ast):
                actual = Interpreter().interpret(input_ast, RuntimeScope(routines))
                self.assertListEqual(actual, expected_results)

    def test_should_correctly_interpret_declarations(self):
        for input_ast, routine_runner, expected_result in declaration_tests:
            with self.subTest(input_ast):
                mutable_routines = routines.copy()
                actions = Interpreter().interpret(input_ast, RuntimeScope(mutable_routines))
                [action() for action in actions]
                new_routines = mutable_routines
                actual_result = routine_runner(new_routines)
                if isinstance(actual_result, List):
                    self.assertListEqual(actual_result, expected_result)
                else:
                    self.assertEqual(actual_result, expected_result)


