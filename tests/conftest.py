from pytest import fixture
from crypto_signals import Signals
import os


@fixture(scope="function")
def signals_(data_directory_):
    return Signals(data_directory=data_directory_)


@fixture(scope="session")
def data_directory_():
    return "dummy_data_for_testing"


@fixture(scope="function")
def filename_(data_directory_):
    return os.path.join(data_directory_, "btc.csv")
