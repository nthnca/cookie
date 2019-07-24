import sys
import re

VARIABLES = {}

class file_iter():
    def __init__(self):
        self.line = None
        self.line_no = 0
        self.pos = 0

    def _next_line(self):
        if self.line:
            return True

        for line in sys.stdin:
            line = line.rstrip()
            self.line_no += 1
            self.pos = 1
            if line:
                self.line = line
                return True

    def next_token(self, regexs, error):
        if not self._next_line():
            sys.exit(1)

        # Skip whitespace.
        m = re.match("\s+", self.line)
        if m:
            self.line = self.line[len(m.group(0)):]
            self.pos += len(m.group(0))

        for r in regexs:
            m = re.match(r, self.line)
            if m:
                self.line = self.line[len(m.group(0)):]
                self.pos += len(m.group(0))
                return m.group(0)

        print("Line %d:%d, Expected: %s, found: %s" %
            (self.line_no, self.pos, error, self.line))
        sys.exit(1)

    def eof(self):
        return self._next_line() == None

func_count=0
def go(embedded):
    global func_count
    stmts = ()
    while True:
        var_exp = "[a-z_][a-z0-9_]*"
        var = src.next_token(("[a-z_][a-z0-9_]*", "}"), "Variable")
        if var == "}":
            if not embedded:
                print("Unexpected '}'")
                sys.exit(1)
            return stmts

        src.next_token(("=",), "=")

        op = src.next_token(("[-]?[1-9][0-9]*", var_exp + "([(][)])?", "{"),
                            "Operation")

        if op == "{":
            var_name = "static_method_name_%d" % (func_count,)
            func_count += 1
            VARIABLES[var_name] = go(True)
            stmts = stmts + ((var, var_name + "()"),)
        else:
            stmts = stmts + ((var, op),)
            src.next_token((";",), ";")

        if src.eof():
            if embedded:
                print("Exiting prematurely")
                exit(1)
            else:
                return stmts

def is_digit(l):
    return l[-1].isdigit()

def is_func(l):
    return l[-2:] == "()"

def get_int(v1):
    return int(v1)

def get_value(v1):
    if v1 not in VARIABLES:
        print("Unknown value:", v1)
        sys.exit(1)

    return VARIABLES[v1]

def exe(code):
    name = code[:-2]
    if name not in VARIABLES:
        print("Unknown method:", name)
        sys.exit(1)

    func = VARIABLES[name]
    if callable(func):
        func()
        return

    for stmt in func:
        if is_func(stmt[1]):
            exe(stmt[1])
        elif is_digit(stmt[1]):
            VARIABLES[stmt[0]] = get_int(stmt[1])
        else:
            VARIABLES[stmt[0]] = get_value(stmt[1])
        # print(VARIABLES)

def printx():
    print(get_value("_1"))
VARIABLES["print"] = printx

def addx():
    VARIABLES["_r"] = get_value("_1") + get_value("_2")
VARIABLES["add"] = addx

def ifx():
    if get_value("_1"):
        exe("_2()")
VARIABLES["if"] = ifx


src = file_iter()
VARIABLES["static_method_name_main"] = go(False)
# print(VARIABLES)
# print("################################################")

exe("static_method_name_main()")
