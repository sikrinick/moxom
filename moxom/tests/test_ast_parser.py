from moxom.compiler.interpreter import *
from moxom.compiler.lexer import StringToken
import unittest


tests = (
    (
        CstNode(
            IdentifierToken("computer"),
            right_node=CstNode(
                IdentifierToken("start")
            )
        ),
        FunctionNode(
            IdentifierToken(value='computer'),
            chain=FunctionNode(IdentifierToken(value='start'))
        )
    ),
    (
        CstNode(
            IdentifierToken("computer"),
            right_node=CstNode(
                StringToken('"Macbook"'),
                right_node=CstNode(
                    IdentifierToken("start")
                )
            )
        ),
        FunctionNode(
            IdentifierToken('computer'),
            chain=AtomNode(
                "Macbook",
                chain=FunctionNode(IdentifierToken("start"))
            )
        )
    ),
    (
        CstNode(
            OperatorToken("then"),
            left_node=CstNode(
                IdentifierToken("computer"),
                right_node=CstNode(
                    StringToken('"Macbook"'),
                    right_node=CstNode(
                        IdentifierToken("start")
                    )
                )
            ),
            right_node = CstNode(
                IdentifierToken("computer"),
                right_node=CstNode(
                    StringToken('"Macbook"'),
                    right_node=CstNode(
                        IdentifierToken("shutdown")
                    )
                )
            )
        ),
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
        )
    ),
    (
        CstNode(
            OperatorToken("and"),
            left_node=CstNode(
                IdentifierToken("computer"),
                right_node=CstNode(
                    StringToken('"Dell"'),
                    right_node=CstNode(
                        IdentifierToken("open"),
                        right_node=CstNode(StringToken('"Chrome"'))
                    )
                )
            ),
            right_node = CstNode(
                IdentifierToken("laptop"),
                right_node=CstNode(
                    StringToken('"Macbook"'),
                    right_node=CstNode(
                        IdentifierToken("open"),
                        right_node=CstNode(StringToken('"Safari"'))
                    )
                )
            )
        ),
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
        )
    ),
    (
        CstNode(
            OperatorToken("and"),
            left_node=CstNode(
                Expr(),
                right_node=CstNode(
                    OperatorToken("then"),
                    left_node=CstNode(
                        IdentifierToken("computer"),
                        right_node=CstNode(IdentifierToken("start"))
                    ),
                    right_node=CstNode(
                        IdentifierToken("computer"),
                        right_node=CstNode(IdentifierToken("shutdown"))
                    )
                )
            ),
            right_node=CstNode(
                Expr(),
                right_node=CstNode(
                    OperatorToken("then"),
                    left_node=CstNode(
                        IdentifierToken("laptop"),
                        right_node=CstNode(IdentifierToken("start"))
                    ),
                    right_node=CstNode(
                        IdentifierToken("laptop"),
                        right_node=CstNode(IdentifierToken("shutdown"))
                    )
                )
            )
        ),
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
                        token=IdentifierToken(value='shutdown')
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
                    chain=FunctionNode(token=IdentifierToken(value='shutdown'))
                )
            )
        )
    ),
    (
        CstNode(
            OperatorToken("="),
            left_node=CstNode(IdentifierToken("full_work")),
            right_node=CstNode(
                OperatorToken("then"),
                left_node=CstNode(
                    Expr(),
                    right_node=CstNode(
                        OperatorToken("then"),
                        left_node=CstNode(
                            IdentifierToken("computer"),
                            right_node=CstNode(IdentifierToken("start"))
                        ),
                        right_node=CstNode(
                            IdentifierToken("computer"),
                            right_node=CstNode(IdentifierToken("shutdown"))
                        )
                    )
                ),
                right_node=CstNode(
                    Expr(),
                    right_node=CstNode(
                        OperatorToken("then"),
                        left_node=CstNode(
                            IdentifierToken("laptop"),
                            right_node=CstNode(IdentifierToken("start"))
                        ),
                        right_node=CstNode(
                            IdentifierToken("laptop"),
                            right_node=CstNode(IdentifierToken("shutdown"))
                        ),
                    )
                )
            )
        ),
        DeclarationNode(
            token=IdentifierToken(value='full_work'),
            arguments=[],
            subroutine=BinaryNode(
                token=OperatorToken(value='then'),
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
        )
    ),
    (
        CstNode(
            OperatorToken("="),
            left_node=CstNode(IdentifierToken("start_mac")),
            right_node=CstNode(
                IdentifierToken("computer"),
                right_node=CstNode(
                    StringToken('"Macbook"'),
                    right_node=CstNode(
                        IdentifierToken("start")
                    )
                )
            )
        ),
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
        )
    ),
    (
        CstNode(
            OperatorToken("="),
            left_node=CstNode(IdentifierToken("full_computer_work")),
            right_node=CstNode(
                OperatorToken("then"),
                left_node=CstNode(
                    IdentifierToken("computer"),
                    right_node=CstNode(
                        IdentifierToken("start")
                    )
                ),
                right_node=CstNode(
                    OperatorToken("then"),
                    left_node=CstNode(
                        IdentifierToken("computer"),
                        right_node=CstNode(
                            IdentifierToken("open"),
                            right_node=CstNode(StringToken('"Youtube"'))
                        )
                    ),
                    right_node=CstNode(
                        IdentifierToken("computer"),
                        right_node=CstNode(IdentifierToken("shutdown"))
                    )
                )
            )
        ),
        DeclarationNode(
            token=IdentifierToken(value='full_computer_work'),
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
                            chain=AtomNode(value="Youtube")
                        )
                    ),
                    rhs=FunctionNode(
                        token=IdentifierToken(value='computer'),
                        chain=FunctionNode(token=IdentifierToken(value='shutdown'))
                    )
                )
            )
        )
    ),
    (
        CstNode(
            OperatorToken("="),
            left_node=CstNode(IdentifierToken("full")),
            right_node=CstNode(
                OperatorToken("and"),
                left_node=CstNode(IdentifierToken("full_computer")),
                right_node=CstNode(IdentifierToken("full_laptop"))
            )
        ),
        DeclarationNode(
            token=IdentifierToken(value='full'),
            arguments=[],
            subroutine=BinaryNode(
                token=OperatorToken(value='and'),
                lhs=FunctionNode(token=IdentifierToken(value='full_computer')),
                rhs=FunctionNode(token=IdentifierToken(value='full_laptop'))
            )
        )
    ),
    (
        CstNode(
            OperatorToken("="),
            left_node=CstNode(
                IdentifierToken("both_open"),
                right_node=CstNode(IdentifierToken("url"))
            ),
            right_node=CstNode(
                OperatorToken("and"),
                left_node=CstNode(
                    IdentifierToken("computer"),
                    right_node=CstNode(
                        IdentifierToken("open"),
                        right_node=CstNode(
                            IdentifierToken("url")
                        )
                    )
                ),
                right_node=CstNode(
                    IdentifierToken("laptop"),
                    right_node=CstNode(
                        IdentifierToken("open"),
                        right_node=CstNode(
                            IdentifierToken("url")
                        )
                    )
                )
            )
        ),
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
        )
    ),
    (
        CstNode(
            OperatorToken("="),
            left_node=CstNode(
                IdentifierToken("url")
            ),
            right_node=CstNode(
                StringToken('"https://test.com"')
            )
        ),
        DeclarationNode(
            IdentifierToken("url"),
            arguments=[],
            subroutine=AtomNode("https://test.com")
        )
    )
)


class AstParserTest(unittest.TestCase):
    def test_should_correctly_parse(self):
        for input_cst, expected_ast in tests:
            with self.subTest(input_cst):
                actual = AstParser().parse(input_cst)
                self.assertEqual(actual, expected_ast)
