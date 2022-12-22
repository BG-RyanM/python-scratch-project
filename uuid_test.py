import uuid

my_uuid = uuid.uuid4()
uuid_to_str = str(my_uuid)
print("result is", uuid_to_str)

uuid_as_bytes = my_uuid.bytes
print("product code is", uuid_as_bytes)

bak_to_str = str(uuid_as_bytes)
print("back to string", bak_to_str)

# PY2, maybe?
"""
uni = unicode(uuid_to_str, "utf-8")
print("unicode version", uni)

uni_as_bytes = bytes(uni)
print("unicode as bytes", uni_as_bytes)

ver_one = bytes(uuid.uuid1())
print("version one uuid ", ver_one)
"""

# bin_code: bytes = bytes("thing", "utf-8")
# print(f"bin_code as string is {bin_code.decode('utf-8')}")


unicode_thing = u"Thingy"
print("type of unicode thing is", type(unicode_thing))
unicode_to_str = str(unicode_thing)
print("unicode as str is", unicode_to_str, "type is", type(unicode_to_str))
