class DumbObj:
    pass


dumb1 = DumbObj()
dumb2 = None

if dumb1:
    print("dumb1 is valid")
if dumb2 and dumb2.some_val:
    print("dumb2 is valid")
