from lexer import *

#######################################
# NODES
#######################################

class NumberNode:
    def __init__(self, tok:Token):
        self.tok = tok

        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end

    def __repr__(self):
        return f'{self.tok}'
    
class BinOpNode:
    def __init__(self, left_node, op_tok:Token, right_node):
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node

        self.pos_start = self.left_node.pos_start
        self.pos_end = self.right_node.pos_end

    def __repr__(self):
        return f'({self.left_node}, {self.op_tok}, {self.right_node})'
    
class UnaryOpNode:
    def __init__(self, op_tok:Token, node):
        self.op_tok = op_tok
        self.node = node

        self.pos_start = self.op_tok.pos_start
        self.pos_end = node.pos_end

    def __repr__(self):
        return f'({self.op_tok}, {self.node})'

class VarAccessNode:
    def __init__(self, var_name_tok):
        self.var_name_tok = var_name_tok

        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.var_name_tok.pos_end

    def __repr__(self):
        return f'{self.var_name_tok} ACCESS'

class VarAssignNode:
    def __init__(self, var_name_tok, value_node):
        self.var_name_tok = var_name_tok
        self.value_node = value_node

        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.value_node.pos_end

    def __repr__(self):
        return f'{self.var_name_tok} = {self.value_node}'

class StringNode:
    def __init__(self, tok:Token):
        self.tok = tok

        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end

    def __repr__(self):
        return f'{self.tok}'

class ReturnNode:
    def __init__(self, node_to_return, pos_start, pos_end):
        self.node_to_return = node_to_return
        self.pos_start = pos_start
        self.pos_end = pos_end

    def __repr__(self):
        return f'return {self.node_to_return}'

class ContinueNode:
    def __init__(self, pos_start, pos_end):
        self.pos_start = pos_start
        self.pos_end = pos_end

    def __repr__(self):
        return f'continue'
    
class BreakNode:
    def __init__(self, pos_start, pos_end):
        self.pos_start = pos_start
        self.pos_end = pos_end
    
    def __repr__(self):
        return f'break'
        
class IfNode:
    def __init__(self, cases, else_case):
        self.cases = cases
        self.else_case = else_case

        self.pos_start = self.cases[0][0].pos_start
        self.pos_end = (self.else_case or self.cases[-1][0]).pos_end

    def __repr__(self):
        return f'if {self.cases}'

class ListNode:
    def __init__(self, element_nodes, pos_start, pos_end):
        self.element_nodes = element_nodes
        self.pos_start = pos_start
        self.pos_end = pos_end

    def __repr__(self):
        return f'{self.element_nodes}'

class ForNode:
    def __init__(self, var_name_tok, start_value_node, end_value_node, step_value_node, body_node):
        self.var_name_tok = var_name_tok
        self.start_value_node = start_value_node
        self.end_value_node = end_value_node
        self.step_value_node = step_value_node
        self.body_node = body_node

        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.body_node.pos_end
        
    def __repr__(self):
        f"for {self.var_name_tok} = {self.start_value_node} to {self.end_value_node} step {self.step_value_node} {self.body_node}"

class WhileNode:
    def __init__(self, condition_node, body_node):
        self.condition_node = condition_node
        self.body_node = body_node

        self.pos_start = self.condition_node.pos_start
        self.pos_end = self.body_node.pos_end

    def __repr__(self):
        return f'while {self.condition_node} {self.body_node}'

class FuncDefNode:
    def __init__(self, var_name_tok, arg_name_toks, body_node):
        self.var_name_tok = var_name_tok
        self.arg_name_toks = arg_name_toks
        self.body_node = body_node

        if self.var_name_tok:
            self.pos_start = self.var_name_tok.pos_start
        elif len(self.arg_name_toks) > 0:
            self.pos_start = self.arg_name_toks[0].pos_start
        else:
            self.pos_start = self.body_node.pos_start

        self.pos_end = self.body_node.pos_end
        
    def __repr__(self):
        return f'fex {self.var_name_tok}({self.arg_name_toks}) -> {self.body_node}'

class FuncCallNode:
    def __init__(self, node_to_call, arg_nodes):
        self.node_to_call = node_to_call
        self.arg_nodes = arg_nodes

        self.pos_start = self.node_to_call.pos_start

        if len(self.arg_nodes) > 0:
            self.pos_end = self.arg_nodes[-1].pos_end
        else:
            self.pos_end = self.node_to_call.pos_end

    def __repr__(self):
        return f'{self.node_to_call}({self.arg_nodes})'

#######################################
# PARSE RESULT
#######################################

