import pytest
import random
from main.reed_solomon import encode, decode


def test_encoding():
    assert encode("0000") == "0000000"
    assert encode("0001") == "0001011"
    assert encode("0010") == "0010110"
    assert encode("0011") == "0011101"
    assert encode("0100") == "0100111"
    assert encode("0101") == "0101100"
    assert encode("0110") == "0110001"
    assert encode("0111") == "0111010"
    assert encode("1000") == "1000101"
    assert encode("1001") == "1001110"
    assert encode("1010") == "1010011"
    assert encode("1011") == "1011000"
    assert encode("1100") == "1100010"
    assert encode("1101") == "1101001"
    assert encode("1110") == "1110100"
    assert encode("1111") == "1111111"
