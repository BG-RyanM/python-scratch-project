# Testing what happens when thing is or'd with other

def or_func(my_var=None):
    return my_var or 0

print("result 1:", or_func(6))
print("result 2:", or_func(1))
print("result 3:", or_func())
