from abc import ABC, abstractmethod


class Animal(ABC):
    def __init__(self):
        print(f"Animal init'd")
        self._is_active = False

    @abstractmethod
    def sound(self):
        pass


class FlyingThingMixin:
    def __init__(self, altitude=200):
        print(f"FlyingThing init'd")
        self._altitude = altitude

    def fly(self):
        self._is_active = True
        print(f"I fly at altitude {self._altitude}!")


class Cat(Animal):
    def __init__(self):
        super().__init__()
        pass

    def sound(self):
        print("meow")


class Eagle(Animal, FlyingThingMixin):
    def __init__(self):
        # Calls parent class constructor, i.e. Animal
        super(Eagle, self).__init__()
        # Calls parent class constructor, i.e. Animal
        super(Animal, self).__init__(altitude=300)
        print("Eagle init'd")

    def sound(self):
        if self._is_active:
            print("skraaaaw!")
        else:
            print("cheep")


eagle = Eagle()
print("eagle is an Animal:", isinstance(eagle, Animal))
print("eagle is a FlyingThing:", isinstance(eagle, FlyingThingMixin))
eagle.sound()  # expect "cheep"
eagle.fly()
eagle.sound()  # expect "skraaaaw!"
try:
    eagle.grab()
except AttributeError:
    pass
