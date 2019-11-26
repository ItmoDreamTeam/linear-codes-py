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


def test_with_two_errors():
    source = "111010111001"
    encoded_codeword = encode(source)
    for _ in range(1000):
        corrupted = make_errors(encoded_codeword, 2)
        assert decode(corrupted) == source


def test_with_three_errors():
    source = "111010111001"
    encoded_codeword = encode(source)
    for _ in range(1000):
        corrupted = make_errors(encoded_codeword, 3)
        assert decode(corrupted) == source


def make_errors(codeword: str, errors_count: int) -> str:
    errors_indices = set()
    while len(errors_indices) < errors_count:
        errors_indices.add(random.randint(0, len(codeword) - 1))
    for error_index in errors_indices:
        corrupted_bit = '0' if codeword[error_index] == '1' else '1'
        codeword = codeword[:error_index] + corrupted_bit + codeword[error_index + 1:]
    return codeword
