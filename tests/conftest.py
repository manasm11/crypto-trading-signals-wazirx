from pytest import fixture
from crypto_signals import Signals
import os
from uuid import uuid4
import shutil
from time import sleep


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
