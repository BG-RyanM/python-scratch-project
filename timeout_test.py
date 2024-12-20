import asyncio


class MyClass:
    def __init__(self):
        self.my_var = 0

    def func_a(self):
        for x in range(10000000):
            self.my_var += 1
        print("run func_a", self.my_var)

    async def func_b(self):
        await asyncio.sleep(2.0)
        self.my_var += 1
        print("run func_b", self.my_var)

    async def do_it(self):
        async def _timeout_helper(the_func, timeout):
            is_coroutine = asyncio.iscoroutinefunction(the_func)

            async def _wrapper_sync():
                the_func()

            try:
                await asyncio.wait_for(
                    the_func() if is_coroutine else _wrapper_sync(), timeout=timeout
                )
            except asyncio.TimeoutError:
                print(f"Timed out while running {the_func}")
            except Exception as e:
                print(f"Unexpected exception {e}.")

        await _timeout_helper(self.func_a, timeout=4.0)
        await _timeout_helper(self.func_b, timeout=4.0)


async def main():
    instance = MyClass()
    await instance.do_it()


asyncio.run(main())
