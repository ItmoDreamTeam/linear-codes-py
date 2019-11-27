import pytest
import random
from main.bch import encode, decode


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


def test_encoding_and_decoding_without_errors():
    failures = []
    iterate_over_all_codewords(lambda codeword: failures.append(decode(encode(codeword)) != codeword))
    if any(failures): pytest.fail()


def test_encoding_and_decoding_with_single_error():
    failures = []
    iterate_over_all_codewords(
        lambda codeword: failures.append(decode(make_single_error(encode(codeword))) != codeword)
    )
    if any(failures): pytest.fail()


def make_single_error(codeword: str) -> str:
    error_index = random.randint(0, len(codeword) - 1)
    new_bit_value = '1' if codeword[error_index] == '0' else '0'
    return codeword[:error_index] + new_bit_value + codeword[error_index + 1:]


def iterate_over_all_codewords(action):
    for a1 in range(2):
        for a2 in range(2):
            for a3 in range(2):
                for a4 in range(2):
                    codeword = str(a1) + str(a2) + str(a3) + str(a4)
                    action(codeword)
