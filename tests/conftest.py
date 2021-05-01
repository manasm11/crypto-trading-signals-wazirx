from pytest import fixture
from crypto_signals import Signals


@fixture(scope="function")
def signals():
    return Signals("data/crypto.csv")
