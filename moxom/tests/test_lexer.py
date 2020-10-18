from moxom.compiler.lexer import *
import unittest

tests = (
    (
        "computer start",
        [IdentifierToken("computer"), IdentifierToken("start")]
    ),
    (
        "computer \"Macbook\" start",
        [IdentifierToken("computer"), StringToken('"Macbook"'), IdentifierToken("start")]
    ),
    (
        "computer \"Macbook\" start then computer \"Macbook\" shutdown",
        [IdentifierToken("computer"), StringToken('"Macbook"'), IdentifierToken("start"),
         OperatorToken("then"),
         IdentifierToken("computer"), StringToken('"Macbook"'), IdentifierToken("shutdown")]
    ),
    (
        "computer \"Dell\" open \"Chrome\" and laptop \"Macbook\" open \"Safari\"",
        [IdentifierToken("computer"), StringToken('"Dell"'), IdentifierToken("open"), StringToken('"Chrome"'),
         OperatorToken("and"),
         IdentifierToken("laptop"), StringToken('"Macbook"'), IdentifierToken("open"), StringToken('"Safari"')]
    ),
    (
        "computer test_float 0.4",
        [IdentifierToken("computer"), IdentifierToken("test_float"), FloatToken("0.4")]
    ),
    (
        "int_test 2",
        [IdentifierToken("int_test"), IntToken("2")]
    ),
    (
        "boolean_True_check True",
        [IdentifierToken("boolean_True_check"), BoolToken("True")]
    ),
    (
        "while True computer open",
        [IdentifierToken("while"), BoolToken("True"), IdentifierToken("computer"), IdentifierToken("open")]
    ),
    (
        "boolean_False_check False",
        [IdentifierToken("boolean_False_check"), BoolToken("False")]
    ),
    (
        "while False laptop open",
        [IdentifierToken("while"), BoolToken("False"), IdentifierToken("laptop"), IdentifierToken("open")]
    ),
    (
        "(computer start then computer open) and (laptop start then laptop open)",
        [LParanToken(),
         IdentifierToken("computer"), IdentifierToken("start"),
         OperatorToken("then"),
         IdentifierToken("computer"), IdentifierToken("open"),
         RParanToken(),
         OperatorToken("and"),
         LParanToken(),
         IdentifierToken("laptop"), IdentifierToken("start"),
         OperatorToken("then"),
         IdentifierToken("laptop"), IdentifierToken("open"),
         RParanToken()
         ]
    ),
    (
        "full = (computer start then computer shutdown) and (laptop start then laptop shutdown)",
        [IdentifierToken("full"),
         OperatorToken('='),
         LParanToken(),
         IdentifierToken("computer"),
         IdentifierToken("start"),
         OperatorToken("then"),
         IdentifierToken("computer"),
         IdentifierToken("shutdown"),
         RParanToken(),
         OperatorToken("and"),
         LParanToken(),
         IdentifierToken("laptop"),
         IdentifierToken("start"),
         OperatorToken("then"),
         IdentifierToken("laptop"),
         IdentifierToken("shutdown"),
         RParanToken()
         ]
    ),
    (
        "start_mac = computer \"Macbook\" start",
        [IdentifierToken("start_mac"),
         OperatorToken('='),
         IdentifierToken("computer"),
         StringToken('"Macbook"'),
         IdentifierToken("start")]
    ),
    (
        "full_work = computer start then computer open \"Youtube\" then computer shutdown",
        [
            IdentifierToken("full_work"),
            OperatorToken('='),
            IdentifierToken("computer"),
            IdentifierToken("start"),
            OperatorToken("then"),
            IdentifierToken("computer"),
            IdentifierToken("open"),
            StringToken('"Youtube"'),
            OperatorToken("then"),
            IdentifierToken("computer"),
            IdentifierToken("shutdown")
        ]
    ),
    (
        "full = full_computer_work and full_laptop_work",
        [
            IdentifierToken("full"),
            OperatorToken('='),
            IdentifierToken("full_computer_work"),
            OperatorToken("and"),
            IdentifierToken("full_laptop_work")
        ]
    ),
    (
        "both_open url = computer open url and laptop open url",
        [
            IdentifierToken("both_open"),
            IdentifierToken("url"),
            OperatorToken("="),
            IdentifierToken("computer"),
            IdentifierToken("open"),
            IdentifierToken("url"),
            OperatorToken("and"),
            IdentifierToken("laptop"),
            IdentifierToken("open"),
            IdentifierToken("url")
        ]
    ),
    (
        "server = \"http://localhost:8080\"",
        [
            IdentifierToken("server"),
            OperatorToken("="),
            StringToken("\"http://localhost:8080\"")
        ]
    )
)


class LexerTest(unittest.TestCase):
    def test_should_correctly_tokenize(self):
        for input_str, expected in tests:
            with self.subTest(input_str):
                lexer = Lexer()
                actual = lexer.parse(input_str)
                self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
