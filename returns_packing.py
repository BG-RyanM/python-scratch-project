# Test of multiple returns as a tuple


def return_stuff():
    x = 12
    y = "abc"
    z = [1, 2]
    return x, y, z


result = return_stuff()
# Result is (12, 'abc', [1, 2])
print("Result is", result)
