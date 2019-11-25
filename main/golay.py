"""
  Golay code [24, 12, 8]
  It can find and correct up to 3 errors
"""

import numpy as np
from main.utils import *

n = 24
k = 12


### Public Functions ###

def encode(input: str) -> str:
    message = np.array(stringToList(input))
    g = get_forming_poly()
    result = normalize(np.polymul(g, message))
    return listToString(result, n)


def decode(input: str) -> str:
    received_message = stringToList(input)
    shift = 0

    while True:
        syndrome = get_syndrome(received_message)
        syndrome_16 = get_syndrome_16(syndrome)
        syndrome_17 = get_syndrome_17(syndrome)

        weight = get_weight(syndrome)

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
        received_message = np.roll(received_message, 1)

    code_word = normalize(np.polyadd(received_message, errors))
    code_word = np.roll(code_word, -shift)

    return listToString(code_word, k)


### Private Functions ###

def get_forming_poly():
    return np.array([1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1])


def get_poly_of_degree(degree):
    if degree == 16:
        return [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    if degree == 17:
        return [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


def get_remainder_16():
    g = get_forming_poly()
    return normalize(np.polydiv(get_poly_of_degree(16), g)[1])


def get_remainder_17():
    g = get_forming_poly()
    return normalize(np.polydiv(get_poly_of_degree(17), g)[1])


def get_weight(syndrome):
    weight = 0
    for bit in list(syndrome):
        if bit:
            weight += 1
    return weight


def get_syndrome(message):
    g = get_forming_poly()
    return normalize(np.polydiv(message, g)[1])


def get_syndrome_16(syndrome):
    g = get_forming_poly()
    remainder = get_remainder_16()
    return normalize(np.polyadd(syndrome, remainder))


def get_syndrome_17(syndrome):
    g = get_forming_poly()
    remainder = get_remainder_17()
    return normalize(np.polyadd(syndrome, remainder))
