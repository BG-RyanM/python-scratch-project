from enum import Enum, unique


@unique
class Codes(Enum):
    ALPHA = "alpha"
    BRAVO = "bravo"
    ROMEO = "romeo"


code_list = [str(code.value) for code in Codes]
if "romeo" in code_list:
    print("romeo there as expected")
if "juliet" not in code_list:
    print("juliet not there as expected")
my_dumb_code = Codes.ALPHA
if my_dumb_code in Codes:
    print("Codes.ALPHA there as expected")
    print(f"is_instance = {isinstance(my_dumb_code, Codes)}")

print(f"type is {type(Codes.ALPHA.value)}")
