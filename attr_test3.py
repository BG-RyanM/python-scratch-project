import copy

import attr
from typing import Dict, Any, Optional, List, Union
import functools


"""
Notes:

Demonstrates how to use attr library. Also some demonstration of how to make a class
cast-able into a Dict.
"""


@attr.s
class TestHeld(object):
    number = attr.ib(type=int, default=-1, validator=attr.validators.instance_of(int))


@attr.s
class TestHolder(object):
    name = attr.ib(type=str, validator=attr.validators.instance_of(str))
    held_thing = attr.ib(type=TestHeld, default=attr.Factory(TestHeld))


holder1 = TestHolder(name="holder1")
holder2 = TestHolder(name="holder2")

different_held_things = holder1.held_thing is not holder2.held_thing
print(f"different_held_things={different_held_things}")

holder1.held_thing = 6
holder2.held_thing = 7

holder3 = copy.deepcopy(holder2)
print("holder3 is", holder3)
