import unittest

from .test_sample import TestAnswer

# initialize the test suite
loader = unittest.TestLoader()
suite = unittest.TestSuite()

# add tests to the test suite
suite.addTests(loader.loadTestsFromTestCase(TestAnswer))

# initialize a runner, pass it your suite and run it
runner = unittest.TextTestRunner(verbosity=3)
runner.run(suite)
