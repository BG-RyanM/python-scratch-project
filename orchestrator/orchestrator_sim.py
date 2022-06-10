import random
import asyncio
from datetime_test import datetime, timedelta
from argparse import ArgumentParser
import yaml


async def custom_sleep(orig_time: float):
    await asyncio.sleep(orig_time / float(speed_up_rate))

def list_to_cs(lst):
    # Converts a list of strings to a single string with commas between items
    comma = False
    result = ""
    for i in lst:
        result = result + (", " if comma else "") + i
        comma = True
    return result


class Container(object):
    """
    Represents a simulated container
    """

    container_list = []

    def __init__(self, id):
        # actual ID of container
        self.id = id
        # what barcode scanner and or queue analysis thinks the container is
        self.reported_id = None
        self.creation_time = datetime.utcnow()
        self.was_kicked = False
        self.container_list.append(self)

    @staticmethod
    def print_outcome():
        """
        Prints the overall results with all the containers processed
        """
        kicked_containers = [container for container in Container.container_list if container.was_kicked]
        kicked_as_str = list_to_cs([str(container.id) for container in kicked_containers])
        success_count = len(Container.container_list) - len(kicked_containers)
        mislabeled_containers = [container for container in Container.container_list
                                 if (container.id != container.reported_id and container.reported_id is not None)]
        mislabeled_str = list_to_cs([f"{container.id} read as {container.reported_id}" for container in mislabeled_containers])
        print(f"Successfully processed {success_count} out of {len(Container.container_list)} containers.")
        print(f"Kicked containers were: {kicked_as_str}")
        if len(mislabeled_containers) > 0:
            print(f"*** ERROR ***: mislabeled containers were: {mislabeled_str}")

