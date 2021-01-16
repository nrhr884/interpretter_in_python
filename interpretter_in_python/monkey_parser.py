from typing import Optional
from token_type import Token, TokenType
from lexer import Lexer
from ast_type import (Program,
                      Statement,
                      LetStatement,
                      Identifier)
from typing import List


class Parser():
    def __init__(self, lexer: Lexer):
        self.lexer: Lexer = lexer
        self.cur_token: Optional[Token] = None
        self.peek_token: Optional[Token] = None
        self.errors: List[str] = []

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

    def parse_program(self) -> Program:
        program = Program(statements=[])

        while self.cur_token.type != TokenType.EOF:
            stmt = self.parse_statement()
            if stmt:
                program.statements.append(stmt)
            self.next_token()
        return program

    def parse_statement(self) -> Statement:
        if self.cur_token.type == TokenType.LET:
            return self.parse_let_statement()
        return None

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



