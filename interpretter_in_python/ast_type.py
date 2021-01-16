from dataclasses import dataclass
from token_type import Token
from abc import ABC, abstractclassmethod
from typing import List


class Node(ABC):
    @abstractclassmethod
    def token_literal(self) -> str:
        pass


@dataclass
class Statement(Node):
    token: Token
    def token_literal(self):
        return self.token.literal


@dataclass
class Expression(Node):
    token: Token
    def token_literal(self):
        return self.token.literal


@dataclass
class Program(Node):
    statements: List[Statement]

    def token_literal(self):
        return self.statements[0].token_literal() if self.statements else ""


@dataclass
class Identifier(Expression):
    value: str



@dataclass
class LetStatement(Statement):
    name: Identifier
    value: Expression

@dataclass
class ReturnStatement(Statement):
    return_value: Expression


@dataclass
class ExpressionStatement(Statement):
    expression: Expression