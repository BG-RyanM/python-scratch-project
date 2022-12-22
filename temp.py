from datetime import datetime
import attr


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
