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
