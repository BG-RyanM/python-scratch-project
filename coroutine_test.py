from tornado.gen import (
    sleep as tornado_sleep,
    Return,
    coroutine,
)
from concurrent.futures import Future
import time
import asyncio

# Tests involving the use of coroutines. Python3 provides async/await, but sometimes we use
# coroutines for backwards compatibility

# This is the coroutine version of an async function. There is no await in it. Notice
# the use of raise Return()
@coroutine
def get_x():
    yield tornado_sleep(0.5)
    raise Return(10)


@coroutine
def do_test1():
    print("getting x...")
    x = yield get_x()
    print("x is", x)
    raise Return(True)


# Helper class
class FutureTester:
    def __init__(self):
        self._future = Future()

    @property
    def future(self):
        return self._future

    async def do_task(self):
        await asyncio.sleep(5.0)
        self._future.set_result(77)


# Testing how to wait on a future without using await
@coroutine
def do_test2(future_tester):
    print("waiting...")
    # GOOD
    while not future_tester.future.done():
        yield tornado_sleep(0.5)
    # BAD
    # yield future_tester.future.done()
    print("done!")


@coroutine
def inner_coroutine():
    yield tornado_sleep(0.5)
    raise Return(5)


@coroutine
def outer_coroutine():
    result = yield inner_coroutine()
    raise Return(result + 1)


async def main():
    print("Test One")
    fut = do_test1()
    await fut

    print("Test Two")
    future_tester = FutureTester()
    asyncio.create_task(future_tester.do_task())
    fut = do_test2(future_tester)
    await fut

    print("Test Three")
    fut = outer_coroutine()
    await fut
    # should be 6
    print("result:", fut.result())


asyncio.run(main())
