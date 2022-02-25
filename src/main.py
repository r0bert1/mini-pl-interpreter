from lexing.lexer import Lexer
from parsing.parser import Parser
from interpreting.interpreter import Interpreter

while True:
    text = input(">> ")
    lexer = Lexer(text)
    tokens = lexer.generate_tokens()
    parser = Parser(tokens)
    tree = parser.parse()
    if not tree: continue
    interpreter = Interpreter()
    value = interpreter.evaluate(tree)
    print(value)
