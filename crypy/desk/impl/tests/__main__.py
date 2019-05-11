import unittest

# import your test modules
from . import test_ccxt
from . import test_mpmath

# initialize the test suite
loader = unittest.TestLoader()
suite  = unittest.TestSuite()

# add tests to the test suite
suite.addTests(loader.loadTestsFromModule(test_ccxt))
suite.addTests(loader.loadTestsFromModule(test_mpmath))

# initialize a runner, pass it your suite and run it
runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)
