from ast_type import (
    Program,
    Identifier,
    LetStatement,
    ReturnStatement,
    Expression,
    ExpressionStatement,
    IntegerLiteral,
    PrefixExpression
    )
from lexer import Lexer
from monkey_parser import Parser
import pytest


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


def test_identifier_expression():
    src = "foobar;"

    program = parse(src)

    assert len(program.statements) == 1
    stmt = program.statements[0]

    assert isinstance(stmt, ExpressionStatement)
    assert isinstance(stmt.expression, Identifier)
    assert stmt.expression.value == "foobar"
    assert stmt.expression.token_literal() == "foobar"


def assert_integer_literal_expression(expression: Expression, value: int):
    assert isinstance(expression, IntegerLiteral)
    assert expression.value == value
    assert expression.token_literal() == str(value)


@pytest.mark.parametrize("src, operator, integer_value", [
    ("!5;", "!", 5),
    ("-15;", "-", 15),
])
def test_parsing_prefix_expressions(src, operator, integer_value):
    program = parse(src)

    assert len(program.statements) == 1
    stmt = program.statements[0]

    assert isinstance(stmt, ExpressionStatement)
    assert isinstance(stmt.expression, PrefixExpression)
    assert stmt.expression.operator == operator
    assert_integer_literal_expression(stmt.expression.right, integer_value)