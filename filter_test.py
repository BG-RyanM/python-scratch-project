import functools

"""
Experiments with Python filter() and reduce() functions.
"""


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
# Error:
# print("last", make_comma_separated_list([]))

# We want the first item in little list that's also in big list
big_list = ["a", "b", "c", "d", "e", "f", "g"]
little_list = ["0", "d", "f", "x", "y"]
best_match = next(filter(lambda _id: _id in big_list, little_list), big_list[0])
print(f"Best match is {best_match}")

array_of_tups = [("c", 3), ("d", 4), ("a", 1), ("b", 2), ("c", 7)]
as_dict = {tup[0]: tup[1] for tup in array_of_tups}
print(f"value for a is {as_dict['a']}")
# Notice special deal with c
print(f"value for c is {as_dict['c']}")
