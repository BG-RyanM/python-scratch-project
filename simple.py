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
