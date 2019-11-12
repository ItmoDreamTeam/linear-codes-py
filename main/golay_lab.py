# for Golay code 24,12,8 which can find up to 3 errors

import numpy as np


def get_forming_poly():
    return np.array([1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1])


def get_poly_of_degree(degree):
    if degree == 16:
        return [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    if degree == 17:
        return [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


def get_remainder_16():
    g = get_forming_poly()

    return normalize_poly(np.polydiv(get_poly_of_degree(16), g)[1])


def get_remainder_17():
    g = get_forming_poly()

    return normalize_poly(np.polydiv(get_poly_of_degree(17), g)[1])


def encode_golay(message):
    if len(message) > 12:
        return 0

    message = np.array(message)
    g = get_forming_poly()

    return normalize_poly(np.polymul(g, message))


def normalize_poly(polynom):
    result = []

    for x in np.nditer(polynom):
        if abs(x) % 2 == 0:
            x = 0
            result.append(x)
        elif abs(x) % 2 == 1:
            x = 1
            result.append(x)
        else:
            result.append(x)

    return result


def get_weight(syndrome):
    weight = 0

    for bit in list(syndrome):
        if bit:
            weight += 1

    return weight


def get_syndrome(message):
    g = get_forming_poly()

    return normalize_poly(np.polydiv(message, g)[1])


def get_syndrome_16(syndrome):
    g = get_forming_poly()
    remainder = get_remainder_16()

    return normalize_poly(np.polyadd(syndrome, remainder))


def get_syndrome_17(syndrome):
    g = get_forming_poly()
    remainder = get_remainder_17()

    return normalize_poly(np.polyadd(syndrome, remainder))


def decode_golay(received_message):
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

    code_word = normalize_poly(np.polyadd(received_message, errors))
    code_word = np.roll(code_word, -shift)

    return code_word
