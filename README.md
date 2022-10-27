
# Helium-Lang
### Version 1.03 :tada:

A handwritten soon-to-be self-compiled language

Helium's goal is to bring declarative yet powerful
code to compiled languages. There are a lot of great
compiled languages, yet not many are declarative, let alone
without their flaws.

## Getting started
No external dependencies are required to install Helium. The Helium-Py
compiler is written in pure Python and the standalone Helium compiler
will be self-hosted and independent of any external libraries :sparkles:

1. Clone or download the git repository
2. Install Python 3.7 or above
3. Execute `python main.py --c="test.he" -r`*

##### * To see the lexer, AST, or codegen results, you must append `-r` or `--results` to your command

## Command-line arguments:
| Argument:     | Usage:       | Required? | Defaults to: | Information:                                         |
|---------------|--------------|-----------|--------------|------------------------------------------------------|
| -c, --compile | -c="file.he" | True      | n/a          | This is the file you would like to compile           |
| -r, --results | -r           | False     | --no-results | This displays the lexer, parser, and codegen results |
| -d, --debug*  | -d           | False     | --no-debug   | This displays useful compiler-related information    |
| -t, --test    | -t           | False     | --no-test    | This executes the compilers tests before compiling   |

##### * Work in progress argument

## Code examples:

```
func main(): u32 {
    hello("Hi world", 3)

    return 0
}

func hello(txt: str, amnt: u32): void {
    for i in range(amnt) {
        println(f"{txt} {i}")
    }
}
```

_which would give us:_

```
Hi world 0
Hi world 1
Hi world 2
```

Helium is syntactically similar to Python, although it is statically typed :bulb:


## Statistics:
| Module:      | test.he speed: | Total: | Per Token: | Total per token: |
|--------------|----------------|--------|------------|------------------|
| Lexer        | ~1.5ms         | ~1.5ms | ~1.065us   | ~1.085us         |
| AST          | n/a            | ~1.5ms | n/a        | ~1.085us         |
| Codegen      | n/a            | ~1.5ms | n/a        | ~1.085us         |
| Assembler    | n/a            | ~1.5ms | n/a        | ~1.085us         |
| Bootstrapper | n/a            | ~1.5ms | n/a        | ~1.085us         |

## TODO:
  - [ ] [95/100]: The lexer
  - [ ] [00/100]: The AST (parser)
  - [ ] [00/100]: The codegen
  - [ ] [00/100]: The assembler
  - [ ] [00/100]: The bootstrapper
  - [x] Setup the Github repository
  - [x] Refactor initial code
  - [x] Add lexer tests
  - [ ] Add AST tests
  - [ ] Add codegen tests
  - [ ] Add assembler tests
  - [ ] Add bootstrapper tests
