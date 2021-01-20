from typing import Optional, List
from object import Object, Integer, Boolean
from ast_type import (Node,
                      IntegerLiteral,
                      Boolean as BooleanLiteral,
                      Program,
                      Statement,
                      ExpressionStatement)


def eval(node: Node) -> Optional[Object]:
    if isinstance(node, Program):
        return eval_statements(node.statements)
    elif isinstance(node, ExpressionStatement):
        return eval(node.expression)
    elif isinstance(node, IntegerLiteral):
        return Integer(node.value)
    elif isinstance(node, BooleanLiteral):
        return Boolean(node.value)
    return None


def eval_statements(stmts: List[Statement]):
    for stmt in stmts:
        result = eval(stmt)
    return result
