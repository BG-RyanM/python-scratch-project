import asyncio
from transitions import EventData
from transitions.extensions import MachineFactory

@unique
class FishingStates(str, Enum):
    INIT = "INIT"
    SETUP = "SETUP"
    BAITING = "BAITING"
    CASTING = "CASTING"
    WAIT_FISH = "WAIT_FISH"
    REEL_FISH = "REEL_FISH"
    REMOVE_FISH = "REMOVE_FISH"

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
            "trigger": "reel_fish",
            "source": FishingStates.WAIT_FISH,
            "dest": FishingStates.REEL_FISH,
        },
    ]