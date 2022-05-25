
import unittest
from compiler_py.lexer import lexer


class TestImports(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lexer = lexer.Lexer()

    def test_from(self):
        test_case: str = 'from foo import bar'
        res = self.lexer.lex(test_case)
        self.assertEqual(
            res,
            [
                {'kw': 'from', 'row': 1, 'col': 1},
                {'var': 'foo', 'row': 1, 'col': 6},
                {'kw': 'import', 'row': 1, 'col': 10},
                {'var': 'bar', 'row': 1, 'col': 17},
            ],
            f'Failed to lex "{test_case}"'
        )
