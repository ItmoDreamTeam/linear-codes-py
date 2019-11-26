"""
  Golay Code (n=23, k=12, d=8)
  It can find and correct up to t=3 errors
  `Reference <https://docplayer.ru/46500923-Dekodirovanie-koda-goleya-dz-ot-ivanova-chast-vtoraya.html>`_
"""

import numpy as np
from main.utils import *

n = 23
k = 12
G = [1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1]
x16 = [1] + [0] * 16
x17 = [1] + [0] * 17


### Public Functions ###

def encode(input: str) -> str:
    message = stringToList(input)
    result = np.polymul(G, message)
    return listToString(normalize(result), n)


def decode(input: str) -> str:
    codeword = stringToList(input)

    shift = 0
    while True:
        syndrome = compute_syndrome(codeword)
        syndrome_16 = compute_syndrome_16(syndrome)
        syndrome_17 = compute_syndrome_17(syndrome)

        if compute_weight(syndrome) <= 3:
            errors = syndrome
            break

        if compute_weight(syndrome_16) <= 2:
            errors = np.polyadd(x16, syndrome_16)
            break

        if compute_weight(syndrome_17) <= 2:
            errors = np.polyadd(x17, syndrome_17)
            break

        shift += 1
        codeword = np.roll(codeword, 1)

    codeword = normalize(np.polyadd(codeword, errors))
    codeword = np.roll(codeword, -shift)
    decoded_codeword = np.polydiv(codeword, G)[0]
    decoded_codeword = normalize(decoded_codeword[len(decoded_codeword) - k:])
    return listToString(decoded_codeword, k)


### Private Functions ###


def compute_syndrome(codeword):
    return normalize(np.polydiv(codeword, G)[1])


def compute_syndrome_16(initial_syndrome):
    remainder = np.polydiv(x16, G)[1]
    return normalize(np.polyadd(initial_syndrome, remainder))


def compute_syndrome_17(initial_syndrome):
    remainder = np.polydiv(x17, G)[1]
    return normalize(np.polyadd(initial_syndrome, remainder))


def compute_weight(syndrome):
    return sum(syndrome)
