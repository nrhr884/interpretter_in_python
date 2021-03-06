from ast_type import (
    Program,
    Identifier,
    Boolean,
    LetStatement,
    ReturnStatement,
    Expression,
    ExpressionStatement,
    IfExpression,
    IntegerLiteral,
    FunctionLiteral,
    PrefixExpression,
    CallExpression,
    InfixExpression
    )
from lexer import Lexer
from monkey_parser import Parser
import pytest
from typing import Union


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


@pytest.mark.parametrize("src, expected_identifier, expected_value", [
    ("let x = 5;", "x", 5),
    ("let y = true;", "y", True),
    ("let foobar = y;", "foobar", "y")
])
def test_let_statements(src, expected_identifier, expected_value):
    program = parse(src)
    assert len(program.statements) == 1

    stmt = program.statements[0]

    assert isinstance(stmt, LetStatement)
    assert_literal_expression(stmt.name, expected_identifier)
    assert_literal_expression(stmt.value, expected_value)

@pytest.mark.parametrize("src, expected_value", [
    ("return 5", 5),
    ("return true", True),
])
def test_return_statements(src, expected_value):
    program = parse(src)
    assert len(program.statements) == 1

    stmt = program.statements[0]

    assert isinstance(stmt, ReturnStatement)
    assert_literal_expression(stmt.return_value, expected_value)


def test_identifier_expression():
    src = "foobar;"

    program = parse(src)

    assert len(program.statements) == 1
    stmt = program.statements[0]

    assert isinstance(stmt, ExpressionStatement)
    assert isinstance(stmt.expression, Identifier)
    assert stmt.expression.value == "foobar"
    assert stmt.expression.token_literal() == "foobar"


def assert_literal_expression(expression: Expression, value: Union[int, str, bool]):
    def assert_integer_literal(expression: Expression, value: int):
        assert isinstance(expression, IntegerLiteral)
        assert expression.value == value
        assert expression.token_literal() == str(value)

    def assert_identifiler(expression: Expression, value: str):
        assert isinstance(expression, Identifier)
        assert expression.value == value
        assert expression.token_literal() == value

    def assert_boolean(expression: Expression, value: bool):
        assert isinstance(expression, Boolean)
        assert expression.value == value
        assert expression.token_literal() == str(value).lower()

    if type(value) == int:
        assert_integer_literal(expression, value)
    elif type(value) == str:
        assert_identifiler(expression, value)
    elif type(value) == bool:
        assert_boolean(expression, value)
    else:
        assert False, "type of value is invalid"

@pytest.mark.parametrize("src, operator, integer_value", [
    ("!5;", "!", 5),
    ("-15;", "-", 15),
    ("!true;", "!", True),
    ("!false;", "!", False),
])
def test_parsing_prefix_expressions(src, operator, integer_value):
    program = parse(src)

    assert len(program.statements) == 1
    stmt = program.statements[0]

    assert isinstance(stmt, ExpressionStatement)
    assert isinstance(stmt.expression, PrefixExpression)
    assert stmt.expression.operator == operator
    assert_literal_expression(stmt.expression.right, integer_value)

def assert_infix_expression(expression: InfixExpression, left_value, operator, right_value):
    assert isinstance(expression, InfixExpression)
    assert expression.operator == operator
    assert_literal_expression(expression.left, left_value)
    assert_literal_expression(expression.right, right_value)

@pytest.mark.parametrize("src, left_value, operator, right_value", [
    ("5 + 5;", 5, "+", 5),
    ("5 - 5;", 5, "-", 5),
    ("5 * 5;", 5, "*", 5),
    ("5 / 5;", 5, "/", 5),
    ("5 > 5;", 5, ">", 5),
    ("5 < 5;", 5, "<", 5),
    ("5 == 5;", 5, "==", 5),
    ("5 != 5;", 5, "!=", 5),
    ("true == true", True, "==", True),
    ("true != true", True, "!=", True),
    ("false == false", False, "==", False),
    ("false != false", False, "!=", False),
])
def test_parsing_infix_expressions(src, left_value, operator, right_value):
    program = parse(src)

    assert len(program.statements) == 1
    stmt = program.statements[0]

    assert isinstance(stmt, ExpressionStatement)
    assert_infix_expression(stmt.expression, left_value, operator, right_value)

