class Base:
    def __init__(self):
        print("base class __init__")

    def show_type(self):
        type_str = str(type(self))
        parts = type_str.strip("<>'").split(".")
        print(f"type is {parts[-1]}")


class SubA(Base):
    def __init__(self):
        super(SubA, self).__init__()
        print("SubA __init__")


class SubB(Base):
    def __init__(self):
        super(SubB, self).__init__()
        print("SubB __init__")


sub_a = SubA()
sub_b = SubB()

sub_a.show_type()
sub_b.show_type()