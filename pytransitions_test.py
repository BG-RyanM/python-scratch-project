from transitions import Machine, EventData
from enum import Enum, auto


class MatterStates(Enum):
    SOLID = auto()
    LIQUID = auto()
    GAS = auto()


class Matter(object):
    def __init__(self):
        transitions = [
            {
                "trigger": "heat",
                "source": MatterStates.SOLID,
                "dest": MatterStates.LIQUID,
            },
            {
                "trigger": "heat",
                "source": MatterStates.LIQUID,
                "dest": MatterStates.GAS,
            },
            {
                "trigger": "cool",
                "source": MatterStates.GAS,
                "dest": MatterStates.LIQUID,
            },
            {
                "trigger": "cool",
                "source": MatterStates.LIQUID,
                "dest": MatterStates.SOLID,
            },
        ]
        self.machine = Machine(
            model=self,
            states=MatterStates,
            transitions=transitions,
            initial=MatterStates.SOLID,
            send_event=True,
        )

    def on_enter_GAS(self, event: EventData):
        print(f"entering GAS from {event.transition.source}")

    def on_enter_LIQUID(self, event: EventData):
        print(f"entering LIQUID from {event.transition.source}")

    def on_enter_SOLID(self, event: EventData):
        print(f"entering SOLID from {event.transition.source}")


matter = Matter()
matter.heat()
matter.heat()
matter.cool()