class Cell(object):
    """
    Represents a simulated Cell/Station
    """

    max_containers = 7
    process_time = 15
    barcode_failure_rate = 5

    cell_list = []
    last_container_routed = False

    def __init__(self, id: int):
        # Serve same functions as in RIS
        self.expected_queue = []
        self.known_queue = []
        self.super_queue = []
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
        for cell in Cell.cell_list:
            await cell.make_tasks()
        while True:
            if Cell.all_done():
                break
            await custom_sleep(0.1)

    def get_score(self) -> int:
        """
        :return: score used by routing heuristic
        """
        total = len(self.expected_queue) + len(self.known_queue)
        return total if total < Cell.max_containers else -1

    @staticmethod
    def all_done():
        """
        :return: True if all cells are finished with their work
        """
        for cell in Cell.cell_list:
            if not cell.is_done():
                return False
        return True

    def is_done(self) -> bool:
        """
        :return: True if cell has finished all its processing
        """
        return Cell.last_container_routed and len(self._enroute_queue) == 0 and len(self._actual_queue) == 0

    def get_queues_as_str(self) -> str:
        """
        :return: Contents of queues as readable string
        """
        ret_str = f"S=[{list_to_cs([str(x.id) for x in self.super_queue])}] " + \
                  f"K=[{list_to_cs([str(x.id) for x in self.known_queue])}]"
        return ret_str

    async def add_container(self, container: Container):
        """
        Adds a container to the *ACTUAL* list of forthcoming arrivals, i.e. it will reliably get there
        :param container: the container
        """
        async with self._lock:
            self._enroute_queue.append(container)

    async def add_expected_container(self, container: Container):
        """
        Adds a container to the Expected queue for this cell
        :param container: the container
        """
        async with self._lock:
            self.expected_queue.append(container)
            self.super_queue.append(container)

    @staticmethod
    def remove_container_from_all_cells_except(container: Container, exclude_cell):
        for cell in Cell.cell_list:
            if cell is exclude_cell:
                continue
            removed = Cell._remove_from_queue(cell.expected_queue, container, surgical=True)
            if removed:
                print(f"cell {cell.id}: container {container.id} pulled from Expected queue, is at cell {exclude_cell.id}")
            removed = Cell._remove_from_queue(cell.known_queue, container, surgical=True)
            if removed:
                print(f"cell {cell.id}: container {container.id} pulled from Known queue, is at cell {exclude_cell.id}")
            removed = Cell._remove_from_queue(cell.super_queue, container, surgical=True)
            if removed:
                print(f"cell {cell.id}: container {container.id} pulled from Super queue, is at cell {exclude_cell.id}")

    async def make_tasks(self):
        """
        Fires up the two coroutines that will indefinitely handle container arrivals and container processing.
        """
        self._arrival_task = asyncio.create_task(self._arrival_coro())
        self._process_task = asyncio.create_task(self._processing_coro())

    @property
    def arrival_time(self):
        """
        :return: how long it takes a container to arrive at this cell
        """
        return self._arrival_time

    @arrival_time.setter
    def arrival_time(self, val):
        self._arrival_time = val

    async def _arrival_coro(self):
        # Runs continuously, handling arriving containers
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
        # Runs continuously, handling the processing of containers in pick area
        while True:
            # If there a container at the pick station, process it
            if self._container_in_processing is not None:
                await custom_sleep(Cell.process_time)
                self._container_in_processing = None
            if len(self._actual_queue) > 0:
                async with self._lock:
                    next_container = self._actual_queue.pop(0)
                    got_barcode = self._handle_pick_area_arrival(next_container)
                    self._container_in_processing = next_container if got_barcode else None
            else:
                # Sleep for small amount of time to return control to other coroutines
                await custom_sleep(0.1)

    def _handle_entrance_arrival(self, container: Container):
        """
        Allows the entrance barcode scanner an opportunity to read the barcode of the arrived container,
        which it might not do successfully. If a success, bookkeeping with the queues will happen.

        Note: it would be cheating for this function to report a container's real ID to the user
        :param container: the container
        """
        if random.randrange(100) < Cell.barcode_failure_rate:
            # Barcode wasn't read, so we can't do any bookkeeping
            return
        # If we get here, barcode scan was a success.
        container.reported_id = container.id
        # Take container out of other cells' queues
        Cell.remove_container_from_all_cells_except(container, self)
        # Take container off the expected queue
        was_in_queue = self._remove_from_queue(self.expected_queue, container)
        # Add to known queue
        self.known_queue.append(container)
        if was_in_queue:
            print(f"cell {self.id}: container {container.reported_id} arrival detected, queues are: {self.get_queues_as_str()}")
        else:
            print(f"cell {self.id}: WARNING, unexpected container {container.reported_id} arrival "
                  f"detected, queues are: {self.get_queues_as_str()}")
            self._add_to_super_queue(container)

    def _handle_pick_area_arrival(self, actual_container: Container) -> bool:
        """
        Allows the cell barcode scanner an opportunity to read the barcode of the container passing into pick area,
        which it might not do successfully. If a success, bookkeeping with the queues will happen.

        Note: it would be cheating for this function to report a container's real ID to the user
        :param actual_container: the container that actually arrives, whether we get barcode or not
        :return: True if barcode read successfully
        """
        bad_barcode_read = False
        known_container = actual_container
        if random.randrange(100) < Cell.barcode_failure_rate:
            bad_barcode_read = True
            known_container = None

        if bad_barcode_read:
            # We couldn't read the barcode, but maybe we can use the Super queue
            if len(self.super_queue) > 0 and self.super_queue[0] in self.known_queue:
                known_container = self.super_queue[0]
                if known_container is not actual_container:
                    print(f"cell {self.id}: *** ERROR ***, container {known_container.id} is not {actual_container.id}")
            else:
                print(f"cell {self.id}: WARNING, container had no barcode, kicked")
                actual_container.was_kicked = True
                return False

        actual_container.reported_id = known_container.id

        # If we get here, barcode scan was a success.
        # Take container out of other cells' queues
        Cell.remove_container_from_all_cells_except(known_container, self)
        # Take container off the Known queue
        was_in_queue = self._remove_from_queue(self.known_queue, known_container)
        if not was_in_queue:
            print(f"cell {self.id}: WARNING, container {known_container.reported_id} not in Known queue.")
        # Take container off the Super queue
        was_in_queue = self._remove_from_queue(self.super_queue, known_container)
        if not was_in_queue:
            print(f"cell {self.id}: WARNING, container {known_container.reported_id} not in Super queue.")
        print(f"cell {self.id}: container {known_container.reported_id} moves to processing area, "
              f"queues are: {self.get_queues_as_str()}")
        return True

    @staticmethod
    def _remove_from_queue(queue, item: Container, surgical: bool = False) -> bool:
        # Returns True if successfully removed
        try:
            index = queue.index(item)
        except ValueError:
            return False
        if surgical:
            # Non-aggressive, so only remove the one item
            queue.pop(index)
        else:
            # Want to also remove everything in queue ahead of item
            for i in range(index+1):
                queue.pop(0)
        return True

    def _add_to_super_queue(self, container: Container):
        # It should go in the queue ahead of later containers
        for i, entry in enumerate(self.super_queue):
            delta_t = (entry.creation_time - container.creation_time).total_seconds()
            if delta_t > 0:
                # This container in the queue was created after the one we want to insert,
                # so insert here.
                self.super_queue.insert(i, container)
                return
        self.super_queue.append(container)