@pytest.mark.parametrize("src, expected", [
    ("-a * b", "((-a) * b)"),
    ("!-a", "(!(-a))"),
    ("a + b + c", "((a + b) + c)"),
    ("a + b - c", "((a + b) - c)"),
    ("a * b * c", "((a * b) * c)"),
    ("a * b / c", "((a * b) / c)"),
    ("a + b / c", "(a + (b / c))"),
    ("a + b * c + d / e - f", "(((a + (b * c)) + (d / e)) - f)"),
    ("3 + 4; -5 + 5", "(3 + 4)((-5) + 5)"),
    ("5 > 4 == 3 < 4", "((5 > 4) == (3 < 4))"),
    ("5 < 4 != 3 > 4", "((5 < 4) != (3 > 4))"),
    ("3 + 4 * 5 == 3 * 1 + 4 * 5", "((3 + (4 * 5)) == ((3 * 1) + (4 * 5)))"),
    ("true", "true"),
    ("false", "false"),
    ("3 > 5 == false", "((3 > 5) == false)"),
    ("3 < 5 == true", "((3 < 5) == true)"),
    ("1 + (2 + 3) + 4", "((1 + (2 + 3)) + 4)"),
    ("(5 + 5) * 2", "((5 + 5) * 2)"),
    ("2 / (5 + 5)", "(2 / (5 + 5))"),
    ("-(5 + 5)", "(-(5 + 5))"),
    ("!(true == true)", "(!(true == true))"),
])
def test_operator_precendence_parsing(src, expected):
    program = parse(src)
    assert program.string() == expected

def test_if_expression():
    src = 'if (x < y) { x }'
    program = parse(src)

    assert len(program.statements) == 1
    stmt = program.statements[0]

    assert isinstance(stmt, ExpressionStatement)
    assert isinstance(stmt.expression, IfExpression)
    assert_infix_expression(stmt.expression.condition, "x", "<", "y")

    assert len(stmt.expression.consequence.statements) == 1
    consequence_stmt = stmt.expression.consequence.statements[0]
    assert isinstance(consequence_stmt, ExpressionStatement)
    assert isinstance(consequence_stmt.expression, Identifier)

    assert_literal_expression(consequence_stmt.expression, "x")

    assert not stmt.expression.alternative


def test_if_else_expression():
    src = 'if (x < y) { x } else { y }'
    program = parse(src)

    assert len(program.statements) == 1
    stmt = program.statements[0]

    assert isinstance(stmt, ExpressionStatement)
    assert isinstance(stmt.expression, IfExpression)
    assert_infix_expression(stmt.expression.condition, "x", "<", "y")

    assert len(stmt.expression.consequence.statements) == 1
    consequence_stmt = stmt.expression.consequence.statements[0]
    assert isinstance(consequence_stmt, ExpressionStatement)
    assert isinstance(consequence_stmt.expression, Identifier)
    assert_literal_expression(consequence_stmt.expression, "x")

    assert len(stmt.expression.alternative.statements) == 1
    alternative_stmt = stmt.expression.alternative.statements[0]
    assert isinstance(alternative_stmt, ExpressionStatement)
    assert isinstance(alternative_stmt.expression, Identifier)
    assert_literal_expression(alternative_stmt.expression, "y")


@pytest.mark.parametrize("src, expected_params", [
    ("fn() { }", []),
    ("fn(x) { }", ["x"]),
    ("fn(x, y, z) { }", ["x", "y", "z"])])
def test_function_literal_parsing(src, expected_params):
    program = parse(src)

    assert len(program.statements) == 1
    stmt = program.statements[0]
    assert isinstance(stmt, ExpressionStatement)
    assert isinstance(stmt.expression, FunctionLiteral)

    function = stmt.expression
    assert len(function.parameters) == len(expected_params)

    for actual, expected in zip(function.parameters, expected_params):
        assert_literal_expression(actual, expected)


def test_call_expression_parsing():
    src = 'add(1, 2 * 3, 4 + 5);'
    program = parse(src)

    assert len(program.statements) == 1
    stmt = program.statements[0]

    assert isinstance(stmt, ExpressionStatement)
    assert isinstance(stmt.expression, CallExpression)

    exp = stmt.expression

    assert_literal_expression(exp.function, "add")

    assert len(exp.arguments) == 3
    assert_literal_expression(exp.arguments[0], 1)
    assert_infix_expression(exp.arguments[1], 2, "*", 3)
    assert_infix_expression(exp.arguments[2], 4, "+", 5)
