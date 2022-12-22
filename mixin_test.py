from abc import ABC

class MyBase(ABC):
    def __init__(self, a=0, b=1):
        self._a = a
        self._b = b
        print(f"MyBase init'd with a={a}, b={b}")

class Mixin(MyBase):
    def __init__(self, params: dict):
        print("Mixin constructor")
        # Calls constructor for Other (the mixed-in class)
        super(MyBase, self).__init__(**params)
        # Calls constructor for MyBase
        super().__init__(a=params["a"], b=params["b"])

class Other:
    def __init__(self, a=0, b=0, x=0, y=0):
        self._x = x
        self._y = y
        print(f"Other init'd with x={x}, y={y}")

class MultiClass(Mixin, Other):
    pass

params = {"a": 1, "b": 2, "x": 3, "y": 4}
multi = MultiClass(params)