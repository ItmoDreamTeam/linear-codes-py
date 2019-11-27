from typing import *


def string_to_list(message: str) -> List[int]:
    return list(map(lambda bit: int(bit), message))


def list_to_string(message: List[int], size: int) -> str:
    representation = "".join(map(lambda bit: str(int(bit)), message))
    return "0" * (size - len(representation)) + representation


def normalize(polynomial) -> List[int]:
    return list(map(lambda e: abs(int(e)) % 2, polynomial))
