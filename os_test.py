import os

real_path = os.path.realpath(__file__)
dir = os.path.dirname(real_path)
parent = os.path.dirname(dir)

print("real path is", real_path)
print("dir is", dir)
print("parent is", parent)
