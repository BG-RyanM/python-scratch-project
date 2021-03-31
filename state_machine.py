import asyncio
import random
from transitions import EventData
from transitions.extensions import MachineFactory
from enum import (
    Enum,
    unique,
)

@unique
class FishingStates(str, Enum):
    INIT = "INIT"
    SETUP = "SETUP"
    BAITING = "BAITING"
    CASTING = "CASTING"
    WAIT_FISH = "WAIT_FISH"
    REEL_FISH = "REEL_FISH"
    REMOVE_FISH = "REMOVE_FISH"
    CLEANUP = "CLEANUP"

# State machine (using transitions library) that represents a person fishing with
# a fishing rod.
class FishingMachine(object):
    _STATES = [state for state in FishingStates]

    _TRANSITIONS = [
        {
            "trigger": "setup_fishing",
            "source": FishingStates.INIT,
            "dest": FishingStates.SETUP,
        },
        {
            "trigger": "bait_line",
            "source": [FishingStates.SETUP, FishingStates.REMOVE_FISH],
            "dest": FishingStates.BAITING,
        },
        {
            "trigger": "do_cast",
            "source": FishingStates.BAITING,
            "dest": FishingStates.CASTING,
        },
        {
            "trigger": "wait_for_fish",
            "source": FishingStates.CASTING,
            "dest": FishingStates.WAIT_FISH,
        },
        {
            "trigger": "reel_fish",
            "source": FishingStates.WAIT_FISH,
            "dest": FishingStates.REEL_FISH,
        },
        {
            "trigger": "remove_fish",
            "source": FishingStates.REEL_FISH,
            "dest": FishingStates.REMOVE_FISH,
        },
        {
            "trigger": "cleanup",
            "source": FishingStates.WAIT_FISH,
            "dest": FishingStates.CLEANUP,
        },
    ]

    def __init__(self):
        self._reel_task = None
        self._timeout_task = None

        # state machine: relies on https://pypi.org/project/transitions/
        self._machine_factory = MachineFactory.get_predefined(asyncio=True)
        self._machine_factory(
            model=self,
            queued=True,
            send_event=True,
            states=FishingMachine._STATES,
            transitions=FishingMachine._TRANSITIONS,
            initial=FishingStates.INIT,
        )

    # corresponds to FishingStates.SETUP. Same idea with other similarly-named functions.
    async def on_enter_SETUP(self, event: EventData):
        print("Machine: SETUP state")

    # corresponds to FishingStates.BAITING
    async def on_enter_BAITING(self, event: EventData):
        print("Machine: BAITING state")
        ret_list = event.kwargs.get('ret_baits', None)
        baits = ["worm", "fly", "radish"]
        if ret_list is not None:
            ret_list.append(baits[random.randrange(3)])
        await asyncio.sleep(5)
        await self.do_cast() # go to next state

    async def on_enter_CASTING(self, event: EventData):
        print("Machine: CASTING state")
        await asyncio.sleep(5)
        await self.wait_for_fish() # go to next state

    async def on_enter_WAIT_FISH(self, event: EventData):

        # if we wait a long time with no bite, it must mean that no fish are left in pond
        async def _timeout():
            await asyncio.sleep(100)
            await self.cleanup() # proceed to CLEANUP state

        print("Machine: WAIT_FISH state")
        self._timeout_task = asyncio.create_task(_timeout())

    async def on_enter_REEL_FISH(self, event: EventData):

        async def _perform_reel(will_succeed):
            await asyncio.sleep(5)
            return will_succeed

        print("Machine: REEL_FISH state")
        if self._timeout_task is not None:
            # we caught a fish, so reset clock for cleaning up and going home
            self._timeout_task.cancel()
            self._timeout_task = None
        successful_catch = random.randrange(2) == 0
        # This task can be inspected to see whether or not fish was caught
        self._reel_task = asyncio.create_task(_perform_reel(successful_catch))
        await self._reel_task
        print("Machine: done reeling")
        await self.remove_fish()

    async def on_enter_REMOVE_FISH(self, event: EventData):
        print("Machine: REMOVE_FISH state")

    async def on_enter_CLEANUP(self, event: EventData):
        print("Machine: CLEANUP state")

    async def run(self):
        await self.setup_fishing()


fishing_machine = FishingMachine()


# Simulates a fish pond with several fish in it
async def run_pond():

    fish_count = 3

    # If a fish nibbles, it might or might not bite the hook, and it might or might not escape if hooked
    # Returns true if fish caught
    async def _do_nibble():
        if random.randrange(5) == 0:
            print("Fish: bit")
            # got hooked, trigger state change
            # (the following function doesn't return until fishing_machine gets to a state whose entry function
            # finishes)
            await fishing_machine.reel_fish()
            caught = fishing_machine._reel_task.result()
            if caught:
                print("Fish: reeled and caught")
            else:
                print("Fish: reeled, but escaped")
            return caught
        else:
            # didn't get hooked
            print("Fish: didn't bite")
            await asyncio.sleep(3)
            return False

    # the main loop: run endlessly until fishing machine in CLEANUP state
    while True:
        if fishing_machine.is_WAIT_FISH() and fish_count > 0:
            # can only nibble if bait in the water
            caught = await _do_nibble()
            if caught:
                fish_count = fish_count - 1
                print("Fish: fish count to", fish_count)
        else:
            if fish_count > 0:
                print("Fish: idle")
            else:
                print("Fish: no more fish in pond")
            await asyncio.sleep(3.0)
            if fishing_machine.is_CLEANUP():
                return


async def run_fishing_simulation():
    while True:
        # Wait until it's possible to bait line
        while not fishing_machine.is_SETUP() and not fishing_machine.is_REMOVE_FISH():
            await asyncio.sleep(0.5)
            if fishing_machine.is_CLEANUP():
                print("Fishing done!!!!!!")
                return

        ret_baits = []
        await fishing_machine.bait_line(ret_baits=ret_baits)
        print("baited line with ", ret_baits)


async def run_main():
    await fishing_machine.run()
    await asyncio.gather(run_pond(), run_fishing_simulation())

asyncio.run(run_main())
