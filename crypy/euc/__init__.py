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

# QUICK HACK
# TODO : properly, maybe with a 'silent' importer,
#  ie. an importer from a specific set of location, without requirng to modify the global interpreter state
# this can be useful in various (albeit advanced - coroutines importing changing source code) usecases
# Check palimport and filefinder2 for reference.


@contextlib.contextmanager
def sys_path_ctx(path):
    sys.path.insert(1, path)
    yield
    sys.path.remove(path)


# Note this is the path from the place where the python interpreter is launched
with sys_path_ctx("submodules/ccxt/python/"):
    import ccxt

# ccxt is now loaded in sys.modules from the git submodules folder
assert sys.modules['ccxt'].__file__ == 'submodules/ccxt/python/ccxt/__init__.py'


__all__ = ['ccxt']




