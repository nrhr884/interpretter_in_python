from dataclasses import dataclass
from token_type import Token
from abc import ABC, abstractclassmethod
from typing import List


class Node(ABC):
    @abstractclassmethod
    def token_literal(self) -> str:
        pass


class Statement(Node):
    pass


class Expression(Node):
    pass


@dataclass
class Program(Node):
    statements: List[Statement]

    def token_literal(self):
        return self.statements[0].token_literal() if self.statements else ""


@dataclass
class Identifier(Expression):
    token: Token
    value: str

    def token_literal(self):
        return self.token.literal


@dataclass
class LetStatement(Statement):
    token: Token
    name: Identifier
    value: Expression

    def token_literal(self):
        return self.token.literal
