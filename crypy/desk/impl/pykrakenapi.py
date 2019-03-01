


"""
Module implementing APIs with kraken, through pykrakenapi.
returns raw data, extracted from the API library
"""



import krakenex
from pykrakenapi import KrakenAPI
api = krakenex.API()
k = KrakenAPI(api)
ohlc, last = k.get_ohlc_data("ETHEUR")
print(ohlc)


# tier=3, retry=.5, crl_sleep=5

def kraken(conf: config.Config = None, public=True):
    """Initializing a public desk for kraken
    public is ony meant to be used by private kraken desk. TODO : better design ?
    """
    conf = conf if conf is not None else config.Config()
    assert 'kraken.com' in conf.sections.keys()  # preventing errors early

    if public:
        exconf = conf.sections.get('kraken.com').public()
    else:
        exconf = conf.sections.get('kraken.com')

    api = krakenex.API(key=exconf.get('apiKey'), secret=exconf.get('secret'))
    k = KrakenAPI(api)
    return k
