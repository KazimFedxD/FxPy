from interpreter import *



def run(file_name: str, text: str) -> tuple[Any, Any]:
    lexer = Lexer(file_name, text)
    tokens, error = lexer.make_tokens()

    if error:
        return None, error
    parser = Parser(tokens)  # type: ignore
    ast = parser.parse()
    if ast.error:
        return None, ast.error

    context = Context("<program>")
    context.symbol_table = global_symbol_table

    interpreter = Interpreter(context)
    result = interpreter.visit(ast.node)

    return result.value, result.error
