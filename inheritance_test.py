"""
Demonstration of simple inheritence in Python.
"""

class Animal:
    def __init__(self, *args, **kwargs):
        print(f"I am an animal\nargs={args}\nkwargs={kwargs}")


class Cow(Animal):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if kwargs.get("dairy"):
            print("I am a dairy cow")


animal = Animal(1, 2, horns=True, tail=False)
cow = Cow(3, 4, horns=True, tail=False)
