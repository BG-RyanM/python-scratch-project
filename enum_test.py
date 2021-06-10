from enum import Enum

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
print(pet_owner.to_string())

print("Bird value is", PetOwner.Animal["BIRD"].value)

dumb_string = "dumb\n123\nxyz"
dumb_parts = dumb_string.split("\n")
if type(dumb_string) == str:
    print("dumb parts ",dumb_parts)