from asyncio import iscoroutinefunction
import asyncio
from .types import Result, And, Then
from typing import Callable, Optional, Any, List


class Runtime:
    def __init__(self):
        self.function_buffer: Optional[Callable] = None
        self.object_stack: [Result] = []

    async def run(self, operations: List[Result]) -> [Result]:
        self.function_buffer: Optional[Callable] = None
        self.object_stack: [Result] = []

        if not isinstance(operations, List):
            operations = [operations]

        for operation in operations:

            if isinstance(operation, Callable):
                await self.check_stack()
                self.function_buffer = operation

            elif isinstance(operation, And) or isinstance(operation, Then):
                left = Runtime().run(operation.lhs)
                right = Runtime().run(operation.rhs)

                if isinstance(operation, And):
                    async def parallelize(*args):
                        await asyncio.gather(left, right)
                    await self.check_stack()
                    self.function_buffer = parallelize

                elif isinstance(operation, Then):
                    async def combine(*args):
                        await left
                        await right
                    await self.check_stack()
                    self.function_buffer = combine
            else:
                self.object_stack.append(operation)

        await self.check_stack()

        output = []
        while len(self.object_stack) > 0:
            arg = self.object_stack[0]
            if isinstance(arg, Callable) or type(arg) in [And, Then]:
                result = await Runtime().run(self.object_stack)
                output.append(result)
                break
            else:
                output.append(self.object_stack.pop(0))
        output = filter(lambda x: x is not None, output)
        output = filter(lambda x: not isinstance(x, List) or len(x) > 0, output)
        return list(output)

    async def check_stack(self):
        if self.function_buffer is not None:
            result = await self.run_function(self.function_buffer, self.object_stack)
            self.function_buffer = None
            if isinstance(result, List):
                self.object_stack = result
            elif result is not None:
                self.object_stack = [result]
            else:
                self.object_stack = []

    async def run_function(self, function: Callable, arguments: [Any]) -> Any:
        if iscoroutinefunction(function):
            return await function(*arguments)
        else:
            return function(*arguments)

