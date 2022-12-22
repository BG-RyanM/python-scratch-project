from random import randrange

# See also generator_test.py

# Returns a generator, which we can call next() on.
# yield is basically like return, except when we call
# next() again, we pick up where we left off
def infinite_sequence():
    num = 0
    while True:
        yield num
        num += 1


gen = infinite_sequence()
print("gen type is", type(gen))
for i in range(10):
    item = next(gen)
    print(f"item is: {item}")

print("\n---------------------")


def animals_generator():
    animals = ["cow", "zebra", "walrus"]
    while True:
        animal = animals[randrange(len(animals))]
        response = yield animal
        outcome = "lose!"
        if animal == "cow" and response == "run":
            outcome = "win!"
        if animal == "zebra" and response == "hide":
            outcome = "win!"
        if animal == "walrus" and response == "fight":
            outcome = "win!"
        yield outcome


responses = ["run", "hide", "fight"]
gen = animals_generator()
for i in range(10):
    # gets us to first yield, which returns animal
    animal = next(gen)
    response = responses[randrange(len(responses))]
    # sends response that comes into generator through first yield, then runs to the second,
    # which returns outcome
    outcome = gen.send(response)
    print(f"outcome for responding to {animal} with {response} was {outcome}")
