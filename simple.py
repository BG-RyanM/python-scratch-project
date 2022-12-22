# Testing what happens when thing is or'd with other

def or_func(my_var=None):
    return my_var or 0

# 6
print("result 1:", or_func(6))
# 1
print("result 2:", or_func(1))
# 0
print("result 3:", or_func())


def str_or_none(item: bytes) -> str:
    return None if item is None else item.decode("UTF-8")

x1: bytes = b"thing"
print(f"x1 to string value is '{str_or_none(x1)}'")
x2: bytes = None
print(f"x2 to string value is '{str_or_none(x2)}'")

some_list = [1, 2, 3, 4, 5]
print("some_list minus last element is:", some_list[:-1])

barcodes = ['R:71875:0.43.15.557,16731', 'BG03081:0.43.15.557,16731']
for raw_bc in barcodes:
    parts = raw_bc.split(":")
    processed = ":".join(parts[0:-1])
    print("processed barcode is", processed)

fruit_set = {"apple", "grape", "pear"}
if None in fruit_set:
    print("None in fruit set?")

none_str = None
print(f"none_str is {none_str}")

some_coords = [(3, 1), (2, 2), (1, 0)]
c1 = (1, 0)
if c1 in some_coords:
    print("c1 in some_coords")
c2 = (5, 7)
if c2 not in some_coords:
    print("c2 not in some_coords")

outer_var = 1
for x in range(10):
    if x % 3 == 0:
        outer_var = 2
    elif x % 5 == 0:
        outer_var = 3

dumb_num = 5.775862068965505e-06
print("dumb num is", dumb_num)

none_val = None
none_as_str = str(none_val)
print(f"none_as_str is [{none_as_str}]")

bytes_val = b"thing"
as_str = str(bytes_val)
really_as_str = bytes_val.decode("utf-8")
print(f"bytes value as string is '{as_str}', really as string is '{really_as_str}'")

str_val = "BEDF001"
as_bytes = bytes(str_val, "utf-8")
print(f"string to bytes is {as_bytes}")
# This doesn't work
#as_bytes_again = bytes(as_bytes, "utf_8")
#print(f"bytes to bytes is {as_bytes}")

var_a = "cat"
var_b = "dog"
var_a, var_b = var_b, var_a
print(f"A and B post-swap are {var_a}, {var_b}")

str_with_spaces = "banana head"
space_free_str = "".join([c for c in str_with_spaces if c != ' '])
print(f"space free str is '{space_free_str}'")

bool_list = [True, True, True, False, False]
print("sum of bools is", sum(bool_list))

fat_thing = None
if fat_thing == "something":
    print("fat_thing is something")
else:
    print("fat_thing is None")