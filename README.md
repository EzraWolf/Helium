
# Helium-Lang

A handwritten, soon-to-be self-compiled language.

Helium's goal is to bring declarative yet powerful
code to compiled languages. There are a lot of great
compiled languages, yet not many are declarative, let alone
without their flaws.

## Getting started
No external dependencies are required to install Helium. The Helium-Py
compiler is purely written in Python.

1. Clone or download the git repository
2. Install Python 3.7 or above
3. Execute `python main.py path/to/your/<file>`

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

As you can see, it's very syntactically similar to Python,
although Helium is statically typed.


## TODO:
  - [ ] [65/100]: The lexer
  - [ ] [00/100]: The parser
  - [ ] [00/100]: The codegen
  - [ ] [00/100]: The assembler
  - [ ] [00/100]: The bootstrapper
  - [x] Setup the Github repository
  - [x] Refactor initial code