
import os
import time
import pprint
import unittest
import argparse

from compiler_py.lexer import tests
from compiler_py.lexer import lexer


def main(args: argparse.Namespace) -> int:

    if not args.file:
        raise BaseException('Usage: main.py path/to/file/file.he')

    if os.path.exists(args.file):
        with open(args.file, 'r') as f:
            txt = f.read()

    else:
        raise BaseException('File {} not found'.format(args[1]))

    lex = lexer.Lexer()
    res: list[dict] = []

    start = time.perf_counter()
    res = lex.lex(txt)
    stop = time.perf_counter()

    if args.is_results:
        print('\n')
        pprint.pp(res)
        print('\n')

    timed = round((stop - start) * 1000, 4)
    per_char = round((timed / len(txt)) * 1000, 4)
    print(f'The Lexer took about: {timed}ms')
    print(f'Per character, about: {per_char}us')


if __name__ == '__main__':

    arg_parse = argparse.ArgumentParser(description='Helium arguments')
    arg_parse.add_argument(
        '--file',
        dest='file',
        type=str,
        required=True,
        help='The path to your file',
    )

    arg_parse.add_argument(
        '--test',
        dest='is_test',
        type=bool,
        default=False,
        required=False,
        action=argparse.BooleanOptionalAction,
        help='Allow tests to occur before execution',
    )

    arg_parse.add_argument(
        '--results',
        dest='is_results',
        type=bool,
        default=False,
        required=False,
        action=argparse.BooleanOptionalAction,
        help='Print the results of the lexer, parser, and codegen',
    )

    arg_parse.add_argument(
        '--debug',
        dest='is_debug',
        type=bool,
        default=False,
        required=False,
        action=argparse.BooleanOptionalAction,
        help='Allows the user to optionally print debug information',
    )

    args: argparse.Namespace = arg_parse.parse_args()

    if args.is_test:

        # Execute unittests from another file
        suite = unittest.TestLoader().loadTestsFromModule(tests)
        unittest.TextTestRunner(verbosity=2).run(suite)

    main(args)
