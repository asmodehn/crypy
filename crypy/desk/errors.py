from ..euc import ccxt
from .. import config


# Ref : https://julien.danjou.info/python-exceptions-guide/

class CrypyException(Exception):
    """Base class for Crypy's exceptions
    """
    def __init__(self, msg=None, fixer=None, original=None):
        """Initializes a Crypy exception.
        Optionally can wrap another exception"""
        msg = "Crypy Exception !" if msg is None else msg
        if original:
            self.original = original
            super().__init__(f"{msg}: {original}")
        else:
            super().__init__(f"{msg}")

        # Dynamically build a method to address this exception
        self.__call__ = fixer


class ExchangeError(CrypyException):
    pass


class AuthenticationError(ExchangeError):
    pass


class PermissionDenied(AuthenticationError):
    pass


class AccountSuspended(AuthenticationError):
    pass




