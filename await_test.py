import random
import asyncio

# Test of asyncio gather() combined with a timeout feature

# A function that sleeps for a random amount of time and might raise an exception
async def test_func(info, raises_exception):
    print(">", info)
    await asyncio.sleep(random.randrange(5))
    if raises_exception:
        x = 7
        bad = x / 0
    print("<", info)
    return info

# Returns list where each entry contains results of task or whatever Exception was raised
async def run_tasks(timeout):
    task_list = []
    for i in range(10):
        raises_exception = (random.randrange(3) == 0)
        task = asyncio.create_task(test_func("test "+str(i), raises_exception))
        task_list.append(task)

    results = []
    try:
        # return_exceptions means exceptions will be returned as objects into
        # results list, rather than thrown right away. This is helpful because
        # we want all tasks to have a chance to finish. If result() is called
        # on task, exception will be raised.
        gather_task = asyncio.gather(*task_list, return_exceptions=True)
        results = await asyncio.wait_for(gather_task, timeout)
    except asyncio.TimeoutError:
        print("out of time!!!")

    try:
        results = await gather_task
    except asyncio.CancelledError:
        print("gather cancelled")
        for t in task_list:
            if t.cancelled():
                results.append(asyncio.TimeoutError())
            else:
                try:
                    t.result()
                except Exception as e:
                    results.append(e)
                else:
                    results.append(t.result())

    return results

async def run_test():
    results = await run_tasks(timeout=3)
    print("Results:")
    for i,r in enumerate(results):
        if isinstance(r, Exception):
            print(f"{i}: is exception {type(r)}")
        else:
            print(f"{i}: {r}")

    async def _do_nothing():
        return None

    nothing_task = asyncio.create_task(_do_nothing())

asyncio.run(run_test())