# Not using the Enum library  because
# this is works just fine for its use
TYPE_KEYWORD: str = "kw"
TYPE_IDENTIFIER: str = "ident"
TYPE_VARIABLE: str = "var"
TYPE_STRING: str = "str"
TYPE_INTEGER: str = "int"
TYPE_FLOAT: str = "flt"
TYPE_DELIMITER: str = "delim"
TYPE_OPERATOR: str = "op"

# The list of keywords
KEYWORDS = [
    "from",
    "import",
    "as",
    "let",
    "mut",
    "typeof",
    "sizeof",
    "if",
    "else",
    "switch",
    "case",
    "default",
    "for",
    "in",
    "range",
    "do",
    "break",
    "continue",
    "while",
    "global",
    "func",
    "pass",
    "enum",
    "template",
    "class",
    "struct",
    "extern",
    "return",
    "throw",
    "assert",
    "async",
    "await",
]

# The start of a potential operator character
OPERATOR_CHARS = ["=", "+", "-", "*", "/", "\\", "!", "%", "<", ">", "|", "&", "^", "~"]

# The list of supported operations
OPERATORS = [
    "==",
    "!=",
    "||",
    "^^",
    "<",
    ">",
    "<=",
    ">=",
    "=",
    "+",
    "-",
    "*",
    "/",
    "%",
    "**",
    "+=",
    "-=",
    "*=",
    "/=",
    "%=",
    "**=",
    "&",
    "|",
    "^",
    "~",
    "<<",
    ">>",
    "<<<",
    ">>>",
    "&=",
    "|=",
    "^=",
    "<<=",
    ">>=",
    "<<<=",
    ">>>=",
    "++",
    "--",
]

# The list of valid delimiters
DELIMITERS = [
    ".",
    ",",
    ":",
    ";",
    "'",
    '"',
    "(",
    ")",
    "[",
    "]",
    "{",
    "}",
]

# Whitespace found with help from
# https://stackoverflow.com/questions/6507056/replace-all-whitespace-characters
# With the addition of ' ' on my part.
WHITESPACE = [
    " ",
    "\f",
    "\n",
    "\r",
    "\t",
    "\v",
    "\u00a0",
    "\u1680",
    "\u2000",
    "\u200a",
    "\u2028",
    "\u2029",
    "\u202f",
    "\u205f",
    "\u3000",
    "\ufeff",
]
