from __future__ import annotations
from abc import ABC
import os
import random
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
        self.value: Optional[Value] = None
        self.error: Optional[Error] = None
        self.func_return_value: Optional[Value] = None
        self.loop_should_continue: bool = False
        self.loop_should_break: bool = False

    def register(self, res: Self) -> "Value | None":
        self.error = res.error
        self.func_return_value = res.func_return_value
        self.loop_should_continue = res.loop_should_continue
        self.loop_should_break = res.loop_should_break
        return res.value

    def success(self, value: "Value | None"):
        self.reset()
        self.value = value
        return self

    def failure(self, error: Error | None):
        self.reset()
        self.error = error 
        return self

    def success_return(self, value: "Value"):
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

    def set_pos(
        self, pos_start: Optional[Position] = None, pos_end: Optional[Position] = None
    ):
        self.pos_start: Optional[Position] = pos_start
        self.pos_end: Optional[Position] = pos_end
        return self

    def set_context(self, context: Optional[Context] = None):
        self.context = context
        return self

    def added_to(
        self, other: Self
    ) -> tuple[Self, None] | tuple[None, Optional[RTError]]:
        return None, self.illegal_operation(other)

    def subbed_by(
        self, other: Self
    ) -> tuple[Self, None] | tuple[None, Optional[RTError]]:
        return None, self.illegal_operation(other)

    def multed_by(
        self, other: Self
    ) -> tuple[Self, None] | tuple[None, Optional[RTError]]:
        return None, self.illegal_operation(other)

    def dived_by(
        self, other: Self
    ) -> tuple[Self, None] | tuple[None, Optional[RTError]]:
        return None, self.illegal_operation(other)

    def powed_by(
        self, other: Self
    ) -> tuple[Self, None] | tuple[None, Optional[RTError]]:
        return None, self.illegal_operation(other)

    def get_comparison_eq(
        self, other: Self
    ) -> tuple[Boolean, None] | tuple[None, Optional[RTError]]:
        return None, self.illegal_operation(other)

    def get_comparison_ne(
        self, other: Self
    ) -> tuple[Boolean, None] | tuple[None, Optional[RTError]]:
        return None, self.illegal_operation(other)

    def get_comparison_lt(
        self, other: Self
    ) -> tuple[Boolean, None] | tuple[None, Optional[RTError]]:
        return None, self.illegal_operation(other)

    def get_comparison_gt(
        self, other: Self
    ) -> tuple[Boolean, None] | tuple[None, Optional[RTError]]:
        return None, self.illegal_operation(other)

    def get_comparison_lte(
        self, other: Self
    ) -> tuple[Boolean, None] | tuple[None, Optional[RTError]]:
        return None, self.illegal_operation(other)

    def get_comparison_gte(
        self, other: Self
    ) -> tuple[Boolean, None] | tuple[None, Optional[RTError]]:
        return None, self.illegal_operation(other)

    def anded_by(
        self, other: Self
    ) -> tuple[Boolean, None] | tuple[None, Optional[RTError]]:
        return None, self.illegal_operation(other)

    def ored_by(
        self, other: Self
    ) -> tuple[Boolean, None] | tuple[None, Optional[RTError]]:
        return None, self.illegal_operation(other)

    def notted(self) -> tuple[Boolean, None] | tuple[None, Optional[RTError]]:
        return None, self.illegal_operation()

    def execute(self, args: list[Value], context: Context):
        return RTResult().failure(self.illegal_operation())

    def copy(self) -> Self:
        raise NotImplemented

    def is_true(self) -> bool:
        return False

    def illegal_operation(self, other: Self | None = None):
        if not other:
            other = self
        if self.pos_start and other.pos_end and self.context:
            return RTError(
                self.pos_start, other.pos_end, "Illegal operation", self.context
            )


