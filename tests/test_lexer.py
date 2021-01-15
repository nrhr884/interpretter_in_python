from interpretter_in_python.lexer import Lexer
from interpretter_in_python.token import Token, TokenType

def test_next_token():
    input_str = '''let five = 5;
    let ten = 10;

    let add = fn(x, y) {
        x + y;
    };
    '''

    lexer = Lexer(input_str)

    expected_tokens = [
        Token(TokenType.LET, "let"),
        Token(TokenType.IDENT, "five"),
        Token(TokenType.ASSIGN, "="),
        Token(TokenType.INT, "5"),
        Token(TokenType.SEMICLOLON, ";"),
        Token(TokenType.LET, "let"),
        Token(TokenType.IDENT, "ten"),
        Token(TokenType.ASSIGN, "="),
        Token(TokenType.INT, "10"),
        Token(TokenType.SEMICLOLON, ";"),
        Token(TokenType.LET, "let"),
        Token(TokenType.IDENT, "add"),
        Token(TokenType.ASSIGN, "="),
        Token(TokenType.FUNCTION, "fn"),
        Token(TokenType.LPAREN, "("),
        Token(TokenType.IDENT, "x"),
        Token(TokenType.COMMA, ","),
        Token(TokenType.IDENT, "y"),
        Token(TokenType.RPAREN, ")"),
        Token(TokenType.LBRACE, "{"),
        Token(TokenType.IDENT, "x"),
        Token(TokenType.PLUS, "+"),
        Token(TokenType.IDENT, "y"),
        Token(TokenType.SEMICLOLON, ";"),
        Token(TokenType.RBRACE, "}"),
        Token(TokenType.SEMICLOLON, ";"),
        Token(TokenType.EOF, ""),
    ]

    for expected in expected_tokens:
        assert lexer.next_token() == expected
