import pytest
import random
from main.golay import encode, decode


def test_1():
    assert encode("000000000010") == "000000000001100011101010"
    assert decode("000000000001100011101010") == "000000000010"


def test_2():
    assert encode("100011100110") == "011001110010100001011110"
    assert decode("011001110010100001011110") == "100011100110"
