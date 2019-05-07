import unittest

# import your test modules
from . import test_errors

# initialize the test suite
loader = unittest.TestLoader()
public_suite  = unittest.TestSuite()

# Specific test suite, not suitable for automated run / CI
private_suite = unittest.TestSuite()

# add tests to the test suite
public_suite.addTests(loader.loadTestsFromModule(test_errors))

# initialize a runner, pass it your suite and run it
runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(public_suite)
# TODO : add basic arguments handling (argparse) to run the private test suite.
