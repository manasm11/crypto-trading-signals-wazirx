from crypto_signals import Crypto
from crypto_signals._Price import Price
from datetime import datetime


def test_crypto(filename_):
    Crypto.all(filename=filename_)
    Crypto.update(filename=filename_)
    symbols = Crypto.SYMBOLS

    crypto = Crypto(symbol="btc", filename=filename_)

    price = Price(
        timestamp=datetime.now().timestamp(),
        low=1,
        high=2,
        value=1.2,
        volume=1000,
        open=1.1,
        sell=1.12,
        buy=1.13,
    )
    crypto.add_price(price)
    crypto.get_price(datetime.now().timestamp())
