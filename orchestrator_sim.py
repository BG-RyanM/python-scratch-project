import random
import asyncio
from datetime import datetime, timedelta

class Container(object):
    def __init__(self, id):
        self.id = id
        self.creation_time = datetime.utcnow()

class Orchestrator(object):

    MAX_CONTAINERS = 7
    ARRIVAL_TIME = 5
    PROCESS_TIME = 15

    def __init__(self, id: int):
        # Serve same functions as in RIS
        self.expected_queue = []
        self.known_queue = []
        # The containers that are REALLY enroute to this cell (the queues above may be unreliable)
        self._enroute_queue = []
        # The containers that are REALLY in line for processing
        self._actual_queue = []
        self._container_in_processing = None
        self.id = id
        self._lock = asyncio.Lock()
        self._arrival_task = None
        self._process_task = None

    def get_score(self) -> int:
        total = len(self.expected_queue) + len(self.known_queue)
        return total if total < Orchestrator.MAX_CONTAINERS else -1

    def get_queues_as_str(self) -> str:
        def _list_to_cs(lst):
            comma = False
            result = ""
            for i in lst:
                result = result + (", " if comma else "") + i
                comma = True
            return result
        ret_str = f"E=[{_list_to_cs([str(x.id) for x in self.expected_queue])}] " + \
                  f"K=[{_list_to_cs([str(x.id) for x in self.known_queue])}]"
        return ret_str

    async def add_container(self, container_id):
        async with self._lock:
            container = Container(container_id)
            self._enroute_queue.append(container)

    async def add_expected_container(self, container_id):
        async with self._lock:
            container = Container(container_id)
            self.expected_queue.append(container)

    async def make_tasks(self):
        self._arrival_task = asyncio.create_task(self._arrival_coro())
        self._process_task = asyncio.create_task(self._processing_coro())

    async def _arrival_coro(self):
        while True:
            if len(self._enroute_queue) > 0:
                # At least one container is enroute; find out if it's there yet.
                container = self._enroute_queue[0]
                time_remaining = Orchestrator.ARRIVAL_TIME - (datetime.utcnow() - container.creation_time).total_seconds()
                if time_remaining > 0.0:
                    # We can sleep some more...
                    await asyncio.sleep(time_remaining)
                else:
                    # Container has had enough time to arrive; deal with it
                    #print(f"*** arrival wants lock for {self.id}")
                    async with self._lock:
                        #print(f"*** arrival got lock for {self.id}")
                        new_arrival = self._enroute_queue.pop(0)
                        self._actual_queue.append(new_arrival)
                        self._handle_entrance_arrival(new_arrival)
                    #print(f"*** arrival for {self.id}")
            else:
                # Sleep for small amount of time to return control to other coroutines
                await asyncio.sleep(0.1)

    async def _processing_coro(self):
        while True:
            # If there a container at the pick station, process it
            if self._container_in_processing is not None:
                await asyncio.sleep(Orchestrator.PROCESS_TIME)
                self._container_in_processing = None
            if len(self._actual_queue) > 0:
                #print(f"*** processing wants lock for {self.id}")
                async with self._lock:
                    #print(f"*** processing got lock for {self.id}")
                    next_container = self._actual_queue.pop(0)
                    self._container_in_processing = next_container
                    self._handle_pick_area_arrival(next_container)
            else:
                # Sleep for small amount of time to return control to other coroutines
                await asyncio.sleep(0.1)

    def _handle_entrance_arrival(self, container: Container):
        # Take it off the expected queue
        self._remove_from_queue(self.expected_queue, container)
        # Add to known queue
        self.known_queue.append(container)
        print(f"cell {self.id}: container {container.id} arrival detected, queues are: {self.get_queues_as_str()}")

    def _handle_pick_area_arrival(self, container: Container):
        # Take it off the known queue
        self._remove_from_queue(self.known_queue, container)
        print(f"cell {self.id}: container {container.id} moves to pick area, queues are: {self.get_queues_as_str()}")

    def _remove_from_queue(self, queue, item: Container):
        try:
            index = queue.index(item)
        except ValueError:
            return
        for i in range(index+1):
            queue.pop(0)

    @staticmethod
    async def run():
        for orch in orchestrator_list:
            await orch.make_tasks()
        await asyncio.sleep(100000)


class Router(object):

    def __init__(self):
        self._index = 0

    async def run(self):
        while True:
            container_name = "BG_{}".format(self._index)
            self._index += 1
            orch = self.choose_cell()
            if orch is None:
                print(f"Router: no destination for {container_name}")
            else:
                print(f"Router: routing container {container_name} to cell {orch.id}")
                await orch.add_expected_container(container_name)
                await orch.add_container(container_name)
            await asyncio.sleep(5.0)

    def choose_cell(self):
        best_orch = None
        best_score = 100000
        for orch in orchestrator_list:
            score = orch.get_score()
            #print(f"*** score for cell {orch.id} is {score}")
            if score >= 0 and score < best_score:
                best_orch = orch
                best_score = score
        return best_orch

orchestrator_list = [Orchestrator(i) for i in range(5)]
router = Router()


async def run_all():
    tasks = [asyncio.create_task(router.run()), asyncio.create_task(Orchestrator.run())]
    await asyncio.wait(tasks, return_when=asyncio.ALL_COMPLETED)

asyncio.run(run_all())
