from typing import *


def stringToList(message: str) -> List[int]:
    return list(map(lambda bit: int(bit), message))


def listToString(message: List[int]) -> str:
    return "".join(map(lambda bit: str(bit), message))
