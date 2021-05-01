import os
from pathlib import Path
import requests


class Crypto:
    SYMBOLS = ["btc"]

    def __init__(self, symbol: str, data_directory: str):
        self.symbol = symbol
        self.data_directory = data_directory

    @classmethod
    def all(cls, data_directory: str):
        return [cls(symbol, data_directory) for symbol in cls.SYMBOLS]

    @classmethod
    def update(cls, data_directory: str):
        if not os.path.exists(data_directory):
            os.makedirs(data_directory)
        filename = os.path.join(data_directory, "btc.csv")
        Path(filename).touch()

    @classmethod
    def _get_data_from_api(cls):
        res = requests.get("https://api.wazirx.com/api/v2/tickers")
        return res.json()

    @classmethod
    def _parse_data_from_api(cls, data: dict):
        result = {}
        for key, value in data.items():
            key = str(key)
            if key.endswith("inr"):
                sym = value["base_unit"]
                result[sym] = Price(value=value["last"])
        return result


class Price(float):
    attrs = [
        "low",
        "high",
        "open_",
        "vol",
        "sell",
        "buy",
        "time",
    ]

    def __new__(self, value, **kwargs):
        return float.__new__(self, value)

    def __init__(
        self,
        value,
        low=-1,
        high=-1,
        open_=-1,
        vol=-1,
        sell=-1,
        buy=-1,
        time=-1,
    ):
        self.low = low
        self.high = high
        self.open_ = open_
        self.vol = vol
        self.sell = sell
        self.buy = buy
        self.time = time
        float.__init__(value)

    def __getitem__(self, name):
        if str(name).strip() == "0":
            raise StopIteration
        return eval(f"self.{name}")

    def __setitem__(self, name, value):
        value = float(value)
        return exec(f"self.{name} = {value}")

    def __setattr__(self, name, value):
        value = float(value)
        return super().__setattr__(name, value)
