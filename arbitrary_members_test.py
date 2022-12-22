
class DynamicObject(object):

    """
    A class whose instances can be dynamically populated with data,
    easily accessible as member variables.

    Example:
        my_obj = DynamicObject(cat=1, dog=2, fish=3)
        my_obj.cat    # returns 1
        my_obj.dog    # returns 2
        my_obj.bird   # returns None
        del my_obj.fish
        my_obj.fish   # returns None
        my_obj.monkey = 5
        my_obj.monkey # returns 5
    """

    def __init__(self, **kwargs):
        """
        Each keyword argument becomes a member of the instance
        :param kwargs: dictionary of keyword arguments
        """
        for k, v in kwargs.items():
            if k != "__dynamic_object__":
                super().__setattr__(k, v)

    def __setattr__(self, key, value):
        # Not necessary to have this function, but including it for understanding
        super().__setattr__(key, value)

    def __getattr__(self, item):
        """
        Called whenever my_obj.member_name can't be found. Simply returns None,
        as though my_obj.member_name is set to None.
        :param item: name of member as string
        :return: None
        """
        return None

    def to_dict(self):
        """
        Turns this instance into a dictionary. Any members that are DynamicObjects
        themselves are recursively turned into dictionaries, with a special key
        to distinguish them from regular dictionaries.
        :return: the resulting dictionary
        """
        out_dict = {}
        for k, v in self.__dict__.items():
            if isinstance(v, DynamicObject):
                out_dict[k] = v.to_dict()
            else:
                out_dict[k] = v
        out_dict["__dynamic_object__"] = True
        return out_dict

    @staticmethod
    def from_dict(the_dict):
        """
        Builds a DynamicObject from a dictionary. If the dictionary contains dictionaries
        that include the key '__dynamic_object__`, these are turned into DynamicObjects
        themselves.
        :param the_dict: dictionary to build from
        :return: DynamicObject
        """
        contruction_kwargs = {}
        for k, v in the_dict.items():
            if isinstance(v, dict) and v["__dynamic_object__"]:
                new_dynamic_object = DynamicObject.from_dict(v)
                contruction_kwargs[k] = new_dynamic_object
            elif k != "__dynamic_object__":
                contruction_kwargs[k] = v
        return DynamicObject(**contruction_kwargs)



obj = DynamicObject(cat=1, dog=2, bird=3)
obj.fish = 4
print("cat member is", obj.cat)
print("fish member is", obj.fish)
print("monkey member is", obj.monkey)
del obj.dog
print("dog member is", obj.dog)
to_dict_func = DynamicObject.to_dict
def wrapper_func():
    return obj.to_dict()
print("obj dictionary is", wrapper_func())


complex_obj = DynamicObject(apple=1, orange=2, grapes=DynamicObject(grape_array=[1, 2, 3, 4]))
print("\ncomplex object dictionary is", complex_obj.to_dict())
rebuild_obj = DynamicObject.from_dict(complex_obj.to_dict())
print("rebuilt complex object dictionary is", complex_obj.to_dict())
print("apple member of rebuilt is", rebuild_obj.apple)
