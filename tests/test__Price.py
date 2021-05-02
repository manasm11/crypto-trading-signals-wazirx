import os
from crypto_signals._Price import Price


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


def test_Price_todict_method(filename_):
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


def test_Price_save_method(price, test, filename_):
    data = price.todict()
    price.save(filename_)
    wrong_filepath = os.path.join("nodirectory", "doge.csv")
    test.assertRaises(NotADirectoryError, price.save, wrong_filepath)
    assert os.path.exists(filename_)
    with open(filename_) as file_:
        lines = file_.readlines()
        assert len(lines) > 0
        for line in lines:
            assert line.count(",") + 1 == len(data.keys())
            for e in line.split(","):
                float(e)

    price_invalid = Price(value=22)
    test.assertRaises(AttributeError, price_invalid.save, filename_)
