import logging
import os

import typing
from pathlib import Path, PosixPath
import configparser

from dataclasses import dataclass, field

sample_config_file = """
[kraken.com]
  apiKey: YOUR_KRAKEN_API_KEY
  secret: YOUR_KRAKEN_API_SECRET
  timeout: 20000
  enableRateLimit: True

[testnet.bitmex.com]
  apiKey: YOUR_BITMEX_KEY
  secret: YOUR_BITMEX_SECRET
  verbose: True

[etc.]

"""


default_filename = 'crypy.ini'


def resolve(filename: str) -> Path:
    pathlist = [
        os.curdir,
        os.path.join(os.path.dirname(__file__), os.path.pardir),
        # having crypy.ini in root of source repo (not for production)
        os.path.expanduser("~"),
        "/etc/crypy",
        os.environ.get("CRYPY_CONF")
    ]

    config_file = None
    # We loop on turthy value only (no empty string, no none, etc.)
    for loc in (p for p in pathlist if p):
        locfile = Path(loc).joinpath(filename)
        if locfile.exists():
            config_file = locfile
            break

    if config_file is None:  # If not present, generate sample file, locally to make it obvious.
        config_file = Path(os.curdir).joinpath(filename)
        logging.warning("config file not found. {config_file} has been generated for you.")
        config_file.write_text(sample_config_file)

    config_file.resolve()
    return config_file


@dataclass(frozen=True)
class ExchangeSection:
    """
    Properly parsed config, ready to use for setting up a remote exchange.
    A Section is immutable.
    """

    # Properly parsed config for an exchange
    apiKey: str = field(default="", repr=False)
    secret: str = field(default="", repr=False)
    timeout: int = 30000
    enableRateLimit: bool = True
    verbose: bool = True

    def public(self):
        """convenience method to strip out sensitive information"""
        return ExchangeSection(timeout=self.timeout, enableRateLimit=self.enableRateLimit, verbose=self.verbose)


@dataclass(frozen=True)
class Config:
    """
    Config class managing parsing of the config file.
    Also holds the various sections already parsed.
    Config is immutable.
    """
    filepath: typing.Optional[Path] = field(init=True,
                                            default=resolve(default_filename),
                                            repr=True)

    parser: configparser.ConfigParser = field(init=False,
                                              default=configparser.ConfigParser(
                                                  interpolation=configparser.ExtendedInterpolation()
                                              ),
                                              repr=False)

    defaults: typing.Dict = field(default_factory=dict, init=False)

    sections: typing.Dict[str, ExchangeSection] = field(default_factory=list, init=False)

    def __post_init__(self):
        self.parser.optionxform = str  # to prevent lowering keys
        # Loading file
        self.parser.read(str(self.filepath))

        # Filling up frozen attributes for later access
        object.__setattr__(self, "defaults", self.parser.defaults())

        def section_parse(section):
            sec_kwargs = {}
            """parses a section according to dataclass annotations"""
            for k, v in ExchangeSection.__annotations__.items():
                try:
                    # TODO : support optional annotation ?
                    if v is bool:
                        sec_kwargs[k] = self.parser.getboolean(section, k)
                    elif v is int:
                        sec_kwargs[k] = self.parser.getint(section, k)
                    elif v is float:
                        sec_kwargs[k] = self.parser.getfloat(section, k)
                    elif v is str:
                        sec_kwargs[k] = self.parser.get(section, k)
                except configparser.NoOptionError:
                    pass  # we will use hte dataclass default instead

            # Note: sections members not in dataclass are ignored
            return sec_kwargs

        object.__setattr__(self, "sections", {
            s: ExchangeSection(**section_parse(s)) for s in self.parser.sections()
        })


if __name__ == '__main__':

    c = Config()
    print(c)

    for n, s in c.sections.items():
        print(f"{n} : {s}")



