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
    def __new__(self, value):
        return float.__new__(self, value)

    def __init__(self, value):
        # self = float(value)
        float.__init__(value)


# class Foo(float):
#     def __new__(self, value, extra):
#         return float.__new__(self, value)
#     def __init__(self, value, extra):
#         float.__init__(value)
#         self.extra = extra

# class Price:
#     """This class is used by Crypto Class to save Prices"""

#     _value = 0

#     def __init__(self, value):
#         self._value = float(value)

#     def __float__(self):
#         return 1.0

#     def __bool__(self):
#         return bool(self._value)

#     def _evaluate(self, other, operator: str):
#         if isinstance(other, self.__class__):
#             return eval(f"self._value {operator} other._value")
#         return eval(f"self._value {operator} other")

#     def __gt__(self, other):
#         return self._evaluate(other, ">")

#     def __lt__(self, other):
#         return self._evaluate(other, "<")

#     def __le__(self, other):
#         return self._evaluate(other, "<=")

#     def __ge__(self, other):
#         return self._evaluate(other, ">=")

#     def __eq__(self, other):
#         return self._evaluate(other, "==")

#     def __abs__(self):
#         return abs(self._value)

#     def __add__(self, other):
#         return self._evaluate(other, "+")

#     def __sub__(self, other):
#         return self._evaluate(other, "-")

#     def __rsub__(self, other):
#         if isinstance(other, self.__class__):
#             return eval(f"other._value - self._value")
#         return eval(f"other - self._value")

#     def __mul__(self, other):
#         return self._evaluate(other, "*")

#     def __truediv__(self, other):
#         return self._evaluate(other, "/")

#     def __floordiv__(self, other):
#         return self._evaluate(other, "//")

#     def __pow__(self, other):
#         return self._evaluate(other, "**")

#     def __mod__(self, other):
#         return self._evaluate(other, "%")