class Orchestrator(object):
    """
    Represents the system orchestrator, which routes containers to cells
    """

    def __init__(self):
        self.total_containers = 100
        self._index = 0
        self._overall_arrival_period = 5
        self._misroute_rate = 2


    def load_params_from_yaml(self, filename: str):
        with open(filename, 'r') as file:
            config = yaml.safe_load(file)
        sim_settings = config["sim_settings"]
        Cell.max_containers = sim_settings["max_containers_per_cell"]
        Cell.process_time = sim_settings["cell_processing_time"]
        Cell.barcode_failure_rate = sim_settings["barcode_failure_rate"]

        num_cells = sim_settings["num_cells"]
        for i in range(num_cells):
            cell = Cell(i)
            Cell.cell_list.append(cell)
            cell.arrival_time = sim_settings["cell_arrival_time"] + i * sim_settings["cell_distance_penalty"]

        self._overall_arrival_period = sim_settings["overall_arrival_period"]
        self._misroute_rate = sim_settings["misroute_rate"]


    async def run(self):
        """
        This coroutine contains the main loop that drives the Orchestrator
        """
        for n in range(self.total_containers):
            container_name = "BG_{}".format(self._index)
            self._index += 1
            cell = self.choose_cell()
            container = Container(container_name)
            if cell is None:
                print(f"Router: no destination for {container_name}")
                container.was_kicked = True
            else:
                print(f"Router: routing container {container_name} to cell {cell.id}")
                await cell.add_expected_container(container)
                # Should there be a misroute?
                if random.randrange(100) < self._misroute_rate:
                    # Yes
                    wrong_cell = self.choose_random_cell(cell)
                    await wrong_cell.add_container(container)
                else:
                    # No, container goes where expected
                    await cell.add_container(container)
            await custom_sleep(self._overall_arrival_period)
        print(f"Router: finished with all containers")
        Cell.last_container_routed = True

    def choose_cell(self):
        """
        Choose cell most suitable for routing a container to
        :return: Cell object or None
        """
        best_cell = None
        best_score = 100000
        for cell in Cell.cell_list:
            score = cell.get_score()
            #print(f"*** score for cell {orch.id} is {score}")
            if score >= 0 and score < best_score:
                best_cell = cell
                best_score = score
        return best_cell

    def choose_random_cell(self, cell_to_skip: Cell = None):
        """
        Choose a random cell, excluding the cell_to_skip as an option.
        :return: the cell
        """
        options = [cell for cell in Cell.cell_list if cell is not cell_to_skip]
        return options[random.randrange(len(options))]

orchestrator = Orchestrator()
speed_up_rate = 1

async def run_all():
    tasks = [asyncio.create_task(orchestrator.run()), asyncio.create_task(Cell.run())]
    await asyncio.wait(tasks, return_when=asyncio.ALL_COMPLETED)
    Container.print_outcome()

if __name__ == "__main__":
    parser = ArgumentParser(
        add_help=True,
        description="Simulation of Cell and client routing systems",
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
    orchestrator.load_params_from_yaml(args.config)
    orchestrator.total_containers = args.containers
    speed_up_rate = args.speed

    asyncio.run(run_all())
