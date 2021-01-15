from interpretter_in_python.token import TokenType, Token

class Lexer:
    def __init__(self, input_str: str):
        self.input_str = input_str
        self.position = 0
        self.read_position = 0
        self.ch = None
        self.read_char()

    def read_char(self):
        if self.read_position >= len(self.input_str):
            self.ch = 0
        else:
            self.ch = self.input_str[self.read_position]
        self.position = self.read_position
        self.read_position += 1

    def read_identifier(self):
        position = self.position
        while self.ch.isalpha():
            self.read_char()
        return self.input_str[position: self.position]

    def read_number(self):
        position = self.position
        while self.ch.isdigit():
            self.read_char()
        return self.input_str[position: self.position]

    def lookup_ident(self, ident: str):
        keywords = {
            'fn' : TokenType.FUNCTION,
            'let' : TokenType.LET
        }
        return keywords.get(ident, TokenType.IDENT)

    def skip_whitespaces(self):
        while self.ch in (' ', '\t', '\n', '\r'):
            self.read_char()

    def next_token(self):
        char_to_toke_type = {
            '=': TokenType.ASSIGN,
            ';': TokenType.SEMICLOLON,
            '(': TokenType.LPAREN,
            ')': TokenType.RPAREN,
            ',': TokenType.COMMA,
            '+': TokenType.PLUS,
            '{': TokenType.LBRACE,
            '}': TokenType.RBRACE,
        }

        self.skip_whitespaces()

        if tokenType := char_to_toke_type.get(self.ch):
            token = Token(tokenType, self.ch)
        elif self.ch == 0:
            token = Token(TokenType.EOF, '')
        elif self.ch.isalpha():
            ident = self.read_identifier()
            tokenType = self.lookup_ident(ident)
            return Token(tokenType, ident)
        elif self.ch.isdigit():
            return Token(TokenType.INT,self.read_number())
        else:
            token = Token(TokenType.ILLEGAL, self.ch)

        self.read_char()
        return token
