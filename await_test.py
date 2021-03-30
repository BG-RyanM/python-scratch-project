import random
import asyncio

# Test of asyncio gather() combined with a timeout feauture

async def test_func(info):
    print(">", info)
    await asyncio.sleep(random.randrange(5))
    print("<", info)
    return info

async def run_tasks():
    task_list = []
    for i in range(10):
        task = asyncio.create_task(test_func("test "+str(i)))
        task_list.append(task)

    results = []
    try:
        gather_task = asyncio.gather(*task_list, return_exceptions=True)
        results = await asyncio.wait_for(gather_task, 4)
    except asyncio.TimeoutError:
        print("out of time!!!")

    try:
        results = await gather_task
    except asyncio.CancelledError:
        print("gather cancelled")
        for t in task_list:
            if t.cancelled():
                results.append(None)
            else:
                results.append(t.result())

    return results

async def run_test():
    results = await run_tasks()
    print("results:", results)

    def _do_nothing():
        return None

    nothing_task = asyncio.create_task(_do_nothing())

asyncio.run(run_test())