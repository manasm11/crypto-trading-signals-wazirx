from pytest import fixture
from crypto_signals import Signals
import os
from uuid import uuid4
import shutil
from time import sleep
import unittest
from crypto_signals.Crypto import Price, Crypto


@fixture(scope="function")
def signals_(data_directory_):
    return Signals(data_directory=data_directory_)


@fixture(scope="session")
def data_directory_():
    dir_path = str(uuid4()).split("-")[2]
    yield dir_path
    shutil.rmtree(dir_path)


@fixture(scope="function")
def filename_(data_directory_):
    return os.path.join(data_directory_, "btc.csv")


@fixture(scope="function")
def price():
    return Price(
        value="201 ",
        low="190.4",
        high="203.4",
        open_="203",
        vol="912234",
        sell="2139821",
        buy="2139321",
        time=" 1619871441 ",
    )


@fixture(scope="session")
def test():
    return unittest.TestCase()


@fixture(scope="function", params=["btc", "win"])
def crypto(request):
    return Crypto(symbol=request.param, data_directory=data_directory_)
