from typing import TYPE_CHECKING, Optional
from string_with_arrows import string_with_arrows, Position

if TYPE_CHECKING:
    from interpreter import Context


#######################################
# ERROR
#######################################

class Error:
    def __init__(self, pos_start: Optional[Position], pos_end: Optional[Position], error_name: str, details:str):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def as_string(self) -> str:
        if not self.pos_start or not self.pos_end:
            return f"{self.error_name}: {self.details}"
        result:str = f"\n{self.error_name}: {self.details}\n"
        result += f"File {self.pos_start.fn}, line {self.pos_start.ln + 1}"
        result += "\n\n" + string_with_arrows(
            self.pos_start.ftxt, self.pos_start, self.pos_end
        )
        return result


class IllegalCharError(Error):
    def __init__(self, pos_start: Position, pos_end: Position, details:str):
        super().__init__(pos_start, pos_end, "Illegal Character", details)


class ExpectedCharError(Error):
    def __init__(self, pos_start: Position, pos_end: Position, details:str):
        super().__init__(pos_start, pos_end, "Expected Character", details)


class InvalidSyntaxError(Error):
    def __init__(self, pos_start: Position, pos_end: Position, details:str=""):
        super().__init__(pos_start, pos_end, "Invalid Syntax", details)


class RTError(Error):
    def __init__(self, pos_start: Optional[Position], pos_end: Optional[Position], details:str, context: Optional[Context]):
        super().__init__(pos_start, pos_end, "Runtime Error", details)
        self.context = context

    def as_string(self):
        if not self.pos_start or not self.pos_end:
            return f"{self.error_name}: {self.details}"
        result = "\n"
        result += self.generate_traceback()
        result += f"{self.error_name}: {self.details}"
        result += "\n\n" + string_with_arrows(
            self.pos_start.ftxt, self.pos_start, self.pos_end
        )
        return result

    def generate_traceback(self) -> str:
        if not self.pos_start:
            return ""
        result:str = ""
        pos:Optional[Position] = self.pos_start.copy()
        ctx:Optional[Context] = self.context

        while ctx and pos:
            result = (
                f"  File {pos.fn}, line {str(pos.ln + 1)}, in {ctx.display_name}\n"
                + result
            )
            pos:Optional[Position] = ctx.parent_entry_pos
            ctx:Optional[Context] = ctx.parent

        return "Traceback (most recent call last):\n" + result


