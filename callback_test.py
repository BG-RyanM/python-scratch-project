from typing import Callable


def func_a(callback: Callable[[int], None]):
    print("in func_a()")
    callback(6)


def func_b():
    y = 0
    def my_callback(x: int):
        nonlocal y
        print("in my_callback(), x is", x)
        y = x

    func_a(my_callback)
    print("y =", y)

func_b()