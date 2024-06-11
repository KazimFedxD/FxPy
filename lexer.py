from errors import *
import string

global_variables = [
    "Null",
    "True",
    "False",
]

TT_INT = "INT"
TT_FLOAT = "FLOAT"
TT_STRING = "STRING"

TT_PLUS = "PLUS"
TT_MINUS = "MINUS"
TT_MUL = "MUL"
TT_DIV = "DIV"
TT_MOD = "MOD"
TT_POW = "POW"
TT_LPAREN = "LPAREN"
TT_RPAREN = "RPAREN"
TT_EOF = "EOF"
TT_IDENTIFIER = "IDENTIFIER"
TT_KEYWORD = "KEYWORD"
TT_EQ = "EQ"
TT_EE = "EE"
TT_NE = "NE"
TT_LT = "LT"
TT_GT = "GT"
TT_LTE = "LTE"
TT_GTE = "GTE"
TT_COMMA = "COMMA"
TT_ARROW = "ARROW"
TT_NEWLINE = "NEWLINE"
TT_COMMENT = "COMMENT"
TT_NOT = "NOT"
TT_TAB = "TAB"
TT_COLON = "COLON"
TT_LSQB = "LSQB"
TT_RSQB = "RSQB"
TT_LBRACE = "LBRACE"
TT_RBRACE = "RBRACE"


RESERVED_KEYWORDS = [
    "and",
    "or",
    "let",
    "if",
    "else",
    "elif",
    "end",
    "for",
    "while",
    "in",
    "to",
    "step",
    "break",
    "continue",
    "return",
    "fex",
    "import",
    "from",
    "as",
]


class Token:
    def __init__(
        self,
        type_: str,
        value: Optional[str | int | float] = None,
        pos_start: Optional[Position] = None,
        pos_end: Optional[Position] = None,
    ):
        self.type = type_
        self.value = value

        if pos_start:
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.advance()

        if pos_end:
            self.pos_end = pos_end.copy()

    def matches(self, type_: str, value: str) -> bool:
        return self.type == type_ and self.value == value

    def __repr__(self):
        return self.type + (f":{self.value}" if self.value != None else "")