class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None
        self.last_registered_advance_count = 0
        self.to_reverse_count = 0
        self.advance_count = 0

    def register_advancement(self):
        self.last_registered_advance_count = 1
        self.advance_count += 1

    def register(self, res):
        self.last_registered_advance_count = res.advance_count
        self.advance_count += res.advance_count
        if res.error:
            self.error = res.error
        return res.node

    def try_register(self, res):
        if res.error:
            self.to_reverse_count = res.advance_count
            return None
        return self.register(res)

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        if not self.error or self.last_registered_advance_count == 0:
            self.error = error
        return self


#######################################
# PARSER
#######################################

class Parser:
    def __init__(self, tokens:list[Token]):
        self.tokens = tokens
        self.tok_idx = -1
        self.advance()
        
    def advance(self):
        self.tok_idx += 1
        if self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]
        return self.current_tok
    
    def parse(self):
        res = self.expr()
        return res
    
    def get_statements(self):
        res = ParseResult()
        statements = []
        pos_start = self.current_tok.pos_start.copy()
        while True:
            while self.current_tok.type == TT_NEWLINE:
                res.register_advancement()
                self.advance()
            if self.current_tok.type == TT_EOF:
                return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected end or expression"))
            if self.current_tok.matches(TT_KEYWORD, "end"):
                break
            statement = res.register(self.statement())
            if res.error:
                return res
            statements.append(statement)
        res.register_advancement()
        self.advance()
        
        return res.success(ListNode(statements, pos_start, statements[-1].pos_end))

    
    def statement(self):
        res = ParseResult()
        pos_start = self.current_tok.pos_start.copy()

        if self.current_tok.matches(TT_KEYWORD, "return"):
            res.register_advancement()
            self.advance()

            expr = res.try_register(self.expr())
            if not expr:
                self.reverse(res.to_reverse_count)
            return res.success(
                ReturnNode(expr, pos_start, self.current_tok.pos_start.copy())
            )

        if self.current_tok.matches(TT_KEYWORD, "continue"):
            res.register_advancement()
            self.advance()
            return res.success(
                ContinueNode(pos_start, self.current_tok.pos_start.copy())
            )

        if self.current_tok.matches(TT_KEYWORD, "break"):
            res.register_advancement()
            self.advance()
            return res.success(BreakNode(pos_start, self.current_tok.pos_start.copy()))

        expr = res.register(self.expr())
        if res.error:
            return res.failure(
                InvalidSyntaxError(
                    self.current_tok.pos_start,
                    self.current_tok.pos_end,
                    "Expected 'return', 'continue', 'break', 'let', 'if', 'for', 'while', 'fex', int, float, identifier, '+', '-', '(', '[' or 'not'",
                )
            )
        return res.success(expr)

    def expr(self):
        res = ParseResult()
        if self.current_tok.matches(TT_KEYWORD, "let"):
            res.register_advancement()
            self.advance()
            if self.current_tok.type == TT_IDENTIFIER:
                varname = self.current_tok

                self.advance()
                
                if self.current_tok.type == TT_EQ:
                    self.advance()
                    expr = res.register(self.expr())
                    if res.error:
                        return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected expression"))
                    return res.success(VarAssignNode(varname, expr))
                else:
                    return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected '='"))
                
            else:
                return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected identifier"))
            
            
        node = res.register(self.bin_op(self.comp_expr, ((TT_KEYWORD, "and"), (TT_KEYWORD, "or"))))
        
        if res.error:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected expression"))
        
        return res.success(node)
    
    def comp_expr(self):
        res = ParseResult()

        if self.current_tok.type == TT_NOT:
            op_tok = self.current_tok
            res.register_advancement()
            self.advance()

            node = res.register(self.comp_expr())
            if res.error:
                return res
            return res.success(UnaryOpNode(op_tok, node))

        node = res.register(
            self.bin_op(self.arith_expr, (TT_EE, TT_NE, TT_LT, TT_GT, TT_LTE, TT_GTE))
        )

        if res.error:
            return res.failure(
                InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end, "Expected expression"
                )
            )
        
        return res.success(node)
    

    def arith_expr(self):
        return self.bin_op(self.mod, ((TT_PLUS, TT_MINUS)))

    def mod(self):
        return self.bin_op(self.term, ((TT_MOD, )))
    
    def term(self):
        return self.bin_op(self.factor, ((TT_MUL, TT_DIV)))
    
    
    def factor(self):
        res = ParseResult()
        tok = self.current_tok
        if tok.type in (TT_PLUS, TT_MINUS):
            res.register_advancement()
            self.advance()
            factor = res.register(self.factor())
            if res.error: return res
            return res.success(UnaryOpNode(tok, factor))
        return self.power()
    
    def power(self):
        return self.bin_op(self.atom, (TT_POW, ), self.factor)

    def if_expr(self):
        res = ParseResult()
        cases = []

        if not self.current_tok.matches(TT_KEYWORD, "if"):
            return res.failure(
                InvalidSyntaxError(
                    self.current_tok.pos_start,
                    self.current_tok.pos_end,
                    f"Expected 'if'",
                )
            )
        
        res.register_advancement()
        self.advance()
        
        condition = res.register(self.expr())
        if res.error:
            return res
        
        if not self.current_tok.type == TT_COLON:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected ':'"))
        
        res.register_advancement()
        self.advance()
        
        statements = res.register(self.get_statements())
        if res.error:
            return res
        
        cases.append((condition, statements))
        while self.current_tok.type == TT_NEWLINE:
            res.register_advancement()
            self.advance()
        while self.current_tok.matches(TT_KEYWORD, "elif"):
            print("ELIF")
            
            res.register_advancement()
            self.advance()
            
            condition = res.register(self.expr())
            if res.error:
                return res
            
            if not self.current_tok.type == TT_COLON:
                return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected ':'"))
            
            res.register_advancement()
            self.advance()
            
            statements = res.register(self.get_statements())
            if res.error:
                return res
            
            cases.append((condition, statements))
            
        while self.current_tok.type == TT_NEWLINE:
            res.register_advancement()
            self.advance()
        
        else_case = None
        if self.current_tok.matches(TT_KEYWORD, "else"):
            res.register_advancement()
            self.advance()
            
            if not self.current_tok.type == TT_COLON:
                return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected ':'"))
            
            res.register_advancement()
            self.advance()
            
            else_case = res.register(self.get_statements())
            if res.error:
                return res
            
        return res.success(IfNode(cases, else_case))
        
    def for_expr(self):
        res = ParseResult()
        
        if not self.current_tok.matches(TT_KEYWORD, "for"):
            return res.failure(
                InvalidSyntaxError(
                    self.current_tok.pos_start,
                    self.current_tok.pos_end,
                    f"Expected 'for'",
                )
            )
            
        res.register_advancement()
        self.advance()
        
        if self.current_tok.type != TT_IDENTIFIER:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected identifier"))
        
        var_name = self.current_tok
        res.register_advancement()
        self.advance()
        
        if self.current_tok.type != TT_EQ:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected '='"))
        
        res.register_advancement()
        self.advance()
        
        start_value = res.register(self.expr())
        if res.error:
            return res
        
        if not self.current_tok.matches(TT_KEYWORD, "to"):
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected 'to'"))
        
        res.register_advancement()
        self.advance()
        
        end_value = res.register(self.expr())
        if res.error:
            return res
        
        step_value = NumberNode(Token(TT_INT, 1, self.current_tok.pos_start, self.current_tok.pos_start))
        if self.current_tok.matches(TT_KEYWORD, "step"):
            res.register_advancement()
            self.advance()
            
            step_value = res.register(self.expr())
            if res.error:
                return res
        
        if not self.current_tok.type == TT_COLON:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected ':'"))
        
        res.register_advancement()
        self.advance()
        
        body = res.register(self.get_statements())
        if res.error:
            return res
        
        return res.success(ForNode(var_name, start_value, end_value, step_value, body))
    
    def while_expr(self):
        res = ParseResult()
        
        if not self.current_tok.matches(TT_KEYWORD, "while"):
            return res.failure(
                InvalidSyntaxError(
                    self.current_tok.pos_start,
                    self.current_tok.pos_end,
                    f"Expected 'while'",
                )
            )
            
        res.register_advancement()
        self.advance()
        
        condition = res.register(self.expr())
        if res.error:
            return res
        
        if not self.current_tok.type == TT_COLON:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected ':'"))
        
        res.register_advancement()
        self.advance()
        
        body = res.register(self.get_statements())
        if res.error:
            return res
        
        return res.success(WhileNode(condition, body))
    
    def var_func_access(self):
        res = ParseResult()
        var_name = self.current_tok
        res.register_advancement()
        self.advance()
        if self.current_tok.type == TT_LPAREN:
            args = []
            res.register_advancement()
            self.advance()
            if self.current_tok.type == TT_RPAREN:
                res.register_advancement()
                self.advance()
            else:
                args.append(res.register(self.expr()))
                if res.error:
                    return res
                while self.current_tok.type == TT_COMMA:
                    res.register_advancement()
                    self.advance()
                    args.append(res.register(self.expr()))
                    if res.error:
                        return res
                if self.current_tok.type != TT_RPAREN:
                    return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected ')' or args"))
                res.register_advancement()
                self.advance()
            return res.success(FuncCallNode(var_name, args))
        return res.success(VarAccessNode(var_name))
        
    def func_def(self):
        res = ParseResult()        
        if not self.current_tok.matches(TT_KEYWORD, "fex"):
            return res.failure(
                InvalidSyntaxError(
                    self.current_tok.pos_start,
                    self.current_tok.pos_end,
                    f"Expected 'fex'",
                )
            )
        
        res.register_advancement()
        self.advance()
        
        if self.current_tok.type == TT_IDENTIFIER:
            var_name_tok = self.current_tok
            res.register_advancement()
            self.advance()
        else:
            var_name_tok = None
            
        if self.current_tok.type != TT_LPAREN:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected '('"))
        
        res.register_advancement()
        self.advance()
        
        arg_name_toks = []
        
        if self.current_tok.type == TT_IDENTIFIER:
            arg_name_toks.append(self.current_tok)
            res.register_advancement()
            self.advance()
            
            while self.current_tok.type == TT_COMMA:
                res.register_advancement()
                self.advance()
                
                if self.current_tok.type != TT_IDENTIFIER:
                    return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected identifier"))
                
                arg_name_toks.append(self.current_tok)
                res.register_advancement()
                self.advance()
                
        if self.current_tok.type != TT_RPAREN:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected ')' or args"))
        
        res.register_advancement()
        self.advance()
        
        if  self.current_tok.type == TT_ARROW:
            res.register_advancement()
            self.advance()
            
            body = res.register(self.expr())
            if res.error:
                return res
        else:
            if self.current_tok.type != TT_COLON:
                return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected ':'"))
            
            res.register_advancement()
            self.advance()
            
            body = res.register(self.get_statements())
            if res.error:
                return res
            
        return res.success(FuncDefNode(var_name_tok, arg_name_toks, body))
            
    def list_expr(self):
        res = ParseResult()
        element_nodes = []
        pos_start = self.current_tok.pos_start.copy()
        
        if self.current_tok.type != TT_LSQB:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected '['"))
        
        res.register_advancement()
        self.advance()
        
        if self.current_tok.type == TT_RSQB:
            res.register_advancement()
            self.advance()
        else:
            element_nodes.append(res.register(self.expr()))
            if res.error:
                return res
            
            while self.current_tok.type == TT_COMMA:
                res.register_advancement()
                self.advance()
                
                element_nodes.append(res.register(self.expr()))
                if res.error:
                    return res
                
            if self.current_tok.type != TT_RSQB:
                return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected ',' or ']'"))
            
            res.register_advancement()
            self.advance()
            
        return res.success(ListNode(element_nodes, pos_start, self.current_tok.pos_end))        
    
    def atom(self):
        res = ParseResult()
        tok = self.current_tok
        if tok.type in (TT_INT, TT_FLOAT):
            res.register_advancement()
            self.advance()
            return res.success(NumberNode(tok))
        elif tok.type == TT_STRING:
            res.register_advancement()
            self.advance()
            return res.success(StringNode(tok))
        elif tok.type == TT_LPAREN:
            res.register_advancement()
            self.advance()
            expr = res.register(self.expr())
            if res.error:
                return res
            if self.current_tok.type == TT_RPAREN:
                res.register_advancement()
                self.advance()
                return res.success(expr)
            else:
                return res.failure(
                    InvalidSyntaxError(
                        self.current_tok.pos_start,
                        self.current_tok.pos_end,
                        "Expected ')'",
                    )
                )
        elif tok.type == TT_IDENTIFIER:
            return res.success(self.var_func_access())

        elif tok.matches(TT_KEYWORD, "if"):
            if_expr = res.register(self.if_expr())
            if res.error:
                return res
            return res.success(if_expr)

        elif tok.matches(TT_KEYWORD, "for"):
            for_expr = res.register(self.for_expr())
            if res.error:
                return res
            return res.success(for_expr)
        
        elif tok.matches(TT_KEYWORD, "while"):
            while_expr = res.register(self.while_expr())
            if res.error:
                return res
            return res.success(while_expr)
        
        elif tok.matches(TT_KEYWORD, "fex"):
            func_def = res.register(self.func_def())
            if res.error:
                return res
            return res.success(func_def)
        
        elif tok.type == TT_LSQB:
            list_expr = res.register(self.list_expr())
            if res.error:
                return res
            return res.success(list_expr)
        

        return res.failure(InvalidSyntaxError(tok.pos_start, tok.pos_end, "Expected int or float or '('"))
    
    
    
    def bin_op(self, func_a, ops, func_b=None):
        func_b = func_b or func_a
        res = ParseResult()
        left = res.register(func_a())
        if res.error: return res
        while (
            self.current_tok.type in ops
            or (self.current_tok.type, self.current_tok.value) in ops
        ):
            op_tok = self.current_tok
            res.register_advancement()
            self.advance()
            right = res.register(func_b())
            if res.error: return res
            left = BinOpNode(left, op_tok, right)
        return res.success(left)
