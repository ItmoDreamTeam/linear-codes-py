import pytest
import random
from main.golay import encode, decode


def test_encoding():
    assert encode("000000000010") == "000000000001100011101010"


def test_decoding():
    assert decode("000000000001100011101010") == "000000000010"
