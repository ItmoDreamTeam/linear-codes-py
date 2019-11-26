import pytest
import random
from main.golay import encode, decode


def test_without_errors_1():
    assert encode("000000000010") == "00000000001100011101010"
    assert decode("00000000001100011101010") == "000000000010"


def test_without_errors_2():
    assert encode("100011100110") == "11001110010100001011110"
    assert decode("11001110010100001011110") == "100011100110"


def test_with_single_error():
    source = "011100101001"
    encoded_codeword = encode(source)
    for error_index in range(len(encoded_codeword)):
        corrupted_bit = '0' if encoded_codeword[error_index] == '1' else '1'
        corrupted = encoded_codeword[:error_index] + corrupted_bit + encoded_codeword[error_index + 1:]
        assert decode(corrupted) == source
