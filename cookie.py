import sys
import re

from tokenizer import Tokenizer


def ERROR(msg):
    print(msg)
    exit(1)


IDENT_RE = re.compile("[a-z_][a-z0-9_]*")
INT_RE = re.compile("[-]?[1-9][0-9]*|0")
SET_RE = re.compile("=")
EOL_RE = re.compile(";")
CURLY_OPEN_RE = re.compile("{")
CURLY_CLOSE_RE = re.compile("}")
FUNCTION_RE = re.compile("[(][)]")

VARIABLES = {}


def retvrn(t):
    return t


class ParseMethod:

    def __init__(self, tokenizer, embedded):
        self.tokenizer = tokenizer
        self.stmts = ()

        while True:
            self.var, self.op, self.op_type = (None, None, None)
            if self.tokenizer.eof():
                if embedded:
                    ERROR("Unexpected end of file.")
                break

            t = self.tokenizer.next_token(
                ((IDENT_RE, self.ident), (CURLY_CLOSE_RE, retvrn)), "Variable")
            if t == "}":
                if not embedded:
                    ERROR("Unexpected '}'")
                break

            self.stmts = self.stmts + ((self.var, self.op, self.op_type),)

    def ident(self, t):
        self.var = t
        self.tokenizer.next_token(
            ((SET_RE, self.set), (FUNCTION_RE, self.function_no_set), ), "=")

    def set(self, t):
        op = self.tokenizer.next_token(
            ((INT_RE, self.getint),
             (IDENT_RE, self.literal),
             (CURLY_OPEN_RE, self.method)),
                            "Operation")

    def method(self, t):
        self.op_type = "RAW"
        self.op = ParseMethod(self.tokenizer, True).stmts

    def getint(self, t):
        self.op = int(t)
        self.op_type = "RAW"
        self.tokenizer.next_token(((EOL_RE, retvrn),), ";")

    def literal(self, t):
        self.op = t
        self.tokenizer.next_token(
            ((EOL_RE, retvrn), (FUNCTION_RE, self.function), ), ";")

    def function_no_set(self, t):
        self.op = self.var
        self.op_type = "EXE"
        self.var = "_"
        self.tokenizer.next_token(((EOL_RE, retvrn),), ";")

    def function(self, t):
        self.op_type = "EXE"
        self.tokenizer.next_token(((EOL_RE, retvrn),), ";")


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
        if stmt[2] == "RAW":
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


def loopx():
    func = get_func("_1")
    continu = True
    while continu:
        exe_func(func)
        continu = get_value("_r")
VARIABLES["loop"] = loopx


exe_func(ParseMethod(Tokenizer(), False).stmts)
