import random
import asyncio
from datetime import datetime, timedelta
from argparse import ArgumentParser
import yaml


async def custom_sleep(orig_time: float):
    await asyncio.sleep(orig_time / float(speed_up_rate))

def list_to_cs(lst):
    comma = False
    result = ""
    for i in lst:
        result = result + (", " if comma else "") + i
        comma = True
    return result


class Container(object):

    container_list = []

    def __init__(self, id):
        self.id = id
        self.creation_time = datetime.utcnow()
        self.was_kicked = False
        self.container_list.append(self)

    @staticmethod
    def print_outcome():
        kicked_containers = [container for container in Container.container_list if container.was_kicked]
        kicked_as_str = list_to_cs([str(container.id) for container in kicked_containers])
        success_count = len(Container.container_list) - len(kicked_containers)
        print(f"Successfully processed {success_count} out of {len(Container.container_list)} containers.")
        print(f"Kicked containers were: {kicked_as_str}")

class Orchestrator(object):

    max_containers = 7
    process_time = 15
    barcode_failure_rate = 5

    orchestrator_list = []
    last_container_routed = False

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
        self._arrival_time = 5

    @staticmethod
    async def run():
        for orch in Orchestrator.orchestrator_list:
            await orch.make_tasks()
        while True:
            if Orchestrator.all_done():
                break
            await custom_sleep(0.1)

    def get_score(self) -> int:
        total = len(self.expected_queue) + len(self.known_queue)
        return total if total < Orchestrator.max_containers else -1

    @staticmethod
    def all_done():
        for orch in Orchestrator.orchestrator_list:
            if not orch.is_done():
                return False
        return True

    def is_done(self) -> bool:
        return Orchestrator.last_container_routed and len(self._enroute_queue) == 0 and len(self._actual_queue) == 0

    def get_queues_as_str(self) -> str:
        ret_str = f"E=[{list_to_cs([str(x.id) for x in self.expected_queue])}] " + \
                  f"K=[{list_to_cs([str(x.id) for x in self.known_queue])}]"
        return ret_str

    async def add_container(self, container: Container):
        async with self._lock:
            self._enroute_queue.append(container)

    async def add_expected_container(self, container: Container):
        async with self._lock:
            self.expected_queue.append(container)

    async def make_tasks(self):
        self._arrival_task = asyncio.create_task(self._arrival_coro())
        self._process_task = asyncio.create_task(self._processing_coro())

    @property
    def arrival_time(self):
        return self._arrival_time

    @arrival_time.setter
    def arrival_time(self, val):
        self._arrival_time = val

    async def _arrival_coro(self):
        while True:
            if len(self._enroute_queue) > 0:
                # At least one container is enroute; find out if it's there yet.
                container = self._enroute_queue[0]
                time_remaining = self._arrival_time - (datetime.utcnow() - container.creation_time).total_seconds()
                if time_remaining > 0.0:
                    # We can sleep some more...
                    await custom_sleep(time_remaining)
                else:
                    # Container has had enough time to arrive; deal with it
                    async with self._lock:
                        new_arrival = self._enroute_queue.pop(0)
                        self._actual_queue.append(new_arrival)
                        self._handle_entrance_arrival(new_arrival)
            else:
                # Sleep for small amount of time to return control to other coroutines
                await custom_sleep(0.1)

    async def _processing_coro(self):
        while True:
            # If there a container at the pick station, process it
            if self._container_in_processing is not None:
                await custom_sleep(Orchestrator.process_time)
                self._container_in_processing = None
            if len(self._actual_queue) > 0:
                #print(f"*** processing wants lock for {self.id}")
                async with self._lock:
                    #print(f"*** processing got lock for {self.id}")
                    next_container = self._actual_queue.pop(0)
                    got_barcode = self._handle_pick_area_arrival(next_container)
                    self._container_in_processing = next_container if got_barcode else None
            else:
                # Sleep for small amount of time to return control to other coroutines
                await custom_sleep(0.1)

    def _handle_entrance_arrival(self, container: Container):
        if random.randrange(100) < Orchestrator.barcode_failure_rate:
            # Barcode wasn't read, so we can't do any bookkeeping
            return
        # Take container off the expected queue
        was_in_queue = self._remove_from_queue(self.expected_queue, container)
        # Add to known queue
        self.known_queue.append(container)
        if was_in_queue:
            print(f"cell {self.id}: container {container.id} arrival detected, queues are: {self.get_queues_as_str()}")
        else:
            print(f"cell {self.id}: WARNING, unexpected container {container.id} arrival "
                  f"detected, queues are: {self.get_queues_as_str()}")

    def _handle_pick_area_arrival(self, container: Container) -> bool:
        # Returns true if barcode was read successfully
        if random.randrange(100) < Orchestrator.barcode_failure_rate:
            # Barcode wasn't read
            print(f"cell {self.id}: WARNING, container {container.id} had no barcode, kicked")
            container.was_kicked = True
            return False
        # Take container off the known queue
        was_in_queue = self._remove_from_queue(self.known_queue, container)
        if not was_in_queue:
            print(f"cell {self.id}: WARNING, container {container.id} not in Known queue.")
        print(f"cell {self.id}: container {container.id} moves to processing area, "
              f"queues are: {self.get_queues_as_str()}")
        return True

    def _remove_from_queue(self, queue, item: Container) -> bool:
        # Returns True if successfully removed
        try:
            index = queue.index(item)
        except ValueError:
            return False
        # Want to also remove everything in queue ahead of item
        for i in range(index+1):
            queue.pop(0)
        return True


