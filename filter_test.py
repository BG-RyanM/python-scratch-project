import functools

def sum_odd_numbers(num_list):
    _num_list = num_list.copy()
    odds_list = filter(lambda n: isinstance(n, int) and n % 2 == 1, _num_list)
    return sum(odds_list)

# 9
print(sum_odd_numbers([1, 2, 3, 4, 5, 6]))
# 80
print(sum_odd_numbers(["rabbit", 77, "monkey", 3]))

def make_comma_separated_list(the_list):
    return functools.reduce(lambda x, y: str(x) + "," + str(y), the_list)

print(make_comma_separated_list(["apple", "banana", "grape"]))
print(make_comma_separated_list(["hat"]))
print("last", make_comma_separated_list([]))

