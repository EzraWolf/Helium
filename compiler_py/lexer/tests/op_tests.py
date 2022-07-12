"""
Tests for operator tokens being properly tokenized in
multiple different ways
"""

import unittest


from compiler_py.lexer import lexer
from compiler_py.lexer import tokens


class LexerTestOperators(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lexer = lexer.Lexer()

    def test_basic_op_usage(self):
        for op in tokens.OPERATORS:
            with self.subTest():
                test: str = f"1 {op} 3.1415"
                res = self.lexer.lex(test)
                self.assertEqual(
                    res,
                    [
                        {"int": 1, "row": 1, "col": 1},
                        {"op": op, "row": 1, "col": 3},
                        {"flt": 3.1415, "row": 1, "col": 4 + len(op)},
                    ],
                    f'Failed to lex "{test}" for operator "{op}"',
                )

    def test_basic_op_usage_no_spaces(self):
        for op in tokens.OPERATORS:
            with self.subTest():
                test: str = f"1{op}3.1415"
                res = self.lexer.lex(test)
                self.assertEqual(
                    res,
                    [
                        {"int": 1, "row": 1, "col": 1},
                        {"op": op, "row": 1, "col": 2},
                        {"flt": 3.1415, "row": 1, "col": 2 + len(op)},
                    ],
                    f'Failed to lex "{test}" for operator "{op}"',
                )

    def test_var_op_usage(self):
        for op in tokens.OPERATORS:
            with self.subTest():
                test: str = f"foo {op} bar"
                res = self.lexer.lex(test)
                self.assertEqual(
                    res,
                    [
                        {"var": "foo", "row": 1, "col": 1},
                        {"op": op, "row": 1, "col": 5},
                        {"var": "bar", "row": 1, "col": 6 + len(op)},
                    ],
                    f'Failed to lex "{test}" for operator "{op}"',
                )

    def test_var_op_usage_no_space(self):
        for op in tokens.OPERATORS:
            with self.subTest():
                test: str = f"foo{op}bar"
                res = self.lexer.lex(test)
                self.assertEqual(
                    res,
                    [
                        {"var": "foo", "row": 1, "col": 1},
                        {"op": op, "row": 1, "col": 4},
                        {"var": "bar", "row": 1, "col": 4 + len(op)},
                    ],
                    f'Failed to lex "{test}" for operator "{op}"',
                )

    def test_var_assign_op_usage(self):
        for op in tokens.OPERATORS:
            with self.subTest():
                test: str = f"foo = bar {op} 42"
                res = self.lexer.lex(test)
                self.assertEqual(
                    res,
                    [
                        {"var": "foo", "row": 1, "col": 1},
                        {"op": "=", "row": 1, "col": 5},
                        {"var": "bar", "row": 1, "col": 7},
                        {"op": op, "row": 1, "col": 11},
                        {"int": 42, "row": 1, "col": 12 + len(op)},
                    ],
                    f'Failed to lex "{test}" for operator "{op}"',
                )

    def test_var_assign_op_usage_no_space(self):
        for op in tokens.OPERATORS:
            with self.subTest():
                test: str = f"foo=bar{op}42"
                res = self.lexer.lex(test)
                self.assertEqual(
                    res,
                    [
                        {"var": "foo", "row": 1, "col": 1},
                        {"op": "=", "row": 1, "col": 4},
                        {"var": "bar", "row": 1, "col": 5},
                        {"op": op, "row": 1, "col": 8},
                        {"int": 42, "row": 1, "col": 8 + len(op)},
                    ],
                    f'Failed to lex "{test}" for operator "{op}"',
                )
