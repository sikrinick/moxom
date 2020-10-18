from moxom.compiler.lexer import *
from dataclasses import dataclass
from typing import Tuple, List


@dataclass
class Expr:
    pass


@dataclass
class CstNode:
    token_or_expr: Union[Token, Expr]
    left_node: Optional['CstNode'] = None
    right_node: Optional['CstNode'] = None


class CstParser:

    def __init__(self):
        self.root: Optional[CstNode] = None

    def parse(self, tokens: [Token]) -> CstNode:
        self.root = None
        cst, _ = self.__inner_parse__(tokens)
        return cst

    def __inner_parse__(self, tokens: [Token]) -> Tuple[CstNode, List[Token]]:
        while len(tokens) > 0:
            token = tokens.pop(0)
            if isinstance(token, LParanToken):
                node, tokens = CstParser().__inner_parse__(tokens)
                self.__push_right__(
                    CstNode(
                        Expr(),
                        right_node=node
                    )
                )
            elif isinstance(token, RParanToken):
                break
            elif isinstance(token, OperatorToken):
                self.__wrap_left__(CstNode(token))
            elif type(token) in [IdentifierToken, FloatToken, IntToken, StringToken]:
                self.__push_right__(CstNode(token))
        return self.root, tokens

    def __push_right__(self, node: CstNode):
        """
        We have to add right to the rightmost
        [0] push right [1] = [0] -> [1]
        [0] -> [1] push right [2] = [0] -> ([1] -> [2])
        [0] <- [1] push right [2] = ([0] <- [1] -> [2])
        [] push right [1] = [1]
        """
        if self.root is not None:
            right_most = self.root
            while True:
                if right_most.right_node is not None:
                    right_most = right_most.right_node
                else:
                    break
            right_most.right_node = node
        else:
            self.root = node

    def __wrap_left__(self, node: CstNode):
        """
        We have to find the rightmost without left node
        and replace it with new node which has old rightmost without left as left
        [0] wrap left 1 = [0] <- [1]
        [0] -> [1] wrap left [2] = [0] -> ([1] <- [2])
        [0] <- [1] wrap left [2] = [0] <- [1] -> [2]
        [] wrap left [0] = [0]
        """
        if self.root is not None:
            last_root: Optional[CstNode] = None
            right_without_left = self.root
            while True:
                if right_without_left.left_node is not None:
                    last_root = right_without_left
                    right_without_left = right_without_left.right_node
                else:
                    break
            node.left_node = right_without_left
            if last_root is None:
                self.root = node
            else:
                last_root.right_node = node
        else:
            self.root = node
