from ast_type import Program, Identifier, LetStatement
from lexer import Lexer
from monkey_parser import Parser

def test_let_statements():
    src = '''
    let x = 5;
    let y = 10;
    let foobar = 838383;
    '''

    lexer = Lexer(src)
    parser = Parser(lexer)
    program = parser.parse_program()

    assert len(program.statements) == 3

    expected_identifier = ["x", "y", "foobar"]

    for i, stmt in zip(expected_identifier, program.statements):
        assert stmt.token_literal() == "let"
        assert isinstance(stmt, LetStatement)
        assert stmt.name.value == i
        assert stmt.name.token_literal() == i


