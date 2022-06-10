import attr
from datetime_test import datetime
from typing import Dict, Any, Optional, List, Union
import functools


@attr.s
class TestHeld(object):
    number = attr.ib(type=int, default=-1, validator=attr.validators.instance_of(int))


@attr.s
class TestHolder(object):
    name = attr.ib(type=str, validator=attr.validators.instance_of(str))
    value = attr.ib(type=bytes, default=None, validator=attr.validators.instance_of((bytes, type(None))))
    some_list = attr.ib(type=List[TestHeld], default=[])
    some_dict = attr.ib(type={}, default={})
    tricky_dict = attr.ib(type=Dict[str, TestHeld], default={})

    @classmethod
    def create(cls, name, value=None):
        ret_obj = cls(name=name, value=value)
        return ret_obj

    def __attrs_post_init__(self):
        print("calling post-init")
        self.populate()

    def populate(self):
        for i in range(10):
            self.some_list.append(TestHeld(number=i+1))
        self.some_dict = {"cat": 1, "dog": 2, "parrot": 3}
        self.tricky_dict = {"temp": TestHeld(number=2112)}

    def print_info(self):
        num_list = list(map(lambda x: x.number, self.some_list))
        contents = functools.reduce(lambda a, b: str(a) + "," + str(b), num_list)
        print(f"name is {self.name}, contents are {contents}, cat index is {self.some_dict['cat']}")
        print("some_dict is a", type(self.some_dict))
        print("tricky_dict contains", self.tricky_dict["temp"].number)

test_holder = TestHolder.create("abc")
#test_holder.populate()
test_holder.print_info()

holder_bytes = TestHolder.create("bytes", value=b"hi")
# Causes error
# holder_str = TestHolder.create("bytes", value="blah")