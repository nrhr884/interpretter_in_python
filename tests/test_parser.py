from ast_type import Program, Identifier, LetStatement, ReturnStatement
from lexer import Lexer
from monkey_parser import Parser


def check_parse_errors(parser: Parser):
    if not parser.errors:
        return

    error_msg = []
    error_msg.append(f"parser has {len(parser.errors)} errors")
    for e in parser.errors:
        error_msg.append(f"parser error: {e}")

    raise Exception("\n".join(error_msg))

def parse(src: str) -> Program:
    lexer = Lexer(src)
    parser = Parser(lexer)
    program = parser.parse_program()
    check_parse_errors(parser)
    return program


def test_let_statements():
    src = '''
    let x = 5;
    let y = 10;
    let foobar = 838383;
    '''

    program = parse(src)
    assert len(program.statements) == 3

    expected_identifier = ["x", "y", "foobar"]

    for i, stmt in zip(expected_identifier, program.statements):
        assert stmt.token_literal() == "let"
        assert isinstance(stmt, LetStatement)
        assert stmt.name.value == i
        assert stmt.name.token_literal() == i

def test_let_statements():
    src = '''
    return 5;
    return 10;
    return 838383;
    '''

    program = parse(src)

    assert len(program.statements) == 3

    for stmt in program.statements:
        assert stmt.token_literal() == "return"
        assert isinstance(stmt, ReturnStatement)
