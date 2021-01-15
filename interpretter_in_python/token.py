from enum import Enum
import dataclasses

class TokenType(Enum):
    ILLEGAL = 'ILLEGAL'
    EOF = 'EOF'

    IDENT = 'IDENT'
    INT = 'INT'

    ASSIGN = '='
    PLUS = '+'

    COMMA = ','
    SEMICLOLON = ';'

    LPAREN = '('
    RPAREN = ')'
    LBRACE = '{'
    RBRACE = '}'

    FUNCTION = 'FUNCTION'
    LET = 'LET'

@dataclasses.dataclass
class Token:
    type: TokenType
    literal: str

