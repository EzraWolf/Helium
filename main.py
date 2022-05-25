
import time
import pprint

from compiler_py.lexer.lexer import Lexer


def bootstrap():
    pass


def main():
    with open('./compiler_py/lexer/test.he') as f:
        txt = f.read()

    lex = Lexer(txt)
    return lex.tokenize()


if __name__ == '__main__':
    start = time.perf_counter()
    res = main()
    end = time.perf_counter()

    timed = round((end - start) * 1000, 5)

    print('\n\n\n')
    pprint.pp(res)
    print('\n')
    print(f'The Lexer took about {timed}ms')
