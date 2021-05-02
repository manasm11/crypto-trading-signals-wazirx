from crypto_signals import Crypto
from crypto_signals.Crypto import Price
from datetime import datetime
import os
import requests_cache
from pytest import mark

requests_cache.install_cache(expire_after=360)


# @mark.xfail(reason="Will Complete After Testing Price")
def test_crypto(data_directory_):
    assert "data" not in data_directory_, "Check the data_directory_ fixture"
    # Crypto.all FUNCTION TESTS
    all_ = Crypto.all(data_directory=data_directory_)
    (_ for _ in all_)  # Check if all_ is iterable
    assert len(all_) > 0
    assert isinstance(all_[0], Crypto)

    # Crypto.update TESTS

    Crypto.update(data_directory=data_directory_)
    assert os.path.exists(data_directory_), f"{data_directory_} not created"
    btc_file = os.path.join(data_directory_, "btc.csv")
    assert os.path.exists(btc_file), f"{btc_file} not created"
    assert os.stat(btc_file).st_size > 0, f"{btc_file} FILE IS EMPTY"

    # HELPER FUNCTIONS
    raw = Crypto._get_data_from_api()
    assert isinstance(raw, dict)
    data = Crypto._parse_data_from_api(raw)
    assert isinstance(data, dict)
    assert len(data.keys()) > 0, "data is empty"
    assert isinstance(data["win"], Price)
    assert data["doge"], "data['doge'] is empty"
    assert data["doge"] > 0
    assert data["doge"] >= 0
    assert data["doge"] < int("9" * 22)
    assert data["doge"] <= int("9" * 22)
    assert data["doge"] == data["doge"]

    # SYMBOLS
    symbols = Crypto.SYMBOLS
    crypto = Crypto(symbol="btc", data_directory=data_directory_)
    price = Price(
        time=datetime.now().timestamp(),
        low=1,
        high=2,
        value=1.2,
        vol=1000,
        open_=1.1,
        sell=1.12,
        buy=1.13,
    )


def test_crypto_add_price(crypto, price):
    crypto.add_price(price)
    crypto.get_price(datetime.now().timestamp())
