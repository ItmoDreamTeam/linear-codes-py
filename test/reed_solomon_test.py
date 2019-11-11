import pytest
import random
from main.reed_solomon import encoding_rs, decoding_rs

k = 12  # input message length


def test_encoding():
    for attempt in range(100):
        input_message = []
        for i in range(k):
            input_message.append(random.randint(0, 1))

        try:
            encoding_rs(input_message)
        except:
            pytest.fail()
