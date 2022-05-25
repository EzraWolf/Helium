
# Helium-Lang

A handwritten, soon-to-be self compiled language.

Helium's main goal is to bring declarative, yet powerful
code to compiled languages. There are a vast amount of wonderful
compiled languages, yet not many are declarative, let alone
without their flaws.

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

As you can see it's very syntactially similar to Python,
though Helium is statically typed.


## TODO:
  - [ ] [//////....] 65%: The lexer
  - [ ] [..........] 0%: The parser
  - [ ] [..........] 0%: The codegen
  - [ ] [..........] 0%: The assembler
  - [ ] [..........] 0%: The bootstrapper
  - [x] Setup the Github repository
  - [x] Refactor initial code