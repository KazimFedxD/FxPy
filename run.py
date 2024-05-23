from interpreter import *

global_symbol_table = SymbolTable()

global_symbol_table.set("Null", Number(0))
global_symbol_table.set("True", Boolean(True))
global_symbol_table.set("False", Boolean(False))


def run(file_name, text):
    lexer = Lexer(file_name, text)
    tokens, error = lexer.make_tokens()
    
    if error:
        return None, error
    print(repr(tokens))    
    parser = Parser(tokens)
    ast = parser.parse()
    print(repr(ast))
    if ast.error:
        return None, ast.error
        
    context = Context('<program>')
    context.symbol_table = global_symbol_table
    
    interpreter = Interpreter(context)
    result = interpreter.visit(ast.node)
    
    return result.value, result.error


