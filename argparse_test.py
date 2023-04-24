import argparse

parser = argparse.ArgumentParser(description="A toy argument parser")
parser.add_argument("--param1", action="store_true", default=True)
parser.add_argument("--param2", action="store_false", default=True)

command_group = parser.add_mutually_exclusive_group()
command_group.add_argument("--a-x", action="store_true", required=False)
command_group.add_argument("--b-x", action="store_true", required=False)
command_group.add_argument("--c-x", action="store_true", required=False)

args = parser.parse_args()

if not args.a_x and not args.b_x and not args.c_x:
    args.a_x = True

print(args)