class Lexer:
    def __init__(self, file_name: str, text: str):
        self.file_name = file_name
        self.text = text
        self.pos = Position(-1, 0, -1, file_name, text)
        self.current_char = None
        self.advance()

    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = (
            self.text[self.pos.idx] if self.pos.idx < len(self.text) else None
        )

    def make_tokens(self) -> tuple[Optional[list[Token]], Optional[Error]]:
        tokens: list[Token] = []
        while self.current_char != None:
            if self.current_char in " \t":
                self.advance()
            elif self.current_char in "\n;":
                tokens.append(Token(TT_NEWLINE, pos_start=self.pos))
                self.advance()
            elif self.current_char in "0123456789":
                tokens.append(self.make_number())
            elif self.current_char in string.ascii_letters + "_":
                tokens.append(self.make_identifier())
            elif self.current_char in "'\"":
                tokens.append(self.make_string())
            elif self.current_char == "=":
                tokens.append(self.make_equals())
            elif self.current_char == "!":
                tokens.append(self.make_not_equals())
            elif self.current_char == "<":
                tokens.append(self.make_less_than())
            elif self.current_char == ">":
                tokens.append(self.make_greater_than())
            elif self.current_char == ",":
                tokens.append(Token(TT_COMMA, pos_start=self.pos))
                self.advance()
            elif self.current_char == "#":
                self.skip_comment()
            elif self.current_char == "+":
                tokens.append(Token(TT_PLUS, pos_start=self.pos))
                self.advance()
            elif self.current_char == "-":
                tokens.append(self.make_sub_or_arrow())
            elif self.current_char == "*":
                tokens.append(Token(TT_MUL, pos_start=self.pos))
                self.advance()
            elif self.current_char == "/":
                tokens.append(Token(TT_DIV, pos_start=self.pos))
                self.advance()
            elif self.current_char == "%":
                tokens.append(Token(TT_MOD, pos_start=self.pos))
                self.advance()
            elif self.current_char == "(":
                tokens.append(Token(TT_LPAREN, pos_start=self.pos))
                self.advance()
            elif self.current_char == ")":
                tokens.append(Token(TT_RPAREN, pos_start=self.pos))
                self.advance()
            elif self.current_char == "^":
                tokens.append(Token(TT_POW, pos_start=self.pos))
                self.advance()
            elif self.current_char == ":":
                tokens.append(Token(TT_COLON, pos_start=self.pos))
                self.advance()
            elif self.current_char == "[":
                tokens.append(Token(TT_LSQB, pos_start=self.pos))
                self.advance()
            elif self.current_char == "]":
                tokens.append(Token(TT_RSQB, pos_start=self.pos))
                self.advance()
            elif self.current_char == "{":
                tokens.append(Token(TT_LBRACE, pos_start=self.pos))
                self.advance()
            elif self.current_char == "}":
                tokens.append(Token(TT_RBRACE, pos_start=self.pos))
                self.advance()
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, "'" + char + "'")
        tokens.append(Token(TT_EOF, pos_start=self.pos))
        return tokens, None

    def make_number(self):
        num_str: str = ""
        dot_count = 0
        pos_start = self.pos.copy()

        while self.current_char != None and self.current_char in "0123456789.":
            if self.current_char == ".":
                if dot_count == 1:
                    break
                dot_count += 1
                num_str += "."
            else:
                num_str += self.current_char
            self.advance()

        if dot_count == 0:
            return Token(TT_INT, int(num_str), pos_start, self.pos)
        else:
            return Token(TT_FLOAT, float(num_str), pos_start, self.pos)

    def make_identifier(self):
        id_str = ""
        pos_start = self.pos.copy()

        while (
            self.current_char != None
            and self.current_char in string.ascii_letters + "_" + "0123456789" + "."
        ):
            id_str += self.current_char
            self.advance()

        if id_str in RESERVED_KEYWORDS:
            token = Token(TT_KEYWORD, id_str, pos_start, self.pos)
        else:
            token = Token(TT_IDENTIFIER, id_str, pos_start, self.pos)

        return token

    def make_equals(self):
        token_type = TT_EQ
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == "=":
            self.advance()
            token_type = TT_EE

        return Token(token_type, pos_start=pos_start, pos_end=self.pos)

    def make_not_equals(self):
        token_type = TT_NOT
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == "=":
            self.advance()
            token_type = TT_NE

        return Token(token_type, pos_start=pos_start, pos_end=self.pos)

    def make_less_than(self):
        token_type = TT_LT
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == "=":
            self.advance()
            token_type = TT_LTE

        return Token(token_type, pos_start=pos_start, pos_end=self.pos)

    def make_greater_than(self):
        token_type = TT_GT
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == "=":
            self.advance()
            token_type = TT_GTE

        return Token(token_type, pos_start=pos_start, pos_end=self.pos)

    def skip_comment(self):
        self.advance()

        while self.current_char != "\n":
            self.advance()

        self.advance()

    def make_string(self):
        string = ""
        pos_start = self.pos.copy()
        quote_type = self.current_char
        self.advance()

        escape_character = {
            "n": "\n",
            "t": "\t",
            "r": "\r",
            "\\": "\\",
            "'": "'",
            '"': '"',
        }
        escape = False
        while self.current_char != None and self.current_char != quote_type:
            if self.current_char == "\\":
                escape = True
            elif escape:
                string += escape_character.get(self.current_char, self.current_char)
            else:
                string += self.current_char
            self.advance()

        self.advance()
        return Token(TT_STRING, string, pos_start, self.pos)

    def make_sub_or_arrow(self):
        token = TT_MINUS
        pos_start = self.pos.copy()
        self.advance()
        if self.current_char == ">":
            self.advance()
            token = TT_ARROW
        return Token(token, pos_start=pos_start, pos_end=self.pos)
