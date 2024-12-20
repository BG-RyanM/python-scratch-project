from typing import Tuple


def return_two_values() -> Tuple[bool, int]:
    return True, 3


def return_three_values() -> Tuple[bool, int, str]:
    return False, 7, "hi"


ret1, *ret2, ret3 = return_two_values()
print(f"return_two_values() returns {ret1}, {ret2}, {ret3}")
ret1, *ret2, ret3 = return_three_values()
print(f"return_three_values() returns {ret1}, {ret2}, {ret3}")
