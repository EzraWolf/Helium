from . import tokens as toks


class Lexer:
    """
    This is Helium's lexer. Here is where the code from your `*.he`
    files gets lexically analyzed and converted into tokens.

    E.G.
    ```
    func main(): u32 {
        print('Hello World')
        return 0
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
        {'var'  : 'u32'        , 'row': 1, 'col': 14}, # Later treated as type
        {'delim': '{'          , 'row': 1, 'col': 18},
        {'ident': 'print'      , 'row': 2, 'col': 5 },
        {'delim': '('          , 'row': 2, 'col': 10},
        {'str'  : 'Hello World', 'row': 2, 'col': 11},
        {'delim': ')'          , 'row': 2, 'col': 24},
        {'kw'   : 'return'     , 'row': 3, 'col': 5 },
        {'int'  : 0            , 'row': 3, 'col': 12},
        {'delim': '}'          , 'row': 4, 'col': 1 },
    ]
    ```
    """

    def __init__(self) -> None:
        self.__txt: str = ""
        self.__pos: int = -1
        self.__col: int = 0
        self.__row: int = 1
        self.__res: list = []

        self.__is_running: bool = True

        self.__prev_char: str = ""
        self.__crnt_char: str = ""

    def lex(self, program: str) -> list[dict]:
        self.__txt = program + " "

        while self.__pos < len(self.__txt) and self.__is_running:
            self.__next_char()

            # ================================================
            # Ignore all whitespace
            # ================================================
            if self.__is_space(self.__crnt_char):
                self.__next_char()

            # ================================================
            # Check if we have a single, or multiline comment
            #
            #   # This is a single-line comment
            #
            #   #[
            #       This is a multiline comment
            #   ]#
            # ================================================
            if self.__crnt_char == "#":
                self.__handle_comments()

            # ================================================
            # Determine if we have a keyword or an identifier
            # 1. First check for a starting character is good
            # 2. Loop until we find a non-acceptable sequence
            # 3. Determine if we have a kw else an identifier
            # ================================================
            if self.__is_potential_ident_start(self.__crnt_char):
                self.__build_ident()

            # ================================================
            # Check if we have a string if our current char is
            # a double quote
            # ================================================
            if self.__crnt_char == '"':
                self.__build_string()

            # ================================================
            # Check if we have an integer or a float
            # by determining if our character is 0-9
            # ================================================
            if self.__is_int(self.__crnt_char):
                self.__build_number()

            # ===============================================
            # Check if the current character is an operator
            # ===============================================
            if self.__crnt_char in toks.OPERATOR_CHARS:
                row = self.__row
                col = self.__col
                operator = ""
                while self.__crnt_char in toks.OPERATOR_CHARS:
                    operator += self.__crnt_char
                    if self.__peak(1) not in toks.OPERATOR_CHARS:
                        break

                    self.__next_char()

                self.__append(toks.TYPE_OPERATOR, operator, row, col)

            # ===============================================
            # Check if we have a delimiter currently.
            # ===============================================
            elif self.__crnt_char in toks.DELIMITERS:
                self.__append(
                    toks.TYPE_DELIMITER, self.__crnt_char, self.__row, self.__col
                )

            # ===============================================
            # We can confidently  say  that  if  our  current
            # char  is  not   a   delimiter,   operator,   or
            # whitespace by now, we have an unknown character
            # ===============================================
            elif not self.__is_space(self.__crnt_char):
                raise SyntaxError(
                    'Unknown character "{}" at line {}, column {}'.format(
                        self.__crnt_char, self.__row, self.__col
                    )
                )

        # Clearing the lexer is absolutely  necessary  to
        # avoid test issues,  as about an hour and a half
        # of debugging showed it was still trying to lex,
        # but with previous stored values in self
        result = self.__res
        self.__clear()

        return result

    def __clear(self):
        self.__txt = ""
        self.__pos = -1
        self.__col = 0
        self.__row = 1
        self.__res = []

        self.__is_running = True

        self.__prev_char = ""
        self.__crnt_char = ""

    def __append(self, type: str, value: str, row: int, col: int) -> None:
        """Appends a token to the lexer's result"""

        self.__res.append(
            {
                type: value,
                "row": row,
                "col": col,
            }
        )

    def __peak(self, amnt: int) -> str:
        """Safely peaks ahead in the text a specified amount"""

        if self.__pos + amnt >= len(self.__txt):
            self.__is_running = False
            return

        return self.__txt[self.__pos + amnt]

    def __next_char(self):
        """
        Advances the lexer's position by one character
        while incrementing the column and row counters
        """

        if self.__pos + 1 >= len(self.__txt):
            self.__is_running = False
            return

        if self.__crnt_char in ["\r", "\n"]:
            self.__row += 1
            self.__col = 1

        else:
            self.__col += 1

        self.__pos += 1

        self.__prev_char = self.__crnt_char
        self.__crnt_char = self.__txt[self.__pos]

    def __handle_comments(self) -> None:
        """
        Loops  through,  and  handles  both
        single-line and multi-line comments
        """

        # Consume the starting #
        self.__next_char()

        # A multi-line comment
        if self.__prev_char == "#" and self.__crnt_char == "[":
            row = self.__row
            col = self.__col

            # While we have not reached the
            # end of the comment, increment
            while not (self.__prev_char == "]" and self.__crnt_char == "#"):
                self.__next_char()

                # If we have reached an EOF, the
                # program ended before a closing
                if not self.__is_running:
                    raise SyntaxError(
                        f'Expected a closing "]#" for line {row}, column {col}'
                    )

            # Consume the closing #
            self.__next_char()
            return

        # A single-line comment
        while self.__crnt_char not in ["\n", "\r"] and self.__is_running:
            self.__next_char()

    def __read_import_stmt(self):
        """
        All import cases covered in this function:

        `import ./<lib>`
        `import ./<lib> as <foo>`
        `import ./<lib>/<dir>`
        `import ./<lib>/<dir> as <foo>`
        `import ../<lib>`
        `import ../<lib> as <foo>`
        `import ../<lib>/<dir>`
        `import ../<lib>/<dir> as <foo>`
        `import <baz> from ./<lib>`
        `import <baz> from ./<lib> as <foo>`
        `import <baz> from ./<lib>/<dir>`
        `import <baz> from ./<lib>/<dir> as <foo>`
        `import <baz> from ../<lib>`
        `import <baz> from ../<lib> as <foo>`
        `import <baz> from ../<lib>/<dir>`
        `import <baz> from ../<lib>/<dir> as <foo>`
        """
        pass

    def __read_from_import_stmt(self):
        """`from <lib> import foo`"""
        pass

    def __read_lib_func_stmt(self):
        """`lib>.function(<args>)`"""
        pass

    def __read_lib_obj_stmt(self):
        """`lib>.<class | enum | template | ...>`"""

    def __read_let_stmt(self):
        """`let: <type> = <const | var>`"""
        pass

    def __read_let_mut_stmt(self):
        """`let mut: <type> = <const | var>`"""
        pass

    def __read_if_stmt(self):
        """
        `if <cond> { ... }`,
        `if <cond> { ... } else { ... }` and,
        `if <cond> { ... } else if <cond> { ... }`
        """
        pass

    def __read_inline_if_stmt(self):
        """`<cond> ? true : false`"""
        pass

    def __read_switch_stmt(self):
        """`switch <var> { case: ... default: }`"""
        pass

    def __read_for_loop_stmt(self):
        """
        `for i in 0..n { ... }`,
        `for i in <iterable> { ... }`
        """
        pass

    def __read_while_loop_stmt(self):
        """
        `while <cond> { ... }`, and
        `do { ... } while <cond>`
        """
        pass

    def __read_func_stmt(self):
        """`func <ident>(<args>): <type> { ... }`"""
        pass

    def __read_enum_stmt(self):
        """`enum <ident> { ... }`"""
        pass

    def __read_template_stmt(self):
        """`template <ident> { ... }`"""
        pass

    def __read_class_stmt(self):
        """`class <ident> { ... }`"""
        pass

    def __read_struct_stmt(self):
        """`struct <ident> { ... }`"""
        pass

    def __read_extern_stmt(self):
        """`extern "<lang>" <ident>(<args>): <type>`"""
        pass

    def __read_try_catch_stmt(self):
        """`try { ... } catch <err> "<msg>"`"""
        pass

    def __read_throw_stmt(self):
        """`throw <err> "<msg>"`"""
        pass

    def __read_assert_stmt(self):
        """`assert <cond> "<err msg>"`"""
        pass

    def __build_ident(self):
        """Handles identifiers, variables, and keywords"""

        row = self.__row
        col = self.__col
        res: str = ""
        while self.__is_potential_ident_char(self.__crnt_char) and self.__is_running:
            res += self.__crnt_char
            self.__next_char()

            if res == "import":
                self.__read_import_stmt()

        self.__append(
            toks.TYPE_KEYWORD if res in toks.KEYWORDS else toks.TYPE_VARIABLE,
            res,
            row,
            col,
        )

    def __build_string(self):
        """
        Builds a string from the given lexer context.
        The context being the current position in the
        lexed file, the current character, row,  col,
        the previous character, etc..
        """

        row = self.__row
        col = self.__col
        string: str = ""

        if not self.__crnt_char == '"':
            raise SyntaxError(
                "LEXER ERROR - Something VERY bad just happened: \
Expected to build a string \
starting with a double quote on line {}, column {}".format(
                    row, col
                )
            )

        # Consume the starting "
        self.__next_char()

        while self.__crnt_char != '"':
            string += self.__crnt_char

            # If the next char is the end quote, break
            if self.__peak(1) == '"':
                self.__next_char()
                break

            self.__next_char()

            # If we have reached an EOF, the
            # program ended before a closing
            if self.__is_running is False:
                raise SyntaxError(
                    "Expected a closing double quote on \
line {}, column {}".format(
                        row, col
                    )
                )

        # Consume the closing '
        self.__next_char()
        self.__append(toks.TYPE_STRING, string, row, col)

    def __build_number(self):
        """
        Builds an int or float  from  the  given  lexer
        context. The context being the current position
        in the lexed file, the current character,  row,
        col, the previous character, etc..
        """

        number: str = ""
        dot_ct: int = 0
        row = self.__row
        col = self.__col
        while self.__is_int(self.__crnt_char) and self.__is_running:
            number += self.__crnt_char
            self.__next_char()
            if self.__crnt_char == ".":
                dot_ct += 1
                number += self.__crnt_char
                self.__next_char()

        # Check for invalid dot counts
        # 3.1.4 is invalid, and so is .123
        if dot_ct > 1:
            raise SyntaxError(f"Invalid number {number}")

        self.__append(
            toks.TYPE_INTEGER if dot_ct == 0 else toks.TYPE_FLOAT,
            int(number) if dot_ct == 0 else float(number),
            row,
            col,
        )

    def __is_space(self, char: str) -> bool:
        """
        Determines if a character is a whitespace
        from a pre-determined list of whitespaces

        TODO: Add support for unicode whitespaces
        """
        return char in toks.WHITESPACE

    def __is_potential_ident_start(self, char: str) -> bool:
        """
        Determines if a character is the start of a potential identifier

        Ripped from, and all credit goes to the python tokenizer
        #define is_potential_identifier_start(c)
        https://github.com/python/cpython/blob/main/Parser/tokenizer.c
        """
        return (char == "_") or (ord(char) > 127) or (self.__is_letter(char))

    def __is_potential_ident_char(self, char: str) -> bool:
        """
        Determines if a character is a potential identifier

        Ripped from, and all credit goes to the python tokenizer
        #define is_potential_identifier_char(c)
        https://github.com/python/cpython/blob/main/Parser/tokenizer.c
        """
        return (
            (char == "_")
            or (ord(char) > 127)
            or (self.__is_int(char))
            or (self.__is_letter(char))
        )

    def __is_letter(self, char: str) -> bool:
        """Determines if a character is a valid ASCII letter"""
        return (char >= "a" and char <= "z") or (char >= "A" and char <= "Z")

    def __is_int(self, char: str) -> bool:
        """Determines if a character is a valid ASCII integer"""
        return char >= "0" and char <= "9"
