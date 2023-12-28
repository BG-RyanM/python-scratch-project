class Singleton:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        if Singleton.__instance:
            return

        # Your code here
        self.some_value = 1


singleton1 = Singleton()
singleton1.some_value = 2

singleton2 = Singleton()

print("singleton2.some_value =", singleton2.some_value)

try:
    Singleton.some_dumb_function()
except AttributeError:
    print("some_dumb_function() does not exist as expected")
