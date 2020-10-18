from .astparser import *
from moxom.compiler.operators import *
from moxom.runtime_context import RuntimeScope, Routine, Routines
from moxom.types import And, Then, Result


class Interpreter:

    def interpret(self, ast_node: AstNode, scope: RuntimeScope) -> [Result]:
        if isinstance(ast_node, AtomNode):
            sub_result = self.interpret(ast_node.chain, scope) if ast_node.chain is not None else []
            return [ast_node.value] + sub_result

        elif isinstance(ast_node, FunctionNode):
            try:
                command = scope.commands[ast_node.token.value]
            except KeyError:
                raise Exception("Command not supported: \"%s\"" % ast_node.token.value)

            outer = scope.commands.copy()
            inner = command.subroutines
            commands = self.dynamic_merge(inner, outer)

            method = command.body
            sub_result = self.interpret(ast_node.chain, RuntimeScope(commands)) if ast_node.chain is not None else []
            return [method] + sub_result

        elif isinstance(ast_node, BinaryNode):
            operator = operator_dict[ast_node.token.value]
            left = self.interpret(ast_node.lhs, scope)
            right = self.interpret(ast_node.rhs, scope)
            if operator is AndOperator:
                return [And(left, right)]
            elif operator is ThenOperator:
                return [Then(left, right)]

        elif isinstance(ast_node, DeclarationNode):
            if isinstance(ast_node.subroutine, AtomNode):
                custom = ast_node.subroutine.value
            else:
                def custom(*args) -> [Result]:
                    arguments = {argument: args[idx] for idx, argument in enumerate(ast_node.arguments)}
                    temp_commands = scope.commands.copy()
                    for token, value in arguments.items():
                        temp_commands[token.value] = Routine(token.value, value)
                    temp_scope = RuntimeScope(temp_commands)
                    return self.interpret(ast_node.subroutine, temp_scope)

            def create_command():
                name = ast_node.token.value
                scope.commands[name] = Routine(name, custom, help="Custom routine or variable")

            return [create_command]

    def dynamic_merge(self, inner: Routines, outer: Routines) -> Routines:
        """
        required by help and other overriding functions
        """
        keys = set(inner.keys()).union(outer.keys())
        routines: Routines = {}
        for key in keys:
            inner_routine = inner.get(key)
            outer_routine = outer.get(key)
            routines[key] = inner_routine if inner_routine is not None else outer_routine
        return routines
