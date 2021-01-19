from dataclasses import dataclass
from token_type import Token
from abc import ABC, abstractclassmethod
from typing import List, Optional


class Node(ABC):
    @abstractclassmethod
    def token_literal(self) -> str:
        pass

    @abstractclassmethod
    def string(self) -> str:
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

    def string(self):
        return self.token.literal


@dataclass
class Program(Node):
    statements: List[Statement]

    def token_literal(self):
        return self.statements[0].token_literal() if self.statements else ""

    def string(self):
        strings = []
        for stmt in self.statements:
            strings.append(stmt.string())
        return "".join(strings)


@dataclass
class Identifier(Expression):
    value: str


@dataclass
class IntegerLiteral(Expression):
    value: int


@dataclass
class Boolean(Expression):
    value: bool


@dataclass
class PrefixExpression(Expression):
    operator: str
    right: Expression

    def string(self):
        return f"({self.operator}{self.right.string()})"


@dataclass
class InfixExpression(Expression):
    left: Expression
    operator: str
    right: Expression

    def string(self):
        return f"({self.left.string()} {self.operator} {self.right.string()})"


@dataclass
class LetStatement(Statement):
    name: Identifier
    value: Expression

    def string(self):
        return f'{self.token_literal()} {self.name.string()} = {self.value.string()};'


@dataclass
class ReturnStatement(Statement):
    return_value: Expression

    def string(self):
        return f'{self.token_literal()} {self.return_value.string()};'


@dataclass
class ExpressionStatement(Statement):
    expression: Expression

    def string(self):
        return self.expression.string()

@dataclass
class BlockStatement(Statement):
    statements: List[Statement]

    def string(self):
        strings = []
        for stmt in self.statements:
            strings.append(stmt.string())
        return "".join(strings)

@dataclass
class IfExpression(Expression):
    condition: Expression
    consequence: BlockStatement
    alternative: Optional[BlockStatement]

    def string(self):
        strings = []
        strings.append("if")
        strings.append(self.consequence.string())
        strings.append(" ")

        if self.alternative:
            strings.append("else ")
            strings.append(self.alternative.string())

        return "".join(strings)
