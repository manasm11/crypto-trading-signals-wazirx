from unittest import TestCase as test
from pytest import mark


# signal.should_buy function
def test_should_buy_returns_boolean(signals):
    signal = signals.should_buy("win")
    assert isinstance(signal, bool)


# signal.should_sell function
def test_should_sell_returns_boolean(signals):
    signal = signals.should_sell("win")
    assert isinstance(signal, bool)
