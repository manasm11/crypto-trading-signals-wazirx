from pytest import fixture
from crypto_signals import Signals


@fixture(scope="function")
def signals_(filename_):
    return Signals(filename_)


@fixture(scope="session")
def filename_():
    return "data/crypto.csv"
