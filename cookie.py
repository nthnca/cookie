import sys

from tokenizer import Tokenizer


def ERROR(msg):
    print(msg)
    exit(1)


IDENT_RE = "[a-z_][a-z0-9_]*"
INT_RE = "[-]?[1-9][0-9]*|0"
SET_RE = "="
EOL_RE = ";"
CURLY_OPEN_RE = "{"
CURLY_CLOSE_RE = "}"
FUNCTION_RE = "[(][)]"

VARIABLES = {}

func_count = 0


def retvrn(t):
    return t


class ParseMethod:

    def __init__(self, embedded):
        self.stmts = ()

        while True:
            self.var, self.op, self.op_type = (None, None, None)
            if src.eof():
                if embedded:
                    ERROR("Unexpected end of file.")
                break

            t = src.next_token(
                ((IDENT_RE, self.ident), (CURLY_CLOSE_RE, retvrn)), "Variable")
            if t == "}":
                if not embedded:
                    ERROR("Unexpected '}'")
                break

            self.stmts = self.stmts + ((self.var, self.op, self.op_type),)

    def ident(self, t):
        self.var = t
        src.next_token(
            ((SET_RE, self.set), (FUNCTION_RE, self.function_no_set), ), "=")

    def set(self, t):
        op = src.next_token(
            ((INT_RE, self.getint),
             (IDENT_RE, self.literal),
             (CURLY_OPEN_RE, self.method)),
                            "Operation")

    def method(self, t):
        global func_count
        var_name = "static_method_name_%d" % (func_count,)
        func_count += 1
        VARIABLES[var_name] = ParseMethod(True).stmts
        self.op = var_name

    def getint(self, t):
        self.op = int(t)
        self.op_type = "INT"
        src.next_token(((EOL_RE, retvrn),), ";")

    def literal(self, t):
        self.op = t
        src.next_token(
            ((EOL_RE, retvrn), (FUNCTION_RE, self.function), ), ";")

    def function_no_set(self, t):
        self.op = self.var
        self.op_type = "EXE"
        self.var = "_"
        src.next_token(((EOL_RE, retvrn),), ";")

    def function(self, t):
        self.op_type = "EXE"
        src.next_token(((EOL_RE, retvrn),), ";")


def get_value(v1):
    if v1 not in VARIABLES:
        print("Unknown value:", v1)
        sys.exit(1)

    return VARIABLES[v1]


def get_func(name):
    if name not in VARIABLES:
        print("Unknown function:", name)
        sys.exit(1)

    return VARIABLES[name]


def exe_func(func):
    if callable(func):
        return func()

    for stmt in func:
        if stmt[2] == "INT":
            VARIABLES[stmt[0]] = stmt[1]
        elif stmt[2] == "EXE":
            VARIABLES[stmt[0]] = exe_func(get_func(stmt[1]))
        else:
            VARIABLES[stmt[0]] = get_value(stmt[1])

    if "_r" in VARIABLES:
        return VARIABLES["_r"]


# Built in functions, these probably belong in their own file.

def printx():
    print(get_value("_1"))
VARIABLES["print"] = printx


def addx():
    x = get_value("_1") + get_value("_2")
    VARIABLES["_r"] = x
    return x
VARIABLES["add"] = addx


def ifx():
    if get_value("_1"):
        exe_func(get_func("_2"))
VARIABLES["if"] = ifx


def loop():
    func = get_func("_1")
    while True:
        exe_func(func)
        if get_value("_r"):
            break
VARIABLES["loop"] = loop


src = Tokenizer()
VARIABLES["static_method_name_main"] = ParseMethod(False).stmts
# print(VARIABLES)
# print("################################################")

exe_func(get_func("static_method_name_main"))
