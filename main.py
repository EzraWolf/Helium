
import sys
import time
import pprint
import unittest

from compiler_py.lexer import tests
from compiler_py.lexer import lexer


def main(*args):
    if len(args) != 1:
        print('Usage: main.py path/to/file/<filename>.he')
        return

    with open(args[0]) as f:
        txt = f.read()

    start = time.perf_counter()
    lex = lexer.Lexer()
    res = lex.lex(txt)
    end = time.perf_counter()

    print('\n')
    pprint.pp(res)
    print('\n')

    timed = round((end - start) * 1000, 5)
    print(f'The Lexer took about {timed}ms')

    return


if __name__ == '__main__':

    # run unittest from another file
    suite = unittest.TestLoader().loadTestsFromModule(tests)
    unittest.TextTestRunner(verbosity=2).run(suite)

    args = sys.argv[1:][0]
    main(args)
