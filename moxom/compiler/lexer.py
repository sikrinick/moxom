from dataclasses import dataclass
from typing import Union, Optional, Iterator, List, Type
import re
from moxom.compiler.operators import operators


@dataclass
class BoolToken:
    def __init__(self, raw: str):
        self.value = raw == "True"
    regex = r'(?:True|False)(?=\s?)'


@dataclass
class IntToken:
    def __init__(self, raw: str):
        self.value = int(raw)
    regex = r'\d+'


@dataclass
class FloatToken:
    def __init__(self, raw: str):
        self.value = float(raw)
    regex = r'\d+\.\d+'


@dataclass
class StringToken:
    value: str
    '''
    \"( - starting with " capture
    (?: - start non-capturing group
    [^\"\\] - match any not " or \\ char 
    | - or
    \\. - match any char with preceding \
    )* - match group 0 or more times
    )\" - stop capturing if ends with "
    '''
    regex = r'\"(?:[^\"\\]|\\.)*\"'


@dataclass(frozen=True)
class IdentifierToken:
    value: str
    regex = r'[a-zA-Z][a-zA-Z0-9_]*'


@dataclass(frozen=True)
class OperatorToken:
    value: chr
    symbols = '|'.join(map(lambda x: x.value + r'(?=\s)', operators))
    regex = r'(?:%s)' % symbols


@dataclass(frozen=True)
class LParanToken:
    value: chr = '('
    regex = r'\('


@dataclass(frozen=True)
class RParanToken:
    value: chr = ')'
    regex = r'\)'


AtomTokens = [BoolToken, FloatToken, IntToken, StringToken]
AtomToken = Union[BoolToken, FloatToken, IntToken, StringToken]

Token = Union[
    AtomToken, OperatorToken, IdentifierToken, LParanToken, RParanToken
]
token_types: List[Type[Token]] = AtomTokens + [OperatorToken, IdentifierToken, LParanToken, RParanToken]


class Lexer:
    def __init__(self):
        self.non_whitespace = re.compile(r'\S')
        self.buf = ""
        self.pos = 0
        regex_parts = []
        self.group_type = {}
        for idx, token in enumerate(token_types):
            group_name = 'GROUP%s' % (idx + 1)
            regex_parts.append('(?P<%s>%s)' % (group_name, token.regex))
            self.group_type[group_name] = token

        self.regex = re.compile('|'.join(regex_parts))

    def parse(self, buf: str) -> [Token]:
        self.buf = buf
        self.pos = 0
        return list(self.tokens())

    def tokens(self) -> Iterator[Token]:
        while True:
            tok = self.next_token()
            if tok is None:
                break
            yield tok

    def next_token(self) -> Optional[Token]:
        if self.pos >= len(self.buf):
            return None
        else:
            m = self.non_whitespace.search(self.buf, self.pos)
            if m:
                self.pos = m.start()
            else:
                return None
            m = self.regex.match(self.buf, self.pos)
            if m:
                groupname = m.lastgroup
                tok_type = self.group_type[groupname]
                group = m.group(groupname)
                tok = tok_type(group)
                self.pos = m.end()
                return tok

            # if we're here, no rule matched
            raise SyntaxError("Syntax error at pos %s: \"%s\"" % (self.pos, self.buf))
        pass
