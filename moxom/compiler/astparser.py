from dataclasses import dataclass
from moxom.compiler.lexer import OperatorToken, IdentifierToken, AtomTokens
from typing import Union, Optional
from .cstparser import CstNode, Expr
import ast
from moxom.compiler.operators import operator_dict, AssignOperator, AndOperator, ThenOperator


@dataclass
class AtomNode:
    value: [str, int, float]
    chain: Union['AtomNode', 'FunctionNode', None] = None


@dataclass
class BinaryNode:
    token: OperatorToken
    lhs: 'AstNode'
    rhs: 'AstNode'


@dataclass
class FunctionNode:
    token: IdentifierToken
    chain: Union[AtomNode, 'FunctionNode', None] = None


@dataclass
class DeclarationNode:
    token: IdentifierToken
    arguments: [IdentifierToken]
    subroutine: Union['AstNode']


AstNode = Union[AtomNode, BinaryNode, FunctionNode, DeclarationNode]


class AstParser:
    def parse(self, cst: CstNode) -> AstNode:

        if isinstance(cst.token_or_expr, IdentifierToken):
            return FunctionNode(
                cst.token_or_expr,
                self.parse(cst.right_node) if cst.right_node is not None else None
            )

        elif type(cst.token_or_expr) in AtomTokens:
            value = cst.token_or_expr.value
            value = ast.literal_eval(value) if type(value) == str else value
            return AtomNode(
                value,
                self.parse(cst.right_node) if cst.right_node is not None else None
            )

        elif isinstance(cst.token_or_expr, Expr):
            return self.parse(cst.right_node)

        elif isinstance(cst.token_or_expr, OperatorToken):
            operator = operator_dict[cst.token_or_expr.value]

            if operator in [AndOperator, ThenOperator]:
                left = self.parse(cst.left_node)
                right = self.parse(cst.right_node)
                return BinaryNode(cst.token_or_expr, left, right)

            elif operator is AssignOperator:
                name, arguments = self.parse_signature(cst.left_node)
                body = self.parse(cst.right_node)
                return DeclarationNode(name, arguments, body)

        raise Exception("Not supported token: %s" % cst.token_or_expr)

    @dataclass
    class FunctionSignature:
        name: IdentifierToken
        arguments: [IdentifierToken]

    def parse_signature(self, cst: CstNode) -> (IdentifierToken, [IdentifierToken]):
        return cst.token_or_expr, self.parse_signature_arguments(cst.right_node)

    def parse_signature_arguments(self, cst: Optional[CstNode]) -> [IdentifierToken]:
        if cst is None:
            return []
        elif type(cst.token_or_expr) is IdentifierToken:
            arguments = [cst.token_or_expr]
            return arguments + self.parse_signature_arguments(cst.right_node)
        else:
            raise Exception("Function signature should contain only identifiers")
