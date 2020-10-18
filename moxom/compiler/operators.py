from dataclasses import dataclass


@dataclass
class Operator:
    value: chr


AndOperator = Operator('and')
ThenOperator = Operator('then')
AssignOperator = Operator('=')

operators = [
    AndOperator,
    ThenOperator,
    AssignOperator
]

operator_dict = {
    operator.value: operator for operator in operators
}
