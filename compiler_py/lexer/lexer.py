from . import tokens as toks


class Lexer:
    """
    This is Helium's lexer. Here is where the code from your `*.he`
    files gets lexically analyzed and converted into tokens.

    E.G.
    ```
    func main(): u32 {
        print("Hello World")
        return 0
    }
    ```

    Becomes:
    ```
    [
        {"kw"   : "func"       , "row": 1, "col": 1 },
        {"ident": "main"       , "row": 1, "col": 6 },
        {"delim": "("          , "row": 1, "col": 10},
        {"delim": ")"          , "row": 1, "col": 11},
        {"delim": ":"          , "row": 1, "col": 12},
        {"var"  : "u32"        , "row": 1, "col": 14}, # Later treated as type
        {"delim": "{"          , "row": 1, "col": 18},
        {"ident": "print"      , "row": 2, "col": 5 },
        {"delim": "("          , "row": 2, "col": 10},
        {"str"  : "Hello World", "row": 2, "col": 11},
        {"delim": ")"          , "row": 2, "col": 24},
        {"kw"   : "return"     , "row": 3, "col": 5 },
        {"int"  : 0            , "row": 3, "col": 12},
        {"delim": "}"          , "row": 4, "col": 1 },
    ]
    ```
    """

    def __init__(self) -> None:
        self._txt: str = ""
        self._pos: int = -1
        self._col: int = 0
        self._row: int = 1
        self._res: list = []

        self._is_running: bool = True

        self._prev_char: str = ""
        self._crnt_char: str = ""

    def lex(self, program: str) -> list[dict]:
        self._txt = program + " "

        while self._pos < len(self._txt) and self._is_running:
            self._next_char()

            # ======================
            # Ignore all whitespace.
            # ======================
            if self._is_space(self._crnt_char):
                self._next_char()

            # ================================================
            # Check if we have a single, or multiline comment.
            #
            #   # This is a single-line comment
            #
            #   #[
            #       This is a multiline comment
            #   ]#
            # ================================================
            if self._crnt_char == "#":
                self._handle_comments()

            # ================================================
            # Determine if we have a keyword or an identifier.
            # 1. First check for a starting character is good.
            # 2. Loop until we find a non-acceptable sequence.
            # 3. Determine if we have a kw else an identifier.
            # ================================================
            if self._is_potential_ident_start(self._crnt_char):
                self._build_ident()

            # ================================================
            # Check if we have a string if our current char is
            # a double quote
            # ================================================
            if self._crnt_char == '"':
                self._build_string()

            # ================================================
            # Check if we have an integer or a float
            # by determining if our character is 0-9
            # ================================================
            if self._is_int(self._crnt_char):
                self._build_number()

            # ===============================================
            # Check if the current character is an operator
            # ===============================================
            if self._crnt_char in toks.OPERATOR_CHARS:
                row = self._row
                col = self._col
                operator = ""
                while self._crnt_char in toks.OPERATOR_CHARS:
                    operator += self._crnt_char
                    if self._peak(1) not in toks.OPERATOR_CHARS:
                        break

                    self._next_char()

                self._append(toks.TYPE_OPERATOR, operator, row, col)

            # ===============================================
            # Check if we have a delimiter currently.
            # ===============================================
            elif self._crnt_char in toks.DELIMITERS:
                self._append(toks.TYPE_DELIMITER, self._crnt_char, self._row, self._col)

            # ===============================================
            # We can confidently  say  that  if  our  current
            # char  is  not   a   delimiter,   operator,   or
            # whitespace by now, we have an unknown character
            # ===============================================
            elif not self._is_space(self._crnt_char):
                raise SyntaxError(
                    'Unknown character "{}" at line {}, column {}'.format(
                        self._crnt_char, self._row, self._col
                    )
                )

        # Clearing the lexer is absolutely  necessary  to
        # avoid test issues,  as about an hour and a half
        # of debugging showed it was still trying to lex,
        # but with previous stored values in self
        result = self._res
        self._clear()

        return result

    def _clear(self):
        self._txt = ""
        self._pos = -1
        self._col = 0
        self._row = 1
        self._res = []

        self._is_running = True

        self._prev_char = ""
        self._crnt_char = ""

    def _append(self, type: str, value: str, row: int, col: int) -> None:
        """Appends a token to the lexer's result"""

        self._res.append(
            {
                type: value,
                "row": row,
                "col": col,
            }
        )

    def _peak(self, amnt: int) -> str:
        """Safely peaks ahead in the text a specified amount"""

        if self._pos + amnt >= len(self._txt):
            self._is_running = False
            return

        return self._txt[self._pos + amnt]

    def _next_char(self):
        """
        Advances the lexer's position by one character
        while incrementing the column and row counters
        """

        if self._pos + 1 >= len(self._txt):
            self._is_running = False
            return

        if self._crnt_char in ["\r", "\n"]:
            self._row += 1
            self._col = 1

        else:
            self._col += 1

        self._pos += 1

        self._prev_char = self._crnt_char
        self._crnt_char = self._txt[self._pos]

    def _handle_comments(self) -> None:
        """
        Loops  through,  and  handles  both
        single-line and multi-line comments
        """

        # Consume the starting #
        self._next_char()

        # A multi-line comment
        if self._prev_char == "#" and self._crnt_char == "[":
            row = self._row
            col = self._col

            # While we have not reached the
            # end of the comment, increment
            while not (self._prev_char == "]" and self._crnt_char == "#"):
                self._next_char()

                # If we have reached an EOF, the
                # program ended before a closing
                if not self._is_running:
                    raise SyntaxError(
                        f'Expected a closing "]#" for line {row}, column {col}'
                    )

            # Consume the closing #
            self._next_char()
            return

        # A single-line comment
        while self._crnt_char not in ["\n", "\r"] and self._is_running:
            self._next_char()

    def _build_ident(self):
        """Handles identifiers, variables, and keywords"""

        row = self._row
        col = self._col
        res: str = ""
        while self._is_potential_ident_char(self._crnt_char) and self._is_running:
            res += self._crnt_char
            self._next_char()

        self._append(
            toks.TYPE_KEYWORD if res in toks.KEYWORDS else toks.TYPE_VARIABLE,
            res,
            row,
            col,
        )

    def _build_string(self):
        """
        Builds a string from the given lexer context.
        The context being the current position in the
        lexed file, the current character, row,  col,
        the previous character, etc..
        """

        row = self._row
        col = self._col
        string: str = ""

        # Consume the starting '
        self._next_char()

        while self._crnt_char != '"':
            string += self._crnt_char

            # If the next char is the end quote, break
            if self._peak(1) == '"':
                self._next_char()
                break

            self._next_char()

            # If we have reached an EOF, the
            # program ended before a closing
            if self._is_running is False:
                raise SyntaxError(
                    "Expected a closing '\"' for line {}, column {}".format(row, col)
                )

        # Consume the closing '
        self._next_char()

        self._append(toks.TYPE_STRING, string, row, col)

    def _build_number(self):
        """
        Builds an int or float  from  the  given  lexer
        context. The context being the current position
        in the lexed file, the current character,  row,
        col, the previous character, etc..
        """

        number: str = ""
        dot_ct: int = 0
        row = self._row
        col = self._col
        while self._is_int(self._crnt_char) and self._is_running:
            number += self._crnt_char
            self._next_char()
            if self._crnt_char == ".":
                dot_ct += 1
                number += self._crnt_char
                self._next_char()

        # Check for invalid dot counts
        # 3.1.4 is invalid, and so is .123
        if dot_ct > 1:
            raise SyntaxError(f"Invalid number {number}")

        self._append(
            toks.TYPE_INTEGER if dot_ct == 0 else toks.TYPE_FLOAT,
            int(number) if dot_ct == 0 else float(number),
            row,
            col,
        )

    def _is_space(self, char: str) -> bool:
        """
        Determines if a character is a whitespace
        from a pre-determined list of whitespaces

        TODO: Add support for unicode whitespaces
        """

        return char in toks.WHITESPACE

    def _is_potential_ident_start(self, char: str) -> bool:
        """
        Determines if a character is the start of a potential identifier

        Ripped from, and all credit goes to the python tokenizer
        #define is_potential_identifier_start(c)
        https://github.com/python/cpython/blob/main/Parser/tokenizer.c
        """

        return (char == "_") or (ord(char) > 127) or (self._is_letter(char))

    def _is_potential_ident_char(self, char: str) -> bool:
        """
        Determines if a character is a potential identifier

        Ripped from, and all credit goes to
        #define is_potential_identifier_char(c)
        https://github.com/python/cpython/blob/main/Parser/tokenizer.c
        """

        return (
            (char == "_")
            or (ord(char) > 127)
            or (self._is_int(char))
            or (self._is_letter(char))
        )

    def _is_letter(self, char: str) -> bool:
        """Determines if a character is a valid ASCII letter"""

        return (char >= "a" and char <= "z") or (char >= "A" and char <= "Z")

    def _is_int(self, char: str) -> bool:
        """Determines if a character is a valid ASCII integer"""

        return char >= "0" and char <= "9"
