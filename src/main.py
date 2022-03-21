import sys

from lexing.lexer import Lexer
from parsing.parser import Parser
from interpreting.interpreter import Interpreter
from interpreting.context import Context
from interpreting.symbol_table import SymbolTable
from interpreting.values import Number

global_symbol_table = SymbolTable()
global_symbol_table.set("false", Number.false)
global_symbol_table.set("true", Number.true)

def run(file_name, text):
    lexer = Lexer(file_name, text)
    tokens, error = lexer.generate_tokens()
    if error:
        print(error)
        return

    parser = Parser(tokens)
    tree = parser.parse()
    if tree.error:
        print(tree.error)
        return
    
    interpreter = Interpreter()
    context = Context('<program>')
    context.symbol_table = global_symbol_table
    result = interpreter.evaluate(tree.node, context)
    if result.error: print(result.error)

if len(sys.argv) == 2:
    lines = []
    try:
        with open(sys.argv[1], "r") as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Failed to load \"{sys.argv[1]}\"\n" + str(e))

    combined = []
    i = 0
    while i < len(lines):
        combined.append(lines[i])
        if lines[i].startswith('for'):
            j = 1
            while not lines[i+j].startswith('end'):
                combined[i] += lines[i+j]
                j += 1
            combined[i] += lines[i+j]
            i += j + 1
            continue
        i += 1

    for line in combined:
        # print(line)
        run(sys.argv[1], line)
else:
    while True:
        text = input(">> ")
        if text.strip() == "": continue
        run('<stdin>', text)




