import attr
from typing import List
from functools import partial


class Obj:
    def __init__(self, **kwargs):
        """
        Each keyword argument becomes a member of the instance
        :param kwargs: dictionary of keyword arguments
        """
        for k, v in kwargs.items():
            super().__setattr__(k, v)

    def add_do_methods(self, names: List[str]):
        for name in names:
            g = partial(self.do, name)

            self.__setattr__(f"do_{name}", g)

    def do(self, name, param):
        print(f"I am doing {name} with param {param}")

    def __getattr__(self, name):
        return None


o = Obj(w=0)
o.add_do_methods(["walk", "run"])

o.x = 1
o.y = 2
o.do_walk(6)
o.do_run(7)

print(o.w)
print(o.x)
print(o.y)
print(o.z)

period_str = "me.you.walk"
simplified_str = period_str.split(".")[-1]
print("simplified string is", simplified_str)
