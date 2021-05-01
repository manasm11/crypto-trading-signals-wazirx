from pytest import fixture
from crypto_signals import Signals


@fixture(scope="function")
def signals_(data_directory_):
    return Signals(data_directory=data_directory_)


@fixture(scope="session")
def data_directory_():
    return "data"