class Router(object):

    def __init__(self):
        self.total_containers = 100
        self._index = 0
        self._overall_arrival_period = 5
        self._misroute_rate = 2


    def load_params_from_yaml(self, filename: str):
        with open(filename, 'r') as file:
            config = yaml.safe_load(file)
        sim_settings = config["sim_settings"]
        Orchestrator.max_containers = sim_settings["max_containers_per_cell"]
        Orchestrator.process_time = sim_settings["cell_processing_time"]
        Orchestrator.barcode_failure_rate = sim_settings["barcode_failure_rate"]

        num_cells = sim_settings["num_cells"]
        for i in range(num_cells):
            orch = Orchestrator(i)
            Orchestrator.orchestrator_list.append(orch)
            orch.arrival_time = sim_settings["cell_arrival_time"] + i * sim_settings["cell_distance_penalty"]

        self._overall_arrival_period = sim_settings["overall_arrival_period"]
        self._misroute_rate = sim_settings["misroute_rate"]


    async def run(self):
        for n in range(self.total_containers):
            container_name = "BG_{}".format(self._index)
            self._index += 1
            orch = self.choose_cell()
            container = Container(container_name)
            if orch is None:
                print(f"Router: no destination for {container_name}")
                container.was_kicked = True
            else:
                print(f"Router: routing container {container_name} to cell {orch.id}")
                await orch.add_expected_container(container)
                # Should there be a misroute?
                if random.randrange(100) < self._misroute_rate:
                    # Yes
                    wrong_cell = self.choose_random_cell(orch)
                    await wrong_cell.add_container(container)
                else:
                    # No, container goes where expected
                    await orch.add_container(container)
            await custom_sleep(self._overall_arrival_period)
        print(f"Router: finished with all containers")
        Orchestrator.last_container_routed = True

    def choose_cell(self):
        best_orch = None
        best_score = 100000
        for orch in Orchestrator.orchestrator_list:
            score = orch.get_score()
            #print(f"*** score for cell {orch.id} is {score}")
            if score >= 0 and score < best_score:
                best_orch = orch
                best_score = score
        return best_orch

    def choose_random_cell(self, orch_to_skip: Orchestrator = None):
        options = [orch for orch in Orchestrator.orchestrator_list if orch is not orch_to_skip]
        return options[random.randrange(len(options))]

router = Router()
speed_up_rate = 1

async def run_all():
    tasks = [asyncio.create_task(router.run()), asyncio.create_task(Orchestrator.run())]
    await asyncio.wait(tasks, return_when=asyncio.ALL_COMPLETED)
    Container.print_outcome()

if __name__ == "__main__":
    parser = ArgumentParser(
        add_help=True,
        description="Simulation of Orchestrator and client routing systems",
    )

    parser.add_argument(
        "--config",
        type=str,
        required=True,
        help="The configuration YAML file",
    )

    parser.add_argument(
        "--containers",
        type=int,
        default=100,
        help="Total number of containers to process",
    )

    parser.add_argument(
        "--speed",
        type=int,
        default=1,
        help="Causes time to go X times faster",
    )

    args = parser.parse_args()
    router.load_params_from_yaml(args.config)
    router.total_containers = args.containers
    speed_up_rate = args.speed

    asyncio.run(run_all())
