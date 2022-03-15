from lexing.lexer import Lexer
from parsing.parser import Parser
from interpreting.interpreter import Interpreter

while True:
    text = input(">> ")

    lexer = Lexer('<stdin>', text)
    tokens, error = lexer.generate_tokens()
    if error: print(error)

    parser = Parser(tokens)
    tree = parser.parse()
    if tree.error: print(tree.error)
    else: print(tree.node)
    
    """
    if not tree: continue
    interpreter = Interpreter()
    value = interpreter.evaluate(tree)
    print(value)
    """