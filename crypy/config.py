import logging
import os

import typing
from pathlib import Path, PosixPath
import configparser

from dataclasses import dataclass, field, asdict

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


default_filename = "settings.ini"


def resolve(filename: str) -> Path:
    pathlist = [
        os.curdir,
        os.path.join(os.path.dirname(__file__), os.path.pardir),
        # having crypy.ini in root of source repo (not for production)
        os.path.expanduser("~/.config/crypy"),
        "/etc/crypy",
        os.environ.get("CRYPY_CONF"),
    ]

    config_file = None
    # We loop on truthy value only (no empty string, no none, etc.)
    for loc in (p for p in pathlist if p):
        locfile = Path(loc).joinpath(filename)
        if locfile.exists():
            config_file = locfile
            break

    if (
        config_file is None
    ):  # If not present, generate sample file, locally to make it obvious.
        config_file = Path(os.curdir).joinpath(filename)
        logging.warning(
            "config file not found. {config_file} has been generated for you."
        )
        config_file.write_text(sample_config_file)

    config_file.resolve()
    return config_file


@dataclass(frozen=True)
class ExchangeSection:
    """
    Properly parsed config, ready to use for setting up a remote exchange.
    A Section is immutable.
    """

    credentials_file: Path  # value computed in config, based on section name
    credentials_parser: configparser.ConfigParser = field(
        init=False,
        default=configparser.ConfigParser(
            interpolation=configparser.ExtendedInterpolation()
        ),
        repr=False,
    )

    name: str
    impl_hook: str = 'print("You need to define impl_hook in the configuration"); exit()'
    timeout: int = 30000
    enableRateLimit: bool = True
    verbose: bool = True

    def parse_creds(self, credentials_file):
        self.credentials_parser.optionxform = str  # to prevent lowering keys
        # Loading file
        resolved_cf = resolve(str(credentials_file))
        try:
            with open(resolved_cf, 'r') as f:
                config_string = f.read()
                try:
                    self.credentials_parser.read_string(config_string)
                except (configparser.MissingSectionHeaderError, ):
                    config_string = '[credentials]\n' + config_string
                    with open(resolved_cf, 'w') as fw:
                        fw.write(config_string)
                    self.credentials_parser.read_string(config_string)
        except Exception as e:
            print(e)

    def exec_hook(self, ccxt):
        # Using the impl_hook from settings.ini
        locals = {'config': asdict(self), 'impl': None}
        # TODO : find a cleaner way to pass globals (config defaults from another place ?)
        exec(self.impl_hook, {'ccxt': ccxt}, locals)  # TODO check exchange id existing in CCXT
        return locals.get('impl')

    @property
    def apiKey(self):
        if 'apiKey' not in self.credentials_parser.defaults():

            self.parse_creds(self.credentials_file)

        return self.credentials_parser['credentials']['apiKey']

    @property
    def secret(self):
        if 'secret' not in self.credentials_parser.defaults():

            self.parse_creds(self.credentials_file)

        return self.credentials_parser['credentials']['secret']


@dataclass(frozen=True)
class Config:
    """
    Config class managing parsing of the config file.
    Also holds the various sections already parsed.
    Config is immutable.
    """

    filepath: typing.Optional[Path] = field(
        init=True, default=resolve(default_filename), repr=True
    )
    #TODO : extract the file reading part to a function, so we can pass strings and more ?
    parser: configparser.ConfigParser = field(
        init=False,
        default=configparser.ConfigParser(
            interpolation=configparser.ExtendedInterpolation()
        ),
        repr=False,
    )

    defaults: typing.Dict = field(default_factory=dict, init=False)

    sections: typing.Dict[str, ExchangeSection] = field(
        default_factory=list, init=False
    )

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
                if k is 'name':
                    sec_kwargs[k] = section
                else:
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
                        pass  # we will use the dataclass default instead

            # Assigning default credential filename if not present.
            # note if settings.ini file is setup with full absolute path, then keyfiles are supposed to be in the same location
            # Otherwise, if settings.ini location is relative, and resolved at runtime, the keyfile location also is, and could be in found in a different location.
            if "credentials_file" not in sec_kwargs:
                sec_kwargs["credentials_file"] = Path(
                    #self.filepath.parent,
                    section + ".key"
                )

            # Note: sections members not in dataclass are ignored
            return sec_kwargs

        # Looping on all sections
        object.__setattr__(
            self,
            "sections",
            {s: ExchangeSection(**section_parse(s)) for s in self.parser.sections()},
        )


if __name__ == "__main__":
    cff = resolve(default_filename)
    print(f"Config file found at {cff.absolute()}")
    c = Config(filepath=cff)
    print(c)

    for n, s in c.sections.items():
        print(f"{n} : {s}")
        cf = resolve(str(s.credentials_file))
        if cf:
            print(f"Credentials found at {cf}")
        else:
            raise FileNotFoundError(f"Credential file not found : {cf}")
