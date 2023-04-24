"""
Notes:

Experiments with inheritance, both multiple and single.
"""


class BaseClassA:
    def __init__(self):
        pass

    def what_am_i(self):
        print("Am BaseClassA")


class BaseClassB:
    def __init__(self, a, b=1, c=2):
        self.a = a
        self.b = b
        self.c = c

    def test(self):
        print(f"test a={self.a}, b={self.b}, c={self.c}")


class Sub(BaseClassB, BaseClassA):
    def __init__(self, a, **kwargs):
        super().__init__(a, **kwargs)

    def what_am_i(self):
        print("Am BaseClassB")
        super(Sub, self).what_am_i()


sub = Sub(8, b=9, c=10)
sub.test()
sub.what_am_i()


class SimpleBase:
    def __init__(self):
        print("I am simple base")
        
    def special_func(self, x=1, y=2):
        print(f"special_func() reports {x}, {y}")


class MoreComplexChild(SimpleBase):
    def __init__(self):
        super(MoreComplexChild, self).__init__()
        print("I am more complex child")

    def extra(self):
        print("I am extra()")
        
    def special_func(self, x=3, y=4):
        super(MoreComplexChild, self).special_func(x)


def base_maker() -> SimpleBase:
    return SimpleBase()


def child_maker() -> SimpleBase:
    return MoreComplexChild()


base = base_maker()
if hasattr(base, "extra"):
    base.extra()
child = child_maker()
if hasattr(child, "extra"):
    child.extra()

base.special_func()
child.special_func()
