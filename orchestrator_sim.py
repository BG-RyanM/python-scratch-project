import random
import asyncio

class Orchestrator(object):

    MAX_CONTAINERS = 7
    ARRIVAL_TIME = 5
    PROCESS_TIME = 15

    def __init__(self, id: int):
        self.expected_queue = []
        self.known_queue = []
        self._enroute_queue = []
        self._actual_queue = []
        self.id = id
        self._lock = asyncio.Lock()
        self._arrival_task = None
        self._process_task = None

    def get_score(self):
        total = len(self.expected_queue) + len(self.known_queue)
        return total if total < Orchestrator.MAX_CONTAINERS else -1

    async def add_container(self, container):
        async with self._lock:
            self._enroute_queue.append(container)

    async def add_expected_container(self, container):
        async with self._lock:
            self.expected_queue.append(container)

    async def update(self):
        async with self._lock:
            if self._arrival_task is None:
                self._arrival_task = asyncio.create_task(asyncio.sleep(Orchestrator.ARRIVAL_TIME))
            elif self._arrival_task.done():
                if len(self._enroute_queue) > 0:
                    new_arrival = self._enroute_queue.pop(0)
                    self._actual_queue.append(new_arrival)
                    self._handle_arrival(new_arrival)
                self._arrival_task = None

            if self._process_task is None:
                self._process_task = asyncio.create_task(asyncio.sleep(Orchestrator.PROCESS_TIME))
            elif self._process_task.done():
                if len(self._actual_queue) > 0:
                    processed = self._actual_queue.pop(0)
                    self._handle_processed(processed)
                self._process_task = None

    def _handle_arrival(self, container):
        print(f"cell {self.id}: container {container} arrival detected")
        # Take it off the expected queue
        self._remove_from_queue(self.expected_queue, container)
        # Add to known queue
        self.known_queue.append(container)

    def _handle_processed(self, container):
        print(f"cell {self.id}: container {container} processed")
        # Take it off the known queue
        self._remove_from_queue(self.known_queue, container)

    def _remove_from_queue(self, queue, item):
        try:
            index = queue.index(item)
        except ValueError:
            return
        for i in range(index+1):
            queue.pop(0)

    @staticmethod
    async def run():
        while True:
            for orch in orchestrator_list:
                await orch.update()
            await asyncio.sleep(1)


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
    tasks = [asyncio.create_task(Orchestrator.run()), asyncio.create_task(router.run())]
    await asyncio.wait(tasks, return_when=asyncio.ALL_COMPLETED)

asyncio.run(run_all())
