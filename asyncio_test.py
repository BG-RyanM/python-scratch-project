import asyncio

class MyException(Exception):
    pass

async def func1(do_exception):
    await asyncio.sleep(4.0)
    if do_exception:
        raise MyException
    return "func1 done"

async def func2():
    await asyncio.sleep(7.0)
    return "func2 done"

async def run_test():
    task1 = asyncio.create_task(func1(True))
    task2 = asyncio.create_task(func2())

    try:
        done, not_done = await asyncio.wait({task1, task2}, return_when=asyncio.FIRST_COMPLETED)
    except MyException:
        print("I got MyException!!")

    if task1 in done:
        try:
            result = task1.result()
        except MyException:
            print("MyException came through in result")

asyncio.run(run_test())