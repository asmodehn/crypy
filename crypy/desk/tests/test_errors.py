import pytest

from .. import errors


def test_raise_nomsg():

    def crypy_except():
        raise errors.CrypyException

    with pytest.raises(errors.CrypyException) as excinfo:
        crypy_except()

    assert excinfo.type is errors.CrypyException
    assert len(str(excinfo.value)) > 0
    assert not hasattr(excinfo.value, 'original')

    #TODO : traceback


def test_raise_msg():
    def crypy_except():
        raise errors.CrypyException("Ayayyayayay!")

    with pytest.raises(errors.CrypyException) as excinfo:
        crypy_except()

    assert excinfo.type is errors.CrypyException
    assert str(excinfo.value) == "Ayayyayayay!"
    assert not hasattr(excinfo.value, 'original')


def test_raise_encaps():
    def crypy_except():
        raise errors.CrypyException("Ayayyayayay!", Exception("bouhouhouh"))

    with pytest.raises(errors.CrypyException) as excinfo:
        crypy_except()

    assert excinfo.type is errors.CrypyException
    assert str(excinfo.value) == "Ayayyayayay!: bouhouhouh"
    assert str(excinfo.value.original) == "bouhouhouh"


if __name__ == '__main__':
    pytest.main(['-s', __file__])
