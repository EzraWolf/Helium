
# `compiler_py`
This folder is Helium's python-based compiler, and it was initially
made to speed up development time so that it could be hand-translated
into Helium to make it self-hosted.

## Subfolders in order of execution:
1. `bootstrap` Use a previously compiler version of Helium to re-compile itself * **
2. `lexer` Take the file you have specified and break it down into a list of valid or invalid tokens
3. `ast` Create an order of operations and expect specific tokens at certain times to preserve syntactically correct code; will repeat steps 2 and 3 for any imported files
4. `codegen` Use the ASTs (parsers) finalized list, attempt to optimize it, and convert it into your target CPUs assembly
5. `assembler` Assemble the target CPUs assembly into one executable

##### * `compiler_py` does not use the bootstrapper, but the self-hosted compiler does
##### ** Sometimes, if there is no previously compiled version of Helium, you must use the bootstrap.py file underneath `bootstrap` to create your Helium-compiled, Helium compiler (its a lot..)
##### (The `error` folder is just a helper folder)
