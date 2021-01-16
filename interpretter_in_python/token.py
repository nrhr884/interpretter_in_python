from enum import Enum
import dataclasses

class TokenType(Enum):
    ILLEGAL = 'ILLEGAL'
    EOF = 'EOF'

    IDENT = 'IDENT'
    INT = 'INT'

    ASSIGN = '='
    PLUS = '+'
    MINUS = '-'
    BANG = '!'
    ASTERISK = '*'
    SLASH = '/'

    LT = '<'
    GT = '>'

    EQ = '=='
    NOT_EQ = '!='

    COMMA = ','
    SEMICLOLON = ';'

    LPAREN = '('
    RPAREN = ')'
    LBRACE = '{'
    RBRACE = '}'

    FUNCTION = 'FUNCTION'
    LET = 'LET'
    TRUE = 'TRUE'
    FALSE = 'FALSE'
    IF = 'IF'
    ELSE = 'ELSE'
    RETURN = 'RETURN'

@dataclasses.dataclass
class Token:
    type: TokenType
    literal: str

