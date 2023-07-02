class Parser(object):
    def __init__(self):
        pass

    def __read_import_stmt(self):
        """
        All import cases covered in this function:

        `import ./<lib>`
        `import ./<lib> as <foo>`
        `import ./<lib>/<dir>`
        `import ./<lib>/<dir> as <foo>`
        `import ../<lib>`
        `import ../<lib> as <foo>`
        `import ../<lib>/<dir>`
        `import ../<lib>/<dir> as <foo>`
        `import <baz> from ./<lib>`
        `import <baz> from ./<lib> as <foo>`
        `import <baz> from ./<lib>/<dir>`
        `import <baz> from ./<lib>/<dir> as <foo>`
        `import <baz> from ../<lib>`
        `import <baz> from ../<lib> as <foo>`
        `import <baz> from ../<lib>/<dir>`
        `import <baz> from ../<lib>/<dir> as <foo>`
        """
        pass

    def __read_from_import_stmt(self):
        """`from <lib> import foo`"""
        pass

    def __read_lib_func_stmt(self):
        """`lib>.function(<args>)`"""
        pass

    def __read_lib_obj_stmt(self):
        """`lib>.<class | enum | template | ...>`"""

    def __read_let_stmt(self):
        """`let: <type> = <const | var>`"""
        pass

    def __read_let_mut_stmt(self):
        """`let mut: <type> = <const | var>`"""
        pass

    def __read_if_stmt(self):
        """
        `if <cond> { ... }`,
        `if <cond> { ... } else { ... }` and,
        `if <cond> { ... } else if <cond> { ... }`
        """
        pass

    def __read_inline_if_stmt(self):
        """`<cond> ? true : false`"""
        pass

    def __read_switch_stmt(self):
        """`switch <var> { case: ... default: }`"""
        pass

    def __read_for_loop_stmt(self):
        """
        `for i in 0..n { ... }`,
        `for i in <iterable> { ... }`
        """
        pass

    def __read_while_loop_stmt(self):
        """
        `while <cond> { ... }`, and
        `do { ... } while <cond>`
        """
        pass

    def __read_func_stmt(self):
        """`func <ident>(<args>): <type> { ... }`"""
        pass

    def __read_enum_stmt(self):
        """`enum <ident> { ... }`"""
        pass

    def __read_template_stmt(self):
        """`template <ident> { ... }`"""
        pass

    def __read_class_stmt(self):
        """`class <ident> { ... }`"""
        pass

    def __read_struct_stmt(self):
        """`struct <ident> { ... }`"""
        pass

    def __read_extern_stmt(self):
        """`extern "<lang>" <ident>(<args>): <type>`"""
        pass

    def __read_try_catch_stmt(self):
        """`try { ... } catch <err> "<msg>"`"""
        pass

    def __read_throw_stmt(self):
        """`throw <err> "<msg>"`"""
        pass

    def __read_assert_stmt(self):
        """`assert <cond> "<err msg>"`"""
        pass
