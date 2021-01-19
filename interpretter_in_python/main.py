import sys
from lexer import Lexer
from monkey_parser import Parser
from token_type import Token, TokenType

if __name__ == "__main__":
    prompt = '>>'

    print('Hello! This is the Monkey programming language!')
    print('Feel free to type in commands')
    print(prompt, end="", flush=True)

    for l in sys.stdin:
        input_str = l.strip()
        lexer = Lexer(input_str=input_str)
        parser = Parser(lexer)
        program = parser.parse_program()

        if parser.errors:
            for e in parser.errors:
                print(f"\t{e}")
        else:
            print(program.string())

        print(prompt, end="", flush=True)
