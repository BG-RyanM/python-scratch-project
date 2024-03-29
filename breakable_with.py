from contextlib import contextmanager

"""
Notes:

Demonstrates:
1. How to create a resource that can be used with Python 'with' operator, e.g.:

    with my_resource() as name:
        ...

2. A method for breaking out of 'with' blocks, not unlike how `break` works for
    for/with loops.
"""


@contextmanager
def dumb_resource():
    print("--- acquiring ---")
    try:
        print("--- using ---")
        yield "dumb"
    except Exception as e:
        print(f"I got an exception {e}")
        raise e
    finally:
        print("--- releasing ---")


print("\n=============== Test One ===============")

try:
    with dumb_resource() as name:
        print("Dumb resource test!! Got:", name)
        raise ValueError
except ValueError:
    pass

print("\n=============== Test Two ===============")


class BreakoutException(Exception):
    pass


@contextmanager
def breakout_resource(withable_generator):
    try:
        with withable_generator as resource:
            yield resource
    except BreakoutException:
        print("Got breakout exception")
    except Exception:
        print("Got some other exception")
        raise


with breakout_resource(dumb_resource()):
    print("Breakable resource test!!")
    raise BreakoutException
print("Onward...")
