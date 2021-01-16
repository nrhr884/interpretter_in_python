from typing import Optional
from token_type import Token, TokenType
from lexer import Lexer
from ast_type import (Program,
                      Statement,
                      LetStatement,
                      ReturnStatement,
                      ExpressionStatement,
                      Expression,
                      Identifier)
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


class Parser():
    def __init__(self, lexer: Lexer):
        self.lexer: Lexer = lexer
        self.cur_token: Optional[Token] = None
        self.peek_token: Optional[Token] = None
        self.errors: List[str] = []
        self.prefix_parse_funcs: dict = {}
        self.infix_parse_funcs: dict = {}

        self.register_prefix(TokenType.IDENT, self.parse_identifier)

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

    def peek_error(self, token_type: TokenType):
        self.errors.append(
            f"expected next token to be {token_type}, got {self.peek_token.type} insted")

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
        if prefix:
            return prefix()
        return None

    def parse_identifier(self) -> Expression:
        return Identifier(token=self.cur_token, value=self.cur_token.literal)



