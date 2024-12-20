"""
Experiments with dictionary creation and usage.
"""

my_list = [("apple", 1), ("orange", 2), ("grape", 3), ("banana", 4)]
my_dict = {tup[0]: tup[1] for tup in my_list}
my_dict["pear"] = 5

to_list = list(my_dict)
for i in to_list:
    print("key is", i)


animal_map = {
    "dog": (1, "canine"),
    "cat": (2, "feline"),
    "bird": (3, "avian"),
}

for name, (idx, _type) in animal_map.items():
    print(f"{name} has idx {idx}, type {_type}")


dict1 = {"a": 1, "b": 2}
dict2 = {"c": 3, "d": 4}
dict1.update(dict2)
print("combined dict is", dict1)

############################################################

letters_map = {"a": 1, "b": 2, "c": 4, "d": 4, "e": 5}

for key, val in letters_map.items():
    if key == "c":
        letters_map[key] = val - 1

print("new letters_map is", letters_map)

non_existent = animal_map["horse"]
