from typing import Optional
from token_type import Token, TokenType
from lexer import Lexer
from ast_type import (Program,
                      Statement,
                      LetStatement,
                      ReturnStatement,
                      ExpressionStatement,
                      Expression,
                      Identifier,
                      Boolean,
                      IntegerLiteral,
                      PrefixExpression,
                      InfixExpression)
from typing import List, Dict, Optional
from enum import IntEnum, auto


class OpPrecedence(IntEnum):
    LOWEST = auto()
    EQUALS = auto()
    LESSGREATER = auto()
    SUM = auto()
    PRODUCT = auto()
    PREFIX = auto()
    CALL = auto()


precendences = {
    TokenType.EQ: OpPrecedence.EQUALS,
    TokenType.NOT_EQ: OpPrecedence.EQUALS,
    TokenType.LT: OpPrecedence.LESSGREATER,
    TokenType.GT: OpPrecedence.LESSGREATER,
    TokenType.PLUS: OpPrecedence.SUM,
    TokenType.MINUS: OpPrecedence.SUM,
    TokenType.SLASH: OpPrecedence.PRODUCT,
    TokenType.ASTERISK: OpPrecedence.PRODUCT,
}


class Parser():
    def __init__(self, lexer: Lexer):
        self.lexer: Lexer = lexer
        self.cur_token: Optional[Token] = None
        self.peek_token: Optional[Token] = None
        self.errors: List[str] = []
        self.prefix_parse_funcs: dict = {}
        self.infix_parse_funcs: dict = {}

        self.register_prefix(TokenType.IDENT, self.parse_identifier)
        self.register_prefix(TokenType.INT, self.parse_integer_literal)
        self.register_prefix(TokenType.BANG, self.parse_prefix_expression)
        self.register_prefix(TokenType.MINUS, self.parse_prefix_expression)
        self.register_prefix(TokenType.TRUE, self.parse_boolean)
        self.register_prefix(TokenType.FALSE, self.parse_boolean)

        self.register_infix(TokenType.PLUS, self.parse_infix_expression)
        self.register_infix(TokenType.MINUS, self.parse_infix_expression)
        self.register_infix(TokenType.SLASH, self.parse_infix_expression)
        self.register_infix(TokenType.ASTERISK, self.parse_infix_expression)
        self.register_infix(TokenType.EQ, self.parse_infix_expression)
        self.register_infix(TokenType.NOT_EQ, self.parse_infix_expression)
        self.register_infix(TokenType.LT, self.parse_infix_expression)
        self.register_infix(TokenType.GT, self.parse_infix_expression)

        self.next_token()
        self.next_token()

    def next_token(self):
        self.cur_token = self.peek_token
        self.peek_token = self.lexer.next_token()

    def cur_token_is(self, token_type: TokenType) -> bool:
        return self.cur_token.type == token_type

    def peek_token_is(self, token_type: TokenType) -> bool:
        return self.peek_token.type == token_type

    def expect_peek(self, token_type: TokenType) -> bool:
        if self.peek_token_is(token_type):
            self.next_token()
            return True
        self.peek_error(token_type)
        return False

    def cur_precendence(self) -> OpPrecedence:
        return precendences.get(self.cur_token.type, OpPrecedence.LOWEST)

    def peek_precendence(self) -> OpPrecedence:
        return precendences.get(self.peek_token.type, OpPrecedence.LOWEST)

    def peek_error(self, token_type: TokenType):
        self.errors.append(
            f"expected next token to be {token_type}, got {self.peek_token.type} insted")

    def no_prefix_parse_func_error(self, token_type: TokenType):
        self.errors.append(
            f"no prefix parse function for {token_type} found"
        )

    def register_prefix(self, token_type: TokenType, func):
        self.prefix_parse_funcs[token_type] = func

    def register_infix(self, token_type: TokenType, func):
        self.infix_parse_funcs[token_type] = func

    def parse_program(self) -> Program:
        program = Program(statements=[])

        while self.cur_token.type != TokenType.EOF:
            stmt = self.parse_statement()
            if stmt:
                program.statements.append(stmt)
            self.next_token()
        return program

    def parse_statement(self) -> Statement:
        parse_funcs = {
            TokenType.LET: self.parse_let_statement,
            TokenType.RETURN: self.parse_return_statement,
        }

        if parse_func := parse_funcs.get(self.cur_token.type):
            return parse_func()

        return self.parse_expression_statement()

    def parse_let_statement(self) -> LetStatement:
        let_token = self.cur_token

        if not self.expect_peek(TokenType.IDENT):
            return None

        name = Identifier(token=self.cur_token, value=self.cur_token.literal)

        if not self.expect_peek(TokenType.ASSIGN):
            return None

        while self.cur_token_is(TokenType.SEMICLOLON):
            self.next_token()

        return LetStatement(token=let_token, name=name, value=None)

    def parse_return_statement(self) -> ReturnStatement:
        return_token = self.cur_token

        self.next_token()

        while not self.cur_token_is(TokenType.SEMICLOLON):
            self.next_token()

        return ReturnStatement(token=return_token, return_value=None)

    def parse_expression_statement(self) -> ExpressionStatement:
        stmt = ExpressionStatement(
            token=self.cur_token, expression=self.parse_expression(OpPrecedence.LOWEST))

        if self.peek_token_is(TokenType.SEMICLOLON):
            self.next_token()

        return stmt

    def parse_expression(self, precendence: OpPrecedence) -> Optional[Expression]:
        prefix = self.prefix_parse_funcs.get(self.cur_token.type, None)
        if not prefix:
            self.no_prefix_parse_func_error(self.cur_token.type)
            return None
        left_expression = prefix()

        while not self.peek_token_is(TokenType.SEMICLOLON) and precendence < self.peek_precendence():
            infix = self.infix_parse_funcs.get(self.peek_token.type, None)
            if not infix:
                return left_expression

            self.next_token()
            left_expression = infix(left_expression)

        return left_expression


    def parse_identifier(self) -> Expression:
        return Identifier(token=self.cur_token, value=self.cur_token.literal)

    def parse_integer_literal(self) -> Expression:
        return IntegerLiteral(token=self.cur_token, value=int(self.cur_token.literal))

    def parse_boolean(self) -> Expression:
        return Boolean(token=self.cur_token, value=self.cur_token_is(TokenType.TRUE))

    def parse_prefix_expression(self) -> Expression:
        token = self.cur_token
        operator = self.cur_token.literal

        self.next_token()

        return PrefixExpression(token=token, operator=operator, right=self.parse_expression(OpPrecedence.PREFIX))

    def parse_infix_expression(self, left: Expression) -> Expression:
        token = self.cur_token
        operator = self.cur_token.literal

        precendence = self.cur_precendence()
        self.next_token()
        return InfixExpression(
            token = token,
            left = left,
            operator = operator,
            right = self.parse_expression(precendence)
        )





