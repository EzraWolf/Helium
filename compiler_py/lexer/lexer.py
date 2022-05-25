
from . import tokens as toks


class Lexer:
    def __init__(self, program: str) -> None:
        self.txt: str = program
        self.pos: int = -1
        self.col: int = 1
        self.row: int = 1
        self.res: list = []

        self.is_running: bool = True

        self.prev_char: str = ''
        self.crnt_char: str = self.txt[self.pos]

    def tokenize(self) -> list[dict]:

        while self.pos < len(self.txt) and self.is_running:
            self._next_char()

            # ======================
            # Ignore all whitespace.
            # ======================
            if self.crnt_char in toks.WHITESPACE:
                continue

            # ================================================
            # Check if we have a single, or multiline comment.
            #
            #   # This is a single-line comment
            #   #[
            #       This is a multiline comment
            #   ]#
            # ================================================
            if self.crnt_char == '#':
                self._next_char()
                if self.prev_char == '#' and self.crnt_char == '[':
                    row = self.row - 1
                    col = self.col + 1

                    while not (
                        self.prev_char == ']' and
                        self.crnt_char == '#'
                    ):
                        if not self.is_running:
                            raise ValueError(
                                f'Expected a closing "]#" \
                                for line {row}, column {col}'
                            )
                        self._next_char()

                else:
                    while (
                        self.crnt_char not in ['\n', '\r'] and
                        self.is_running
                    ):
                        self._next_char()

            # ================================================
            # Determine if we have a keyword or an identifier.
            # 1. First check for a starting character is good.
            # 2. Loop until we find a non-acceptable sequence.
            # 3. Determin if we have a kw, else an identifier.
            # ================================================
            if self._is_potential_ident_start(self.crnt_char):
                res: str = ''
                while (
                    self._is_potential_ident_char(self.crnt_char) and
                    self.is_running
                ):
                    res += self.crnt_char
                    self._next_char()

                if res in toks.KEYWORDS:
                    self._append(toks.TYPE_KEYWORD, res)

                else:
                    self._append(toks.TYPE_VARIABLE, res)

            if self._is_int(self.crnt_char):
                res:    str = ''
                dot_ct: int = 0
                while self._is_int(self.crnt_char):
                    res += self.crnt_char
                    self._next_char()

                    if self.crnt_char == '.':
                        self._next_char()
                        dot_ct += 1
                        res += '.'

                if dot_ct > 1:
                    raise ValueError(f'Invalid number {res}')

                if dot_ct == 0:
                    self._append(toks.TYPE_INTEGER, res)

                else:
                    self._append(toks.TYPE_FLOAT, res)

        return self.res

    def _append(self, type: str, value: str) -> None:
        self.res.append(
            {
                type: value,
                'row': self.row,
                'col': self.col - len(value),
            }
        )

    def _next_char(self):
        if self.pos + 1 >= len(self.txt):
            self.is_running = False
            return

        if self.crnt_char in ['\r', '\n']:
            self.row += 1
            self.col = 1

        else:
            self.col += 1

        self.pos += 1

        self.prev_char = self.crnt_char
        self.crnt_char = self.txt[self.pos]

    # Ripped from, and all credit goes to
    # #define is_potential_identifier_start(c)
    # https://github.com/python/cpython/blob/main/Parser/tokenizer.c
    def _is_potential_ident_start(self, char: str) -> bool:
        return (
            (char == '_') or
            (ord(char) > 127) or
            (self._is_letter(char))
        )

    # Ripped from, and all credit goes to
    # #define is_potential_identifier_char(c)
    # https://github.com/python/cpython/blob/main/Parser/tokenizer.c
    def _is_potential_ident_char(self, char: str) -> bool:
        return (
            (char == '_') or
            (ord(char) > 127) or
            (self._is_int(char)) or
            (self._is_letter(char))
        )

    def _is_letter(self, char: str) -> bool:
        return (
            (char >= 'a' and char <= 'z') or
            (char >= 'A' and char <= 'Z')
        )

    def _is_int(self, char: str) -> bool:
        return char >= '0' and char <= '9'

    def _build_float(self, string: str) -> bool:
        dot_ct: int = 0
        for char in string:
            if char == '.':
                dot_ct += 1

            if (dot_ct > 1) or not (char >= '0' and char <= '9'):
                return False

        return True

    def _find_num(self):
        res: str = ''
        dot_count: int = 0

        while self._is_int(self.crnt_char) and self.is_running:
            res += self.crnt_char
            self._next_char()

            if self.crnt_char == '.':
                res += self.crnt_char
                dot_count += 1
                self._next_char()

        if dot_count == 0 and len(res) > 0:
            self._append(toks.TOKTYPE_INTEGER, res)
            return res

        elif dot_count == 1 and len(res) > 0:
            self._append(toks.TOKTYPE_FLOAT, res)
            return res

        elif dot_count > 1:
            raise ValueError(f'Too many dots in the number "{res}"')
