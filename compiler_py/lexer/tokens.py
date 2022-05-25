
# Not using the Enum library because
# this is simpler and works just fine
TYPE_UNKNOWN:    str = 'unknown'
TYPE_KEYWORD:    str = 'keyword'
TYPE_IDENTIFIER: str = 'identifier'
TYPE_VARIABLE:   str = 'variable'
TYPE_STRING:     str = 'string'
TYPE_INTEGER:    str = 'integer'
TYPE_FLOAT:      str = 'float'
TYPE_DELIMITER:  str = 'delimiter'
TYPE_OPERATOR:   str = 'operator'

# The list of keywords
KEYWORDS = [
    'from',   'use',
    'as',     'let',
    'const',  'typeof',
    'sizeof', 'if',
    'else',   'switch',
    'case',   'default',
    'for',    'in',
    'range',  'do',
    'break',  'continue',
    'while',  'pub',
    'func',   'pass',
    'enum',   'template',
    'class',  'struct',
    'extern', 'return',
    'try',    'catch',
    'throw',  'assert',
    'async',  'await',
]

# The start of a potential operator character
OPERATOR_CHARS = [
    '=', '+',
    '-', '*',
    '/', '!',
    '<', '>',
    '|', '&',
    '^', '~'
]

# The list of supported operations
OPERATORS = [
    '==',   '!=',
    '||',   '^^',
    '<',    '>',
    '<=',   '>=',
    '=',    '+',
    '-',    '*',
    '/',    '%',
    '**',   '+=',
    '-=',   '*=',
    '/=',   '%=',
    '**=',  '&',
    '|',    '^',
    '~',    '<<',
    '>>',   '<<<',
    '>>>',  '&=',
    '|=',   '^=',
    '<<=',  '>>=',
    '<<<=', '>>>=',
    '++',   '--',
]

# The list of valid delimiters
DELIMITERS = [
    '.',  ',',
    ':',  ';',
    '\'', '"',
    '(',  ')',
    '[',  ']',
    '{',  '}',
]

# Whitespace found with help from
# https://stackoverflow.com/questions/6507056/replace-all-whitespace-characters
# With the addition of ' ' on my part.
WHITESPACE = [
    ' ',
    '\f',
    '\n',
    '\r',
    '\t',
    '\v',
    '\u00a0',
    '\u1680',
    '\u2000',
    '\u200a',
    '\u2028',
    '\u2029',
    '\u202f',
    '\u205f',
    '\u3000',
    '\ufeff',
]
