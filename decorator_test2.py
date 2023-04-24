import asyncio

"""
Demonstrates how to make a deocorator that you can use with @.
"""


def my_decorator(func):
    async def inner(*args, **kwargs):
        print("--- start ---")
        await func(*args, **kwargs)
        print("--- end ---")

    return inner


class MyClass(object):
    def __int__(self):
        pass

    @my_decorator
    async def do_stuff(self, some_string: str):
        print("waiting...")
        await asyncio.sleep(2.0)
        print("the string is", some_string)


async def main():
    obj = MyClass()
    await obj.do_stuff("cat")


asyncio.run(main())
