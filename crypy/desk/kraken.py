import typing
import logging

from ..euc import ccxt

from . import errors

# TODO :check pydantic to verify config data
Credentials = typing.NamedTuple(typename="Credentials", fields=[
    ("apiKey", str),
    ("secret", str),
    ("uid", typing.Optional[str]),
    ("login", typing.Optional[str]),
    ("password", typing.Optional[str]),
    ("twofa", typing.Optional[str]),  # 2-factor authentication (one-time password key)
    ("privateKey", typing.Optional[str]),  # a "0x"-prefixed hexstring private key for a wallet
    ("walletAddress", typing.Optional[str])
])




class Kraken:
    """
    Kraken API returning panda dataframes

    TODO : consolidate to make a more functional interface... see Caerbannog.
    TODO : test it, extensively.
    TODO :  support different libraries as implementation.
    """

    @property
    def credentials(self):
        logging.warning("Credentials accessed for Kraken")
        return

    @credentials.setter
    def credentials_set(self, credentials: Credentials):
        logging.warning("Credentials loaded for Kraken")
        for i in vars(credentials):
            setattr(self.exchange, i)
        # WIP : is this enough or do we need to reset the exchange ??

    def __init__(self, conf):
        # conf = dict(config.config().items('kraken.com'))

        for i in vars(Credentials):
            if i in conf:
                logging.warning("Credentials loaded for Kraken")

        # TMP
        conf['verbose'] = True

        self.exchange = ccxt.kraken(conf)


    ## Public API

    @property
    def markets(self):
        if self.exchange.markets is None:
            self.exchange.load_markets()
        return self.exchange.markets

    def load_markets(self, reload=False):
        """This calls self.exchange.fetch_markets internally"""
        self.exchange.load_markets(reload=reload)
        return self

    def fetch_markets(self):
        self.exchange.fetch_markets()
        return self

    def fetch_currencies(self):
        return self.exchange.fetch_currencies()

    def fetch_ticker(self):
        return self.exchange.fetch_ticker()

    def fetch_tickers(self):
        return self.exchange.fetch_tickers()

    def fetch_orderbook(self):
        return self.exchange.fetch_orderbook()

    def fetch_ohlcv(self):
        return self.exchange.fetch_ohlcv()

    def fetch_trades(self):
        return self.exchange.fetch_trades()

    @property
    def balance(self):
        """Fetches the balance of the account.
        If this fails because we are not authenticated, provide a solution in the exception.
        """
        try:
            self.exchange.fetch_balance()
        except ccxt.base.errors.AuthenticationError as exc:

            def auth_n_retry(*args, **kwargs):
                self.credentials_set(*args, **kwargs)
                return self.balance

            raise errors.AuthenticationError(original=exc, fixer=auth_n_retry)
        return self.exchange.balance

    def create_order(self):
        return self.exchange.create_order()

    def cancel_order(self):
        return self.exchange.cancel_order()

    def fetch_order(self):
        return self.exchange.fetch_order()

    def fetch_orders(self):
        return self.exchange.fetch_orders()

    def fetch_open_orders(self):
        return self.exchange.fetch_open_orders()

    def fetch_closed_orders(self):
        return self.exchange.fetch_closed_orders()

    def fetch_my_trades(self):
        return self.exchange.fetch_my_trades()

    def deposit(self):
        return self.exchange.deposit()

    def withdraw(self):
        return self.exchange.withdraw()


if __name__ == '__main__':

    k = Kraken()
    print(k.load_markets())

    print(k.fetch_markets())

    c = config.config().items('kraken.com')

    b = k.fetch_balance()
    if callable(b):  # b needs extra info, authentication
        b(c.get('apiKey'), c.get('secret'))

    print(b)
