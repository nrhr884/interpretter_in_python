import pytest
from lexer import Lexer
from monkey_parser import Parser
from object import Object, Integer, Boolean, Null
from evaluator import eval


def eval_src(src: str):
    lexer = Lexer(src)
    parser = Parser(lexer)
    program = parser.parse_program()
    return eval(program)

def assert_integer_object(obj: Object, expected: int):
    assert isinstance(obj, Integer)
    assert obj.value == expected

def assert_boolean_object(obj: Object, expected: bool):
    assert isinstance(obj, Boolean)
    assert obj.value == expected

@pytest.mark.parametrize("src, expected", [
    ("5", 5),
    ("10", 10),
])
def test_eval_integer_expression(src, expected):
    evaluated = eval_src(src)
    assert_integer_object(evaluated, expected)

@pytest.mark.parametrize("src, expected", [
    ("true", True),
    ("false", False),
])
def test_eval_boolean_expression(src, expected):
    evaluated = eval_src(src)
    assert_boolean_object(evaluated, expected)

