import asyncio


async def my_func() -> bool:
    print("hi!!!")
    return True


async def main():
    my_future = await my_func()
    print("Type is:", type(my_future))
    my_future = my_func()
    print("Type is:", type(my_future))
    await my_future


asyncio.run(main())
