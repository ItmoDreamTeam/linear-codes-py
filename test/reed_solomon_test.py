import pytest
import random
from main.reed_solomon import encoding_bch, decoding_bch

k = 12  # input message length


def test_encoding():
    for attempt in range(100):
        input_message = []
        for i in range(k):
            input_message.append(random.randint(0, 1))

        try:
            encoding_bch(input_message)
        except:
            pytest.fail()
