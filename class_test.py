from typing import Dict

"""
Notes:

Simple experiments with classes and a factory method that can make classes of an
arbitrary type.
"""


class Dumb:
    def __init__(self, x, y):
        print("x, y =", x, ",", y)


def make_thing(the_class: type, params: Dict):
    return the_class(**params)


# params_dict = {"x": 2, "y": 3, "z": 4}
params_dict = {"x": 2, "y": 3}
make_thing(Dumb, params_dict)


class Simple:
    pass

    def set_name(self, name):
        self.name = name


simple = Simple()
simple.set_name("MyName")

print("name for simple object is", simple.name)

Dumb.z = 4
dumb2 = Dumb(1, 2)
print("dumb2.z is", dumb2.z)
