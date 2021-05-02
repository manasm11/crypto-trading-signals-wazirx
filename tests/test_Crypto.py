from crypto_signals import Crypto
from crypto_signals.Crypto import Price
from datetime import datetime
import os
import shutil
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

    assert os.stat(btc_file).st_size > 0, f"{btc_file} FILE IS EMPTY"

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
    crypto.add_price(price)
    crypto.get_price(datetime.now().timestamp())


def test_price_operators():
    assert Price(value=1) > Price(value=0)
    assert Price(value=1) >= Price(value=0)
    assert Price(value=0) >= Price(value=0)
    assert Price(value=1) < Price(value=2)
    assert Price(value=1) <= Price(value=1)
    assert Price(value=1) <= Price(value=2)
    assert Price(value=100) == Price(value=100)
    assert Price(value=1) > 0
    assert Price(value=1) >= 0
    assert Price(value=0) >= 0
    assert Price(value=1) < 2
    assert Price(value=1) <= 1
    assert Price(value=1) <= 2
    assert Price(value=1) <= 2.2
    assert Price(value=100) == 100
    assert 100 == Price(value=100)
    assert 100 <= Price(value=100)
    assert 200 == Price(value=190) + 10
    assert 180 == Price(value=190) - 10
    assert -180 == 10 - Price(value=190)
    assert 1900 == Price(value=190) * 10
    assert 1.9 == Price(value=19) / 10
    assert 1 == Price(value=19) // 10
    assert 25 == Price(value=5) ** 2
    assert 0 == Price(value=190) % 10
    assert 2 == Price(value=192) % 10
    assert Price(value=2) and Price(value=5)
    assert Price(value=2) and 5
    assert Price(value=2) or 5
    price = Price(10)
    Price(
        value=201,
        low=190.4,
        high=203.4,
        open_=203,
        vol=912234,
        sell=2139821,
        buy=2139321,
        time=1619871441,
    )
    Price(
        value="201",
        low="190.4",
        high="203.4",
        open_="203",
        vol="912234",
        sell="2139821",
        buy="2139321",
        time="1619871441",
    )
    Price(
        value="201 ",
        low="190.4",
        high="203.4",
        open_="203",
        vol="912234",
        sell="2139821",
        buy="2139321",
        time=" 1619871441 ",
    )
    price = Price(109)
    price.low = 123
    price.high = 234
    price.open_ = 456
    price.vol = 4756
    price.sell = 4567
    price.time = 1234345

    assert price["low"] == price.low
    assert price["high"] == price.high
    assert price["open_"] == price.open_
    assert price["vol"] == price.vol
    assert price["sell"] == price.sell
    assert price["time"] == price.time


def test_Price_methods(filename_):
    price = Price(
        value="201 ",
        low="190.4",
        high="203.4",
        open_="203",
        vol="912234",
        sell="2139821",
        buy="2139321",
        time=" 1619871441 ",
    )
    attrs = ["time", "price", "low", "high", "open_", "vol", "sell"]
    data = price.todict()
    for attr in attrs:
        assert attr in data.keys()
    for attr in attrs:
        try:
            exec(f"price.{attr} = '3xx54'")
        except ValueError as e:
            assert "could not convert" in str(e)
        else:
            assert False, "Error not raised"

    for attr in attrs:
        try:
            price["low"] = "abcd"
        except ValueError as e:
            assert "could not convert" in str(e)
        else:
            assert False, "Error not raised"

    price.save(filename_)

    try:
        price.save(os.path.join("nodirectory", "doge"))
    except NotADirectoryError:
        pass
    except Exception:
        assert False, "Invalid Error Raised"
    else:
        assert False, "No Error raised"

    assert os.path.exists(filename_)
    with open(filename_) as file_:
        lines = file_.readlines()
        assert len(lines) > 0
        for line in lines:
            assert line.count(",") + 1 == len(data.keys())
            for e in line.split(","):
                float(e)
