from lexing.lexer import Lexer
from parsing.parser import Parser
from interpreting.interpreter import Interpreter

while True:
    text = input(">> ")
    lexer = Lexer('<stdin>', text)
    tokens, error = lexer.generate_tokens()
    if error: print(error)
    else : print(tokens)
    """parser = Parser(list(tokens))
    tree = parser.parse()
    if not tree: continue
    interpreter = Interpreter()
    value = interpreter.evaluate(tree)
    print(value)
    """