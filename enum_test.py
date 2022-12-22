from enum import Enum, unique, IntEnum
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
problem_map[PetOwner.Animal.CAT] = "worms"
problem_map[PetOwner.Animal.DOG] = "fleas"
for k, v in problem_map.items():
    print(f"problem for {k} is {v}")

# Bird value is 3
print("Bird value is", PetOwner.Animal["BIRD"].value)

dumb_string = "dumb\n123\nxyz"
dumb_parts = dumb_string.split("\n")
if type(dumb_string) == str:
    print("dumb parts ",dumb_parts)
# dumb parts  ['dumb', '123', 'xyz']


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
print(f"stack light state regular is {stack_light_state}, as str is '{str(stack_light_state)}'")

for state in StackLightState:
    print(f"state in StackLightState is '{state}'")