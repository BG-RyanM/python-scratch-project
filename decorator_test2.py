import asyncio

"""
Demonstrates how to make a deocorator that you can use with @.
"""


def my_decorator(start_word: str = "start", end_word: str = "end"):
    def my_decorator_inner(func):
        async def inner(*args, **kwargs):
            print(f"--- {start_word} ---")
            await func(*args, **kwargs)
            print(f"--- {end_word} ---")

        return inner

    return my_decorator_inner


class MyClass(object):
    def __int__(self):
        pass

    @my_decorator()
    async def do_stuff(self, some_string: str):
        print("waiting...")
        await asyncio.sleep(2.0)
        print("the string is", some_string)


async def main():
    obj = MyClass()
    await obj.do_stuff("cat")
    print(f"MyClass type is {type(MyClass)}")


asyncio.run(main())
