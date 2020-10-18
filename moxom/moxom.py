from .compiler import Lexer, CstParser, AstParser, Interpreter
from .runtime import Runtime
from .runtime_context import Routines, RuntimeScope
from .helper import Helper
from typing import Optional
from pathlib import Path
import os
import sys
import asyncio


class Moxom:

    def __init__(self, routines: Routines, moxom_env: Optional[str] = None):
        self.lexer = Lexer()
        self.cst_parser = CstParser()
        self.ast_parser = AstParser()
        self.interpreter = Interpreter()
        self.runtime = Runtime()
        self.runtime_scope = RuntimeScope(Helper.with_help(routines))
        if moxom_env is not None:
            self.__set_moxom_env__(moxom_env)

    def __set_moxom_env__(self, env_file_path: str):
        if not Path(env_file_path).is_file():
            env_file_path = os.path.join(os.path.dirname(sys.argv[0]), env_file_path)
        with open(env_file_path, "r") as environment:
            for line in environment:
                self.execute(line)

    def execute(self, line):
        try:
            if len(line) == 0 or line.startswith("#"):
                return

            tokens = self.lexer.parse(line)
            if len(tokens) == 0:
                return

            cst_node = self.cst_parser.parse(tokens)
            ast_node = self.ast_parser.parse(cst_node)
            operations = self.interpreter.interpret(ast_node, self.runtime_scope)
            output = asyncio.get_event_loop().run_until_complete(self.runtime.run(operations))
            for line in output:
                print(line)

        except Exception as e:
            print("Runtime Error: %s" % e)
