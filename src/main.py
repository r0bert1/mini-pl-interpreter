from lexing.lexer import Lexer
from parsing.parser import Parser

while True:
    text = input(">> ")
    lexer = Lexer(text)
    tokens = lexer.generate_tokens()
    # print(list(tokens))
    parser = Parser(tokens)
    tree = parser.parse()
    print(tree)
