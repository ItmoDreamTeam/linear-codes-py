import numpy as np
from main.utils import *

n = 7
r = 3
k = n - r
G = [1, 0, 1, 1]  # G = x^3 + x + 1


### Public Functions ###

def encode(input_message: str) -> str:
    """
    :return: A * x^r + (A * x^r) mod G, where A is input codeword
    """
    input = np.array(stringToList(input_message))
    extended = np.polymul(input, [1, 0, 0, 0])
    result = np.polyadd(extended, np.polydiv(extended, G)[1])
    return listToString(normalize_poly(result), n)


def decode(input_message: str) -> str:
    input = np.array(stringToList(input_message))
    result = input
    return listToString(normalize_poly(result), k)


### Private Functions ###

def get_field_poly():
    return np.array([1, 0, 1, 1])


def normalize_poly(polynomial):
    result = []

    for x in np.nditer(polynomial):
        if abs(x) % 2 == 0:
            x = 0
            result.append(x)
        elif abs(x) % 2 == 1:
            x = 1
            result.append(x)
        else:
            result.append(x)

    return result


def code_word_check(codeword):
    h = np.array([
        [1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1],
        [0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0],
        [0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0],
        [0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1],

        [1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1],
        [0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1],
        [0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1],
        [0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1],

        [1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1],
        [0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1],
        [0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ])

    try:
        for x in np.nditer(np.matmul(h, (np.flip(codeword)).transpose())):
            if x % 2 != 0:
                return 0
            return 1
    except ZeroDivisionError:
        return 0


def get_field(degree):
    if degree == 4:
        a1 = np.array([0, 0, 0, 1])  # 1
        a2 = np.array([0, 0, 1, 0])  # 2
        a3 = np.array([0, 1, 0, 0])  # 4
        a4 = np.array([0, 0, 1, 1])  # 3
        a5 = np.array([0, 1, 1, 0])  # 6
        a6 = np.array([1, 1, 0, 0])  # 12
        a7 = np.array([1, 0, 1, 1])  # 11
        a8 = np.array([0, 1, 0, 1])  # 5
        a9 = np.array([1, 0, 1, 0])  # 10
        a10 = np.array([0, 1, 1, 1])  # 7
        a11 = np.array([1, 1, 1, 0])  # 14
        a12 = np.array([1, 1, 1, 1])  # 15
        a13 = np.array([1, 1, 0, 1])  # 13
        a14 = np.array([1, 0, 0, 1])  # 9
        a15 = np.array([0, 0, 0, 1])  # 1

        return [a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14, a15]
    elif degree == 3:
        a0 = np.array([0, 0, 1])
        a1 = np.array([0, 1, 0])
        a2 = np.array([1, 0, 0])
        a3 = np.array([0, 1, 1])
        a4 = np.array([1, 1, 0])
        a5 = np.array([1, 1, 1])
        a6 = np.array([1, 0, 1])
        return [a0, a1, a2, a3, a4, a5, a6]


def get_syndrome(received_message):
    return np.array(normalize_poly(mod_field(received_message)))


def mod_field(polynomial):
    return np.polydiv(polynomial, get_field_poly())[1]


def decode_bch(received_message, field_degree):
    r = np.array(received_message)
    s = get_syndrome(r)
    field = get_field(field_degree)
    i = 0

    for value in field:
        if np.array_equal(s, np.array(value)):
            return i
        i += 1
    return 0
