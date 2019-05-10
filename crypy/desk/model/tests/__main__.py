import unittest
import doctest

# import your test modules
from . import test_balance
from . import test_symbol
from . import test_order

# initialize the test suite
loader = unittest.TestLoader()
suite = unittest.TestSuite()

# add tests to the test suite
suite.addTests(loader.loadTestsFromModule(test_balance))
suite.addTests(loader.loadTestsFromModule(test_symbol))
suite.addTests(loader.loadTestsFromModule(test_order))

suite.addTest(doctest.DocTestSuite(test_balance.balance))
suite.addTest(doctest.DocTestSuite(test_symbol.symbol))
suite.addTest(doctest.DocTestSuite(test_order.order))

# initialize a runner, pass it your suite and run it
runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)
