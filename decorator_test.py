"""
Demonstrates how Python decorators work, without making use of @.
"""


def get_string_as_upper(my_string: str):
    return my_string.upper()


def add_brackets(func):
    # Think of this as a factory function, returning the wrapper function
    def _wrapper(my_string):
        string = func(my_string)
        return "[" + string + "]"

    return _wrapper


get_string_as_upper = add_brackets(get_string_as_upper)

print("test:", get_string_as_upper("hello"))


def add_plus_decorator(func):
    def _wrapper(obj):
        return func(obj) + "+"

    return _wrapper


class MyClass(object):
    def __init__(self, name):
        self._my_name = name

    def test(self):
        return f"{self._my_name} says hi"

    test = add_plus_decorator(test)


my_thing = MyClass("George")
print(my_thing.test())
