import pytest
import random
from main.golay import encode_golay, decode_golay


def test_encoding():
    assert encode_golay("0000") == "0000000"
