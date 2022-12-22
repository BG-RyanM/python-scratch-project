import random

def generate_string():
    i = 0
    while True:
        my_string = "string" + str(i)
        i += 1
        yield my_string


my_generator = generate_string()


def keep_printing(getter_func):
    for i in range(10):
        print(getter_func())


keep_printing(lambda: next(my_generator))

def get_random_number_maker(num_digits):
    return lambda: random.randrange(1, 10 ** num_digits)

rand_func = get_random_number_maker(6)
for r in range(10):
    print(rand_func())

# The next() test
test_tuples = [("cat", 1), ("bird", 2), ("dog", 1), ("fish", 2)]


def find_animal(num):
    result = next((tup[0] for tup in test_tuples if tup[1] == num), None)
    print(f"First animal of type {num} is {result}")

find_animal(1)
find_animal(2)
find_animal(3)