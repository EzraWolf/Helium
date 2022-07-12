import unittest


from .tests import code_block_tests
from .tests import expr_tests
from .tests import misc_tests
from .tests import op_tests
from .tests import stmt_tests
from .tests import var_tests


def execute():

    # Execute unittests from another file
    suite = unittest.TestLoader().loadTestsFromModule(code_block_tests)
    suite.addTest(unittest.TestLoader().loadTestsFromModule(expr_tests))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(misc_tests))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(op_tests))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(stmt_tests))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(var_tests))
    unittest.TextTestRunner(verbosity=2).run(suite)
