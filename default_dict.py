from collections import defaultdict
from datetime import datetime
import time

"""
Demonstration of how to use Python defaultdict collection.

It's like a regular dictionary, except my_dict[x] returns a default value if
my_dict[x] hasn't been set.
"""

the_dict = defaultdict(lambda: datetime.utcnow())

print(f"first read of the_dict[1] is {the_dict[1]}")
time.sleep(3)
print(f"second read of the_dict[1] is {the_dict[1]}")
print(f"first read of the_dict[2] is {the_dict[2]}")
