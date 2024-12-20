def contained_func(x, y):
    print(f"contained_func(x={x}, y={y})")


def some_func(req_param, optional_param=None, **other_params):
    print("some_func()")
    print(f"req_param={req_param}, optional_param={optional_param}")
    print("other params are", other_params)
    contained_func(**other_params)


some_func("A", x=1, y=2)
some_func("B", optional_param="opt", x=3, y=4)
