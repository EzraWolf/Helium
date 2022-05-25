
import sys
import time
import pprint

from compiler_py.lexer.lexer import Lexer


def main(*args):
    if len(args) != 1:
        print('Usage: main.py path/to/file/<filename>.he')
        return

    with open(args[0]) as f:
        txt = f.read()

    start = time.perf_counter()
    lex = Lexer(txt)
    res = lex.tokenize()
    end = time.perf_counter()

    print('\n')
    pprint.pp(res)
    print('\n')

    timed = round((end - start) * 1000, 5)
    print(f'The Lexer took about {timed}ms')

    return


if __name__ == '__main__':

    args = sys.argv[1:][0]
    main(args)
