from __future__ import annotations
from abc import ABC
from typing import Self
from fxparser import *
import sys

sys.set_int_max_str_digits(1000000)

#######################################
# RUNTIME RESULT
#######################################


class RTResult:
    def __init__(self):
        self.reset()

    def reset(self):
        self.value:Optional[Value] = None
        self.error:Optional[RTError] = None
        self.func_return_value:Optional[Value] = None
        self.loop_should_continue:bool = False
        self.loop_should_break:bool = False

    def register(self, res:Self) -> "Value | None":
        self.error = res.error
        self.func_return_value = res.func_return_value
        self.loop_should_continue = res.loop_should_continue
        self.loop_should_break = res.loop_should_break
        return res.value

    def success(self, value:"Value | None"):
        self.reset()
        self.value = value
        return self

    def failure(self, error:RTError|None):
        self.reset()
        self.error = error
        return self

    def success_return(self, value:"Value"):
        self.reset()
        self.func_return_value = value
        return self

    def success_continue(self):
        self.reset()
        self.loop_should_continue = True
        return self

    def success_break(self):
        self.reset()
        self.loop_should_break = True
        return self

    def should_return(self):
        return (
            self.error
            or self.func_return_value
            or self.loop_should_continue
            or self.loop_should_break
        )


#######################################
# VALUES
#######################################


class Value(ABC):
    def __init__(self):
        self.set_pos()
        self.set_context()

    def set_pos(self, pos_start:Optional[Position]=None, pos_end:Optional[Position]=None):
        self.pos_start:Optional[Position] = pos_start
        self.pos_end:Optional[Position] = pos_end
        return self

    def set_context(self, context:Optional[Context]=None):
        self.context = context
        return self

    def added_to(self, other:Self) -> tuple[Self, None] | tuple[None, Optional[RTError]]:
        return None, self.illegal_operation(other)

    def subbed_by(self, other:Self) -> tuple[Self, None] | tuple[None, Optional[RTError]]:
        return None, self.illegal_operation(other)

    def multed_by(self, other:Self) -> tuple[Self, None] | tuple[None, Optional[RTError]]:
        return None, self.illegal_operation(other)

    def dived_by(self, other:Self) -> tuple[Self, None] | tuple[None, Optional[RTError]]:
        return None, self.illegal_operation(other)

    def powed_by(self, other:Self) -> tuple[Self, None] | tuple[None, Optional[RTError]]:
        return None, self.illegal_operation(other)

    def get_comparison_eq(self, other:Self) -> tuple[Boolean, None] | tuple[None, Optional[RTError]]:
        return None, self.illegal_operation(other)

    def get_comparison_ne(self, other:Self) -> tuple[Boolean, None] | tuple[None, Optional[RTError]]:
        return None, self.illegal_operation(other)

    def get_comparison_lt(self, other:Self) -> tuple[Boolean, None] | tuple[None, Optional[RTError]]:
        return None, self.illegal_operation(other)

    def get_comparison_gt(self, other:Self) -> tuple[Boolean, None] | tuple[None, Optional[RTError]]:
        return None, self.illegal_operation(other)

    def get_comparison_lte(self, other:Self) -> tuple[Boolean, None] | tuple[None, Optional[RTError]]:
        return None, self.illegal_operation(other)

    def get_comparison_gte(self, other:Self) -> tuple[Boolean, None] | tuple[None, Optional[RTError]]:
        return None, self.illegal_operation(other)

    def anded_by(self, other:Self) -> tuple[Boolean, None] | tuple[None, Optional[RTError]]:
        return None, self.illegal_operation(other)

    def ored_by(self, other:Self) -> tuple[Boolean, None] | tuple[None, Optional[RTError]]:
        return None, self.illegal_operation(other)

    def notted(self) -> tuple[Boolean, None] | tuple[None, Optional[RTError]]:
        return None, self.illegal_operation()

    def execute(self, args:list[Value]):
        return RTResult().failure(self.illegal_operation())

    def copy(self) -> Self:
        raise NotImplemented
    def is_true(self) -> bool:
        return False

    def illegal_operation(self, other:Self|None=None):
        if not other:
            other = self
        if self.pos_start and other.pos_end and self.context:
            return RTError(self.pos_start, other.pos_end, "Illegal operation", self.context)

