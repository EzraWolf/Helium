
import unittest
from compiler_py.lexer import lexer

from . import tokens as toks


# ======================================== #
#                                          #
# === OPERATOR TESTS ===================== #
#                                          #
# ======================================== #
class LexerTestOperators(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lexer = lexer.Lexer()

    def test_basic_op_usage(self):
        for op in toks.OPERATORS:
            with self.subTest():
                test: str = f'1 {op} 3.1415'
                res = self.lexer.lex(test)
                self.assertEqual(
                    res,
                    [
                        {'int': 1, 'row': 1, 'col': 1},
                        {'op': op, 'row': 1, 'col': 3},
                        {'flt': 3.1415, 'row': 1, 'col': 4 + len(op)},
                    ],
                    f'Failed to lex "{test}" for operator "{op}"'
                )

    def test_basic_op_usage_no_spaces(self):
        for op in toks.OPERATORS:
            with self.subTest():
                test: str = f'1{op}3.1415'
                res = self.lexer.lex(test)
                self.assertEqual(
                    res,
                    [
                        {'int': 1, 'row': 1, 'col': 1},
                        {'op': op, 'row': 1, 'col': 2},
                        {'flt': 3.1415, 'row': 1, 'col': 2 + len(op)},
                    ],
                    f'Failed to lex "{test}" for operator "{op}"'
                )

    def test_var_op_usage(self):
        for op in toks.OPERATORS:
            with self.subTest():
                test: str = f'foo {op} bar'
                res = self.lexer.lex(test)
                self.assertEqual(
                    res,
                    [
                        {'var': 'foo', 'row': 1, 'col': 1},
                        {'op': op, 'row': 1, 'col': 5},
                        {'var': 'bar', 'row': 1, 'col': 6 + len(op)},
                    ],
                    f'Failed to lex "{test}" for operator "{op}"'
                )

    def test_var_op_usage_no_space(self):
        for op in toks.OPERATORS:
            with self.subTest():
                test: str = f'foo{op}bar'
                res = self.lexer.lex(test)
                self.assertEqual(
                    res,
                    [
                        {'var': 'foo', 'row': 1, 'col': 1},
                        {'op': op, 'row': 1, 'col': 4},
                        {'var': 'bar', 'row': 1, 'col': 4 + len(op)},
                    ],
                    f'Failed to lex "{test}" for operator "{op}"'
                )

    def test_var_assign_op_usage(self):
        for op in toks.OPERATORS:
            with self.subTest():
                test: str = f'foo = bar {op} 42'
                res = self.lexer.lex(test)
                self.assertEqual(
                    res,
                    [
                        {'var': 'foo', 'row': 1, 'col': 1},
                        {'op': '=', 'row': 1, 'col': 5},
                        {'var': 'bar', 'row': 1, 'col': 7},
                        {'op': op, 'row': 1, 'col': 11},
                        {'int': 42, 'row': 1, 'col': 12 + len(op)},
                    ],
                    f'Failed to lex "{test}" for operator "{op}"'
                )

    def test_var_assign_op_usage_no_space(self):
        for op in toks.OPERATORS:
            with self.subTest():
                test: str = f'foo=bar{op}42'
                res = self.lexer.lex(test)
                self.assertEqual(
                    res,
                    [
                        {'var': 'foo', 'row': 1, 'col': 1},
                        {'op': '=', 'row': 1, 'col': 4},
                        {'var': 'bar', 'row': 1, 'col': 5},
                        {'op': op, 'row': 1, 'col': 8},
                        {'int': 42, 'row': 1, 'col': 8 + len(op)},
                    ],
                    f'Failed to lex "{test}" for operator "{op}"'
                )


# ====================================== #
#                                        #
# === IMPORT TESTS ===================== #
#                                        #
# ====================================== #
class LexerTestImports(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lexer = lexer.Lexer()

    def test_import(self):
        test: str = 'import foo'
        res = self.lexer.lex(test)
        self.assertEqual(
            res,
            [
                {'kw': 'import', 'row': 1, 'col': 1},
                {'var': 'foo', 'row': 1, 'col': 8},
            ],
            f'Failed to lex "{test}"'
        )

    def test_import_as(self):
        test: str = 'import foo as bar'
        res = self.lexer.lex(test)
        self.assertEqual(
            res,
            [
                {'kw': 'import', 'row': 1, 'col': 1},
                {'var': 'foo', 'row': 1, 'col': 8},
                {'kw': 'as', 'row': 1, 'col': 12},
                {'var': 'bar', 'row': 1, 'col': 15},
            ],
            f'Failed to lex "{test}"'
        )

    def test_from_import(self):
        test: str = 'from foo import a'
        res = self.lexer.lex(test)
        self.assertEqual(
            res,
            [
                {'kw': 'from', 'row': 1, 'col': 1},
                {'var': 'foo', 'row': 1, 'col': 6},
                {'kw': 'import', 'row': 1, 'col': 10},
                {'var': 'a', 'row': 1, 'col': 17},
            ],
            f'Failed to lex "{test}"'
        )

    def test_from_import_as(self):
        test: str = 'from foo import a as b'
        res = self.lexer.lex(test)
        self.assertEqual(
            res,
            [
                {'kw': 'from', 'row': 1, 'col': 1},
                {'var': 'foo', 'row': 1, 'col': 6},
                {'kw': 'import', 'row': 1, 'col': 10},
                {'var': 'a', 'row': 1, 'col': 17},
                {'kw': 'as', 'row': 1, 'col': 19},
                {'var': 'b', 'row': 1, 'col': 22},
            ],
            f'Failed to lex "{test}"'
        )

    def test_import_illegal_chars(self):
        test: str = 'import 3.1415'
        res = self.lexer.lex(test)
        self.assertEqual(
            res,
            [
                # Helium does not fix this in the  lexer,
                # because the parser will take care of it
                {'kw': 'import', 'row': 1, 'col': 1},
                {'flt': 3.1415, 'row': 1, 'col': 8},
            ],
            f'Failed to lex "{test}"'
        )

    def test_import_as_illegal_chars(self):
        test: str = 'import 42 as {'
        res = self.lexer.lex(test)
        self.assertEqual(
            res,
            [
                # Helium does not fix this in the  lexer,
                # because the parser will take care of it
                {'kw': 'import', 'row': 1, 'col': 1},
                {'int': 42, 'row': 1, 'col': 8},
                {'kw': 'as', 'row': 1, 'col': 11},
                {'delim': '{', 'row': 1, 'col': 14},
            ],
            f'Failed to lex "{test}"'
        )

    def test_import_illegal_spacing(self):
        test: str = 'importfoo bar'
        res = self.lexer.lex(test)
        self.assertEqual(
            res,
            [
                # Helium does not fix this in the  lexer,
                # because the parser will take care of it
                {'var': 'importfoo', 'row': 1, 'col': 1},
                {'var': 'bar', 'row': 1, 'col': 11},
            ],
            f'Failed to lex "{test}"'
        )


# ====================================== #
#                                        #
# === CLASS TESTS ====================== #
#                                        #
# ====================================== #
class LexerTestClasses(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lexer = lexer.Lexer()

    def test_class_def(self):
        test: str = 'class Foo {}'
        res = self.lexer.lex(test)
        self.assertEqual(
            res,
            [
                {'kw': 'class', 'row': 1, 'col': 1},
                {'var': 'Foo', 'row': 1, 'col': 7},
                {'delim': '{', 'row': 1, 'col': 11},
                {'delim': '}', 'row': 1, 'col': 12},
            ],
            f'Failed to lex "{test}"'
        )

    def test_class_def_with_method(self):
        test: str = '''\
class Foo {
    init(self) {
        self.num = 42
    }

    func foo(self) {
        return self.num
    }
}'''
        res = self.lexer.lex(test)
        self.assertEqual(
            res,
            [
                {'kw': 'class', 'row': 1, 'col': 1},
                {'var': 'Foo', 'row': 1, 'col': 7},
                {'delim': '{', 'row': 1, 'col': 11},
                {'var': 'init', 'row': 2, 'col': 5},
                {'delim': '(', 'row': 2, 'col': 9},
                {'var': 'self', 'row': 2, 'col': 10},
                {'delim': ')', 'row': 2, 'col': 14},
                {'delim': '{', 'row': 2, 'col': 16},
                {'var': 'self', 'row': 3, 'col': 9},
                {'delim': '.', 'row': 3, 'col': 13},
                {'var': 'num', 'row': 3, 'col': 14},
                {'op': '=', 'row': 3, 'col': 18},
                {'int': 42, 'row': 3, 'col': 20},
                {'delim': '}', 'row': 4, 'col': 5},
                {'kw': 'func', 'row': 6, 'col': 5},
                {'var': 'foo', 'row': 6, 'col': 10},
                {'delim': '(', 'row': 6, 'col': 13},
                {'var': 'self', 'row': 6, 'col': 14},
                {'delim': ')', 'row': 6, 'col': 18},
                {'delim': '{', 'row': 6, 'col': 20},
                {'kw': 'return', 'row': 7, 'col': 9},
                {'var': 'self', 'row': 7, 'col': 16},
                {'delim': '.', 'row': 7, 'col': 20},
                {'var': 'num', 'row': 7, 'col': 21},
                {'delim': '}', 'row': 8, 'col': 5},
                {'delim': '}', 'row': 9, 'col': 1},
            ],
            f'Failed to lex "{test}"'
        )

    def test_class_def_with_method_no_spaces(self):
        test: str = '''\
class Foo{init(self){self.num=42}\
func foo(self){return self.num}}'''
        res = self.lexer.lex(test)
        self.assertEqual(
            res,
            [
                {'kw': 'class', 'row': 1, 'col': 1},
                {'var': 'Foo', 'row': 1, 'col': 7},
                {'delim': '{', 'row': 1, 'col': 10},
                {'var': 'init', 'row': 1, 'col': 11},
                {'delim': '(', 'row': 1, 'col': 15},
                {'var': 'self', 'row': 1, 'col': 16},
                {'delim': ')', 'row': 1, 'col': 20},
                {'delim': '{', 'row': 1, 'col': 21},
                {'var': 'self', 'row': 1, 'col': 22},
                {'delim': '.', 'row': 1, 'col': 26},
                {'var': 'num', 'row': 1, 'col': 27},
                {'op': '=', 'row': 1, 'col': 30},
                {'int': 42, 'row': 1, 'col': 31},
                {'delim': '}', 'row': 1, 'col': 33},
                {'kw': 'func', 'row': 1, 'col': 34},
                {'var': 'foo', 'row': 1, 'col': 39},
                {'delim': '(', 'row': 1, 'col': 42},
                {'var': 'self', 'row': 1, 'col': 43},
                {'delim': ')', 'row': 1, 'col': 47},
                {'delim': '{', 'row': 1, 'col': 48},
                {'kw': 'return', 'row': 1, 'col': 49},
                {'var': 'self', 'row': 1, 'col': 56},
                {'delim': '.', 'row': 1, 'col': 60},
                {'var': 'num', 'row': 1, 'col': 61},
                {'delim': '}', 'row': 1, 'col': 64},
                {'delim': '}', 'row': 1, 'col': 65},
            ],
            f'Failed to lex "{test}"'
        )


# ======================================== #
#                                          #
# === FUNCTION TESTS ===================== #
#                                          #
# ======================================== #
class LexerTestFunctions(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lexer = lexer.Lexer()

    def test_func_def(self):
        test: str = '''\
func main(): u32 {
    let text = "Hi, world."
    println(text)
    return 0
}'''
        res = self.lexer.lex(test)
        self.assertEqual(
            res,
            [
                {'kw': 'func', 'row': 1, 'col': 1},
                {'var': 'main', 'row': 1, 'col': 6},
                {'delim': '(', 'row': 1, 'col': 10},
                {'delim': ')', 'row': 1, 'col': 11},
                {'delim': ':', 'row': 1, 'col': 12},
                {'var': 'u32', 'row': 1, 'col': 14},
                {'delim': '{', 'row': 1, 'col': 18},
                {'kw': 'let', 'row': 2, 'col': 5},
                {'var': 'text', 'row': 2, 'col': 9},
                {'op': '=', 'row': 2, 'col': 14},
                {'str': 'Hi, world.', 'row': 2, 'col': 16},
                {'var': 'println', 'row': 3, 'col': 5},
                {'delim': '(', 'row': 3, 'col': 12},
                {'var': 'text', 'row': 3, 'col': 13},
                {'delim': ')', 'row': 3, 'col': 17},
                {'kw': 'return', 'row': 4, 'col': 5},
                {'int': 0, 'row': 4, 'col': 12},
                {'delim': '}', 'row': 5, 'col': 1},
            ],
            f'Failed to lex "{test}"'
        )


# ====================================== #
#                                        #
# === STRUCT TESTS ===================== #
#                                        #
# ====================================== #
class LexerTestStructs(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lexer = lexer.Lexer()

    def test_struct_def(self):
        pass


# ==================================== #
#                                      #
# === ENUM TESTS ===================== #
#                                      #
# ==================================== #
class LexerTestEnums(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lexer = lexer.Lexer()

    def test_enum_def(self):
        pass


# ======================================== #
#                                          #
# === TEMPLATE TESTS ===================== #
#                                          #
# ======================================== #
class LexerTestTemplates(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lexer = lexer.Lexer()

    def test_template_def(self):
        pass


# ====================================== #
#                                        #
# === EXTERN TESTS ===================== #
#                                        #
# ====================================== #
class LexerTestExterns(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lexer = lexer.Lexer()

    def test_extern_def(self):
        pass


# ====================================== #
#                                        #
# === IF STATEMENT TESTS =============== #
#                                        #
# ====================================== #
class LexerTestIfStmts(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lexer = lexer.Lexer()

    def test_if_stmt(self):
        pass


# ========================================== #
#                                            #
# === SWITCH STATEMENT TESTS =============== #
#                                            #
# ========================================== #
class LexerTestSwitchStmts(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lexer = lexer.Lexer()

    def test_switch_stmt(self):
        pass


# ======================================= #
#                                         #
# === FOR LOOP TESTS ==================== #
#                                         #
# ======================================= #
class LexerTestForLoops(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lexer = lexer.Lexer()

    def test_for_loop(self):
        pass


# ========================================= #
#                                           #
# === WHILE LOOP TESTS ==================== #
#                                           #
# ========================================= #
class LexerTestWhileLoops(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lexer = lexer.Lexer()

    def test_while_loop(self):
        pass


# ========================================== #
#                                            #
# === ASYNC & AWAIT TESTS ================== #
#                                            #
# ========================================== #
class LexerTestAsyncAwaits(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lexer = lexer.Lexer()

    def test_async_await_def(self):
        pass


# ================================================ #
#                                                  #
# === USER-DEFIND ERROR HANDLING TESTS =========== #
#                                                  #
# ================================================ #
class LexerTestUserErrorHandling(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lexer = lexer.Lexer()

    def test_user_throw(self):
        pass

    def test_user_assert(self):
        pass
