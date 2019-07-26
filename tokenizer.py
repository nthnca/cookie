import sys
import re


def ERROR(msg):
    sys.stderr.write(msg + "\n")
    exit(1)


SPACE_RE = re.compile(r"\s+")


class Tokenizer:
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
            ERROR("Unexpected end of file.")

        # Skip whitespace.
        m = SPACE_RE.match(self.line)
        if m:
            self.line = self.line[len(m.group(0)):]
            self.pos += len(m.group(0))

        for r in regexs:
            m = r[0].match(self.line)
            if m:
                self.line = self.line[len(m.group(0)):]
                self.pos += len(m.group(0))
                return r[1](m.group(0))

        ERROR("Line %d:%d, Expected: %s, found: '%s'" %
              (self.line_no, self.pos, error, self.line))

    def eof(self):
        return self._next_line() is None
