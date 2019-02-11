import logging
import os
from typing import Optional
from pathlib import Path, PosixPath
import configparser

sample_config_file = """
[kraken.com]
  apiKey = "YOUR KRAKEN API KEY"
  secret = "YOUR KRAKEN API SECRET"
  verbose = true

[testnet.bitmex.com]
  apiKey = "YOUR BITMEX KEY"
  secret = "YOUR BITMEX SECRET"
  verbose = true

[etc.]

"""


def locate(filename: Optional[str] = None) -> Path:
    config_file = None

    filename = 'crypy.ini' if filename is None else filename
    l=[
        os.curdir,
        os.path.join(os.getcwd(), os.path.pardir),
        os.path.expanduser("~"),
        "/etc/crypy",
        os.environ.get("CRYPY_CONF")
    ]

    # We loop on turthy value only (no empty string, no none, etc.)
    for loc in (p for p in l if p):
        locfile = Path(loc).joinpath(filename)
        if locfile.exists():
            config_file = locfile
            break

    if config_file is None:  # If not present, generate sample file
        config_file = Path(os.curdir).joinpath(filename)
        logging.warning("config file not found. {config_file} has been generated for you.")
        config_file.write_text(sample_config_file)

    config_file.resolve()
    return config_file


_default_config = {}

_config_instances = dict()

config = _default_config


def configure(filename: Optional[str] = None, reset: bool = False) -> configparser.ConfigParser:

    config_file = locate(filename)

    if (config_file not in _config_instances) or reset:

        # Preparing config
        c = configparser.ConfigParser()
        c.optionxform = str

        # Loading file
        c.read(str(config_file))

        _config_instances[config_file] = dict(c)

    # we set the module attribute
    config = _config_instances.get(config_file, _default_config)

    return config

