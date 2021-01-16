import sys
from lexer import Lexer
from token_type import Token, TokenType

if __name__ == "__main__":
    prompt = '>>'

    print('Hello! This is the Monkey programming language!')
    print('Feel free to type in commands')
    print(prompt, end="", flush=True)

    for l in sys.stdin:
        input_str = l.strip()
        lexer = Lexer(input_str=input_str)
        while True:
            tk = lexer.next_token()
            print(tk)
            if tk.type == TokenType.EOF:
                break
        print(prompt, end="", flush=True)
