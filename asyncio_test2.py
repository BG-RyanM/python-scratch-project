import asyncio
from copy import deepcopy


class EventWithData(asyncio.Event):
    """An extension of asyncio.Event that provides a settable data field"""

    def __init__(self, do_deepcopy=True):
        """
        :param do_deepcopy: Whether or not to make a deep copy of the internal
            data object before sharing with waiters. Defaults to True
        """
        self._do_deepcopy = do_deepcopy
        self._data = None
        super().__init__()

    async def wait(self):
        """
        Functions identically similar to asyncio.Event.wait(), except
        returns the contents of self._data after await completes

        :returns: data stored in the object when set()
        """
        await super().wait()
        if self._do_deepcopy:
            return deepcopy(self._data)
        return self._data

    def get(self):
        """
        Gets the data corresponding to this event

        :return: The data that should be stored within this event to be sent to any
                 waiters, if any
        :rtype:  Any
        """
        return self._data

    def set(self, data=None):
        """
        Sets the event, similar to asyncio.Event.set() along with the
        provided data.

        :param data: The data that should be stored within this event
            to be sent to any waiters
        """
        self._data = data
        return super().set()

    def clear(self):
        """
        clears the event, similar to asyncio.Event.clear() along with any
        stored data
        """
        self._data = None
        return super().clear()


async def process(my_event: EventWithData):
    while True:
        try:
            count = await asyncio.wait_for(
                my_event.wait(), timeout=15.0
            )
        except asyncio.TimeoutError:
            print("Timeout")
            break
        print("got count", count)
        count -= 1
        if count == 0:
            print("**** clearing")
            my_event.clear()
            print("**** done")
        else:
            my_event.set(count)


async def do_test():
    my_event = EventWithData()
    process_task = asyncio.create_task(process(my_event))

    def increase_count():
        count = my_event.get()
        if count is None:
            count = 0
        my_event.set(count + 1)

    increase_count()
    await asyncio.sleep(4)
    increase_count()
    await asyncio.sleep(4)

    await process_task

asyncio.run(do_test())
