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
