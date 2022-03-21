from lexing.lexer import Lexer
from parsing.parser import Parser
from interpreting.interpreter import Interpreter
from interpreting.context import Context
from interpreting.symbol_table import SymbolTable
from interpreting.values import Number

global_symbol_table = SymbolTable()
global_symbol_table.set("false", Number.false)
global_symbol_table.set("true", Number.true)

while True:
    text = input(">> ")
    if text.strip() == "": continue

    lexer = Lexer('<stdin>', text)
    tokens, error = lexer.generate_tokens()
    if error:
        print(error)
        continue

    parser = Parser(tokens)
    tree = parser.parse()
    if tree.error:
        print(tree.error)
        continue
    
    interpreter = Interpreter()
    context = Context('<program>')
    context.symbol_table = global_symbol_table
    result = interpreter.evaluate(tree.node, context)
    if result.error: print(result.error)
    else: print(result.value)
