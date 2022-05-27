
import unittest
from compiler_py.lexer import lexer


class TestImports(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lexer = lexer.Lexer()

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

    def test_from(self):
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