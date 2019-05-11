# External Untrusted Code :
# Currently implemented as git submodules that we can update,
# and copy paste in the appropriate place, only if it passes all tests...

# TODO : activate or not...

# TODO : easy way to run tests

# DONT DO : automatic copy of code :
# it should be done manually, and via git commit only to keep trac of things.



# Importing euc will import these
import contextlib
import sys
import importlib.util
from pathlib import Path

# QUICK HACK
# TODO : properly, maybe with a 'silent' importer,
#  ie. an importer from a specific set of location, without requirng to modify the global interpreter state
# this can be useful in various (albeit advanced - coroutines importing changing source code) usecases
# Check palimport and filefinder2 for reference.


@contextlib.contextmanager
def sys_path_ctx(path):
    sys.path.insert(1, str(path))
    yield
    sys.path.remove(str(path))


# CCXT
# Note this is the path from the place where the python interpreter is launched
ccxt_path = Path(__file__).parents[2].joinpath("submodules/ccxt/python/").resolve()


with sys_path_ctx(ccxt_path):
    import ccxt

# ccxt is now loaded in sys.modules from the git submodules folder
assert sys.modules['ccxt'].__file__ == str(ccxt_path.joinpath('ccxt').joinpath('__init__.py'))


# MPMATH
# Note this is the path from the place where the python interpreter is launched
mpmath_path = Path(__file__).parents[2].joinpath("submodules/mpmath/").resolve()

with sys_path_ctx(mpmath_path):
    import mpmath

# ccxt is now loaded in sys.modules from the git submodules folder
assert sys.modules['mpmath'].__file__ == str(mpmath_path.joinpath('mpmath').joinpath('__init__.py'))

__all__ = ['ccxt', 'mpmath']




