"""
  Golay Code (n=23, k=12, d=8)
  It can find and correct up to t=3 errors
"""

import numpy as np
from main.utils import *

n = 23
k = 12
G = [1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1]


### Public Functions ###

def encode(input: str) -> str:
    message = stringToList(input)
    result = np.polymul(G, message)
    return listToString(normalize(result), n)


def decode(input: str) -> str:
    codeword = stringToList(input)

    shift = 0
    while True:
        syndrome = get_syndrome(codeword)
        syndrome_16 = get_syndrome_16(syndrome)
        syndrome_17 = get_syndrome_17(syndrome)

        if get_weight(syndrome) <= 3:
            errors = syndrome
            break

        if get_weight(syndrome_16) <= 2:
            errors = np.polyadd(get_poly_of_degree(16), syndrome_16)
            break

        if get_weight(syndrome_17) <= 2:
            errors = np.polyadd(get_poly_of_degree(17), syndrome_17)
            break

        shift += 1
        codeword = np.roll(codeword, 1)

    codeword = normalize(np.polyadd(codeword, errors))
    codeword = np.roll(codeword, -shift)
    decoded_codeword = np.polydiv(codeword, G)[0]
    decoded_codeword = normalize(decoded_codeword[len(decoded_codeword) - k:])
    return listToString(decoded_codeword, k)


### Private Functions ###


def get_syndrome(message):
    return normalize(np.polydiv(message, G)[1])


def get_syndrome_16(syndrome):
    remainder = get_remainder_16()
    return normalize(np.polyadd(syndrome, remainder))


def get_remainder_16():
    return normalize(np.polydiv(get_poly_of_degree(16), G)[1])


def get_syndrome_17(syndrome):
    remainder = get_remainder_17()
    return normalize(np.polyadd(syndrome, remainder))


def get_remainder_17():
    return normalize(np.polydiv(get_poly_of_degree(17), G)[1])


def get_weight(syndrome):
    return sum(syndrome)


def get_poly_of_degree(degree):
    if degree == 16:
        return [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    if degree == 17:
        return [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
