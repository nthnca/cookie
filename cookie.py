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


class Method:

    def __init__(self, embedded):
        self.stmts = ()
        self.var = None

        while True:
            if src.eof():
                if embedded:
                    ERROR("Unexpected end of file.")
                break

            var = src.next_token(
                ((IDENT_RE, self.ident), (CURLY_CLOSE_RE, retvrn)), "Variable")
            if var == "}":
                if not embedded:
                    ERROR("Unexpected '}'")
                break

            self.stmts = self.stmts + ((self.var, self.op),)

    def ident(self, t):
        self.var = t
        src.next_token(
            ((SET_RE, self.set), (FUNCTION_RE, self.function), ), "=")

    def set(self, t):
        op = src.next_token(
            ((INT_RE, self.literal),
             (IDENT_RE + "([(][)])?", self.literal),
             (CURLY_OPEN_RE, self.method)),
                            "Operation")

    def method(self, t):
        global func_count
        var_name = "static_method_name_%d" % (func_count,)
        func_count += 1
        VARIABLES[var_name] = Method(True).stmts
        self.op = var_name

    def literal(self, t):
        self.op = t
        src.next_token(((EOL_RE, retvrn),), ";")

    def function(self, t):
        self.op = self.var + "()"
        self.var = "_"
        src.next_token(((EOL_RE, retvrn),), ";")


def is_digit(l):
    return l[0].isdigit() or l[0] == "-"


def is_func(l):
    return l[-2:] == "()"


def get_int(v1):
    return int(v1)


def get_value(v1):
    if v1 not in VARIABLES:
        print("Unknown value:", v1)
        sys.exit(1)

    return VARIABLES[v1]


def get_func(code):
    name = code[:-2]
    if name not in VARIABLES:
        print("Unknown method:", name)
        sys.exit(1)

    return VARIABLES[name]


def exe_func(func):
    if callable(func):
        func()
        return

    for stmt in func:
        if is_func(stmt[1]):
            exe_func(get_func(stmt[1]))
        elif is_digit(stmt[1]):
            VARIABLES[stmt[0]] = get_int(stmt[1])
        else:
            VARIABLES[stmt[0]] = get_value(stmt[1])

# Built in functions, these probably belong in their own file.


def printx():
    print(get_value("_1"))
VARIABLES["print"] = printx


def addx():
    VARIABLES["_r"] = get_value("_1") + get_value("_2")
VARIABLES["add"] = addx


def ifx():
    if get_value("_1"):
        exe_func(get_func("_2()"))
VARIABLES["if"] = ifx


def loop():
    func = get_func("_1()")
    while True:
        exe_func(func)
        if get_value("_r"):
            break
VARIABLES["loop"] = loop


src = Tokenizer()
VARIABLES["static_method_name_main"] = Method(False).stmts
# print(VARIABLES)
# print("################################################")

exe_func(get_func("static_method_name_main()"))