class Boolean(Value):
    def __init__(self, value: Any):
        super().__init__()
        self.value = value

    def copy(self) -> Boolean:
        copy = Boolean(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def is_true(self):
        return self.value

    def anded_by(self, other: Value):
        if isinstance(other, Boolean):
            return Boolean(self.value and other.value).set_context(self.context), None
        elif (
            isinstance(other, Number)
            or isinstance(other, String)
            or isinstance(other, List)
        ):
            return (
                Boolean(self.value and other.is_true()).set_context(self.context),
                None,
            )
        else:
            return None, Value.illegal_operation(self, other)

    def added_to(self, other: Value):
        if isinstance(other, Boolean):
            return Boolean(self.value or other.value).set_context(self.context), None
        elif (
            isinstance(other, Number)
            or isinstance(other, String)
            or isinstance(other, List)
        ):
            return (
                Boolean(self.value or other.is_true()).set_context(self.context),
                None,
            )
        else:
            return None, Value.illegal_operation(self, other)

    def multed_by(self, other: Value):
        if isinstance(other, Boolean):
            return Boolean(self.value and other.value).set_context(self.context), None
        elif (
            isinstance(other, Number)
            or isinstance(other, String)
            or isinstance(other, List)
        ):
            return (
                Boolean(self.value and other.is_true()).set_context(self.context),
                None,
            )
        else:
            return None, Value.illegal_operation(self, other)

    def ored_by(self, other: Value):
        if isinstance(other, Boolean):
            return Boolean(self.value or other.value).set_context(self.context), None
        elif (
            isinstance(other, Number)
            or isinstance(other, String)
            or isinstance(other, List)
        ):
            return (
                Boolean(self.value or other.is_true()).set_context(self.context),
                None,
            )
        else:
            return None, Value.illegal_operation(self, other)

    def notted(self):
        return Boolean(not self.value).set_context(self.context), None

    def __str__(self):
        return "True" if self.value else "False"

    def __repr__(self):
        return "True" if self.value else "False"


class Number(Value):
    def __init__(self, value: int | float):
        super().__init__()
        self.value = value

    def added_to(self, other: Value): # type: ignore
        if isinstance(other, Number):
            return Number(self.value + other.value).set_context(self.context), None
        elif isinstance(other, String):
            return String(str(self.value) + other.value).set_context(self.context), None 
        else:
            return None, Value.illegal_operation(self, other)

    def subbed_by(self, other: Value):
        if isinstance(other, Number):
            return Number(self.value - other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def multed_by(self, other: Value):
        if isinstance(other, Number):
            return Number(self.value * other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def dived_by(self, other: Value):
        if isinstance(other, Number):
            if other.value == 0:
                return None, RTError(
                    other.pos_start, other.pos_end, "Division by zero", self.context
                )

            return Number(self.value / other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def powed_by(self, other: Value):
        if isinstance(other, Number):
            return Number(self.value**other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_eq(self, other: Value):
        if isinstance(other, Number):
            return (
                Boolean(int(self.value == other.value)).set_context(self.context),
                None,
            )
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_ne(self, other: Value):
        if isinstance(other, Number):
            return (
                Boolean(int(self.value != other.value)).set_context(self.context),
                None,
            )
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_lt(self, other: Value):
        if isinstance(other, Number):
            return (
                Boolean(int(self.value < other.value)).set_context(self.context),
                None,
            )
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_gt(self, other: Value):
        if isinstance(other, Number):
            return (
                Boolean(int(self.value > other.value)).set_context(self.context),
                None,
            )
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_lte(self, other: Value):
        if isinstance(other, Number):
            return (
                Boolean(int(self.value <= other.value)).set_context(self.context),
                None,
            )
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_gte(self, other: Value):
        if isinstance(other, Number):
            return (
                Boolean(int(self.value >= other.value)).set_context(self.context),
                None,
            )
        else:
            return None, Value.illegal_operation(self, other)

    def copy(self):
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


Null = Number(0)
class String(Value):
    def __init__(self, value: str):
        super().__init__()
        self.value = value

    def added_to(self, other: Value):
        if isinstance(other, String) or isinstance(other, Number):
            return String(self.value + str(other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def multed_by(self, other: Value):
        if isinstance(other, Number) and isinstance(other.value, int):
            return String(self.value * other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def is_true(self):
        return len(self.value) > 0

    def get_comparison_eq(self, other: Value):
        if isinstance(other, String):
            return (
                Boolean((self.value == other.value)).set_context(self.context),
                None,
            )
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_ne(self, other: Value):
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
    def __init__(self, elements: list[Value | None]):
        super().__init__()
        self.elements = elements

    def added_to(self, other: Value):
        if isinstance(other, List):
            return List(self.elements + other.elements).set_context(self.context), None
        else:
            newlist = self.copy()
            newlist.elements.append(other)
            return newlist, None

    def multed_by(self, other: Value):
        if isinstance(other, Number) and isinstance(other.value, int):
            return List(self.elements * other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def subbed_by(self, other: Value):
        if isinstance(other, Number) and isinstance(other.value, int):
            try:
                newlist = self.copy()
                newlist.elements.pop(other.value)
                return newlist, None
            except:
                return None, RTError(
                    other.pos_start, other.pos_end, "Index out of bounds", self.context
                )
        else:
            return None, Value.illegal_operation(self, other)

    def dived_by(self, other: Value):  # type: ignore
        if isinstance(other, Number) and isinstance(other.value, int):
            try:
                return self.elements[other.value], None
            except:
                return None, RTError(
                    other.pos_start, other.pos_end, "Index out of bounds", self.context
                )
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_eq(self, other: List):
        return Boolean(self.elements == other.elements).set_context(self.context), None

    def get_comparison_ne(self, other: List):
        return Boolean(self.elements != other.elements).set_context(self.context), None

    def get_comparison_gt(self, other: List):
        return (
            Boolean(len(self.elements) > len(other.elements)).set_context(self.context),
            None,
        )

    def get_comparison_lt(self, other: List):
        return (
            Boolean(len(self.elements) < len(other.elements)).set_context(self.context),
            None,
        )

    def get_comparison_gte(self, other: List):
        return (
            Boolean(len(self.elements) >= len(other.elements)).set_context(
                self.context
            ),
            None,
        )

    def get_comparison_lte(self, other: List):
        return (
            Boolean(len(self.elements) <= len(other.elements)).set_context(
                self.context
            ),
            None,
        )

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

class Dictionary(Value):
    def __init__(self, elements: dict[str|int, Value]):
        super().__init__()
        self.elements = elements
        
    def added_to(self, other: Value):
        if isinstance(other, Dictionary):
            return Dictionary({**self.elements, **other.elements}).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
        
    def subbed_by(self, other: Value):
        if isinstance(other, String):
            try:
                del self.elements[other.value]
                return self, None
            except:
                return None, RTError(other.pos_start, other.pos_end, "Key not found", self.context)
        else:
            return None, Value.illegal_operation(self, other)
        
    def dived_by(self, other: Value): # type: ignore
        if isinstance(other, String):
            try:
                return self.elements[other.value], None
            except:
                return None, RTError(other.pos_start, other.pos_end, "Key not found", self.context)
        else:
            return None, Value.illegal_operation(self, other)
        
    def get_comparison_eq(self, other: Dictionary):
        return Boolean(self.elements == other.elements).set_context(self.context), None
    
    def get_comparison_ne(self, other: Dictionary):
        return Boolean(self.elements != other.elements).set_context(self.context), None
    
    def is_true(self):
        return len(self.elements) > 0
    
    def copy(self):
        copy = Dictionary(self.elements.copy())
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy
    
    def __str__(self):
        return f"{{{', '.join(f'{k}: {v}' for k, v in self.elements.items())}}}"
    
    def __repr__(self):
        return f"{{{', '.join(f'{k}: {repr(v)}' for k, v in self.elements.items())}}}"
    
    
    
    


#######################################
# FUNCTIONS
#######################################
class BaseFunction(Value):
    def __init__(self, name: str):
        super().__init__()
        self.name = name

    def generate_new_context(self, context:Context) -> Context:
        new_context = Context(self.name, context, self.pos_start)
        new_context.symbol_table = SymbolTable(context.symbol_table) # type: ignore
        return new_context
    
    def check_args(self, arg_names: list[str], args: list[Value]):
        res = RTResult()
        
        if len(args) > len(arg_names):
            return res.failure(RTError(self.pos_start, self.pos_end, f"{len(args) - len(arg_names)} too many args passed into '{self.name}'", self.context))
        
        if len(args) < len(arg_names):
            return res.failure(RTError(self.pos_start, self.pos_end, f"{len(arg_names) - len(args)} too few args passed into '{self.name}'", self.context))
        
        return res.success(None)
    
    def populate_args(self, arg_names: list[str], args: list[Value], exec_ctx: Context):
        for i in range(len(args)):
            arg_name = arg_names[i]
            arg_value = args[i]
            arg_value.set_context(exec_ctx)
            exec_ctx.symbol_table.set(arg_name, arg_value) # type: ignore
            
    def check_and_populate_args(self, arg_names: list[str], args: list[Value], exec_ctx: Context):
        res = RTResult()
        res.register(self.check_args(arg_names, args))
        if res.error:
            return res
        self.populate_args(arg_names, args, exec_ctx)
        return res.success(None)
    
    def __str__(self):
        return f"<function {self.name}>"
    
    def __repr__(self):
        return f"<function {self.name}>"
    
class Function(BaseFunction):
    def __init__(self, name: str, body_node: Any, arg_names: list[str], auto_return: bool = False):
        super().__init__(name)
        self.body_node = body_node
        self.arg_names = arg_names
        self.auto_return = auto_return
        
    def execute(self, args: list[Value], context: Context):
        res = RTResult()
        interpreter = Interpreter(self.generate_new_context(context))
        res.register(self.check_and_populate_args(self.arg_names, args, interpreter.context))
        if res.error:
            return res
        value = res.register(interpreter.visit(self.body_node))
        if res.error:
            return res
        return_value = (value if self.auto_return else None) or res.func_return_value or Number(0)
        
        return res.success(return_value)
    
    def copy(self):
        copy = Function(self.name, self.body_node, self.arg_names, self.auto_return)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start, self.pos_end)
        return copy
    
class BuiltInFunction(BaseFunction):
    def __init__(self, name: str):
        super().__init__(name)
        
    def execute(self, args: list[Value], context: Context):
        res = RTResult()
        exec_ctx = self.generate_new_context(context)
        
        method_name = f"execute_{self.name}"
        method = getattr(self, method_name, self.no_visit_method)
        
        res.register(self.check_and_populate_args(method.arg_names, args, exec_ctx)) # type: ignore
        if res.should_return():
            return res
        
        return_value = res.register(method(exec_ctx)) # type: ignore
        if res.should_return():
            return res
        
        return res.success(return_value)
    
    def no_visit_method(self, node: Any, context: Context):
        raise Exception(f"No execute_{self.name} method defined")
    
    def copy(self):
        copy = BuiltInFunction(self.name)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start, self.pos_end)
        return copy
    
    def execute_print(self, exec_ctx: Context):
        print(str(exec_ctx.symbol_table.get("value")), end="") # type: ignore
        return RTResult().success(Null)
    
    execute_print.arg_names = ["value"] # type: ignore
    
    def execute_input(self, exec_ctx: Context):
        text = input()
        return RTResult().success(String(text))
    
    execute_input.arg_names = [] # type: ignore
    
    def execute_clear(self, exec_ctx: Context):
        os.system("cls" if os.name == "nt" else "clear")
        return RTResult().success(Null)
    
    execute_clear.arg_names = [] # type: ignore
    
    def execute_type(self, exec_ctx: Context):
        value = exec_ctx.symbol_table.get("value") # type: ignore
        return RTResult().success(String(type(value).__name__))

    execute_type.arg_names = ["value"] # type: ignore
    
    def execute_len(self, exec_ctx: Context):
        value = exec_ctx.symbol_table.get("value") # type: ignore
        if isinstance(value, String):
            return RTResult().success(Number(len(value.value)))
        elif isinstance(value, List):
            return RTResult().success(Number(len(value.elements)))
        else:
            return RTResult().failure(RTError(self.pos_start, self.pos_end, "Argument must be string or list", exec_ctx))
        
    execute_len.arg_names = ["value"] # type: ignore
    
    def execute_eval(self, exec_ctx: Context):
        value = exec_ctx.symbol_table.get("value") # type: ignore
        if not isinstance(value, String):
            return RTResult().failure(RTError(self.pos_start, self.pos_end, "Argument must be string", exec_ctx))
        try:
            return RTResult().success(eval(value)) # type: ignore
        except Exception as e:
            return RTResult().failure(RTError(self.pos_start, self.pos_end, f"Invalid expression: {e}", exec_ctx))

    execute_eval.arg_names = ["value"] # type: ignore
    
    def execute_convert(self, exec_ctx: Context):
        value = exec_ctx.symbol_table.get("value") # type: ignore
        to = exec_ctx.symbol_table.get("to") # type: ignore
        if not isinstance(to, String):
            return RTResult().failure(RTError(self.pos_start, self.pos_end, "Conversion type must be string", exec_ctx))
        if to.value == "string":
            return RTResult().success(String(str(value)))
        elif to.value == "number": 
            try:
                return RTResult().success(Number(int(value.value))) # type: ignore
            except Exception as e:
                print(e)
                return RTResult().failure(RTError(self.pos_start, self.pos_end, "Invalid conversion", exec_ctx))
        elif to == "boolean": # type: ignore
            return RTResult().success(Boolean(value.is_true())) # type: ignore
        else:
            return RTResult().failure(RTError(self.pos_start, self.pos_end, "Invalid conversion", exec_ctx))
        
    execute_convert.arg_names = ["value", "to"] # type: ignore
    
    def execute_random(self, exec_ctx: Context):
        value = exec_ctx.symbol_table.get("value") # type: ignore
        count = exec_ctx.symbol_table.get("count") # type: ignore
        if isinstance(value, List):
            return RTResult().success(random.choices(value.elements, k=count.value)) # type: ignore
        else:
            return RTResult().failure(RTError(self.pos_start, self.pos_end, "Argument must be list", exec_ctx))
        
    
    execute_random.arg_names = ["value", "count"] # type: ignore
    
    def execute_exit(self, exec_ctx: Context):
        sys.exit()

            

#######################################
# CONTEXT
#######################################


class Context:
    def __init__(
        self,
        display_name: str,
        parent: Self | None = None,
        parent_entry_pos: Position | None = None,
    ):
        self.display_name = display_name
        self.parent = parent
        self.parent_entry_pos = parent_entry_pos
        self.symbol_table: SymbolTable | None = None


#######################################
# SYMBOL TABLE
#######################################


class SymbolTable:
    def __init__(self, parent: Self | None = None):
        self.symbols: dict[str, Value] = {}
        self.parent = parent

    def get(self, name: str) -> Value | None:
        value: Value | None = self.symbols.get(name, None)
        if value == None and self.parent:
            return self.parent.get(name)
        return value

    def set(self, name: str, value: Value):
        self.symbols[name] = value

    def remove(self, name: str):
        del self.symbols[name]

    def copy(self):
        copy = SymbolTable(self.parent)
        copy.symbols = self.symbols.copy()
        return copy

global_symbol_table = SymbolTable()

global_symbol_table.set("Null", Number(0))
global_symbol_table.set("True", Boolean(True))
global_symbol_table.set("False", Boolean(False))
global_symbol_table.set("print", BuiltInFunction("print"))
global_symbol_table.set("input", BuiltInFunction("input"))
global_symbol_table.set("type", BuiltInFunction("type"))
global_symbol_table.set("clear", BuiltInFunction("clear"))
global_symbol_table.set("len", BuiltInFunction("len"))
global_symbol_table.set("exit", BuiltInFunction("exit"))
global_symbol_table.set("eval", BuiltInFunction("eval"))
global_symbol_table.set("convert", BuiltInFunction("convert"))
global_symbol_table.set("random", BuiltInFunction("random"))

#######################################
# INTERPRETER
#######################################


class Interpreter:
    def __init__(self, context: Context) -> None:
        self.context = context
        self.methods: dict[str, function] = {
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
            "FunctionDefNode": self.visit_FuncDefNode,
            "FunctionCallNode": self.visit_FuncCallNode,
            "ReturnNode": self.visit_ReturnNode,
            "ImportNode": self.visit_ImportNode,
            "FromImportNode": self.visit_FromImportNode,
            "DictNode": self.visit_DictNode,
        }

    def visit(self, node: Any, context: Optional[Context] = None):
        context = context or self.context
        method_name = f"visit_{type(node).__name__}"
        method = getattr(self, method_name, self.no_visit_method)
        return method(node, context)

    def no_visit_method(self, node: Any, context: Context):
        raise Exception(f"No visit_{type(node).__name__} method defined")

    ###################################

    def visit_NumberNode(self, node: NumberNode, context: Context):
        return RTResult().success(
            Number(node.tok.value)  # type: ignore
            .set_context(context)
            .set_pos(node.pos_start, node.pos_end)
        )

    def visit_BinOpNode(self, node: BinOpNode, context: Context):
        res = RTResult()
        left: Value = res.register(self.visit(node.left_node, context))  # type: ignore
        if res.should_return():
            return res
        right: Value = res.register(self.visit(node.right_node, context))  # type: ignore
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

    def visit_UnaryOpNode(self, node: UnaryOpNode, context: Context):
        res = RTResult()
        number: Number | Boolean = res.register(self.visit(node.node, context))  # type: ignore
        if res.should_return():
            return res

        error = None

        if node.op_tok.type == TT_MINUS:
            number, error = number.multed_by(Number(-1))  # type: ignore
        elif node.op_tok.type == TT_NOT:
            number, error = number.notted()  # type: ignore

        if error:
            return res.failure(error)
        else:
            return res.success(number.set_pos(node.pos_start, node.pos_end))

    def visit_VarAccessNode(self, node: VarAccessNode, context: Context):
        res = RTResult()
        var_name = node.var_name_tok.value
        value = context.symbol_table.get(var_name)  # type: ignore
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

    def visit_VarAssignNode(self, node: VarAssignNode, context: Context):
        res = RTResult()
        var_name = node.var_name_tok.value
        value = res.register(self.visit(node.value_node, context))
        if res.should_return():
            return res
        context.symbol_table.set(var_name, value)  # type: ignore
        return res.success(value)  # type: ignore

    def visit_StringNode(self, node: StringNode, context: Context):
        return RTResult().success(
            String(node.tok.value)  # type: ignore
            .set_context(context)
            .set_pos(node.pos_start, node.pos_end)
        )

    def visit_IfNode(self, node: IfNode, context: Context):
        res = RTResult()
        for condition, expr in node.cases:
            condition_value = res.register(self.visit(condition, context))
            if res.should_return():
                return res
            if condition_value.is_true():  # type: ignore
                expr_value = res.register(self.visit(expr, context))
                if res.should_return():
                    return res
                return res.success(expr_value)  # type: ignore

        if node.else_case:
            else_value = res.register(self.visit(node.else_case, context))
            if res.should_return():
                return res
            return res.success(else_value)  # type: ignore
        return res.success(None)  # type: ignore

    def visit_ListNode(self, node: ListNode, context: Context):
        res = RTResult()
        elements: list[Value | None] = []
        for element_node in node.element_nodes:
            elements.append(res.register(self.visit(element_node, context)))
            if res.should_return():
                return res
        return res.success(
            List(elements).set_context(context).set_pos(node.pos_start, node.pos_end)
        )

    def visit_ForNode(self, node: ForNode, context: Context):
        res = RTResult()
        start_value: Number = res.register(self.visit(node.start_value_node, context))  # type: ignore
        if res.should_return():
            return res
        end_value = res.register(self.visit(node.end_value_node, context))
        if res.should_return():
            return res
        step_value = res.register(self.visit(node.step_value_node, context))
        if res.should_return():
            return res
        i = start_value.value
        if step_value == 0:  # type: ignore
            return res.failure(
                RTError(
                    node.pos_start, node.pos_end, "Step value cannot be zero", context
                )
            )
        elif step_value.value > 0:  # type: ignore
            condition = lambda: i <= end_value.value  # type: ignore
        else:
            condition = lambda: i >= end_value.value  # type: ignore
        while condition():
            context.symbol_table.set(node.var_name_tok.value, Number(i))  # type: ignore
            i += step_value.value  # type: ignore
            res.register(self.visit(node.body_node, context))
            if res.should_return():
                if res.loop_should_continue:
                    continue
                if res.loop_should_break:
                    break
                return res
        return res.success(None)

    def visit_WhileNode(self, node: WhileNode, context: Context):
        res = RTResult()
        while True:
            condition = res.register(self.visit(node.condition_node, context))
            if res.should_return():
                return res
            if not condition.is_true():  # type: ignore
                break
            res.register(self.visit(node.body_node, context))
            if res.should_return():
                if res.loop_should_continue:
                    continue
                if res.loop_should_break:
                    break
                return res
        return res.success(None)

    def visit_BreakNode(self, node: BreakNode, context: Context):
        return RTResult().success_break()

    def visit_ContinueNode(self, node: ContinueNode, context: Context):
        return RTResult().success_continue()

    def visit_FuncDefNode(self, node: FuncDefNode, context: Context):
        res = RTResult()
        func_name:str = node.var_name_tok.value  # type: ignore
        body_node = node.body_node
        arg_names:list[str] = [arg_name.value for arg_name in node.arg_name_toks] # type: ignore
        func_value = Function(func_name, body_node, arg_names).set_context(context).set_pos(node.pos_start, node.pos_end)
        context.symbol_table.set(func_name, func_value) # type: ignore
        return res.success(func_value)
    
    def visit_FuncCallNode(self, node: FuncCallNode, context: Context):
        res = RTResult()
        args:list[Any] = []
        
        value_to_call = res.register(self.visit(node.node_to_call, context))
        if not value_to_call:
            return res.failure(RTError(node.pos_start, node.pos_end, "Function not defined", context))
        for arg_node in node.arg_nodes:
            args.append(res.register(self.visit(arg_node, context)))
            if res.should_return():
                return res
    
        return_value = res.register(value_to_call.execute(args, context))
        if res.should_return():
            return res
        return_value = return_value.copy().set_pos(node.pos_start, node.pos_end).set_context(context)  # type: ignore function always returns a value or Null
        
        return res.success(return_value)
    
    def visit_ReturnNode(self, node: ReturnNode, context: Context):
        res = RTResult()
        if node.node_to_return:
            value = res.register(self.visit(node.node_to_return, context))
            if res.should_return():
                return res
        else:
            value = Number(0)
        return res.success_return(value) # type: ignore
         
    def visit_ImportNode(self, node: ImportNode, context: Context):
        res = RTResult()
        module = node.module_name.value
        
        if not isinstance(module, str):
            return
        file = module.replace('.', '/') 
        file += ".fx"  
        try:
            with open(file, "r") as f: 
                script = f.read()
        except:
            return res.failure(RTError(node.pos_start, node.pos_end, f"Module '{module}' not found", context))  # type: ignore
        lexer = Lexer(file, script)
        tokens, error = lexer.make_tokens()
        
        if error:
            return res.failure(error) 
        if not tokens:
            return res.failure(RTError(node.pos_start, node.pos_end, f"Module '{module}' is empty", context)) # type: ignore
        parser = Parser(tokens) 
        ast = parser.parse()
        
        if ast.error:
            return res.failure(ast.error) 
        execcontext = Context(file)
        execcontext.symbol_table = global_symbol_table.copy()

        interpreter = Interpreter(execcontext)
        value = interpreter.visit(ast.node) 
        
        if value.error:
            return res.failure(value.error)

        alias = node.alias.value or module
        
        
        symbols:dict[str, str] = {
            f"{alias}.{key}": value for key, value in interpreter.context.symbol_table.symbols.items() # type: ignore
        }
        
        context.symbol_table.symbols.update(symbols) # type: ignore
        
        return res.success(value.value)
    
    def visit_FromImportNode(self, node: FromImportNode, context: Context):
        res = RTResult()
        module = node.module_name.value
        if not isinstance(module, str):
            return
        file:str = module.replace('.', '/')
        file += ".fx"
        try:
            with open(file, "r") as f:
                script = f.read()
        except:
            return res.failure(RTError(node.pos_start, node.pos_end, f"Module '{module}' not found", context))
            
        lexer = Lexer(file, script) 
        tokens, error = lexer.make_tokens()
        
        if error:
            return res.failure(error) 
        if not tokens:
            return res.failure(RTError(node.pos_start, node.pos_end, f"Module '{module}' is empty", context))
        parser = Parser(tokens) 
        ast = parser.parse()
        
        if ast.error:
            return res.failure(ast.error) 
        
        context = Context(file, context) 
        context.symbol_table = global_symbol_table
        
        interpreter = Interpreter(context)
        value = interpreter.visit(ast.node)
        
        if value.error:
            return res.failure(value.error) 
        
        modulesymbols = interpreter.context.symbol_table.symbols # type: ignore
        
        functions = node.functions
        
        symbols = {}
        
        for function in functions:
            if function[0].value in modulesymbols:
                alias = function[1].value if function[1] else None
                if not alias:
                    alias = function[0].value
                
                symbols[f"{alias}"] = modulesymbols[function[0].value]
                
        self.context.symbol_table.symbols.update(symbols) # type: ignore
        
        return res.success(value.value)
            
    def visit_DictNode(self, node: DictNode, context: Context):
        res = RTResult()
        elements:dict[str|int, Value] = {}
        for key, value in node.key_value_pairs.items():
            key:Value|None = res.register(self.visit(key, context))
            if res.should_return():
                return res
            if not isinstance(key, String):
                return res.failure(RTError(node.pos_start, node.pos_end, "Dictionary keys must be strings", context))
            
            elements[key.value] = res.register(self.visit(value, context)) # type: ignore

            if res.should_return():
                return res
        return res.success(
            Dictionary(elements).set_context(context).set_pos(node.pos_start, node.pos_end)
        )

        
        
            
    