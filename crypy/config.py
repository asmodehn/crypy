import logging
import os
from pathlib import Path

sample_config = """
[kraken.com]
  apiKey = "YOUR API KEY"
  secret = "YOUR API SECRET"
  verbose = true

[testnet.bitmex.com]
  apiKey = "YOUR BITMEX KEY"
  secret = "YOUR BITMEX SECRET"
  verbose = true

[etc.]

"""

locations = [
    os.curdir,
    os.path.expanduser("~"),
    "/etc/crypy",
    os.environ.get("CRYPY_CONF")
]


def locate(filename=None):
    config_file = None

    filename = 'crypy.ini' if filename is None else filename

    for loc in locations:
        locfile = Path(loc).joinpath(filename)
        if locfile.exists():
            config_file = locfile
            break

    if config_file is None:  # If not present, generate sample file
        config_file = Path(os.curdir).joinpath(filename)
        logging.warning("config file not found. {config_file} has been generated for you.")
        config_file.write_text(sample_config)

    config_file.resolve()
    return config_file


def config(filename=None):

    config_file = locate(filename)

    # Preparing config
    import configparser
    config = configparser.ConfigParser()
    config.optionxform = str

    # Loading file
    config.read(str(config_file))

    return config

