# The change-log:

## Version 1.05 (LATEST):
 * Removed the `range` keyword in favor of `x..y`
 * Removed the `global` keyboard, useless.
 * Removed the `try` and `catch` keywords, you should never have to use these in good code
 * Restructured `lexer.py`
 * Temporarily removed the `async` and `await` keywords, not ready to add them yet.

## Version 1.04:
 * Cleaned up `lexer.py`
 * Maintained consistency and code format
 * Fixed a handful of `lexer.py` grammar errors
 * Changed command-line argument names

## Version 1.03:
 * Added a documentation folder, and documented the compiler
 * Added a `how_you_can_contribute.md` file under the documentation folder
 * Cleaned up pre-existing *.MD files
 * Improved consistency within files
 * Changed `pub` to `global` because `pub` sounds odd
 * Removed the `noxfile.py` file because of hundreds of SSL and untraced errors

## Version 1.02:
 * Added more tests for the lexer
 * Updated the lexers timer
 * Updated argument parsing
 * Refactored & linted code
 * Replaced `const` with `mut` in favor of `let` being constant by default
 * Updated the README.md
 * Added the CHANGELOG.md
 * Fixed all bugs in the lexer related to a token's current row and column
 * Updated the `test.he` file, more `test.he` file updates to come
 * Removed dead code in the lexer
 * Added detailed comments on how the code inside of the lexer works

## Version 1.01:
 * Began adding tests for the lexer
 * Updated the lexer
 * Refactored code
 * Added a timer to time the lexers speed

## Version 1.00:
 * The initial setup of Helium began here
 * Started partial work on the lexer
 * Added the README.md file
 * Setup the project directories
