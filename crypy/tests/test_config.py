import time
import unittest
import tempfile
import os
from pathlib import Path

from crypy import config

"""
Module testing the config module.
This is tricky to test because of the integration with the surrounding environment and file system...
"""


class TestResolve(unittest.TestCase):
    def test_resolve_existing(self):

        with tempfile.TemporaryDirectory(
            prefix="crypy_test_resolve_existing_"
        ) as tmpdir:

            with tempfile.NamedTemporaryFile(
                suffix=".ini", prefix="conftest_", dir=tmpdir
            ) as conffile:

                # Making sure our resolve can find a file where it actually is.
                assert (
                    str(
                        config.resolve(
                            filename=os.path.basename(conffile.name), pathlist=[tmpdir]
                        )
                    )
                    == conffile.name
                )

    def test_resolve_absent(self):

        with tempfile.TemporaryDirectory(prefix="crypy_test_resolve_absent_") as tmpdir:

            # TODO : make sure a warning is logged... and prevent it during test (via log config)...

            # Making sure our resolve can create a file where it should be.
            created_conf = config.resolve(
                filename="conftest_created", pathlist=[tmpdir]
            )

            assert str(created_conf.absolute()) == os.path.join(
                tmpdir, "conftest_created"
            )

            # Assert content is created as expected
            with open(str(created_conf), "r") as conf:

                expected = config.sample_config_file.splitlines()
                actual = conf.read().splitlines()
                assert expected == actual


class TestExchangeSection(unittest.TestCase):
    def test_exchange_section(self):
        pass


class TestConfig(unittest.TestCase):
    def test_config(self):
        pass


if __name__ == "__main__":
    unittest.main()
