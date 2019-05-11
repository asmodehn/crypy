import unittest

# import your test modules
from . import test_balance
from . import test_symbol

# initialize the test suite
loader = unittest.TestLoader()
suite = unittest.TestSuite()

# add tests to the test suite
suite.addTests(loader.loadTestsFromModule(test_balance))
suite.addTests(loader.loadTestsFromModule(test_symbol))

# initialize a runner, pass it your suite and run it
runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)
