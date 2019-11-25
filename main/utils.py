from typing import *


def stringToList(message: str) -> List[int]:
    return list(map(lambda bit: int(bit), message))


def listToString(message: List[int], size: int) -> str:
    representation = "".join(map(lambda bit: str(int(bit)), message))
    return "0" * (size - len(representation)) + representation
