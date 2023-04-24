import os

current_dir = os.path.dirname(os.path.realpath(__file__))
print("current_dir is", current_dir)
parent_dir = os.path.dirname(current_dir)
print("parent_dir is", parent_dir)

this_filename = os.path.basename(os.path.realpath(__file__))
print("this_filename is", this_filename)

some_filename = os.path.basename("../somefolder/butt.py")
print("some_filename is", some_filename)

some_filename2 = os.path.basename(some_filename)
print("some_filename2 is", some_filename2)

joined_path = os.path.join(current_dir, "dir/subdir")
print("joined_path is", joined_path)
deeper_joined_path = os.path.join(joined_path, "butt.py")
print("deeper_joined_path is", deeper_joined_path)
