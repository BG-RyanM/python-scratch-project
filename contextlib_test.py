import asyncio
from contextlib import asynccontextmanager
from typing import Optional


"""
Code that demonstrates use of contextlib for creating a function that can be used with
Python's 'async with`. Also demonstrates a helper function that waits on an asyncio Lock,
but with a timeout. 
"""

class LockTimeoutException(Exception):
    """
    Raised if a wait for a lock times out
    """


@asynccontextmanager
async def wait_for_lock_with_timeout(
    lock: asyncio.Lock, timeout: Optional[float] = None
):
    """
    Waits for a lock to be acquired, but times out after a while.
    :param lock: the asyncio lock
    :param timeout: how many seconds to wait before raising exception, None if no timeout
    :raises: LockTimeoutException
    """
    lock_task = asyncio.create_task(lock.acquire())

    done, pending = await asyncio.wait(
        [lock_task], timeout=timeout, return_when=asyncio.ALL_COMPLETED
    )
    if lock_task in pending:
        raise LockTimeoutException

    try:
        yield lock
    finally:
        lock.release()


async def run_test():
    lock = asyncio.Lock()
    await lock.acquire()
    try:
        async with wait_for_lock_with_timeout(lock, 3.0):
            print("whee!")
    except LockTimeoutException as e:
        print("time out!")


asyncio.run(run_test())
