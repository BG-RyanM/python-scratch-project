import re
from typing import List

def list_to_cs_str(the_list: List):
    outstr = None
    for item in the_list:
        if outstr is None:
            outstr = str(item)
        else:
            outstr += ", " + str(item)
    if outstr is None:
        outstr = "Empty list"
    return outstr

def match_test(pattern: str, test_str: str):
    result = re.match(pattern, test_str)
    if result:
        print(f"successfully matched '{test_str}' to '{pattern}', result is {result}")
    else:
        print(f"couldn't match '{test_str}' to '{pattern}'")

def findall_test(pattern: str, test_str: str):
    result = re.findall(pattern, test_str)
    if result:
        print(f"successfully matched '{test_str} to {pattern}, result is {result}")
    else:
        print(f"couldn't match {test_str} to {pattern}")

# Given a string x, analysis generally starts with the left-most character of x
# and moves left to right, trying to match against the pattern. The pattern must
# be matched completely.
#
# If we start matching the pattern at character 7 and fail, then we try again to
# get a match starting with character 8, and so on.

print("\n==================================")
print("basics")
match_test("ham", "ham sandwich")  # yes: 'ham'
match_test("ham", "he's such a ham")  # no
match_test("ham", "ha ha ha")  # no

print("\n==================================")
print("[] metacharacters")
# If contains any of characters [abc]
match_test("[abc]", "alpha bravo")  # yes: 'a'
match_test("[abc]", "bravo alpha")  # yes: 'b'
match_test("[abc]", "alpha bravo charlie")  # yes: 'a'
match_test("[abc]", "xyzabc")  # no
match_test("[abc]", "aaaaaaaahhh")  # yes: 'a'
match_test("[abc]", "non-entity")  # no

print("\n==================================")
print("[] ranges")
match_test("[0-9]", "101st airborne")  # yes
match_test("[0-9]", "circus")  # no
# Any character other than abc
match_test("[^abc]", "gnome")  # yes
match_test("[^abc]", "abc")  # no

print("\n==================================")
print(". metacharacter")
# A . matches any single character
match_test("..", "a")  # no
match_test("..", "ab")  # yes: 'ab'

print("\n==================================")
print("^ metacharacter")
# ^ means "starts with"
match_test("^a", "ass")  # yes
match_test("^a", "butt")  # no

print("\n==================================")
print("* metacharacter")
# * matches zero or more occurrences of pattern to its left
# (in this case, the * applies to the 'a' only)
match_test("ba*d", "bad")  # yes
match_test("ba*d", "baaaaaaad")  # yes
match_test("ba*d", "bd")  # yes
match_test("ba*d", "cod")  # no

print("\n==================================")
print("+ metacharacter")
# * matches one or more occurrences of pattern to its left
# (in this case, the + applies to the 'a' only)
match_test("ba+d", "bad")  # yes
match_test("ba+d", "baaaaaaad")  # yes
match_test("ba+d", "bd")  # no
match_test("ba+d", "cod")  # no

print("\n==================================")
print("? metacharacter")
# ? matches one or zero occurrences of pattern to its left
# (in this case, the ? applies to the 'a' only)
match_test("ba?d", "bad")  # yes
match_test("ba?d", "baaaaaaad")  # no
match_test("ba?d", "bd")  # yes
match_test("ba?d", "cod")  # no

print("\n==================================")
print("{} metacharacters")
match_test("(ha){2,3}", "ha")  # no
match_test("(ha){2,3}", "haha")  # yes
match_test("(ha){2,3}", "hahaha")  # yes
match_test("(ha){2,3}", "hahahaha")  # yes
match_test("(ha){2,3}", "hh")  # no

print("\n==================================")
print("| metacharacter")
match_test("(h|b)a", "hah")  # yes: 'ha'
match_test("(h|b)a", "bah")  # yes: 'ba'
match_test("(h|b)a", "baaaaaaaah")  # yes: 'ba'
match_test("(h|b)a", "caw")  # no

print("\n==================================")
print("Whitespace finder")
match_test("(\s)*$", "  ")  # yes: '  '
match_test("(\s)*$", "  ")  # yes: 'tab'
match_test("(\s)*$", "")  # yes: ''
match_test("(\s)*$", "BG03081")  # no
match_test("(\s)*$", "  BG03081")  # no
match_test("(\s)*$", "BG03081  ")  # no

print("\n==================================")
print("| find_all() test")
findall_test('R: ?[0-9] ?[0-9] ?[0-9] ?[0-9] ?[0-9] ?', 'R:71055:23.18.48.165,53453R:70293:23.18.48.165,53453')
findall_test(r'abc(def|xyz)', "abcxyz")
# Note special sequence '(?:' -- tells findall() that () are for grouping only
findall_test(r'abc(?:def|xyz)', "abcxyz")
findall_test(r'abc(?:def|xyz)', "abcxyz abcdef abc789")
findall_test(r'(?:BG)[0-9]{5,5}', "BG03081")
findall_test(r'(?:BG)[0-9]{5,5}', "BG03081BG03082")

print("\n==================================")
print("Scratch")

sample_barcodes = ["BG03081", "BG03081:somecrap,1234", "BG03088BG03089", "^%$^TGJRGROGJ",
                   "R:12345", "R: 12345", "R:12345 ", "BG03082", "BG03083",
                   "xR:12345", "R:R:12345", "R::R:12345", "R:12345xyzR:67890"]


def extract_matches(string, pattern):
    ret_strings = []
    _string = string
    while len(_string) > 0:
        result = re.search(pattern, _string)
        if result:
            ret_strings.append(result.group())
            _string = _string[result.span()[1]:]
        else:
            break
    return ret_strings

for bc in sample_barcodes:
    # "(BG)[0-9]{5,5}"
    patterns = ["(R:)( )?[0-9]( )?[0-9]( )?[0-9]( )?[0-9]( )?[0-9]( )?",
                "(BG03081)|(BG03082)|(BG03084)|(BG03085)"]
    success = False
    for pattern in patterns:
        strings = extract_matches(bc, pattern)
        if strings:
            print(f"Matches for {bc} using {pattern} are: {strings}")
            success = True
            break
    if not success:
        print(f"Failed to match {bc}")

match_test("(ho)[me]{2,2}", "home")
result = re.search("(ho)[me]{2,2}", "home")
print(f"match object is", result, "functions are", dir(result))
print("group is", result.group())
