
# Not using the Enum library because
# this is simpler and I plan to  use
# as  little   external  or  interal
# libraries       as        possible
TYPE_UNKNOWN:    str = 'unknown'
TYPE_KEYWORD:    str = 'keyword'
TYPE_IDENTIFIER: str = 'identifier'
TYPE_VARIABLE:   str = 'variable'
TYPE_STRING:     str = 'string'
TYPE_INTEGER:    str = 'integer'
TYPE_FLOAT:      str = 'float'
TYPE_DELIMITER:  str = 'delimiter'
TYPE_OPERATOR:   str = 'operator'

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

OPERATOR_CHARS = [
    '=', '+',
    '-', '*',
    '/', '!',
    '<', '>',
    '|', '&',
    '^', '~'
]

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
