from lexing.lexer import Lexer

while True:
    text = input(">> ")
    lexer = Lexer(text)
    tokens = lexer.generate_tokens()
    print(list(tokens))