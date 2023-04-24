from datetime import datetime
import attr
import os

from pretty_table import pretty_table


def log_print(msg, *args):
    print(msg, *args)


log_print("hi", 1, 2)

thing1 = None
thing2 = datetime.utcnow()
if thing1 and not thing2:
    print("case 1")
if not thing1 and thing2:
    print("case 2")


@attr.s(slots=True)
class Dumb(object):
    x = attr.ib(type=int, default=None)


dumb = Dumb(x=1)
print(f"dumb type is {type(dumb)}")
print("dumb.x =", dumb.x)


def list_checker(the_list, name):
    if not the_list:
        print(f"List {name} is empty")
    else:
        print(f"List {name} is not empty")


my_list1 = None
my_list2 = []
my_list3 = ["A", "B", "C"]

list_checker(my_list1, "my_list1")
list_checker(my_list2, "my_list2")
list_checker(my_list3, "my_list3")

print("neat my_list3 is", ", ".join(my_list3))

dumb_list = ["A", "B", "C"]
dumb_set = set(dumb_list)
print("dumb set is ", dumb_set)

dumb_list2 = []
dumb_set2 = set(dumb_list2)
if not dumb_set2:
    print("yay!")

f_string = "Hi {name}, it is {day}. Your name is {name}."
print("Message is", f_string.format(name="Ryan", day="Friday"))

my_table = [
    ["Alvin", "Chipmunk", "Male"],
    ["Porpy", "Porpoise", "Male"],
    ["Maxwell", "Cat", "Female"],
]
my_table_with_header = [["Name", "Species", "Sex"]] + my_table
print("my table is:\n-------------------\n" + pretty_table(my_table_with_header))

hour = 15
minute = 33
time_str = f"{hour:02}:{minute:02}"
print("time_str is " + time_str)

try:
    int_cast = int("xxx")
except ValueError:
    pass

print("BG_ZOOKEEPER_ROOT env variable is", os.environ.get("BG_ZOOKEEPER_ROOT"))
print("DUMB_VAR env variable is", os.environ.get("DUMB_VAR"))
print("NONEXISTENT_VAR env variable is", os.environ.get("NONEXISTENT_VAR"))
