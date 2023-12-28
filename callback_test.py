from typing import Callable
from functools import partial

print("Part One\n===============================================")


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

print("Part Two\n===============================================")


class MyClassA:
    def __init__(self):
        pass

    def handler(self, x):
        print("Got to handler, x is", x)


class MyClassB:
    def __init__(self):
        self._callback = None

    def set_callback(self, func):
        self._callback = func

    def run_callback(self, val):
        print("Running callback")
        self._callback(val)


my_a = MyClassA()
my_b = MyClassB()

my_b.set_callback(partial(MyClassA.handler, my_a))
my_b.run_callback(6)
