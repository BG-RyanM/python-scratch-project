from collections import namedtuple

"""
Demonstration of Python's namedtuple factory function.
"""

QueueInfo = namedtuple("QueueInfo", ["container_list", "known_flags_list"])

queue_info = QueueInfo(
    container_list=[1, 2, 3, 4, 5], known_flags_list=[True, True, False, False, False]
)

queue_info.container_list.clear()
queue_info.container_list.extend([2, 3, 4, 5])
queue_info.known_flags_list.clear()
queue_info.known_flags_list.extend([True, False, False, False])

print("new container list", queue_info.container_list)

a = [6, 7, 8]
b = [True, False, False]
params = {"container_list": a, "known_flags_list": b}
another_one = QueueInfo(**params)

print("another_one.container_list =", another_one.container_list)
print("another_one.known_flags_list =", another_one.known_flags_list)
