import asyncio
import math


def count_long_time():
    print("count long time begins")
    x = 0
    for i in range(10000000):
        x += 1
        a = math.sqrt(float(i)) * math.cos(x)
    print("count long time ends")


async def do_it():
    async def count_wrapper():
        count_long_time()

    print("making count wrapper")
    count_task = asyncio.create_task(count_wrapper())
    print("making count wrapper is done")


count_task = asyncio.run(do_it())
