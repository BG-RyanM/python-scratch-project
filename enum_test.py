from enum import Enum, unique, IntEnum, auto
from typing import Dict


class PetOwner:
    class Animal(Enum):
        UNKNOWN = 0
        CAT = 1
        DOG = 2
        BIRD = 3

    def __init__(self, animal_type=Animal.UNKNOWN):
        self._animal_type = animal_type

    def to_string(self):
        return f"pet owner has {self._animal_type.name}"


pet_owner = PetOwner(PetOwner.Animal.CAT)
# pet owner has CAT
print(pet_owner.to_string())
print("Individual Animal values")
for a in PetOwner.Animal:
    print(a)
problem_map: Dict[PetOwner.Animal, str] = {}


class Fruit(Enum):
    APPLE = 0
    GRAPE = 1
    ORANGE = 2

    def is_grape(self):
        return self == Fruit.GRAPE


fruit: Fruit = Fruit.GRAPE
print("Is grape", fruit.is_grape())
fruit = Fruit.ORANGE
print("Is grape", fruit.is_grape())


@unique
class TimeUnits(str, Enum):

    SECONDS = "seconds"
    MINUTES = "minutes"
    HOURS = "hours"
    DAYS = "days"

    def __repr__(self) -> str:
        """
        Formats the TimeUnits object as a string.

        :return: The serialized SettingName.
        """
        return self.name

    def __str__(self) -> str:
        """
        Formats the TimeUnits object as a string.

        :return: The serialized TimeUnits.
        """
        return repr(self)


day_unit = TimeUnits("days")
print("day unit is", day_unit, "as str is", str(day_unit))
try:
    eons_unit = TimeUnits("eons")
except ValueError:
    print("eons not valid time unit")


@unique
class MoveStatus(IntEnum):
    STOPPED = 0
    WALKING = 1
    RUNNING = 2


move_status = MoveStatus(MoveStatus.WALKING)
print(f"move_status regular is {move_status}, as str is {str(move_status)}")
for ms in MoveStatus:
    print(f"move_status is {ms}, string name is {str(ms)}")

print("Reverse lookup in MoveStatus:", MoveStatus(2))


class StackLightState(Enum):
    """
    Stack Light States enumeration
    """

    OPERATIONAL = "OPERATIONAL"
    PAUSED = "PAUSED"
    ESTOPPED = "ESTOPPED"
    DATABASE_ERROR = "DATABASE_ERROR"
    BLOCKING = "BLOCKING"
    MAINTENANCE = "MAINTENANCE"


stack_light_state = StackLightState(StackLightState.OPERATIONAL)
print(
    f"stack light state regular is {stack_light_state}, as str is '{str(stack_light_state)}'"
)
if stack_light_state == StackLightState.OPERATIONAL:
    print("OPERATIONAL, as expected")

for state in StackLightState:
    print(f"state in StackLightState is '{state}'")


class OrderState(Enum):
    """
    State of an order
    RECEIVED: Order has been assigned to a putwall
    ACTIVE: Order is currently being put into a specific cubby
    TRANSFER_COMPLETE: all SKUs that *can* be placed in the cubby have
        been, whether the tote was fully picked or sent to QA. In the
        latter case, the order will be short, but it still goes to TC
        when all *other SKUs* (besides the ones short on) have been
        transferred to the cubby. This is a "ready to packout except
        we're waiting on the packout signal from the customer" state.
    READY_TO_PACKOUT: Order is transfer-complete and we have received
        signal from customer to let operator pack it out. Note that
        customer signals can sometimes override necessity of order
        being transfer complete.
    PACKOUT_IN_PROGRESS: Operator has pressed the cubby button
        and is presumably in the process of physically removing the items
    COMPLETED: Order has been packed-out and can no longer be interacted
        with.
    CANCELLED: Order was cancelled by the submitter prior to processing.
        This is a legacy state; consider it deprecated.
    """

    # Standard flow
    RECEIVED = auto()
    ACTIVE = auto()
    TRANSFER_COMPLETE = auto()
    READY_TO_PACKOUT = auto()
    PACKOUT_IN_PROGRESS = auto()
    COMPLETED = auto()
    CANCELLED = auto()

    def __str__(self):
        return self.name


my_order_state = OrderState.ACTIVE
print("my_order_state =", str(my_order_state))

print("All order states:")
for os in OrderState:
    print(f"state {os.value}: {os.name}")
