"""
A Trader class, to be used in an async context.
One Trader manages one currency pair on one exchange
"""

class Trader:
    """
    A Trader is in charge of watching one currency pair. Then:
    - Sends to storage everything that was seen
    - Provides an interface for doing a trade (TODO : improve that part with simple decision making, to be able to follow and adjust indicators)
    - Logs any ongoing trade, positions entered/exited.
    """
    def __init__(self, currency_pair: tuple[Currency], exchange) -> Trader:
        self.currency_pair = currency_pair
        self.exchange = exchange

