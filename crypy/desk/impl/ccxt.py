import dataclasses

try:
    from ...euc import ccxt
    from ... import config
except (ImportError, ValueError):
    from crypy.euc import ccxt
    from crypy import config

try:
    from . import errors, limiter
except ImportError:
    from crypy.desk import errors, limiter


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

    return ccxt.kraken(dataclasses.asdict(exconf))


def bitmex(conf: config.Config = None, public=True, paper=True):
    """Initializing a public desk for kraken
    public is ony meant to be used by private kraken desk. TODO : better design ?
    """
    conf = conf if conf is not None else config.Config()
    if paper:
        host = 'testnet.bitmex.com'
    else:
        host = 'bitmex.com'

    assert host in conf.sections.keys()  # preventing errors early

    if public:
        exconf = conf.sections.get(host).public()
    else:
        exconf = conf.sections.get(host)

    return ccxt.bitmex(dataclasses.asdict(exconf))