class Boolean(Value):
    def __init__(self, value:Any["str", "int", "bool", "float", "list"]):
        super().__init__()
        self.value = value

    def copy(self) -> Boolean:
        copy = Boolean(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy
    
    def is_true(self):
        return self.value
    
    def anded_by(self, other:Value):
        if isinstance(other, Boolean):
            return Boolean(self.value and other.value).set_context(self.context), None
        elif isinstance(other, Number) or isinstance(other, String) or isinstance(other, List):
            return Boolean(self.value and other.is_true()).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
        
    def added_to(self, other:Value):
        if isinstance(other, Boolean):
            return Boolean(self.value or other.value).set_context(self.context), None
        elif isinstance(other, Number) or isinstance(other, String) or isinstance(other, List):
            return Boolean(self.value or other.is_true()).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
        
    def multed_by(self, other:Value):
        if isinstance(other, Boolean):
            return Boolean(self.value and other.value).set_context(self.context), None
        elif isinstance(other, Number) or isinstance(other, String) or isinstance(other, List):
            return Boolean(self.value and other.is_true()).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
    
    def ored_by(self, other:Value):
        if isinstance(other, Boolean):
            return Boolean(self.value or other.value).set_context(self.context), None
        elif isinstance(other, Number) or isinstance(other, String) or isinstance(other, List):
            return Boolean(self.value or other.is_true()).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
        
    def notted(self):
        return Boolean(not self.value).set_context(self.context), None
    
    def __str__(self):
        return "True" if self.value else "False"

    def __repr__(self):
        return "True" if self.value else "False"
    
class Number(Value):
    def __init__(self, value:int|float):
        super().__init__()
        self.value = value

    def added_to(self, other:Value):
        if isinstance(other, Number):
            return Number(self.value + other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def subbed_by(self, other:Value):
        if isinstance(other, Number):
            return Number(self.value - other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def multed_by(self, other:Value):
        if isinstance(other, Number):
            return Number(self.value * other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def dived_by(self, other:Value):
        if isinstance(other, Number):
            if other.value == 0:
                return None, RTError(
                    other.pos_start, other.pos_end, "Division by zero", self.context
                )

            return Number(self.value / other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def powed_by(self, other:Value):
        if isinstance(other, Number):
            return Number(self.value**other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_eq(self, other:Value):
        if isinstance(other, Number):
            return (
                Boolean(int(self.value == other.value)).set_context(self.context),
                None,
            )
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_ne(self, other:Value):
        if isinstance(other, Number):
            return (
                Boolean(int(self.value != other.value)).set_context(self.context),
                None,
            )
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_lt(self, other:Value):
        if isinstance(other, Number):
            return Boolean(int(self.value < other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_gt(self, other:Value):
        if isinstance(other, Number):
            return Boolean(int(self.value > other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_lte(self, other:Value):
        if isinstance(other, Number):
            return (
                Boolean(int(self.value <= other.value)).set_context(self.context),
                None,
            )
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_gte(self, other:Value):
        if isinstance(other, Number):
            return (
                Boolean(int(self.value >= other.value)).set_context(self.context),
                None,
            )
        else:
            return None, Value.illegal_operation(self, other)

    def copy(self) :
        copy = Number(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def is_true(self):
        return self.value != 0

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self.value)
    
class String(Value):
    def __init__(self, value:str):
        super().__init__()
        self.value = value

    def added_to(self, other:Value):
        if isinstance(other, String) or isinstance(other, Number):
            return String(self.value + str(other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def multed_by(self, other:Value):
        if isinstance(other, Number) and isinstance(other.value, int):
            return String(self.value * other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def is_true(self):
        return len(self.value) > 0

    def get_comparison_eq(self, other:Value):
        if isinstance(other, String):
            return (
                Boolean((self.value == other.value)).set_context(self.context),
                None,
            )
        else:
            return None, Value.illegal_operation(self, other)
    
    def get_comparison_ne(self, other:Value):
        if isinstance(other, String):
            return (
                Boolean((self.value != other.value)).set_context(self.context),
                None,
            )
        else:
            return None, Value.illegal_operation(self, other)

    def copy(self):
        copy = String(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value

class List(Value):
    def __init__(self, elements:list[Value|None]):
        super().__init__()
        self.elements = elements

    def added_to(self, other:Value):
        if isinstance(other, List):
            return List(self.elements + other.elements).set_context(self.context), None
        else:
            newlist = self.copy()
            newlist.elements.append(other)
            return newlist, None
        
    def multed_by(self, other:Value):
        if isinstance(other, Number) and isinstance(other.value, int):
            return List(self.elements * other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
    
    def subbed_by(self, other:Value):
        if isinstance(other, Number) and isinstance(other.value, int):
            try:
                newlist = self.copy()
                newlist.elements.pop(other.value)
                return newlist, None
            except:
                return None, RTError(other.pos_start, other.pos_end, "Index out of bounds", self.context)
        else:
            return None, Value.illegal_operation(self, other)
        
    def dived_by(self, other:Value):  # type: ignore
        if isinstance(other, Number) and isinstance(other.value, int):
            try:
                return self.elements[other.value], None
            except:
                return None, RTError(other.pos_start, other.pos_end, "Index out of bounds", self.context)
        else:
            return None, Value.illegal_operation(self, other)
        
    def get_comparison_eq(self, other:List):
        return Boolean(self.elements == other.elements).set_context(self.context), None
    
    def get_comparison_ne(self, other:List):
        return Boolean(self.elements != other.elements).set_context(self.context), None
    
    def get_comparison_gt(self, other:List):
        return Boolean(len(self.elements) > len(other.elements)).set_context(self.context), None
    
    def get_comparison_lt(self, other:List):
        return Boolean(len(self.elements) < len(other.elements)).set_context(self.context), None
    
    def get_comparison_gte(self, other:List):
        return Boolean(len(self.elements) >= len(other.elements)).set_context(self.context), None
    
    def get_comparison_lte(self, other:List):
        return Boolean(len(self.elements) <= len(other.elements)).set_context(self.context), None
    
    def is_true(self):
        return len(self.elements) > 0
    
        
    def copy(self):
        copy = List(self.elements)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy
    
    def __str__(self):
        return f"[{', '.join(str(x) for x in self.elements)}]"
    
    def __repr__(self):
        return f"{', '.join(repr(x) for x in self.elements)}"
    
    

#######################################
# CONTEXT
#######################################


class Context:
    def __init__(self, display_name:str, parent:Self|None=None, parent_entry_pos:Position|None=None):
        self.display_name = display_name
        self.parent = parent
        self.parent_entry_pos = parent_entry_pos
        self.symbol_table:SymbolTable|None = None


#######################################
# SYMBOL TABLE
#######################################


class SymbolTable:
    def __init__(self, parent:Self|None=None):
        self.symbols:dict[str, Value] = {}
        self.parent = parent

    def get(self, name:str) -> Value|None:
        value:Value|None = self.symbols.get(name, None)
        if value == None and self.parent:
            return self.parent.get(name)
        return value

    def set(self, name:str, value:Value):
        self.symbols[name] = value

    def remove(self, name:str):
        del self.symbols[name]

    def copy(self):
        copy = SymbolTable(self.parent)
        copy.symbols = self.symbols.copy()
        return copy

#######################################
# INTERPRETER
#######################################



class Interpreter:
    def __init__(self, context:Context) -> None:
        self.context = context
        self.methods:dict[str, function] = {
            "NumberNode": self.visit_NumberNode,
            "BinOpNode": self.visit_BinOpNode,
            "UnaryOpNode": self.visit_UnaryOpNode,
            "VarAccessNode": self.visit_VarAccessNode,
            "VarAssignNode": self.visit_VarAssignNode,
            "StringNode": self.visit_StringNode,
            "IfNode": self.visit_IfNode,
            "ListNode": self.visit_ListNode,
            "ForNode": self.visit_ForNode,
            "WhileNode": self.visit_WhileNode,
            "BreakNode": self.visit_BreakNode,
            "ContinueNode": self.visit_ContinueNode,
        }
        
    def visit(self, node:Any["Node"], context:Optional[Context]=None):
        context = context or self.context
        method_name = f"visit_{type(node).__name__}"
        method = getattr(self, method_name, self.no_visit_method)
        return method(node, context)

    def no_visit_method(self, node:Any["Node"], context:Context):
        raise Exception(f"No visit_{type(node).__name__} method defined")

    ###################################


    def visit_NumberNode(self, node:NumberNode, context:Context):
        return RTResult().success(
            Number(node.tok.value) # type: ignore
            .set_context(context)
            .set_pos(node.pos_start, node.pos_end)
        )
    def visit_BinOpNode(self, node:BinOpNode, context:Context):
        res = RTResult()
        left:Value = res.register(self.visit(node.left_node, context)) # type: ignore
        if res.should_return():
            return res
        right:Value = res.register(self.visit(node.right_node, context)) # type: ignore
        if res.error:
            return res

        if node.op_tok.type == TT_PLUS:
            result, error = left.added_to(right)
        elif node.op_tok.type == TT_MINUS:
            result, error = left.subbed_by(right)
        elif node.op_tok.type == TT_MUL:
            result, error = left.multed_by(right)
        elif node.op_tok.type == TT_DIV:
            result, error = left.dived_by(right)
        elif node.op_tok.type == TT_POW:
            result, error = left.powed_by(right)
        elif node.op_tok.type == TT_EE:
            result, error = left.get_comparison_eq(right)
        elif node.op_tok.type == TT_NE:
            result, error = left.get_comparison_ne(right)
        elif node.op_tok.type == TT_LT:
            result, error = left.get_comparison_lt(right)
        elif node.op_tok.type == TT_GT:
            result, error = left.get_comparison_gt(right)
        elif node.op_tok.type == TT_LTE:
            result, error = left.get_comparison_lte(right)
        elif node.op_tok.type == TT_GTE:
            result, error = left.get_comparison_gte(right)
        elif node.op_tok.matches(TT_KEYWORD, "and"):
            result, error = left.anded_by(right)
        elif node.op_tok.matches(TT_KEYWORD, "or"):
            result, error = left.ored_by(right)
        else:
            result, error = None, RTError(
                node.pos_start, node.pos_end, "Invalid operation", context
            )
        
        if not result or error:
            return res.failure(error)
        else:
            return res.success(result.set_pos(node.pos_start, node.pos_end))

    def visit_UnaryOpNode(self, node:UnaryOpNode, context:Context):
        res = RTResult()
        number:Number|Boolean = res.register(self.visit(node.node, context)) # type: ignore
        if res.should_return():
            return res

        error = None

        if node.op_tok.type == TT_MINUS:
            number, error = number.multed_by(Number(-1))  # type: ignore
        elif node.op_tok.type == TT_NOT:
            number, error = number.notted() # type: ignore

        if error:
            return res.failure(error)
        else:
            return res.success(number.set_pos(node.pos_start, node.pos_end))

    def visit_VarAccessNode(self, node:VarAccessNode, context:Context):
        res = RTResult()
        var_name = node.var_name_tok.value
        value = context.symbol_table.get(var_name) # type: ignore
        if not value:
            return res.failure(
                RTError(
                    node.pos_start,
                    node.pos_end,
                    f"'{var_name}' is not defined",
                    context,
                )
            )
        value = value.copy().set_pos(node.pos_start, node.pos_end)
        return res.success(value)
    
    def visit_VarAssignNode(self, node:VarAssignNode, context:Context):
        res = RTResult()
        var_name = node.var_name_tok.value
        value = res.register(self.visit(node.value_node, context))
        if res.should_return():
            return res
        context.symbol_table.set(var_name, value) # type: ignore
        return res.success(value) # type: ignore
    
    def visit_StringNode(self, node: StringNode, context:Context):
        return RTResult().success(
            String(node.tok.value) # type: ignore
            .set_context(context)
            .set_pos(node.pos_start, node.pos_end)
        )
        
    def visit_IfNode(self, node: IfNode, context:Context):
        res = RTResult()
        for condition, expr in node.cases:
            condition_value = res.register(self.visit(condition, context))
            if res.should_return():
                return res
            if condition_value.is_true(): # type: ignore
                expr_value = res.register(self.visit(expr, context))
                if res.should_return():
                    return res
                return res.success(expr_value) # type: ignore
                
        if node.else_case:
            else_value = res.register(self.visit(node.else_case, context))
            if res.should_return():
                return res
            return res.success(else_value) # type: ignore
        return res.success(None) # type: ignore
    
    def visit_ListNode(self, node:ListNode, context:Context):
        res = RTResult()
        elements:list[Value|None] = []
        for element_node in node.element_nodes:
            elements.append(res.register(self.visit(element_node, context)))
            if res.should_return():
                return res
        return res.success(
            List(elements)
            .set_context(context)
            .set_pos(node.pos_start, node.pos_end)
        )
        
    def visit_ForNode(self, node:ForNode, context:Context):
        res = RTResult()
        start_value:Number = res.register(self.visit(node.start_value_node, context)) # type: ignore
        if res.should_return():
            return res
        end_value = res.register(self.visit(node.end_value_node, context))
        if res.should_return():
            return res
        step_value = res.register(self.visit(node.step_value_node, context))
        if res.should_return():
            return res
        i = start_value.value
        if step_value == 0: # type: ignore
            return res.failure(
                RTError(
                    node.pos_start,
                    node.pos_end,
                    "Step value cannot be zero",
                    context
                )
            )
        elif step_value.value > 0: # type: ignore
            condition = lambda: i <= end_value.value # type: ignore
        else:
            condition = lambda: i >= end_value.value # type: ignore
        while condition():
            context.symbol_table.set(node.var_name_tok.value, Number(i)) # type: ignore
            i += step_value.value # type: ignore
            res.register(self.visit(node.body_node, context))
            if res.should_return():
                if res.loop_should_continue:
                    continue
                if res.loop_should_break:
                    break
                return res
        return res.success(None)
    
    def visit_WhileNode(self, node:WhileNode, context:Context):
        res = RTResult()
        while True:
            condition = res.register(self.visit(node.condition_node, context))
            if res.should_return():
                return res
            if not condition.is_true(): # type: ignore
                break
            res.register(self.visit(node.body_node, context))
            if res.should_return():
                if res.loop_should_continue:
                    continue
                if res.loop_should_break:
                    break
                return res
        return res.success(None)
    
    def visit_BreakNode(self, node:BreakNode, context:Context):
        return RTResult().success_break()
    
    def visit_ContinueNode(self, node:ContinueNode, context:Context):
        return RTResult().success_continue()
    
    
    
    