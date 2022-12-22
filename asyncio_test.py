import asyncio
from random import randrange
from typing import Any, Callable


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


#asyncio.run(run_test())


def run_async_func(done_callback: Callable[[bool, Any], Any]):
    # func: Callable[[], Awaitable[Any]], done_callback: Callable[[Any, bool], Any], timeout: Optional[float] = None
    """
    Launches a function asynchronously,

    :param func: the function to run asynchronously (must be an async function)
    :param done_callback: gets called when function completes or times out.
        Parameters: [Whatever 'func' returns, True if completed without timeout]
    :param timeout: how many seconds to time out after, None for no timeout
    """
    try:
        loop = asyncio.get_running_loop()
        print("Got loop!")
    except RuntimeError:  # 'RuntimeError: There is no current event loop...'
        loop = None
        print("No loop!")

    async def _the_func():
        print("running the function")
        await asyncio.sleep(randrange(6))
        print("success!")
        return 77

    async def _func_wrapper():
        # Returns (True if succeeded without timeout, the result of 'func')
        tsk = loop.create_task(_the_func())
        done, pending = await asyncio.wait([tsk], timeout=3, return_when=asyncio.FIRST_COMPLETED)
        if tsk in pending:
            return False, None
        return True, tsk.result()

    def _handle_done(t):
        tup = t.result()
        print(f"Am done, yay! Result {tup}")
        done_callback(*tup)

    if loop and loop.is_running():
        print('Async event loop already running. Adding coroutine to the event loop.')
        main_task = loop.create_task(_func_wrapper())
        # ^-- https://docs.python.org/3/library/asyncio-task.html#task-object
        # Optionally, a callback function can be executed when the coroutine completes
        main_task.add_done_callback(_handle_done)


async def second_test():

    def _done(success, result):
        print("got into done callback")

    run_async_func(_done)
    await asyncio.sleep(6.5)

print("\n----------------------------------------\n")

#asyncio.run(second_test())

timer_task = None

def setup_timer():
    async def _do_it():
        await asyncio.sleep(3)
        print("timer expired")
        setup_timer()

    global timer_task
    timer_task = asyncio.create_task(_do_it())

async def third_test():
    setup_timer()
    await asyncio.sleep(15)

asyncio.run(third_test())