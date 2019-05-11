import unittest

from crypy.desk import errors


class TestErrors(unittest.TestCase):
    def test_raise_nomsg(self):
        def crypy_except():
            raise errors.CrypyException

        with self.assertRaises(errors.CrypyException) as excinfo:
            crypy_except()

        assert len(str(excinfo.exception)) > 0
        assert not hasattr(excinfo.exception, "original")

        # TODO : traceback

    def test_raise_msg(self):
        def crypy_except():
            raise errors.CrypyException("Ayayyayayay!")

        with self.assertRaises(errors.CrypyException) as excinfo:
            crypy_except()

        assert str(excinfo.exception) == "Ayayyayayay!"
        assert not hasattr(excinfo.exception, "original")

    def test_raise_original(self):
        def crypy_except():
            raise errors.CrypyException(
                "Ayayyayayay!", original=Exception("bouhouhouh")
            )

        with self.assertRaises(errors.CrypyException) as excinfo:
            crypy_except()

        assert str(excinfo.exception) == "Ayayyayayay!: bouhouhouh"
        assert str(excinfo.exception.original) == "bouhouhouh"

    def test_raise_fixer(self):
        def crypy_fixer_except():
            return 42

        def crypy_except():
            raise errors.CrypyException("Ayayyayayay!", fixer=crypy_fixer_except)

        with self.assertRaises(errors.CrypyException) as excinfo:
            crypy_except()

        assert str(excinfo.exception) == "Ayayyayayay!"
        assert excinfo.exception.fixme == crypy_fixer_except


if __name__ == "__main__":
    unittest.main()
