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
    input = np.array(string_to_list(input_message))
    extended = np.polymul(input, [1, 0, 0, 0])
    result = np.polyadd(extended, np.polydiv(extended, G)[1])
    return list_to_string(normalize(result), n)


def decode(input_message: str) -> str:
    input = np.array(string_to_list(input_message))
    error_index = find_single_error_index(input)
    result = input[:k] if error_index < 0 else correct_single_error(input, error_index)[:k]
    return list_to_string(normalize(result), k)


### Private Functions ###

syndrome_to_error_index_map = {
    (0, 0, 1): 4,
    (0, 1, 0): 5,
    (0, 1, 1): 2,
    (1, 0, 0): 6,
    (1, 0, 1): 0,
    (1, 1, 0): 3,
    (1, 1, 1): 1,
}


def find_single_error_index(input):
    syndrome = normalize(np.polydiv(input, G)[1])
    if sum(syndrome) == 0: return -1
    return syndrome_to_error_index_map[
        syndrome[-1],
        0 if len(syndrome) < 2 else syndrome[-2],
        0 if len(syndrome) < 3 else syndrome[-3]
    ]


def correct_single_error(codeword: np.ndarray, error_index: int) -> np.ndarray:
    codeword[error_index] = 0 if codeword[error_index] == 1 else 1
    return codeword
