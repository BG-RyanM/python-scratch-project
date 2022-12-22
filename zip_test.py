list_one = ["a", "b", "c", "d"]
list_two = ["1", "2", "3", "4"]
out_tups = list(zip(list_one, list_two))
print("Out tups are", out_tups)

in_tups = [("apple", 1), ("orange", 2), ("grape", 3), ("banana", 4)]
out_list1, out_list2 = tuple(zip(*in_tups))
print("out list 1", out_list1)
print("out list 2", out_list2)

if ("grape", 3) in in_tups:
    print("grape is there")

empty_tups = []
try:
    out_list1, out_list2 = tuple(zip(*empty_tups))
except ValueError as e:
    print("Exception", e)
else:
    print("out_list1", out_list1)

print("hi")
in_tups2 = [("beetle", 1, True), ("fly", 2, False), ("roach", 4, True)]
try:
    out_list1_2, out_list2_2 = tuple(zip(*in_tups2))
except ValueError as e:
    print("Exception", e)
else:
    print("out list 1", out_list1_2)
    print("out list 2", out_list2_2)

container_tups = [
    ("A", 1),
    ("B", 2),
    ("B+", 2),
    ("C", 3),
    ("D", 1),
    ("E", 2),
    ("F", 3),
    ("G", 1),
    ("H", 2),
    ("I", 3),
]
inactive_stations = [1, 2]

# Basically, we find a block of containers that need shifting to the right in the list. The first container
# AFTER this block that doesn't need shifting, we pull it out of the list and insert it in front of the block.
# Then we look for the next block.
insert_index = None
for i in range(len(container_tups)):
    container_needs_shift = container_tups[i][1] in inactive_stations
    if container_needs_shift:
        if insert_index is None:
            insert_index = i
    else:
        if insert_index is not None:
            # perform switch
            to_move = container_tups.pop(i)
            container_tups.insert(insert_index, to_move)
            insert_index = None

print("new container tups are", container_tups)
