
from . import tokens as toks


class Lexer:
    '''
    This is Helium's lexer. Here is where the code from your *.he
    files gets lexically analyzed and converted into tokens.

    E.G.
    ```
    func main(): u32 {
        print('Hello World')
    }
    ```

    Becomes:
    ```
    [
        {'kw'   : 'func'       , 'row': 1, 'col': 1 },
        {'ident': 'main'       , 'row': 1, 'col': 6 },
        {'delim': '('          , 'row': 1, 'col': 10},
        {'delim': ')'          , 'row': 1, 'col': 11},
        {'delim': ':'          , 'row': 1, 'col': 12},
        {'var'  : 'u32'        , 'row': 1, 'col': 14}, # Later used as a type
        {'delim': '{'          , 'row': 1, 'col': 18},
        {'ident': 'print'      , 'row': 2, 'col': 5 },
        {'delim': '('          , 'row': 2, 'col': 10},
        {'str'  : 'Hello World', 'row': 2, 'col': 11},
        {'delim': ')'          , 'row': 2, 'col': 22},
        {'delim': '}'          , 'row': 3, 'col': 1 },
    ]
    ```
    '''

    def __init__(self) -> None:
        self._txt: str = ''
        self._pos: int = -1
        self._col: int = 0
        self._row: int = 1
        self._res: list = []

        self._is_running: bool = True

        self._prev_char: str = ''
        self._crnt_char: str = ''

    def lex(self, program: str) -> list[dict]:
        self._txt = program

        while self._pos < len(self._txt) and self._is_running:
            self._next_char()

            # ======================
            # Ignore all whitespace.
            # ======================
            if self._crnt_char in toks.WHITESPACE:
                continue

            # ================================================
            # Check if we have a single, or multiline comment.
            #
            #   # This is a single-line comment
            #   #[
            #       This is a multiline comment
            #   ]#
            # ================================================
            if self._crnt_char == '#':
                self._next_char()
                if self._prev_char == '#' and self._crnt_char == '[':
                    row = self._row - 1
                    col = self._col + 1

                    while not (
                        self._prev_char == ']' and
                        self._crnt_char == '#'
                    ):
                        if not self._is_running:
                            raise ValueError(
                                f'Expected a closing "]#" \
                                for line {row}, column {col}'
                            )
                        self._next_char()

                else:
                    while (
                        self._crnt_char not in ['\n', '\r'] and
                        self._is_running
                    ):
                        self._next_char()

            # ================================================
            # Determine if we have a keyword or an identifier.
            # 1. First check for a starting character is good.
            # 2. Loop until we find a non-acceptable sequence.
            # 3. Determin if we have a kw, else an identifier.
            # ================================================
            if self._is_potential_ident_start(self._crnt_char):
                res: str = ''
                while (
                    self._is_potential_ident_char(self._crnt_char) and
                    self._is_running
                ):
                    res += self._crnt_char
                    self._next_char()

                if res in toks.KEYWORDS:
                    self._append(toks.TYPE_KEYWORD, res)

                else:
                    self._append(toks.TYPE_VARIABLE, res)

            if self._is_int(self._crnt_char):
                res:    str = ''
                dot_ct: int = 0
                while self._is_int(self._crnt_char):
                    res += self._crnt_char
                    self._next_char()

                    if self._crnt_char == '.':
                        self._next_char()
                        dot_ct += 1
                        res += '.'

                if dot_ct > 1:
                    raise ValueError(f'Invalid number {res}')

                if dot_ct == 0:
                    self._append(toks.TYPE_INTEGER, res)

                else:
                    self._append(toks.TYPE_FLOAT, res)

        return self._res

    def _append(self, type: str, value: str) -> None:
        self._res.append(
            {
                type: value,
                'row': self._row,
                'col': self._col - len(value),
            }
        )

    def _next_char(self):
        if self._pos + 1 >= len(self._txt):
            self._is_running = False
            return

        if self._crnt_char in ['\r', '\n']:
            self._row += 1
            self._col = 1

        else:
            self._col += 1

        self._pos += 1

        self._prev_char = self._crnt_char
        self._crnt_char = self._txt[self._pos]

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

        while self._is_int(self._crnt_char) and self._is_running:
            res += self._crnt_char
            self._next_char()

            if self._crnt_char == '.':
                res += self._crnt_char
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
