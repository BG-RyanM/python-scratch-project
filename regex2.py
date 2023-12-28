import re

string1 = "My datetimes are 2023-1-10 06:17:31pm and 2023-1-10 14:24:00"
pattern1 = (
    r"[0-9]{4,4}-[0-9]{1,2}-[0-9]{1,2} [0-9]{2,2}:[0-9]{2,2}:[0-9]{2,2}(?:am|pm)?"
)

string2 = "My datetime is 2023-02-14T08:55:20.232230"
pattern2 = (
    r"[0-9]{4,4}-[0-9]{1,2}-[0-9]{1,2}T[0-9]{2,2}:[0-9]{2,2}:[0-9]{2,2}(?:.[0-9]{6,6})?"
)

string3 = "E1C3"
string3_2 = "w12j"
pattern3 = r"(?:E|e|W|w)[0-9]{1,2}(?:[A-Z]|[a-z])[0-9]{1,2}"

# "2023-02-14T08:55:20.232230"

patterns = [pattern1, pattern2, pattern3, pattern3]
strings = [string1, string2, string3, string3_2]

for pattern, string in zip(patterns, strings):
    results = re.findall(pattern, string)
    print(f"findall results are", results)

# Split string into parts
remaining_str = string3
part_1 = re.match("(?:E|e|W|w)", remaining_str)
print("part_1 is", part_1.group())
remaining_str = remaining_str[part_1.span()[1] :]
part_2 = re.match("[0-9]{1,2}", remaining_str)
print("part_2 is", part_2.group())
remaining_str = remaining_str[part_2.span()[1] :]
part_3 = re.match("(?:[A-Z]|[a-z])", remaining_str)
print("part_3 is", part_3.group())
remaining_str = remaining_str[part_3.span()[1] :]
part_4 = re.match("[0-9]{1,2}", remaining_str)
print("part_4 is", part_4.group())
remaining_str = remaining_str[part_4.span()[1] :]

# Balint's method
# 4 named capture groups to read out the 4 parts. Compile the regex just once
# for better performance.
cubby_regex = re.compile(r"([eEwW]?)([0-9]{1,2})([a-zA-Z]?)([0-9]{1,2})")
print("cubby regex is", cubby_regex)

match = re.match(cubby_regex, string3)
print("match for group 0 is", match.group(0))
print("match for group 1 is", match.group(1))
print("match for group 2 is", match.group(2))
print("match for group 3 is", match.group(3))
print("match for group 4 is", match.group(4))
new_cubby_id = "".join([match.group(2), match.group(1), match.group(4), match.group(3)])
print("new cubby ID (Balint method) is:", new_cubby_id)
